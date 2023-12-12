class Visitor:
    def visit_pipe(self, pipe):
        pass

    def visit_command(self, command):
        pass

    def visit_seq(self, seq):
        pass

    def visit_call(self, call):
        pass

    def visit_atom(self, atom):
        pass

    def visit_argument(self, argument):
        pass

    def visit_redirection(self, redirection):
        pass

    def visit_unquoted(self, unquoted):
        pass

    def visit_backquoted(self, backquoted):
        pass

    def visit_quoted(self, quoted):
        pass


class MemoShellVisitor(Visitor):
    def visit_again(self, node):
        pass

    def already_visited(self, node):
        pass
