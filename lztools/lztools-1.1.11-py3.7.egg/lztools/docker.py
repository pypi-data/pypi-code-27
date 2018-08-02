from lztools.Bash import command_result
from lztools.DataTypes.DockerData import DockerData

def get_running():
    res = command_result("sudo", "docker", "ps", "-a", u"--format '{{.ID}}*{{.Image}}*{{.Command}}*{{.CreatedAt}}*{{.RunningFor}}*{{.Ports}}*{{.Status}}*{{.Size}}*{{.Names}}*{{.Labels}}*{{.Mounts}}*{{.Networks}}'")

    for d in res[1].splitlines():
        yield DockerData(d, delimiter="*")
