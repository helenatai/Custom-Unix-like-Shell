import os
import re
import sys
from collections import deque




class Command:
    def execute(self, *args):
        pass

class pwd(Command):
    def execute(self, *args):
        try:
            if args:
                print("pwd command does not accept arguments.")
            else:
                #print(os.getcwd())
                return (os.getcwd())
                #print(os.getcwd())
        except Exception as e:
            print(f"An error occurred: {e}")


class cd(Command):
    def execute(self, *args):
        try:
            if len(args) == 1:
                os.chdir(args[0])
                #print("worked!")
                #print(os.getcwd())
                return (os.getcwd())
                #out.append
            else:
                print("cd command requires 1 directory argument.")
        except Exception as e:
            print(f"An error occurred: {e}")


class echo(Command):
    def execute(self, *args):
        try:
            #out = []
            #print("output from echo ->")
            #print(" ".join(args))
            #print(" ".join(args) + "\n")

            #out = (" ".join(args) + "\n")
            #out.append(" ".join(args) + "\n")
            # print("echo worked")
            return (" ".join(args) + "\n")
        except Exception as e:
            print(f"An error occurred: {e}")

class exit(Command):
    def execute(self, *args):
        sys.exit(0)


class ls(Command):
    def execute(self, *args):
        try:
            if args:
                path = args[0]
            else:
                path = os.getcwd()

            path_contents = os.listdir(path)
            path_contents = " ".join(path_contents)
            print(path_contents)

        except Exception as e:
            print(f"An error occurred: {e}")


class clear(Command):
    def execute(self, *args):
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except Exception as e:
            print(f"An error occurred: {e}")



class cat(Command):
    def execute(self, *args):
        try:
            if args:
                for file_path in args:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        print(content)
            else:
                # If no files are specified, read from stdin
                content = input("Enter text. Press Ctrl+D (Ctrl+Z on Windows) when done:\n")
                print(content)
            return content
        except Exception as e:
            print(f"An error occurred: {e}")


class head(Command):
    def execute(self, *args):
        try:
            value, file_path = self.parse_options(args)
            if file_path:
                with open(file_path, 'r') as file:
                    for i in range(value):
                        line = file.readline()
                        if not line:
                            break
                        print(line, end='')
            else:
                for i in range(value):
                    try:
                        line = input()
                        print(line)
                    except EOFError:
                        break
        except Exception as e:
            print(f"An error occurred: {e}")

    def parse_options(self, args):
        value = 10
        file_path = None
        if len(args) > 0:
            #for arg in args:
            if args[0].startswith('-'):
                value = int(args[1])
                if len(args) > 2:
                    file_path = args[2]
            else:
                file_path = args[0]

        return value, file_path


class grep(Command): #DOESNT USE STDIN
    def execute(self, *args):

        try:
            pattern = args[0]
            file_path = None
            if len(args) > 1:
                file_path = args[-1]
            else:
                pass # implement stdin
            try:
                if file_path:
                    with open(file_path, 'r') as file:
                        for line_number, line in enumerate(file, start=1):
                            if re.search(pattern, line, flags=re.IGNORECASE):
                                print(f"{file_path}:{line_number}:{line.strip()}")
            except Exception as e:
                print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")




class tail(Command):
    def execute(self, *args):
        try:
            value, file_path = self.parse_options(args)
            if file_path:
                if value == 0:
                    pass
                else:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines[-value:]:
                            print(line.strip())
            else:
                pass #USE STDIN
        except Exception as e:
            print(f"An error occurred: {e}")

    def parse_options(self, args):
        value = 10
        file_path = None
        if len(args) > 0:
            # for arg in args:
            if args[0].startswith('-'):
                value = int(args[1])
                if len(args) > 2:
                    file_path = args[2]
            else:
                file_path = args[0]

        return value, file_path



