import subprocess

def read_words_from_disk():
    return (w.decode("utf8") for w in subprocess.check_output(["cat", "/usr/share/dict/words"]).splitlines())