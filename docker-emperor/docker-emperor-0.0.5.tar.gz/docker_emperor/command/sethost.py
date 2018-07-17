
def cmd_sethost(self, host, ip="0.0.0.0"):
    bin_path = os.path.join(self.module_root, 'bin')
    self.cmd("docker run -t -i -v {bin_path}/sethost:/bin/sethost -v /etc/hosts:/etc/hosthosts -v /etc/hosts.bak:/etc/hosthosts.bak busybox sh /bin/sethost {} {}".format(ip, host))