class sort(Command):
    def execute(self, *args):
        try:

            # Check the number of arguments for sort
            if len(args) > 2:
                raise ValueError("wrong number of command line arguments for 'sort'", len(args))

            reverse = False

            if len(args) > 0:
                if args[0].startswith("-r"):
                    reverse = True
            # Read from stdin or a specified file
            if sys.stdin.isatty():
                input_lines = sys.stdin.readlines()
            else:
                input_lines = []

            if args and args[-1] != "-r":
                file_name = args[-1]
                try:
                    with open(file_name) as file:
                        input_lines.extend(file.readlines())
                except FileNotFoundError:
                    raise ValueError(f"File not found: {file_name}")

            # Sort the input lines
            sorted_result = sorted(input_lines, reverse=reverse)

            # Construct a string from the sorted lines
            result = "".join(sorted_result)
            #sorted_result = sorted(input_lines, key=lambda s: s.lower(), reverse=reverse)
            #sorted_result = [line.rstrip('\n') for line in sorted_result] Potentially fixes the ns
            print(result)
            return result
            #return result
        except Exception as e:
            print(f"An error occurred: {e}")



class uniq(Command):
    def execute(self, *args):
        try:
            case_insensitive = False

            # Check the number of arguments for uniq
            if len(args) > 2:
                raise ValueError("wrong number of command line arguments for 'uniq'", len(args))

            if args and args[0].startswith("-i"):
                case_insensitive = True
                file_name = args[-1]

            # Read from stdin or a specified file
            input_lines = sys.stdin.readlines() if sys.stdin.isatty() else []
            if args and not args[0].startswith("-"):
                file_name = args[0]

            if file_name:
                with open(file_name) as file:
                    input_lines.extend(file.readlines())

            unique_result = []
            for line in input_lines:
                if case_insensitive:
                    processed_line = line.lower().rstrip('\n')
                else:
                    processed_line = line.rstrip('\n')
                if not unique_result or processed_line != unique_result[-1]:
                    unique_result.append(line.rstrip('\n'))
                    print(line.rstrip('\n'))
                else:
                    pass

            result = "\n".join(unique_result)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")



class find(Command):
    def execute(self, *args):
        try:
            # Check the number of arguments for the 'find' application
            if (len(args) != 2) and (len(args) != 3):
                print("len", len(args))
                raise ValueError("Usage: find [PATH] -name PATTERN")


            # Extract the search directory and search pattern from the arguments
            search_dir = args[0] if len(args) == 3 else os.getcwd()
            search_pattern = args[-1]

            # Store matching file paths in a list
            matching_files = []

            # Convert the search pattern to a regular expression
            regex_pattern = re.compile("^" + search_pattern.replace("*", ".*") + "$") #replacved that

            # Walk through the directory and find files matching the pattern
            for root, _, files in os.walk(search_dir):
                for file in files:
                    # Check if the file matches the pattern using re.match
                    if regex_pattern.match(file):
                        # Append the matching file path to the list
                        matching_files.append(os.path.abspath(os.path.join(root, file)))


            # Check if any matching files were found
            if matching_files:
                # Convert the list to a sorted string and join the paths with newline characters
                result = "\n".join(sorted(matching_files))
                print(result)
            else:
                print("No matching files found.")
        except Exception as e:
            print(f"An error occurred: {e}")


class cut(Command):
    def execute(self, *args):
        try:
            # Check if there are enough arguments for cut
            if len(args) != 3 and len(args) != 2:
                raise ValueError("wrong number of command line arguments for 'cut'", len(args))

            # Extract the cut options and file (if provided)
            cut_options = args[1]
            file_name = args[2] if len(args) == 3 else None

            # Read the content from the file or stdin
            if file_name:
                with open(file_name, 'r') as file:
                    lines = file.readlines()
            else:
                lines = sys.stdin.readlines()

            # Process each line based on cut options
            for line in lines:
                # Split the cut options into individual selections
                selections = cut_options.split(',')
                print("sels", selections)

                # Initialize the result string
                result = ''
                done = False

                if cut_options.startswith('-'):
                    beginning = int(cut_options[1])
                    end = int(cut_options[3])
                    result = result + line[:beginning] + line[(end-1):]
                    done = True

                if not done:
                    # Process each selection
                    for selection in selections:
                        if '-' in selection:
                            # Handle range selection
                            start, end = map(int, selection.split('-'))
                            result += line[start - 1:end]
                        else:
                            # Handle single byte selection
                            index = int(selection)
                            if 1 <= index <= len(line):
                                result += line[index - 1]

                # Append the result to the output
                print(result.strip())

        except Exception as e:
            print(f"An error occurred: {e}")
