from subprocess import check_output

def run_command(name, *args):
    x = check_output([name, *args], universal_newlines=True)
    return x.strip()