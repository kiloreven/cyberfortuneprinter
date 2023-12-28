import os 
from random import randint

import toml
from escpos.printer import Serial


WIDTH = 42
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FORTUNE_FILE = os.path.join(CURRENT_DIR, "fortunes.txt")
# Lazy dir handling...
CONFIG_FILE = os.path.join(CURRENT_DIR, "../config.toml")
HEADER = """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                        @
@     @@ @@     @@ @@@@@@ @@@@@@ @@@@@@  @
@   @@@   @@   @@  @@@@@@ @@@@@@ @@@@@@  @
@  @@      @@ @@   @@  @@ @@     @@  @@  @
@ @@        @@@@   @@  @@ @@     @@  @@  @
@ @@         @@    @@ @@  @@@@@@ @@ @@   @
@ @@         @@    @@@@   @@@@@@ @@@@    @
@ @@         @@    @@ @@  @@     @@ @@   @
@  @@        @@    @@  @@ @@     @@  @@  @
@   @@@      @@    @@@@@@ @@@@@@ @@  @@  @
@    @@      @@    @@@@@@ @@@@@@ @@  @@  @
@                                        @
@      @@@ @@@ @@@ @@@ @ @ @  @ @@@      @
@      @   @ @ @ @  @  @ @ @@ @ @        @
@      @@@ @ @ @@   @  @ @ @ @@ @@       @
@      @   @ @ @ @  @  @ @ @ @@ @        @
@      @   @@@ @ @  @  @@@ @  @ @@@      @
@                                        @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
FOOTER = "- - - @coldnorth@chaos.social - - -\n#cyberfortune"


def _get_fortune():
    with open(FORTUNE_FILE) as f:
        data = f.read()
    fortunes = data.split("\n-\n")
    fortune = fortunes[randint(0, len(fortunes)-1)]
    return _fix_line_maxlength(fortune)

def _fix_line_maxlength(text):
    """
    text = "The quick brown fox jumped over the lazy dog\nFinito"
    parts = [
        "The quick brown fox jumped over the lazy dog",
        "Finito"
    ]
    """
    ret = []
    for part in text.split("\n"):
        if len(part) > WIDTH:
            ret = ret or [""]
            for word in part.split(" "):
                if len(f"{ret[-1]} {word}") > WIDTH:
                    ret.append("")
                ret[-1] = f"{ret[-1]} {word}"
        else:
            ret.append(part)
    return "\n".join(ret)



def _setup_printer():
    data = toml.load(CONFIG_FILE)
    return Serial(**data["printer"])

def _print_fortune(printer, fortune):
    printer.textln(HEADER)
    printer.textln("-"*42)
    printer.textln(fortune)
    printer.textln("-"*42)
    printer.set(align="center")
    printer.textln(FOOTER)
    printer.set(align="left")
    printer.cut()

def entry():
    fortune = _get_fortune()
    printer = _setup_printer()
    _print_fortune(printer, fortune)
