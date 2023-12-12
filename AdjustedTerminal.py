from directory_manager import directory_manager
from commands import Command, pwd, cd, echo, ls, clear, cat, head, grep, tail, sort, uniq, cut, find
from Converter import Converter
from evaluators import Evaluator
import sys
from antlr4 import *
from ShellLexer import ShellLexer
from ShellParser import ShellParser

specialCharacters =  ["'", '"', "<", ">", ";", "|", "`"]

class Terminal:
    def __init__(self, initial_directory, home_directory):
        self.directory_manager = directory_manager(initial_directory, home_directory)
        self.commands = {
            "pwd": pwd(),
            "cd": cd(),
            "echo": echo(),
            "ls": ls(),
            "clear": clear(),
            "cat": cat(),
            "head": head(),
            "grep": grep(),
            "tail": tail(),
            "sort": sort(),
            "uniq": uniq(),
            "cut": cut(),
            "find": find(),
            # Add more commands as needed
        }

    def run(self, user_input, out):
        user_input_list = user_input.split(' ; ')
        results = []
        #print("run, ui and out", user_input, out)

        for command_str in user_input_list:
            tokens = command_str.split()
            if tokens:
                command_name = tokens[0]
                args = tokens[1:]
                result = self.execute_command(command_name, args, out)
                #print("the res", result)
                results.append(result)
        return results
        #print("the results", results)
        #return results

    def execute_command(self, command_name, args, out):
        command_instance = self.commands.get(command_name)
        if command_instance:
            try:
                #print("args n out1", args, out)
                return command_instance.execute(*args)
            except Exception as e:
                print(f"Error executing command '{command_name}': {e}")
        else:
            return
            # print(f"Unknown command: {command_name}")



    def main(self, input_command, out=None):
        #print("inp com: ", input_command)
        #input_command = input("Enter a command: ")
        if not any(char in input_command for char in specialCharacters):
            terminal = Terminal("/initial/directory", "/home/user")
            #result = terminal.run(input_command) #make sure that you can enter multiple commands after the first one
            out.extend(terminal.run(input_command, out))
            #print("out passed from terminal", out)
            return out
        else:
            lexer = ShellLexer(InputStream(input_command))
            token_stream = CommonTokenStream(lexer)
            parser = ShellParser(token_stream)
            parse_tree = parser.start()
            #print(parse_tree.toStringTree(recog=parser))
            expression = parse_tree.accept(Converter()) #parser.command -> CommandContext class, ComCont.accept(Conv) -> Converter.visitCommand(self) -> Pipe()
            #print("onto eval", expression)
            out.extend(expression.accept(Evaluator()))
            # print(out, "output (grammar)")
            return out
            #print(result, "thats result")
            #print(f"Result: {expression.accept(Evaluator())}")

# if __name__ == "__main__":
#     terminal = Terminal("/initial/directory", "/home/user")
#     terminal.main()


