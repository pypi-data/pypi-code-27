from typing import Mapping, Any
from dataclasses import dataclass
from tulgey.PortScanResult import PortScanResult
from tulgey.utils import tulgeyDatetime
from datetime import datetime

@dataclass
class IPScanResult:
    ip: str
    isUp: bool
    ports: Mapping[int, PortScanResult]
    scannedPorts: str
    dt: datetime

    def toJsonDict(self) -> Mapping[str, Any]:
        return {
            "ip": self.ip,
            "isUp": self.isUp,
            "ports": [psr.toJsonDict() for psr in self.ports.values()],
            "scannedPorts": self.scannedPorts,
            "datetime": tulgeyDatetime.toString(self.dt),
        }

    @staticmethod
    def fromJsonDict(jsonDict) -> "IPScanResult":
        return IPScanResult(
            jsonDict["ip"],
            jsonDict["isUp"],
            {PortScanResult.fromJsonDict(psrjd).port:PortScanResult.fromJsonDict(psrjd) for psrjd in jsonDict["ports"]},
            jsonDict["scannedPorts"],
            tulgeyDatetime.fromString(jsonDict["datetime"]),
        )
