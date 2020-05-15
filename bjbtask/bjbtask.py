#!/usr/bin/python
#
# bjbtask - Barry's command line task manager
#

import sys
import os.path
import re
# import exceptions

class bjbTask:

    # Class "constants"
    TEXT = 0
    CONTEXT = 1
    STATUS = 2
    DUE_DATE = 3
    START_DATE = 4

    # Class variables
    db_file = "taskdb"
    tasks = []

    def __init__(self):
        # Check for config file
        if os.path.isfile(os.path.expanduser("~/.bjbtask")):
            with open(os.path.expanduser("~/.bjbtask")) as f:
                self.db_file =  f.readline().strip()
        # Read database
        if os.path.isfile(os.path.expanduser(self.db_file)):
            with open(os.path.expanduser(self.db_file), "r") as f:
                for line in f:
                        bjbTask.tasks.append(line.strip().split(','))
        else:
            print("ERROR: Database file not found")


    def arg_parse(self, argv):
        if (len(argv) < 2):
            print ("No command specified (try bjbtask.py help)")
        else:
            if ((argv[1] == 'add') or (argv[1] == 'a')):
                self.add(argv[2:])
            elif ((argv[1] == 'list') or (argv[1] == 'l')):
                self.list(argv[2:])
            elif ((argv[1] == 'board') or (argv[1] == 'b')):
                self.board()
            elif argv[1] == 'start':
                self.start(argv[2:])
            elif argv[1] == 'done':
                self.done(argv[2:])
            elif ((argv[1] == 'del') or (argv[1] == 'delete')):
                self.delete(argv[2:])
            elif argv[1] == 'archive':
                self.archive(argv[2:])
            elif argv[1] == 'init':
                self.init()
            elif ((argv[1] == 'help') or (argv[1] == '?')):
                self.help(argv[2:])
            else:
                print ("Command not recognised: {}".format(argv[1]))
        self.save()

    def add(self, argv):
        # Check arguments for special commands
        # --- Context handling
        context_found = False
        context = "--"
        num = 0
        for arg in argv:
            m = re.search('@.*', arg)
            if m != None:
                 context_found = True
                 context_position = num
                 context = argv[context_position]
            num = num + 1
        # Remove context from argument list
        if context_found == True:
            if context_position == 0:
                argv = argv[1:]
            else:
                argv = argv[:(context_position)]
        # --- End of Context handling
        # Convert remaining argument list to a string
        text = " ".join(argv)
        task = [text, context, "--"]
        bjbTask.tasks.append(task)
        print ("Task added: {}".format(text))
        if context_found == True:
            print ("Task added in context: {}".format(context))

    def list(self, argv):
        print ("Current Tasks")
        if len(argv) >= 1:
            arg = argv[0]
        else:
            arg = '--'
        num = 0
        for task in bjbTask.tasks:
            if (arg[0] == "@"):
                if (arg == task[self.CONTEXT]):
                    print ("{:<3} {:30}".format((num + 1), task[self.TEXT]))
            else:
                if ((arg == 'all') or (task[self.STATUS] != 'DONE')):
                    if (arg == 'all'):
                        print ("{:<3} {:30} {:20} {}".format((num + 1), task[self.TEXT], task[self.CONTEXT], task[self.STATUS]))
                    else:
                        print ("{:<3} {:30} {}".format((num + 1), task[self.TEXT], task[self.CONTEXT]))
            num = num + 1

    def print_spaces(self, num):
        for space in range(num):
            print (" ", end = '')

    def board(self):
        line = 0
        backlog = []
        started = []
        done = []
        for task in bjbTask.tasks:
            if task[self.STATUS] == '--':
                backlog.append(task[self.TEXT])
            if task[self.STATUS] == 'STARTED':
                started.append(task[self.TEXT])
            if task[self.STATUS] == 'DONE':
                done.append(task[self.TEXT])

        print ("Backlog                  Started                  Done")
        print ("-------                  -------                  ----")
        while ((line < len(backlog)) or (line < len(started)) or (line < len(done))):
            if line < len(backlog):
                print (backlog[line], end = '')
                self.print_spaces(25 - len(backlog[line]))
            else:
                print ("               ", end = '')
            if line < len(started):
                print (started[line], end = '')
                self.print_spaces(25 - len(started[line]))
            else:
                print ("               ", end = '')
            if line < len(done):
                print (done[line])
            else:
                print ("               ")
            line = line + 1

    def done(self, argv):
        try:
            num = int(argv[0])
        except ValueError:
            print ("Error: Task number not valid")
            num = len(bjbTask.tasks) + 1
            invalid = True
        if ((num > 0) and ((num <= len(bjbTask.tasks)))):
            text = bjbTask.tasks[num - 1]
            bjbTask.tasks[num - 1][self.STATUS] = "DONE"
            print ("Task marked as done: {}".format(text))
        else:
            if invalid != True:
                print ("Task mumber out of range: {}".format(num))

    def start(self, argv):
        try:
            num = int(argv[0])
        except ValueError:
            print ("Error: Task number not valid")
            num = len(bjbTask.tasks) + 1
            invalid = True
        if ((num > 0) and ((num <= len(bjbTask.tasks)))):
            text = bjbTask.tasks[num - 1]
            bjbTask.tasks[num - 1][self.STATUS] = "STARTED"
            print ("Task marked as started: {}".format(text))
        else:
            if invalid != True:
                print ("Task mumber out of range: {}".format(num))

    def delete(self, argv):
        try:
            num = int(argv[0])
        except ValueError:
            print ("Error: Task number not valid")
            num = len(bjbTask.tasks) + 1
            invalid = True
        if ((num > 0) and ((num <= len(bjbTask.tasks)))):
            text = bjbTask.tasks[num - 1]
            del(bjbTask.tasks[num - 1])
            print ("Task deleted: {}".format(text))
        else:
            if invalid != True:
                print ("Task mumber out of range: {}".format(num))

    def archive(self, argv):
        with open(os.path.expanduser("~/.bjbtask_archive"), "a") as f:
            # Inerate over a copy of the task list
            for task in bjbTask.tasks[:]:
                if task[self.STATUS] == "DONE":
                    f.write("{},{},{}\n".format(task[self.TEXT].strip(), task[self.CONTEXT], task[self.STATUS]))
                    print ("Task archived: {}".format(task))
                    bjbTask.tasks.remove(task)
    def init(self):
        f = open(os.path.expanduser(self.db_file),"w+")
        f.close()

    def help(self, argv):
        if len(argv) < 1:
            arg = "no arg"
        else:
            arg = argv[0]
        if ((arg == 'add') or (arg == 'a')):
            print ("bjbtask add command - add a task")
            print ("   add [@context] <task description> [@context]")
            print ("   Short command name a")
            print ("Add a new task with the given description to the database")
            print ("Put @context_name as the first or last word to make the task context @context_name")
        elif ((arg == 'list') or (arg == 'l')):
            print ("bjbtask list command - list tasks")
            print ("   list [all]")
            print ("   Short command name l")
            print ("Print all tasks prepended with a task number")
            print ("The number is used to identify the task for other commands")
            print ("with all modifier even completed tasks are displayed")
        elif ((arg == 'board') or (arg == 'b')):
            print ("bjbtask board command - show task board")
            print ("   board")
            print ("   Short command name b")
        elif arg == 'start':
            print ("bjbtask start command - start a task")
            print ("   start <task number>")
        elif arg == 'done':
            print ("bjb task done commend - mark a task as done")
            print ("   done <task number>")
        elif ((arg == 'del') or (arg == 'delete')):
            print ("bjbtask delete command - delete a task")
            print ("   del <task number>")
            print ("   delete <task number>")
            print ("Deletes the task with the given number")
        elif arg == 'archive':
            print ("bjbtask archive command - archive completed tasks")
            print ("   archive")
            print ("Moves completed tasks into the archive file")
        else:
            print ("bjbtask commands")
            print ("   add - add a task")
            print ("   list - list tasks")
            print ("   board - show a task (canban) board")
            print ("   start - mark a task as started")
            print ("   done - mark a task as done")
            print ("   del or delete - delete a task")
            print ("   archive - archive completed tasks")

    def save(self):
        # Overwrite file with all current data - THIS WILL NOT SCALE!!!!
        with open(os.path.expanduser(self.db_file), "w") as f:
            for task in bjbTask.tasks:
                f.write("{},{},{}\n".format(task[self.TEXT].strip(), task[self.CONTEXT], task[self.STATUS]))

if __name__ == "__main__":
    bjb_task = bjbTask()

    bjb_task.arg_parse(sys.argv)
