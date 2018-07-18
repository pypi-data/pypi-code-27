import subprocess
import re
import os


def call_black():
    output = subprocess.run(
        ["black", '--exclude="/(\.serverless|node_modules)/"', "--check", "."],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return (output.stdout or output.stderr).decode("utf-8").splitlines()[-1]


def parse_black_result(black_result):
    unchanged = 0
    changed = 0

    re_changed = re.search(
        r"([0-9]+) file(s?) would be reformatted", black_result, re.M
    )

    re_unchanged = re.search(
        r"([0-9]+) file(s?) would be left unchanged.", black_result, re.M
    )

    if re_unchanged is not None:
        unchanged = int(re_unchanged.groups()[0])

    if re_changed is not None:
        changed = int(re_changed.groups()[0])

    return (changed, unchanged)


def calculate_percentage(changed, unchanged):
    return unchanged / (changed + unchanged)
