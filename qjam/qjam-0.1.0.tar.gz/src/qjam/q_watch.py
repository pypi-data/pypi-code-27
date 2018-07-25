#!/usr/bin/env python
# coding: utf-8
"""
watch job status
"""
__author__ = "Riku Okajima<riku.okajima@gmail.com>"
__date__ = "2018-06-21"

import argparse
import subprocess


def main(args: argparse.Namespace):
    """
    main function
    """
    invert_match = ""
    if args.invert_match is not None:
        invert_match = ["| grep -v {}".format(v) for v in args.invert_match]
    command = [
        "watch",
        "-td",
        (
            "echo "
            "'job-ID    prior    name    user      "
            "state  submit/start at   queue';"
            "qstat"
            "|sed -e 's/^  //g' -e 's/  */  /g'"
        ) +
        "{}".format("".join(invert_match)) +
        "|tail -n +3"
    ]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        pass
