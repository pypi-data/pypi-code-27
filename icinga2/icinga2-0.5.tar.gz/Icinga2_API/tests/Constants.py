username = "root"
password = "icinga"
url = "https://localhost:5665"

TestHost_data = {
    "templates": [ "generic-host" ],
    "attrs": {
        "name": "test.localdomain",
        "address": "192.168.1.1",
        "check_command": "hostalive",
        "vars.os" : "Linux"
        }
}
