from io import StringIO
import xml.etree.ElementTree as ET


LLL2 = u"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
   xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
   SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<SOAP-ENV:Body>
<m:GetAttachDeviceResponse xmlns:m="urn:NETGEAR-ROUTER:service:DeviceInfo:1">    <NewAttachDevice>6@1;192.168.0.1;GOOGLE-HOME-MINI;11:22:24;wireless;61;11;Allow@2;192.168.0.2;LALALA;11:22:33:44:55:66;wireless;121;11;Allow@3;192.168.0.9;;11:22:33:44:55:79;wireless;2;50;Allow@4;192.168.0.7;XXX;11:22:33:44:55:66;wireless;64;61;Allow@5;192.168.0.2;DDD;11:11:11:11:22:33;wireless;71;78;Allow@6;192.168.1.11;GFRTER;11:11:22:22:33:44;wireless;11;11;Allow</NewAttachDevice>
</m:GetAttachDeviceResponse>
<ResponseCode>000</ResponseCode>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

LLL = u"""<?xml version="1.0" encoding="UTF-8"?>
<soap-env:Envelope
        xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"
        soap-env:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
        >
<soap-env:Body>
    <m:GetAttachDeviceResponse
        xmlns:m="urn:NETGEAT-ROUTER:service:DeviceInfo:1">
        <NewAttachDevice>15@1;192.168.10.2;DD-WRT;20:4E:7F:71:D5:AB;wired;;100;Allow@2;192.168.10.4;EmilieTmsiniPad;A8:FA:D8:3F:5F:71;wireless;52;60;Allow@3;192.168.10.5;WN2000RPTv2;4C:60:DE:E5:BB:DA;wireless;216;100;Allow@4;192.168.10.6;ESP_8102F6;BC:DD:C2:81:02:F6;wireless;72;75;Allow@5;192.168.10.8;Haralds-iPad;98:FE:94:7D:F2:DC;wireless;58;55;Allow@6;192.168.10.9;Living room;EC:66:D1:0C:C0:97;wireless;36;83;Allow@7;192.168.10.10;Apple-TV;1C:1A:C0:6C:49:E6;wireless;72;76;Allow@8;192.168.10.13;Fiskene;28:10:7B:05:16:DF;wireless;52;64;Allow@9;192.168.10.14;--;00:23:C1:14:10:01;wired;;100;Allow@10;192.168.10.16;sonoff_switch_1-2015;B4:E6:2D:24:E7:DF;wireless;12;55;Allow@11;192.168.10.19;pi-gw;B8:27:EB:E6:68:0C;wired;;100;Allow@12;192.168.10.20;DESKTOP-R5K1PV1;00:24:D7:64:13:28;wireless;117;60;Allow@13;192.168.10.23;7pgmini;00:24:D6:82:65:18;wireless;150;67;Allow@14;192.168.10.29;homeassistant;B8:27:EB:C0:6B:C8;wireless;72;84;Allow@15;192.168.10.201;NAS520;5C:F4:AB:65:7B:9A;wired;;100;Allow</NewAttachDevice>
    </m:GetAttachDeviceResponse>
    <ResponseCode>000</ResponseCode>
</soap-env:Body>
</soap-env:Envelope>"""


