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
)
log = logging.getLogger(__name__)

DEFAULT_MAKEFILE = os.path.join(os.getcwd(), "Makefile")
TERM_COLORS = {
    "PURPLE": "\033[0;35m",
    "BLUE": "\033[0;34m",
    "LGRAY": "\033[0;37m",
    "NC": "\033[0m",
}
TERM_NOCOLORS = {color: "" for color in TERM_COLORS}
SELFUPDATE_URL = (
    "https://github.com/jweede/makefile-pretty-help-script/raw/master/makefile_self_document.py")

doc_lines_re = re.compile(
    r"^[#]{4}>?\s*(?P<header>.*?)\s*<?[#]*$"
    r"|^\.PHONY:\s+(?P<pcmd_name>.*)\s*#+\s*(?P<pcmd_doc>.*)\s*$"
    r"|^[#]{2}>?\s*(?P<cmd_name>.*)\s*:\s*(?P<cmd_doc>.*)\s*<?[#]*$",
    flags=re.MULTILINE,
)
header_fmt = "\n{c[PURPLE]}>> {0} <<{c[NC]}\n"
cmd_fmt = "{c[LGRAY]}make {c[BLUE]}{0: <24}{c[NC]}{1}"


def script_selfupdate():
    """best effort self-updating"""
    import requests

    log.debug("Attempting self-update via %s", SELFUPDATE_URL)
    this_script = os.path.realpath(__file__)
    res = requests.get(SELFUPDATE_URL)
    with open(this_script, "w") as fp:
        fp.write(res.text)
    log.info("Update complete.")


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
parser.add_argument(
    "makefile",
    nargs="*",
    default=(DEFAULT_MAKEFILE,),
    help="List of makefiles to check. "
    "Recommend using `$(MAKEFILE_LIST)` when embedding into your Makefile",
)
parser.add_argument(
    "--no-color",
    action="store_false",
    dest="colorterm",
    help="disable colored output.",
)
parser.add_argument(
    "--update", action="store_true", help="update this script after running."
)
parser.add_argument(
    "--debug", "-d", action="store_true", help="print extra debug output."
)


def main(argv=None):
    args = parser.parse_args(argv)
    colors = TERM_COLORS if args.colorterm else TERM_NOCOLORS
    if args.debug:
        log.setLevel(logging.DEBUG)

    if not args.makefile:
        log.warn("No Makefile?")
    for makefile in args.makefile:
        assert os.path.exists(makefile)
        log.debug("Scanning %s", makefile)
        with open(makefile, "r") as fp:
            for line in help_output(fp, colors):
                print(line)

    if args.update:
        script_selfupdate()


if __name__ == "__main__":
    main()
