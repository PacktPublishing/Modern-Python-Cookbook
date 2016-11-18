"""Python Cookbook

Chapter 5, recipe 5, part "py"
"""

import cmd
import sys

class REPL(cmd.Cmd):
    prompt=">>> "
    def preloop(self):
        print( sys.version )
    def do_def(self, arg):
        pass
    def do_class(self, arg):
        pass
    def do_EOF(self, arg):
        return True
    def default(self, arg):
        if "=" in arg:
            print( "Assignment" )
        else:
            print( "Expression" )

if __name__ == "__main__":
    py = REPL()
    py.cmdloop()
