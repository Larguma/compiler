# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

import io
import typing
from enum import Enum
from typing import ClassVar


class Token(Enum):
    IDENT = 1
    LITERAL = 2
    LPAREN = 3
    LBRAK = 4
    LBRACE = 5
    BAR = 6
    EQL = 7
    RPAREN = 8
    RBRAK = 9
    RBRACE = 10
    PERIOD = 11
    OTHER = 12


class Scanner:
    token_map: ClassVar[dict[str, Token]] = {
        "=": Token.EQL,
        "(": Token.LPAREN,
        ")": Token.RPAREN,
        "[": Token.LBRAK,
        "]": Token.RBRAK,
        "{": Token.LBRACE,
        "}": Token.RBRACE,
        "|": Token.BAR,
        ".": Token.PERIOD,
    }

    def __init__(self, src: typing.TextIO):
        self.src = src  # type: typing.TextIO
        self.sym = None  # type: Token
        self.ch = None  # type: str
        self.value = None  # type: str
        self.next_char()

    def skip_space(self):
        while self.ch.isspace():
            self.next_char()

    def eof(self):  # -> bool:
        return self.ch == ""

    def error(self, msg: str):
        print(f"Error: {msg} at position {self.src.tell()}")

    def next_char(self):  # -> str:
        self.ch = self.src.read(1)
        return self.ch

    def next_symbol(self):  # -> Token:
        self.skip_space()
        if self.ch.isalpha():
            self.sym = Token.IDENT
            self.value = self.ch
            while (ch := self.next_char()).isalpha():
                self.value += ch
        elif self.ch == '"':
            self.sym = Token.LITERAL
            self.value = ""
            while not self.eof() and (ch := self.next_char()) != '"':
                self.value += ch
            if self.eof():
                self.error("Unterminated literal")
            self.next_char()
        elif self.ch in self.token_map:
            self.sym = self.token_map[self.ch]
            self.value = self.ch
            self.next_char()
        else:
            self.sym = Token.OTHER
            self.value = self.ch
            self.next_char()
        return self.sym


def main():
    src = """
    ident = letter { letter | digit }.
    number = digit { digit }.
    digit = "0" | "1" | "2" | "3".
    letter = "a" | "b" | "c" | "d".
    junk = " " | "\t" | "\n".
    """
    scanner = Scanner(io.StringIO(src))
    while True:
        sym = scanner.next_symbol()
        if scanner.eof():
            break
        print(f"{sym:20s}{scanner.value}")


if __name__ == "__main__":
    main()