BBB = u"""@1;192.168.30.166;IPCAM;EC:3D:FD:F7:87:A2;wireless;50;56;Allow@2;192.168.30.21;ESP_EDE74A;5C:CF:7F:ED:E7:4A;wireless;70;82;Allow@3;192.168.30.186;IPHONE;3C:2E:FF:10:5C:BB;wireless;761;54;Allow@4;192.168.30.12;ESP_A76BF4;5C:CF:7F:A7:6B:F4;wireless;70;62;Allow@5;192.168.30.155;PHILIPS-HUE;00:17:88:2B:07:DF;wired;;100;Allow@6;192.168.30.182;SUPERIPAD;20:EE:28:3E:F3:B5;wireless;845;64;Allow@7;192.168.30.184;RUNES-MBP;5C:96:9D:70:1D:D7;wireless;439;62;Allow@8;192.168.30.11;ESP_055C8E;2C:3A:E8:05:5C:8E;wireless;50;80;Allow@9;192.168.30.3;ESP_05730E;2C:3A:E8:05:73:0E;wireless;50;70;Allow@10;192.168.30.4;ESP_EAB7F1;5C:CF:7F:EA:B7:F1;wireless;70;100;Allow@11;192.168.30.5;ESP_EAF11C;5C:CF:7F:EA:F1:1C;wireless;56;62;Allow@12;192.168.30.6;ESP_EAEAFC;5C:CF:7F:EA:EA:FC;wired;;100;Allow@13;192.168.30.17;ESP_A396B0;5C:CF:7F:A3:96:B0;wireless;70;88;Allow@14;192.168.30.18;ESP_A3A4E2;5C:CF:7F:A3:A4:E2;wireless;63;72;Allow@15;192.168.30.110;HP9856AF;EC:8E:B5:98:56:B0;wireless;56;62;Allow@16;192.168.30.187;APPLE-TV4K;DC:56:E7:40:2D:95;wireless;845;56;Allow@17;192.168.30.15;ESP_ACAEF5;5C:CF:7F:AC:AE:F5;wireless;56;84;Allow@18;192.168.30.189;LOCALHOST;FC:F1:36:EA:80:52;wired;;100;Allow@19;192.168.30.13;ESP_AF6760;5C:CF:7F:AF:67:60;wireless;56;70;Allow@20;192.168.30.2;ESP_AF6ECF;5C:CF:7F:AF:6E:CF;wireless;70;64;Allow@21;192.168.30.10;ESP_AF647A;5C:CF:7F:AF:64:7A;wireless;70;76;Allow@22;192.168.30.20;ESP_AF110C;5C:CF:7F:AF:11:0C;wireless;70;56;Allow@23;192.168.30.9;ESP_AF6831;5C:CF:7F:AF:68:31;wireless;56;50;Allow@24;192.168.30.28;GW-DCEFCABD27CF;DC:EF:CA:BD:27:CF;wired;;100;Allow@25;192.168.30.8;ESP_29078B;A0:20:A6:29:07:8B;wireless;70;100;Allow@26;192.168.30.180;IPI-6;9C:FC:01:1E:85:D9;wireless;56;64;Allow@27;192.168.30.105;HASSBIANS;4C:60:DE:71:8D:C2;wireless;140;100;Allow@28;192.168.30.7;ESP_FD81E5;5C:CF:7F:FD:81:E5;wireless;70;56;Allow@29;192.168.30.24;<unknown>;00:24:8D:F6:9E:EA;wireless;35;56;Allow@30;192.168.30.181;HONOR_9;5C:03:39:C7:53:06;wireless;285;60;Allow@31;192.168.30.19;ESP_15CAB6;A0:20:A6:15:CA:B6;wireless;70;60;Allow@32;192.168.30.16;ESP_1600D0;A0:20:A6:16:00:D0;wireless;70;88;Allow@33;192.168.30.148;NETTDISKEN;00:11:32:12:73:72;wired;;100;Allow@34;192.168.30.14;ESP_178871;A0:20:A6:17:88:71;wireless;38;40;Allow@35;192.168.30.44;IPCAM;48:02:2D:82:7E:29;wireless;70;70;Allow@36;192.168.30.145;HEIMEN;B8:27:EB:DA:CA:4A;wired;;100;Allow@37;192.168.30.23;ANDROID-E2A0AF84B028CB56;7C:B9:60:0C:68:2D;wireless;70;64;Allow@38;192.168.30.50;MOTIONEYEOS;B8:27:EB:DC:DE:AA;wireless;70;86;Allow@39;192.168.30.183;GAMPAD;64:20:0C:70:FD:1A;wireless;63;62;Allow"""


HHH = u""

UNKNOWN_DEVICE_DECODED = '<unknown>'
UNKNOWN_DEVICE_ENCODED = '&lt;unknown&gt;'


def main():
    devices = []
    # Netgear inserts a double-encoded value for "unknown" devices
    decoded = HHH.strip().replace(UNKNOWN_DEVICE_ENCODED,
                                        UNKNOWN_DEVICE_DECODED)

    if not decoded or decoded == "0":
        return devices

    entries = decoded.split("@")

    # First element is the total device count
    entry_count = None
    if len(entries) > 1:
        entry_count = _convert(entries.pop(0), int)

    if entry_count is not None and entry_count != len(entries):
        print(entry_count)
        print(len(entries))
        print(
            """Number of devices should \
                be: %d but is: %d""".format(entry_count, len(entries)))

    for entry in entries:
        info = entry.split(";")

        if len(info) == 0:
            continue

        # Not all routers will report those
        signal = None
        link_type = None
        link_rate = None
        allow_or_block = None

        if len(info) >= 8:
            allow_or_block = info[7]
        if len(info) >= 7:
            link_type = info[4]
            link_rate = _convert(info[5], int)
            signal = _convert(info[6], int)

        if len(info) < 4:
            print("Unexpected entry: %s".format(info))
            continue
        
        print(info)


def main_old():
    success, node = _find_node(
        LLL,
        u".//GetAttachDeviceResponse/NewAttachDevice")
    if not success:
        return None
    print(node)


def _find_node(response, xpath):
    it = ET.iterparse(StringIO(response))
    # strip all namespaces
    for _, el in it:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]
    node = it.root.find(xpath)
    if node is None:
        print("Error finding node in response: %s".format(response))
        return False, None

    return True, node


def _convert(value, to_type, default=None):
    """Convert value to to_type, returns default if fails."""
    try:
        return default if value is None else to_type(value)
    except ValueError:
        # If value could not be converted
        return default


if __name__ == '__main__':
    main()
