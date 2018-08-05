from typing import Mapping, Any
from enum import Enum
from dataclasses import dataclass


class PortStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    # Are there other ones? Like filtered? Do we care? Does masscan care?

    def __repr__(self):
        return "PortStatus." + self.name

    def __str__(self):
        return self.name

    @staticmethod
    def fromString(str: str) -> "PortStatus":
        if str == "OPEN":
            return PortStatus.OPEN
        if str == "CLOSED":
            return PortStatus.CLOSED
        raise Exception("Got invalid PortStatus=%s" % str)


@dataclass(frozen=True)
class PortScanResult:
    port: int
    status: PortStatus
    serviceName: str
    banner: str

    def toJsonDict(self) -> Mapping[str, Any]:
        return {
            "port": self.port,
            "status": str(self.status),
            "serviceName": self.serviceName,
            "banner": self.banner,
        }

    @staticmethod
    def fromJsonDict(jsonDict) -> "PortScanResult":
        return PortScanResult(
            jsonDict["port"],
            PortStatus.fromString(jsonDict["status"]),
            jsonDict["serviceName"],
            jsonDict["banner"],
        )
