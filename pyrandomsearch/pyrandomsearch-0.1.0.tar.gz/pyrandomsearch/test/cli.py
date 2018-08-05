import subprocess
import sys


def check_output(
        self, module, args, stdin, expected_stdout, expected_stderr=None):
    proc = subprocess.Popen(
        [sys.executable, '-m', module] + list(args),
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(stdin)
    try:
        self.assertEqual(proc.returncode, 0)
    except AssertionError:
        print(stderr)
        raise
    self.assertEqual(expected_stdout.strip(), stdout.strip())
    if expected_stderr:
        self.assertEqual(expected_stderr.strip(), stderr.strip())


def check_fails(self, module, args, stdin):
    proc = subprocess.Popen(
        [sys.executable, '-m', module] + list(args),
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(stdin)
    self.assertNotEqual(proc.returncode, 0)


def check_success(self, module, args, stdin):
    proc = subprocess.Popen(
        [sys.executable, '-m', module] + list(args),
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(stdin)
    self.assertEqual(proc.returncode, 0)
