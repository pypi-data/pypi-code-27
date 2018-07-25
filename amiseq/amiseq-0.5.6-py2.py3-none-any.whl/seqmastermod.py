#-*- encoding=utf-8 -*-
import  datetime
import sys
import uuid
import redis
import  sqlalchemy
import amiconn
import  binascii
from  datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

class SeqMasterMod(Base):
    __tablename__="Seq_master"
    __table_args__ = {'implicit_returning': False}
    id=Column("Id",String(36),primary_key=True)
    appPjId=Column("App_pj_id",BigInteger)
    appPjType=Column("App_pj_type",String(32))
    seqType=Column("Seq_type",String(32))
    seqName=Column("Seq_name",String(64))
    minSeq=Column("Min_seq",BigInteger)
    maxSeq=Column("Max_seq",BigInteger)
    step=Column("Step",Integer)
    fillLetter=Column("Fill_letter",String(1))
    preNo=Column("Pre_no",String(64))
    aftNo=Column("Aft_no",String(64))
    seqLength=Column("Seq_length",Integer)
    status=Column("Status",Integer)
    operateTime=Column("Operate_time",DATETIME,default=func.getdate(),onupdate=func.getdate())
    unitId=Column("Unit_id",BigInteger)
    seqCd=Column("Seq_cd",String(32))
    isWriteSeqLine=Column("Is_write_seq_line",String(1))
    isResetNumByDay=Column("Is_reset_num_by_day",Integer)

class SeqLineMod(Base):
    __tablename__="Seq_line"
    __table_args__ = {'implicit_returning': False}
    id = Column("Id", String(36),primary_key=True)
    pjId = Column("Pj_id", BigInteger)
    unitId = Column("Unit_id", BigInteger)
    seqType = Column("Seq_type", String(32))
    nowSeq = Column("Now_seq", BigInteger)
    status = Column("Status", Integer)
    operateTime = Column("Operate_time", DATETIME,default=func.getdate(),onupdate=func.getdate())

def _getSession():
    connString = amiconn.GetMsSqlConnStringByConnName("300",11)
    print(connString)
    engine = create_engine(connString, echo=False)
    dbSession = sessionmaker(bind=engine,autocommit=False,autoflush=False)
    session = dbSession()
    return  session

def test():
    session=_getSession()
    result= session.query(SeqMasterMod).filter(SeqMasterMod.status >= 0).all()
    for  seqMasterMod in result:
        print(seqMasterMod.id)
    session.close()


#if __name__=="__main__":
#   test()