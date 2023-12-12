from ShellParser import ShellParser
from ShellVisitor import ShellVisitor
from expressions import * #no more imports needed
from evaluators import Evaluator




class Converter(ShellVisitor):
    def visitStart(self, ctx):
        #print(ctx, "start ctx")
        return self.visitCommand(ctx.command())


    def visitCommand(self, ctx):
        #print(ctx.getText(), "ctx from visCom")
        # Base case, call | pipe
        if ctx.pipe():
            #print("it is a pipe")
            return self.visitPipe(ctx.pipe())
        elif ctx.seq():
            #print("it is a sequence")
            if ctx.command():
                #print("2 commands", ctx.seq(), ctx.command())
                #return self.visitCommand(ctx.command())
                (self.visitCommand(ctx.command())).accept(Evaluator())
            return self.visitSeq(ctx.seq())
        elif ctx.call():
            #print("it is a call")
            return self.visitCall(ctx.call())
        else:
            raise NotImplementedError("Unexpected command type")

    def visitSeq(self, ctx):
        #print("ctx", ctx, ctx[0].getText())
        # if ctx.command(1) and ctx.seq(2):
        #     #print("ctx call 1 and 2", ctx.call(1), ctx.call(2))
        #     return Command
        return Seq(self.visitCommand(ctx[0].command()))
        #return self.visitCommand(ctx.command(1)) #QUESTIONABLE

    def visitCall(self, ctx):
        # Note that call can contain a nonkeyword or a quoted
        redirections = []
        arguments = []
        atoms = []

        for child in ctx.getChildren():
            if isinstance(child, ShellParser.RedirectionContext):
                #print("redirection")
                #print(ctx.getText(), "thats ctx")
                redirections.append(self.visitRedirection(child))
            elif isinstance(child, ShellParser.ArgumentContext):
                #print("arg")
                #print(ctx.getText(), "thats ctx")
                arguments.append(self.visitArgument(child))
                #print(arguments, "arguments",)
                #arguments.append(self.visitArgument(ctx.getText()))
            elif isinstance(child, ShellParser.AtomContext):
                #print("atom")
                atoms.append(self.visitAtom(child))

            else:
                # Skip terminal nodes (spaces)
                continue
            #print(arguments, "arguments")
        #print(elements)

        return Call(redirections, arguments, atoms)

    def visitAtom(self, ctx):
        if ctx.redirection():
            return self.visitRedirection(ctx.redirection())

        elif ctx.argument():
            return self.visitArgument(ctx.argument())

        else:
            assert False, "Atom shouldn't have any other children"

    def visitArgument(self, ctx):
        # if parts is None:
        #     parts = []
        parts = []
        #print("argument is", ctx, ctx.getText(), "no of ch", ctx.getChildCount())
        #print("argument is", ctx)
        for child in ctx.getChildren():
        #for child in ctx:
            #parts.append(self.visit(child)) #Maybe change to ctx.arguments or whatever attribute ctx has??
            #parts.append(child)
            parts.append(ctx.getText()) #dont change
            #print("parts", parts, child)
        return Argument(*parts)

    def visitRedirection(self, ctx):
        redirection_type = None
        #print("got to redirection", ctx, ctx.getText())
        if str(ctx.getChild(0)) == "<":
            redirection_type = "input"
        elif str(ctx.getChild(0)) == ">":
            redirection_type = "output"
        else:
            raise LookupError("Unexpected redirection symbol")

        return Redirection(redirection_type, self.visitArgument(ctx.argument()))

    def visitQuoted(self, ctx):
        # Parser breaks on whitespaces, so just concatenate
        if ctx.singlequoted():
            return self.visitSinglequoted(ctx.singlequoted())
        elif ctx.doublequoted():
            return self.visitDoublequoted(ctx.doublequoted())
        else:
            return self.visitBackquoted(ctx.backquoted())

    def visitUnquoted(self, ctx):
        return UnQuoted(ctx.getText())

    def visitPipe(self, ctx):
        #print(ctx, "ctx")
        # Base case, call | call
        if ctx.call(1) and ctx.call(2):
            #print("ctx call 1 and 2", ctx.call(1), ctx.call(2))
            return Pipe(self.visitCall(ctx.call(1)), self.visitCall(ctx.call(2)))

        calls = []
        for child in ctx.getChildren():
            if isinstance(child, ShellParser.PipeContext):
                #print("pipe and calls ", calls)
                calls.append(self.visitPipe(child))

            elif isinstance(child, ShellParser.CallContext):
                #print("call and calls ", calls)
                calls.append(self.visitCall(child))

        results = calls[0]
        for i in range(1, len(calls)):
            #print("exec Pipe", results, calls[i])

            results = Pipe(results, calls[i])

        return results

    def visitSinglequoted(self, ctx):
        return SingleQuoted(ctx.getText()[1:-1])

    def visitDoublequoted(self, ctx):
        elements = []
        curr = ""
        for child in ctx.getChildren():
            if isinstance(child, ShellParser.BackquotedContext):
                if curr:
                    elements.append(curr)
                    curr = ""
                elements.append(self.visitBackquoted(child))

            else:
                # Skip "" in converter formatting
                if child.getText() == '"':
                    continue

                curr += child.getText()

        if curr:
            elements.append(curr)

        return DoubleQuoted(*elements)

    def visitBackquoted(self, ctx):
        return BackQuoted(ctx.getText()[1:-1])



    # def visitCommand(self, ctx):
    #     # Base case, call | pipe
    #     print("WE ARE IN VISCOM", (ctx.getChild(0)).getText())
    #     if ctx.getChildCount() == 1:
    #         #return self.visit(ctx.getChild(0))
    #         return Command(self.visit(ctx.getChild(0)))
    #
    #     elif ctx.getChildCount() > 1:
    #         elements = []
    #         for child in ctx.getChildren():
    #             # Note that visitSeq & visitCommand can return a list or a single match
    #             if isinstance(child, ShellParser.SeqContext):
    #                 elements.append(self.visit(child))
    #
    #             elif isinstance(child, ShellParser.CommandContext):
    #                 elements.append(self.visit(child))
    #         return Command(Seq(*elements))
    #     else:
    #         raise NotImplementedError("Empty Command?")