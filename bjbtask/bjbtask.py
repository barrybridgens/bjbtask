#
# bjbtask - Barry's command line task manager
#

import argparse

parser = argparse.ArgumentParser(description='Command line task manager.')
parser.add_argument('add')

args = parser.parse_args()

print (args)
