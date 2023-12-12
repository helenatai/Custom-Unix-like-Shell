class ShellExpression:
    def accept(self, visitor):
        pass

    def accept_memo(self, visitor):
        pass


class Pipe(ShellExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right


    def accept(self, visitor, input=None):  # Add the input parameter . remove input NOT SURE
        return visitor.visit_pipe(self, input)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_pipe(self)


class Seq(ShellExpression):
    def __init__(self, commands):
        self.commands = commands

    def accept(self, visitor):
        return visitor.visit_seq(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_seq(self)


class Call(ShellExpression):
    def __init__(self, redirections, arguments, atoms):
        self.redirections = redirections
        self.arguments = arguments
        self.atoms = atoms
        #print("call of expressions", self.redirections, self.arguments, self.atoms)


    def accept(self, visitor, input=None):
        move = False
        if input == None:
            input = []

        if isinstance(input, str):
            input = [input]
            move = True
         # for i in self.atoms:
         #     input.append(i)

        #print(input, "thats the input", self.atoms)
        #input.extend(i for i in self.atoms)
        if len(self.atoms) > 0:
            redirection = False
            for i in self.atoms:
                if hasattr(i, "elements"):
                    input.append(i.elements)
                elif hasattr(i, "argument"):
                    #input.append((i.argument.elements)) #commented out
                    redirection = True
                    file_name = i
                    #visitor.visit_redirection(i) # do call firts andf then the redirection!"
                else:
                    pass # it must be a redirection
            if redirection:
                if file_name.symbol == "output":
                    input_for_redirection = visitor.visit_call(self, input)
                    return visitor.visit_redirection(file_name, input_for_redirection)
                elif file_name.symbol == "input":
                    #input_for_redirection = visitor.visit_redirection(file_name)
                    input.append(file_name.argument.elements)
                    return visitor.visit_call(self, input)


        #move the first one to the last place
        if len(input) > 1:
            if move:
                input = input[1:] + [input[0]]
            else:
                pass


        return visitor.visit_call(self, input)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_call(self)


class Redirection(ShellExpression):
    #def __init__(self, symbol, whitespace, argument):
    def __init__(self, symbol, argument):
        self.symbol = symbol
        #self.whitespace = whitespace
        self.argument = argument

    def accept(self, visitor):
        return visitor.visit_redirection(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_redirection(self)



class Command(ShellExpression):
    def __init__(self, pipe, commands, call):
        self.pipe = pipe
        self.commands = commands
        self.call = call

    def accept(self, visitor):
        return visitor.visit_command(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_command(self)


class UnQuoted(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_unquoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_unquoted(self)


class BackQuoted(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_backquoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_backquoted(self)


class Atom(ShellExpression):
    def __init__(self, redirection, argument):
        self.redirection = redirection
        self.argument = argument

    def accept(self, visitor):
        return visitor.visit_atom(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_atom(self)


class Argument(ShellExpression):
    def __init__(self, elements):
        self.elements = elements
        #print(self.elements, "elems of argument") #RETURN ELEMENTS?

    def accept(self, visitor):
        #print("going to visit argument")
        return visitor.visit_argument(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_argument(self)


class Whitespace(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_whitespace(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_whitespace(self)


class Newline(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_newline(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_newline(self)


class Unquoted(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_unquoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_unquoted(self)


class SingleQuoted(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_single_quoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_single_quoted(self)


class DoubleQuoted(ShellExpression):
    def __init__(self, value, backquoted):
        self.value = value
        self.backquoted = backquoted

    def accept(self, visitor):
        return visitor.visit_double_quoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_double_quoted(self)


class Backquoted(ShellExpression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_backquoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_backquoted(self)


class Quoted(ShellExpression):
    def __init__(self, single_quoted, double_quoted, backquoted):
        self.single_quoted = single_quoted
        self.double_quoted = double_quoted
        self.backquoted = backquoted

    def accept(self, visitor):
        return visitor.visit_quoted(self)

    def accept_memo(self, visitor):
        if visitor.already_visited(self):
            return visitor.visit_again(self)
        return visitor.visit_quoted(self)
