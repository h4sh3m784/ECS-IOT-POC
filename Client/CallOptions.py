
"""
To add new function calls: Create function, with a single parameter.
The parameter will be treated as list of arguments that you've passed on.
The arguments are by default strings. 

Example:
def addition(args):
    return int(args[0]) + int(args[1])

Add the function name to the 'calls' dictionary. the name of the key will be used to reference the function.
"""

def addition(args):
    return int(args[0]) + int(args[1])

def substraction(args):
    return int(args[0]) - int(args[1])

calls = {
    "addition" : addition,
    "substraction" : substraction
}
