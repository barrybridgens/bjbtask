#!/usr/bin/python
#
# bjbtask - Barry's command line task manager
#

import sys
import os.path

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

    def save(self):
        # Overwrite file with all current data - THIS WILL NOT SCALE!!!!
         with open("taskdb", "w") as f:
             for line in bjbTask.tasks:
                 f.write("{}\n".format(line.strip()))

if __name__ == "__main__":
    bjb_task = bjbTask()
    bjb_task.arg_parse(sys.argv)
