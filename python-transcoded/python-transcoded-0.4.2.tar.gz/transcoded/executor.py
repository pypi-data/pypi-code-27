import re
import shlex
import shutil
import subprocess


def _dump_command(command):
    sanitized = []
    for part in command:
        sanitized.append(shlex.quote(part))
    return " ".join(sanitized)


def execute_ffmpeg(command, metadata):
    total_time = metadata.length
    executable = 'ffmpeg'
    if shutil.which('ffmpeg') is None and shutil.which('avconv') is not None:
        executable = 'avconv'

    command.insert(0, executable)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    regex_time = re.compile(r'time=(\d+:\d+:\d+)')
    last_progress = 0

    all_output = []

    for line in process.stdout:
        all_output.append(line)
        time = regex_time.search(line)
        if time:
            time = time.groups()[0]
            hours, minutes, seconds = time.split(':')
            seconds = int(seconds)
            minutes = int(minutes)
            hours = int(hours)
            minutes += hours * 60
            seconds += minutes * 60
            progress = int((seconds / total_time) * 100.0)
            if progress > last_progress:
                last_progress = progress
                yield progress
    process.stdout.close()
    process.wait()
    if process.returncode > 0:
        cmd = _dump_command(command)
        print(cmd)
        print("\n".join(all_output))
