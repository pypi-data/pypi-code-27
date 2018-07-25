# author:QiQi ,Create on 2018/07/25
# check Que_order_job, read que_order_head, que_order_Line to  Scm_order_head , Scm_order_line
#-*- encoding=utf-8 -*-
import  datetime
import traceback
import sys
import  sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging
import amiconn
from seqmastermod import  SeqMasterMod, SeqLineMod

class SeqMasterMng(object):
    def __init__(self,session,pjId,appId,seqCd,unitId=0):
        self.pjId=pjId
        self.appId=appId
        self.unitId=unitId
        self.seqCd=seqCd
        self.seqNoList=[]
        self.lastSeqNo=""
        # create session
        sessionConn=str(session.bind.engine.url)
        engine = create_engine(sessionConn, echo=False)
        dbSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        self.session = dbSession()

    def run(self,num=1):
        try:
            filterText="((app_pj_id={0} and app_pj_type='p') or (app_pj_id={0} and app_pj_type='p'))".format(self.pjId,self.appId)
            seqMasterMod = self.session.query(SeqMasterMod).filter(SeqMasterMod.status >= 0,SeqMasterMod.seqCd==self.seqCd,SeqMasterMod.unitId==self.unitId) \
                .filter(text(filterText)).order_by(desc(SeqMasterMod.appPjType)).first()
            #=============
            if  seqMasterMod==False:
                errMsg="seq_master not find"
                raise errMsg
            #============
            seqType=seqMasterMod.seqType
            #==
            seqLineMod=self.session.query(SeqLineMod).filter(SeqLineMod.pjId==self.pjId,SeqLineMod.seqType==SeqMasterMod.seqType,SeqLineMod.unitId==self.unitId,SeqLineMod.status>=0).first()
            if seqLineMod==None:
                seqLineMod=SeqLineMod()
                seqLineMod.pjId=self.pjId
                seqLineMod.unitId=self.unitId
                seqLineMod.seqType=seqMasterMod.seqType
                seqLineMod.nowSeq=0
                self.session.add(seqLineMod)
                nowSeq=0
            else:
                seqLineMod.operateTime=datetime.datetime.now()
                self.session.commit()   # update and lock this record !
                nowSeq=seqLineMod.nowSeq
            for  i in range(num):
                nowSeq+=seqMasterMod.step
                if  nowSeq>seqMasterMod.maxSeq:
                    nowSeq=seqMasterMod.minSeq
                strSeq=seqMasterMod.preNo+str(nowSeq).rjust(seqMasterMod.seqLength,seqMasterMod.fillLetter)+seqMasterMod.aftNo
                self.seqNoList.append(strSeq)
                self.lastSeqNo=strSeq
            seqLineMod.nowSeq=nowSeq
            self.session.commit()
            self.session.close()
        except Exception as e:
            self.session.close()
            logging.error(traceback.print_exc())
            raise e

def _getSession():
    connString = amiconn.GetMsSqlConnStringByConnName("300",11)
    engine = create_engine(connString, echo=False)
    dbSession = sessionmaker(bind=engine,autocommit=False,autoflush=False)
    session = dbSession()
    return  session

def test():
    session=_getSession()
    seqMasterMng=SeqMasterMng(session,81009,0,"od")
    seqMasterMng.run(100)
    orderNo=seqMasterMng.lastSeqNo
    print(orderNo)

if  __name__=="__main__":
    test()
    #print("good morning")





