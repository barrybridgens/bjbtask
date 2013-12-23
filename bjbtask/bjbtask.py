#!/usr/bin/python
#
# bjbtask - Barry's command line task manager
#

import sys
import os.path
import exceptions

class bjbTask:

    # Class variables
    tasks = []

    def __init__(self):
        if os.path.isfile("taskdb"):
            with open("taskdb", "r") as f:
                for line in f:
                        bjbTask.tasks.append(line.strip())

    def arg_parse(self, argv):
        if argv[1] == 'add':
            self.add(argv[2:])
        elif argv[1] == 'show':
            self.show(argv[2:])
        elif ((argv[1] == 'del') or (argv[1] == 'delete')):
            self.delete(argv[2:])
        elif ((argv[1] == 'help') or (argv[1] == '?')):
            self.help(argv[2:])
        else:
            print ("Command not recognised: {}".format(argv[1]))
        self.save()

    def add(self, argv):
        # Convert argumwnt list to a string
        text = " ".join(argv)
        bjbTask.tasks.append(text)
        print ("Task added: {}".format(text))

    def show(self, argv):
        print ("Current Tasks")
        num = 0
        for task in bjbTask.tasks:
            print ("{}   {}".format((num + 1), task))
            num = num + 1

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
            print ("   add <task description>")
            print ("Add a new task with the given description to the database")
        elif arg == 'show':
            print ("bjbtask show command - show tasks")
            print ("   show")
            print ("Print all tasks prepended with a task number")
            print ("The number is used to identify the task for other commands")
        elif ((arg == 'del') or (arg == 'delete')):
            print ("bjbtask delete command - delete a task")
            print ("   del <task number>")
            print ("   delete <task number>")
            print ("Deletes the task with the given number")
        else:
            print ("bjbtask commands")
            print ("   add - add a task")
            print ("   show - show tasks")
            print ("   del or delete - delete a task")

    def save(self):
        # Overwrite file with all current data - THIS WILL NOT SCALE!!!!
         with open("taskdb", "w") as f:
             for line in bjbTask.tasks:
                 f.write("{}\n".format(line.strip()))

if __name__ == "__main__":
    bjb_task = bjbTask()
    bjb_task.arg_parse(sys.argv)
