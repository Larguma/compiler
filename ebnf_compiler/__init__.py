# SPDX-FileCopyrightText: 2025 Jacques Supcik <jacques.supcik@hefr.ch>
#
# SPDX-License-Identifier: Apache-2.0 OR MIT

"""
EBNF Compiler
"""

import sys
from pathlib import Path
from typing import Annotated

import typer
from loguru import logger

from ebnf_compiler.parser import Parser
from ebnf_compiler.scanner import Scanner

app = typer.Typer()


@app.command(context_settings={"ignore_unknown_options": True})
def main(
    source: Annotated[Path, typer.Argument()],
    debug: bool = False,
):
    logger.remove()
    if debug:
        logger.add(sys.stdout, level="DEBUG")
    else:
        logger.add(sys.stdout, level="INFO")

    scanner = Scanner()
    scanner.open(source)

    parser = Parser(scanner=scanner)

    try:
        parser.parse()
    except SyntaxError as e:
        print(f"{e.msg} (File {e.filename}, Line {e.lineno}, Column {e.offset})")

    if parser.has_error:
        print("Syntax errors. aborting")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
