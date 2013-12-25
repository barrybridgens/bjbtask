#!/usr/bin/python
#
# bjbtask - Barry's command line task manager
#

import sys
import os.path
import re
import exceptions

class bjbTask:

    # Class variables
    tasks = []

    def __init__(self):
        if os.path.isfile("taskdb"):
            with open("taskdb", "r") as f:
                for line in f:
                        bjbTask.tasks.append(line.strip().split(','))


    def arg_parse(self, argv):
        if argv[1] == 'add':
            self.add(argv[2:])
        elif argv[1] == 'show':
            self.show(argv[2:])
        elif argv[1] == 'done':
            self.done(argv[2:])
        elif ((argv[1] == 'del') or (argv[1] == 'delete')):
            self.delete(argv[2:])
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

    def show(self, argv):
        print ("Current Tasks")
        if len(argv) >= 1:
            arg = argv[0]
        else:
            arg = '--'
        num = 0
        for task in bjbTask.tasks:
            if ((arg == 'all') or (task[2] == '--')):
                if (arg == 'all'):
                    print ("{:<3} {:30} {:20} {}".format((num + 1), task[0], task[1], task[2]))
                else:
                    print ("{:<3} {:30} {}".format((num + 1), task[0], task[1]))
            num = num + 1

    def done(self, argv):
        try:
            num = int(argv[0])
        except exceptions.ValueError:
            print ("Error: Task number not valid")
            num = len(bjbTask.tasks) + 1
            invalid = True
        if ((num > 0) and ((num <= len(bjbTask.tasks)))):
            text = bjbTask.tasks[num - 1]
            bjbTask.tasks[num - 1][2] = "DONE"
            print ("Task marked as done: {}".format(text))
        else:
            if invalid != True:
                print ("Task mumber out of range: {}".format(num))

    def delete(self, argv):
        try:
            num = int(argv[0])
        except exceptions.ValueError:
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

    def help(self, argv):
        if len(argv) < 1:
            arg = "no arg"
        else:
            arg = argv[0]
        if arg == 'add':
            print ("bjbtask add command - add a task")
            print ("   add [@context] <task description> [@context]")
            print ("Add a new task with the given description to the database")
            print ("Put @context_name as the first or last word to make the task context @context_name")
        elif arg == 'show':
            print ("bjbtask show command - show tasks")
            print ("   show [all]")
            print ("Print all tasks prepended with a task number")
            print ("The number is used to identify the task for other commands")
            print ("with all modifier even done tasks are displayed")
        elif arg == 'done':
            print ("bjb task done commend - mark a task as done")
            print ("   done <task number>")
        elif ((arg == 'del') or (arg == 'delete')):
            print ("bjbtask delete command - delete a task")
            print ("   del <task number>")
            print ("   delete <task number>")
            print ("Deletes the task with the given number")
        else:
            print ("bjbtask commands")
            print ("   add - add a task")
            print ("   show - show tasks")
            print ("   done - mark a task as done")
            print ("   del or delete - delete a task")

    def save(self):
        # Overwrite file with all current data - THIS WILL NOT SCALE!!!!
         with open("taskdb", "w") as f:
             for task in bjbTask.tasks:
                 f.write("{},{},{}\n".format(task[0].strip(), task[1], task[2]))

if __name__ == "__main__":
    bjb_task = bjbTask()
    bjb_task.arg_parse(sys.argv)
