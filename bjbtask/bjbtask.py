#!/usr/bin/python
#
# bjbtask - Barry's command line task manager
#

import sys

class bjbTask:

    def __init__(self):
        pass

    def arg_parse(self, argv):
        if argv[1] == 'add':
            self.add(argv)
        elif argv[1] == 'show':
            self.show(argv)
        else:
            print ("Command not recognised: {}".format(argv[1]))

    def add(self, argv):
        print ("---- Add command")

    def show(self, argv):
        print ("---- Show Command")

if __name__ == "__main__":
    bjb_task = bjbTask()
    bjb_task.arg_parse(sys.argv)
