import subprocess
import os


def get_connected_devices() -> list:
    """
    Returns a list of tuples containing the Device name and the android Version
    :return:
    """
    devices = []
    devices_output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip("List of devices attached").split("\n")
    for device in devices_output:
        if device is None or device == "":
            pass
        else:
            device_name = device.strip('\tdevice')
            android_version = subprocess.check_output(["adb", "-s", device_name, "shell", "getprop", "ro.build.version.release"])
            devices.append((device_name, android_version.decode('utf-8').strip("\r\n")))

    return devices


def install_app(apk_path=None, device=None) -> bool:
    """
    Installs an APK file into a device.
    The app installed with the -r option so the apk gets replaced it exists or installed if it doenst
    :param apk_path: Path for the APK
    :param device:   Device name
    :return: True if success , False if fail
    """
    path = os.getcwd() + apk_path if str(apk_path).startswith("/") else os.getcwd() + "/" + apk_path

    if apk_path is not None and device is not None:
        if os.path.isfile(path):
            command = ["adb", "-s" , device, "install", "-r", path]
            p = subprocess.Popen(command, stdout=None)
            p.wait()
            p.terminate()
            print("APK {0} was installed in {1}".format(apk_path, device))
            return True
        else:
            print("File {0} not found!".format(path))

    else:
        print("Device and/or apk not found or not specified")
        return False


def is_device_connected(device) -> bool:
    all_connected = get_connected_devices()
    for device_connected, version in all_connected:
        if device == device_connected:
            return True
    return False


def unintall_app(package=None, device=None) -> None:
    """
    Uninstall an app from the device
    :return:
    """
    command = ["adb", "-s", device, "uninstall", package]

    if package is not None:
        if device is None:
            command.pop(1)
            command.pop(1)

        p = subprocess.Popen(command, stdout=None)
        p.wait()
        p.terminate()
    else:
        print("App package was not specified.")


def is_app_installed(package=None, device=None) -> bool:
    """
    Returns True if the package is installed or False if it is not
    :param package:
    :return:
    """
    command = ["adb", "-s", device, "shell", "pm", "list", "packages |", "grep", package]

    if device is None:
        command.pop(1)
        command.pop(1)

    out = subprocess.check_output(command, stderr=None)

    return True if out.decode('utf-8').strip("\r\n") == "package:{0}".format(package) else False


def run_command(arg_string=None, arg_list=None) -> None:
    """
    Run a general ABD command
    :return:
    """
    command = arg_list if arg_list else str(arg_string).split(" ")

    p = subprocess.check_output(command, stderr=None)
    print(p.decode('utf-8'))


def kill_server() -> None:
    """
    Kills the ADB server
    :return: None
    """
    command = ["adb", "kill-server"]

    p = subprocess.Popen(command, stdout=None, stderr=None)
    p.wait(timeout=10)
    print("ADB server has been killed.")


def start_server() -> None:
    """
    Starts the ADB server
    :return: None
    """
    command = ["adb", "start-server"]

    p = subprocess.Popen(command, stderr=None, stdout=None)
    p.wait(timeout=10)
    print("ADB server has been started.")


def get_apk_from_device(package=None, device=None) -> bool:
    """
    Retrieves the APK of an application if it exists
    :param package:
    :param device:
    :return: bool
    """

    # adb shell pm path com.example.someapp
    # adb pull /data/app/com.example.someapp-2.apk path/to/desired/destination

    command_apk_path = ["adb", "-s", device, "pm", "path", package]

    if package is None:
        print("Package is required but it was not specified.")
        return False

    if device is None and len(get_connected_devices()) != 1:
        print("There are multiple devices connected, please specify a device to get the APK from")
        return False

    elif device is None:
        command_apk_path.pop(1)
        command_apk_path.pop(1)

    apk_path = subprocess.check_output(command_apk_path, stderr=None)

    # TODO: Rest of the stuff


def push_file_to_device() -> None:  # For now...
    """
    Pushes a file to the device
    :param device:
    :return: None
    """
    pass


def list_files_in_device() -> None:
    """
    Gets a list of files in a specific folder
    :param device:
    :param path:
    :return: list of files
    """
    pass


def unlock_device(password=None, device=None) -> bool:
    """
    Unlocks a device given a device name and the password
    :param password:
    :param device:
    :return: True is sucess, False if error
    """

    command_input = ["adb", "-s", device, "shell", "input", "text", password]
    command_submit = ["adb", "-s", device, "shell", "input", "keyevent", 66]

    if device is None and len(get_connected_devices()) != 1:
        print("No device was specified and/or multiple devices are connected")
        return False


    if device is None:
        command_input.pop(1)
        command_input.pop(1)
        command_submit.pop(1)
        command_submit.pop(1)

    p = subprocess.Popen(command_input, stdout=None)
    p.wait()
    p.terminate()

    p1 = subprocess.Popen(command_submit, stdout=None)
    p1.wait()
    p1.terminate()

    return True
