grammar Shell;

// Parser

start
    : command EOF;

command
    : pipe
    | command seq+
    | call;

pipe
    : call '|' WHITESPACE? call
    | pipe '|' WHITESPACE? call;

seq
    : ';' WHITESPACE? command;

call
    : (WHITESPACE? redirection)* argument (WHITESPACE atom)* WHITESPACE?;

atom
    : redirection
    | argument;

argument
    : (quoted | UNQUOTED)+;

redirection
    : '<' WHITESPACE? argument
    | '>' WHITESPACE? argument;

// Lexer

WHITESPACE
    : [ \t]+;

NEWLINE
    : [\r\n]+ -> skip;

UNQUOTED
    : ~[ \t\r\n'"`|;<>]+;

SINGLE_QUOTED
    : '\'' ~('\n' | '\'')* '\'';

DOUBLE_QUOTED
    : '"' (BACKQUOTED | ~('\n' | '"' | '`'))* '"';

BACKQUOTED
    : '`' ~('\n' | '`')* '`';

quoted
    : SINGLE_QUOTED
    | DOUBLE_QUOTED
    | BACKQUOTED;
