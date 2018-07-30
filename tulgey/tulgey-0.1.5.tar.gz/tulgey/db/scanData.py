from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, Sequence, Boolean, Text, DateTime, LargeBinary

from tulgey.db import Base
from tulgey.PortScanResult import PortScanResult, PortStatus
from tulgey.IPScanResult import IPScanResult
from tulgey.utils.iputils import normalizeIPv6

class PortScanResultModel(Base):
    __tablename__ = "portscanresult"
    id = Column(Integer, primary_key=True)
    port = Column(Integer, nullable=False)
    status = Column(Text, nullable=False)  # "OPEN" || "CLOSED"
    serviceName = Column(Text, nullable=True)
    banner = Column(LargeBinary, nullable=True)

    ipScanResultModel_id = Column(Integer, ForeignKey("ipscanresult.id"))

    @staticmethod
    def frum(portScanResult):
        return PortScanResultModel(
            port=portScanResult.port,
            status=str(portScanResult.status),
            serviceName=portScanResult.serviceName,
            banner=(None if portScanResult.banner is None else portScanResult.banner.encode('utf-8')),
        )

    def to(self) -> PortScanResult:
        return PortScanResult(
            port=self.port,
            status=(PortStatus.fromString(self.status)),
            serviceName=self.serviceName,
            banner=(None if self.banner is None else self.banner.decode('utf-8')),
        )

class IPScanResultModel(Base):
    __tablename__ = "ipscanresult"
    id = Column(Integer, primary_key=True)
    isUp = Column(Boolean, nullable=False)
    scannedPorts = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)

    ip_id = Column(Text, ForeignKey("ip.ip"), index=True)
    portScanResults = relationship("PortScanResultModel", backref="ipscanresult")

    @staticmethod
    def frum(ipScanResult: IPScanResult):
        return IPScanResultModel(
            ip_id=normalizeIPv6(ipScanResult.ip),
            isUp=ipScanResult.isUp,
            scannedPorts=ipScanResult.scannedPorts,
            portScanResults=[
                PortScanResultModel.frum(psr) for psr in ipScanResult.ports.values()
            ],
            datetime=ipScanResult.dt,
        )

    def to(self) -> IPScanResult:
        return IPScanResult(
            ip=normalizeIPv6(self.ip_id),
            isUp=self.isUp,
            ports={psrm.to().port:psrm.to() for psrm in self.portScanResults},
            scannedPorts=self.scannedPorts,
            dt=self.datetime,
        )


class IP(Base):
    __tablename__ = "ip"
    ip = Column(Text, primary_key=True, nullable=False)
    lastScanDate = Column(DateTime, nullable=True, index=True)  # null if it has never been scanned
    lastTraceDate = Column(DateTime, nullable=True, index=True)  # null if it has never been traced
    sources = Column(Text, nullable=False)
    isIPv4 = Column(Boolean, nullable=False)
    everPingable = Column(Boolean, nullable=True)

    ipScanResults = relationship("IPScanResultModel", backref="ip")