from visitors import *
from expressions import *
from commands import *
from ShellParser import ShellParser
from ShellVisitor import ShellVisitor


class Evaluator(Visitor):
    def visit_pipe(self, pipe, input=None):
        #print("pipe from evaluators", pipe.left, pipe.right)
        # Execute the left command
        #print("left output n pipe", pipe)
        left_output = pipe.left.accept(self) #it goes to expressions.Pipe
        #print(left_output, "left output")
        # Execute the right command with the output of the left command as input
        right_output = pipe.right.accept(self, input=left_output)
        #print(right_output, "right output")

        return right_output

    def visit_call(self, call, input=None):
        #print(call, "call", input)
        #arguments_instance = call.arguments
        #arguments = arguments_instance
        #print(arguments_instance[0].elements, "argument?")

        # Extract and process the arguments
        #arguments = [arg.accept(self) for arg in call.arguments]
        arguments = []
        for i in range(len(call.arguments)):
        #for i in range(len(call.arguments) + len(input.arguments)):
            #print(len(call.arguments), call.arguments[i])
            arguments.append((call.arguments[i].elements))
        # for j in range(len(input)):
        #     print(len(input), input[j])
        #     arguments.append((input[j].elements))
        # print(arguments, input, call.arguments[i].elements, "args n input")
        #arguments = [arg.accept(self) for arg in call.arguments]
        #print(arguments, "args 1")

        # Assuming you have a command class, you can instantiate it and execute
        command_name = arguments[0] #FIGURE OUT HOW TO DECODE IT INTO COMMAND
        # command_args = []
        # command_args.append(input)
        # if command_args[0] == None:
        #     if len(arguments[1:]) > 0:
        #         command_args = arguments[1:]
        # else:
        #     command_args.append(arguments[1:])

        #command_args = input

        #input = ''.join(str(atom) for atom in input)
        #print(len(input), "len of input")

        command_args = arguments[1:]
        if (input != None) and (input != []):
            #print(input, "input from eval")
            if isinstance(input, str):
                command_args.append(input)
            else:
                for i in range(len(input)):
                    if hasattr(input, "elements"):
                        command_args.append(input[i].elements)
                    else:
                        command_args.append(input[i])

        #print(command_name, command_args, "name n args") #gettext(command_name))

        # Map command names to corresponding classes
        command_classes = {
            "pwd": pwd,
            "cd": cd,
            "ls": ls,
            "sort": sort,
            "echo": echo,
            "grep": grep,
            "clear": clear,
            "cat": cat,
            "head": head,
            "tail": tail,
            "uniq": uniq,
            "cut": cut,
            "find": find,
            # Add more commands as needed
        }

        #print("com name", command_name)
        command_class = command_classes.get(command_name) #returns None
        #print("thats the command class", command_class)

        if command_class:
            command_instance = command_class()
            try:
                result = command_instance.execute(*command_args)
                return result
            except Exception as e:
                print(f"Error executing command '{command_name}': {e}")
        else:
            print(f"Unknown command: {command_name}")

    def visit_argument(self, argument):
        #print("entered the visit_argument", argument)
        # Handle different types of arguments: quoted, unquoted, etc.
        if argument.quoted():
            return argument.quoted().accept(self)  # Assuming you have a visit_quoted method
        elif argument.UNQUOTED():
            return argument.UNQUOTED().getText()
        else:
            # Handle other cases as needed
            return None

    def visit_seq(self, seq, result=None):
        #print("thats seq", seq, seq.commands, seq.commands.arguments)
        result = seq.commands.accept(self)
        #print(seq.commands.accept(self))
        #print(result.strip())


        # You can return something meaningful here if needed
        if result:
            return result
        else:
            return None

    def visit_redirection(self, redirection, input=None): #input is what we are gonna enter
        # Execute the command associated with the redirection
        command_result = redirection.argument.elements
        #print("cm res and symbol", command_result, redirection.symbol)
        # Perform the redirection based on the type (input or output)
        if redirection.symbol == "input":
            # Input redirection logic
            try:
                with open(command_result, 'r') as file:
                    # Read the content of the file and return it as the result
                    return file.read()
            except FileNotFoundError:
                print(f"Error: File not found - {command_result}")
                return None

        elif redirection.symbol == "output":
            # Output redirection logic
            try:
                with open(command_result, 'w') as file:
                    # Write the command result to the specified file
                    file.write(str(input))
            except PermissionError:
                print(f"Error: Permission denied - {command_result}")

        # Return the result of the command
        return input