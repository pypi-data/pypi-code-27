from subprocess import Popen, PIPE


def can_sudo():
    proc = Popen(['sudo', '-n', 'ls'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.communicate()
    if proc.returncode == 1:
        return False
    return True
