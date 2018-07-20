# coding=utf-8
# author zhangchao
import logging
import datetime
import os
from command import CommandRunner
import re
import time
import sys
import zipfile

from string_utils import gen_random_str


class AdbUtil:

    def __init__(self, device_id="", logger_name=None):
        self.device_id = device_id
        self.logger = logging.getLogger(logger_name)

    @staticmethod
    def get_aapt_path():
        base_dir = os.getcwd()
        if sys.platform == "win32":
            aapt_path = os.path.join(base_dir, "aapt.exe")
        else:
            aapt_path = os.path.join(base_dir, "aapt")
        return aapt_path

    @staticmethod
    def list_devices():
        command = "adb devices"
        cmd = CommandRunner(command, 180)
        code, output = cmd.run()
        devices = output.split("\n")
        device_list = []
        for device in devices[1:]:
            device_id = device.replace("device", "").strip()
            if len(device_id) == 0:
                continue
            device_list.append(device_id)

        return device_list

    @staticmethod
    def run_command(command, timeout=180):
        cmd = CommandRunner(command, timeout)
        code, output = cmd.run()
        return output

    @classmethod
    def get_apk_permissions(cls, apk_path):
        # get package name
        aapt_command = "%s d permissions %s" % (cls.get_aapt_path(), apk_path)
        content = cls.run_command(aapt_command)
        pattern = re.compile(".*name='(.*)'")
        permissions = []
        for line in content.split("\n"):
            if line.startswith("package"):
                continue

            matcher = pattern.match(line)
            if matcher:
                permissions.append(matcher.group(1).strip())

        return permissions

    @classmethod
    def get_apk_icon(cls, apk_path):
        aapt_command = "%s d badging %s" % (cls.get_aapt_path(), apk_path)
        content = cls.run_command(aapt_command)
        pattern = re.compile(".*application-icon-.*:'(.*)'")
        icons = []
        for line in content.split("\n"):
            matcher = pattern.match(line)
            if matcher:
                icons.append(matcher.group(1).strip())

        if len(icons) == 0:
            return None

        zip_f = zipfile.ZipFile(apk_path)
        icon_data = zip_f.read(icons[-1])
        save_dir = "icon"
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        apk_name = os.path.basename(apk_path)
        suffix = icons[-1].split(".")[-1]
        save_path = "%s/%s.%s" % (save_dir, apk_name.replace(".apk", ""), suffix)

        if not os.path.exists(save_path):
            with open(save_path, 'w+b') as f:
                f.write(icon_data)
        return save_path

    def adb_command(self, command, timeout=180):
        if len(self.device_id) != 0:
            cmd = "adb -s %s %s" % (self.device_id, command)
        else:
            cmd = "adb %s" % command
        return self.run_command(cmd, timeout)

    def keep_app_alive(self, package):
        running_apps = self.get_running_apps()
        if package not in running_apps:
            self.start_app(package)

    def set_phone_time(self):
        now_time = datetime.datetime.now().strftime('%m%d%H%M%Y.%S')
        command = "shell date %s" % now_time
        self.adb_command(command)

    def prepare_phone_for_test(self):
        # root
        self.adb_command("root")
        # 最大化休眠时间
        self.adb_command("shell settings put system screen_off_timeout 1800000")
        # 取消时区自动获取
        self.adb_command("shell settings put global auto_time 0")
        # 接电不息屏
        self.adb_command("shell settings put global stay_on_while_plugged_in 3")
        # 禁止旋转
        self.adb_command("shell settings put system user_rotation 0")
        # 24小时制
        self.adb_command("shell settings put system time_12_24 24")
        # 设置当前时间
        self.set_phone_time()

    def start_app(self, package):
        self.adb_command("shell monkey -p %s -c android.intent.category.LAUNCHER 1" % package)

    def install_app(self, apk_path):
        return self.adb_command("install -r %s" % apk_path)

    def uninstall_app(self, package):
        self.adb_command("uninstall %s" % package)

    def monkey_app(self, package, times):
        return self.adb_command("shell monkey -p %s %d" % (package, times))

    def uninstall_app(self, package):
        self.adb_command("uninstall %s" % package)
        self.adb_command("shell rm -fr /data/app/%s*" % package)

    def clear_data(self, package):
        self.adb_command("shell pm clear %s" % package)

    def get_install_path(self, package):
        return self.adb_command("shell pm path %s" % package)

    def stop_app(self, package):
        running_apps = self.get_running_apps()
        if package in running_apps:
            self.adb_command("shell am force-stop %s" % package)

    def kill_app(self, package):
        self.adb_command("shell killall %s" % package)

    def get_packages(self, white_list=[]):
        command = "shell pm list package -3"
        content = self.adb_command(command)

        package_list = []
        for line in content.split("\n"):
            try:
                package = line.split(":")[1].strip()

                is_white = 0
                for white_app in white_list:
                    if package.find(white_app) != -1:
                        is_white = 1
                        break
                if is_white == 1:
                    continue

                package_list.append(package)
            except:
                pass
        return package_list

    def clean_all_app(self, white_list):
        package_list = self.get_packages(white_list)
        for package in package_list:
            self.stop_app(package)
            self.uninstall_app(package)

    def enable_wifi(self):
        self.adb_command("shell svc wifi enable")

    @classmethod
    def get_apk_package(cls, apk_path):
        name_pattern = re.compile(".*name=\'(.*?)\'.*")

        # get package name
        aapt_command = "%s d badging %s" % (cls.get_aapt_path(), apk_path)
        content = cls.run_command(aapt_command)
        for line in content.split("\n"):
            match = name_pattern.match(line)
            if match:
                return match.group(1)

        return None

    def disable_airplane_model(self):
        self.adb_command("shell settings put global airplane_mode_on 0")
        self.adb_command("shell am broadcast -a android.intent.action.AIRPLANE_MODE")

    def hide_status_bar(self):
        self.adb_command("settings put global policy_control immersive.full=*")

    def reboot_device(self, password):
        self.adb_command("reboot")
        while True:
            device_online = self.device_id in self.list_devices()
            if device_online:
                break
            time.sleep(5)
            print "waiting for %s bootup..." % self.device_id

        print "device %s bootup success..." % self.device_id
        time.sleep(15)
        self.adb_command("shell input tap 1178 1452")
        self.adb_command("shell input text %s" % password)
        self.adb_command("shell input keyevent 66")
        time.sleep(15)
        self.adb_command("shell input tap 1178 1452")

    def check_if_screen_on(self):
        content = self.adb_command("shell dumpsys window policy")
        for line in content.split("\n"):
            if line.find("mScreenOnEarly") != -1:
                if line.find("mScreenOnEarly=false") != -1:
                    return False
                if line.find("mScreenOnEarly=true") != -1:
                    return True

    def check_if_screen_lock(self):
        content = self.adb_command("shell dumpsys window policy")
        for line in content.split("\n"):
            if line.find("isStatusBarKeyguard") != -1:
                if line.find("isStatusBarKeyguard=false") != -1:
                    return False
                if line.find("isStatusBarKeyguard=true") != -1:
                    return True

    def unlock_device(self, password):
        if self.check_if_screen_on():
            self.adb_command("shell input keyevent 26")
            time.sleep(2)
        self.adb_command("shell input keyevent 26")
        if not self.check_if_screen_lock():
            return
        # adb_command(device_id, "shell input keyevent 66")
        self.adb_command("shell input keyevent 82")
        self.adb_command("shell input text %s" % password)
        self.adb_command("shell input keyevent 66")

    def retrieve_data(self, pattern, local_dir):
        command = "shell ls /sdcard/"
        output = self.adb_command(command)
        for file_name in output.split("\n"):
            file_name = file_name.strip()
            match = pattern.match(file_name)
            if match:
                print "get", file_name
                command = "pull /sdcard/%s %s" % (file_name, "%s/%s_%s_%s" % (local_dir, self.device_id, gen_random_str(4), file_name))
                self.adb_command(command)
                print command

    def get_running_apps(self):
        command = "shell ps -A"
        output = self.adb_command(command)
        pattern = re.compile("\s+")
        running_apps = []
        for line in output.split("\n"):
            line = line.strip()
            if len(line) == 0:
                continue
            parts = pattern.split(line)
            if not parts[0].startswith("u0"):
                continue

            if parts[-1].find(".") == -1:
                continue

            package = parts[-1].split(":")[0]
            running_apps.append(package)

        return running_apps

    def get_crash_packages(self):
        output = self.adb_command("logcat -s AndroidRuntime -t 10000")
        pattern = re.compile(".*AndroidRuntime: Process: (.*), PID:.*")
        crash_packages = []
        for line in output.split("\n"):
            match = pattern.match(line)
            if match:
                crash_package = match.group(1).strip()
                crash_package = crash_package.split(":")[0].strip()
                crash_packages.append(crash_package)

        return crash_packages, output


if __name__ == "__main__":

    adb_util = AdbUtil("6e50acb9")
    pattern = re.compile(".*\d{4}_\d{2}_\d{2}.csv")
    # adb_util.retrieve_data(pattern, "./")
    print adb_util.get_apk_icon("FBB5F61C084A2922BD1A7B1D424314B0.apk")

    exit()
    sample_dir = sys.argv[1]
    device_admin_permission = "android.permission.BIND_DEVICE_ADMIN"
    count = 0
    total = 0
    for file_name in os.listdir(sample_dir):
        if not file_name.endswith(".apk"):
            continue
        total += 1
        file_path = os.path.join(sample_dir, file_name)
        print file_path
        permissions = adb_util.get_apk_permissions(file_path)
        if device_admin_permission in permissions:
            count += 1

    print "result: %d/%d" % (count, total)
