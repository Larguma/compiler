# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Parser
"""

from loguru import logger
from pydantic import BaseModel

from ebnf_compiler.scanner import Scanner
from ebnf_compiler.tokens import Token


class Parser(BaseModel):
    scanner: Scanner
    has_error: bool = False

    def raise_error(self, msg: str) -> None:
        self.has_error = True
        self.scanner.raise_error(msg)

    def raise_expected_error(self, expected: Token):
        self.raise_error(f"Expected '{expected}', but got '{self.scanner.sym}'")

    def factor(self):
        logger.debug("Factor")
        sym = self.scanner.sym
        if sym == Token.IDENT:
            self.scanner.get_next_symbol()
        elif sym == Token.LITERAL:
            self.scanner.get_next_symbol()
        elif sym == Token.LPAREN:
            self.scanner.get_next_symbol()
            self.expression()
            if self.scanner.sym != Token.RPAREN:
                self.raise_expected_error(Token.RPAREN)
            self.scanner.get_next_symbol()
        elif sym == Token.LBRAK:
            self.scanner.get_next_symbol()
            self.expression()
            if self.scanner.sym != Token.RBRAK:
                self.raise_expected_error(Token.RBRAK)
            self.scanner.get_next_symbol()
        elif sym == Token.LBRACE:
            self.scanner.get_next_symbol()
            self.expression()
            if self.scanner.sym != Token.RBRACE:
                self.raise_expected_error(Token.RBRACE)
            self.scanner.get_next_symbol()
        else:
            self.raise_error(
                f"Expected identifier, literal, (', '['. or '{{' got {sym}"
            )

    def term(self):
        logger.debug("Term")
        while self.scanner.sym in (
            Token.IDENT,
            Token.LITERAL,
            Token.LPAREN,
            Token.LBRAK,
            Token.LBRACE,
        ):
            self.factor()

    def expression(self):
        logger.debug("Expression")
        self.term()
        while self.scanner.sym == Token.BAR:
            self.scanner.get_next_symbol()
            self.term()

    def production(self):
        logger.debug("Production")
        self.scanner.get_next_symbol()
        if self.scanner.sym != Token.EQL:
            self.raise_expected_error(Token.EQL)
        self.scanner.get_next_symbol()
        self.expression()
        if self.scanner.sym != Token.PERIOD:
            self.raise_expected_error(Token.PERIOD)
        self.scanner.get_next_symbol()

    def syntax(self):
        logger.debug("Syntax")
        while self.scanner.sym != Token.EOF:
            if self.scanner.sym != Token.IDENT:
                self.raise_expected_error(Token.IDENT)
            self.production()

    def parse(self):
        logger.debug("Parsing")
        self.scanner.get_next_symbol()
        self.syntax()
