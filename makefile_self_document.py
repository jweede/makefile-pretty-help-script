#!/usr/bin/env python
"""\
Automate the output of the `make help` command.

Annotate your Makefile with section headers and command help:

A header looks like:

    #### In The Beginning

Commands can be documented inline via:

    .PHONY: killall # Kills all the things

or for non-phony targets, like this:

    ## killall: Kills all the things

"""
from __future__ import print_function
import argparse
import os
import re
import logging

# mirrors salt.log
logging.basicConfig(
    level=logging.INFO,
    stream=os.sys.stderr,
    format="[%(levelname)-8s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

HERE = os.path.realpath(os.path.dirname(__file__))
DEFAULT_MAKEFILE = os.path.join(os.getcwd(), "Makefile")
TERM_COLORS = {"PURPLE": "\033[0;35m", "BLUE": "\033[0;34m", "LGRAY": "\033[0;37m", "NC": "\033[0m"}
TERM_NOCOLORS = {color: "" for color in TERM_COLORS}

doc_lines_re = re.compile(
    r"^[#]{4}>?\s*(?P<header>.*?)\s*<?[#]*$"
    r"|^\.PHONY:\s+(?P<pcmd_name>.*)\s*#+\s*(?P<pcmd_doc>.*)\s*$"
    r"|^[#]{2}>?\s*(?P<cmd_name>.*)\s*:\s*(?P<cmd_doc>.*)\s*<?[#]*$",
    flags=re.MULTILINE,
)
header_fmt = "\n{c[PURPLE]}>> {0} <<{c[NC]}\n"
cmd_fmt = "{c[LGRAY]}make {c[BLUE]}{0: <24}{c[NC]}{1}"


def help_output(makefile_fp, colors=TERM_COLORS):
    """scrape help output from makefile"""
    ms = doc_lines_re.finditer(makefile_fp.read())
    for m in ms:
        header, cmd_name, cmd_doc, pcmd_name, pcmd_doc = m.groups()
        log.debug("line match: %r", m.groups())
        if header is not None:
            line = header_fmt.format(header, c=colors)
        elif cmd_name is not None and cmd_doc is not None:
            line = cmd_fmt.format(cmd_name, cmd_doc, c=colors)
        elif pcmd_name is not None and pcmd_doc is not None:
            line = cmd_fmt.format(pcmd_name, pcmd_doc, c=colors)
        else:
            log.warn("Weird match: %r", m.groups())
            line = ""
        yield line


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("makefile", nargs="*", default=(DEFAULT_MAKEFILE,))
parser.add_argument(
    "--no-color", action="store_false", dest="colorterm", help="disable colored output"
)


def main(argv=None):
    args = parser.parse_args(argv)
    colors = TERM_COLORS if args.colorterm else TERM_NOCOLORS

    for makefile in args.makefile:
        assert os.path.exists(makefile)
        with open(makefile, "r") as fp:
            for line in help_output(fp, colors):
                print(line)


if __name__ == "__main__":
    main()
