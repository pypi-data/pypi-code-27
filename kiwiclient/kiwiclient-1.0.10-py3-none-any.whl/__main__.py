#  _*_ coding: utf-8
# Client to the KiWi engine for box calculations.
# (c) ISC Clemenz & Weinbrecht GmbH 2018
# License: https://www.apache.org/licenses/LICENSE-2.0
#

import argparse
import configparser
import json
import logging
import logging.handlers
import os
import requests
from shutil import copyfile
import io
import xlrd
import xlsxwriter


LOG = None
KIWI_CFG = None


def init(conf_file_name):
    global LOG, KIWI_CFG
    
    # 1. init logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    LOG = logging.getLogger('kiwi-client')
    logHandler = logging.handlers.RotatingFileHandler('kiwi-client.log',
                                                      maxBytes = 1024 * 1000 * 50,
                                                      backupCount = 5)
    logFmt = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logHandler.setFormatter(logFmt)
    LOG.addHandler(logHandler)
    
    # 2. load configuration
    cfg = io.StringIO()
    prsr = configparser.ConfigParser()
    with open(conf_file_name, mode='r') as f:
        cfg.write(f.read())
        cfg.seek(0,os.SEEK_SET)
        prsr.read_file(cfg)
        
    cfg_dict = dict(prsr.items('kiwi'))
    
    for k,v in cfg_dict.items():
        # check for a comment symbol and remove the comment if found
        pos = v.rfind('#')
        if pos == 0:
            cfg_dict[k] = ''
        elif pos > 0:
            cfg_dict[k] = v[:pos]
        else:
            pass
        cfg_dict[k] = cfg_dict[k].strip() 
        
    KIWI_CFG = cfg_dict
    if not 'kiwi.key' in KIWI_CFG or KIWI_CFG['kiwi.key'] is None:
        raise Exception('No kiwi key')
    

def read_sheet(wb, sheet_name, other_int_fields = None):    
    global LOG
    
    LOG.debug("read sheet: {0}".format(sheet_name))
    sheet = wb.sheet_by_name(sheet_name)
    
    if sheet is None:
        LOG.error("No {0} found".format(sheet_name))
        raise Exception("No {0} found".format(sheet_name))
    
    NAMES_ROW = 0
    # 1. fetch the names
    col_names = list()
    for c in range(sheet.ncols):
        col_names.append(sheet.cell(NAMES_ROW,c).value)
    
    # 2. all data, we start at row 1
    data = list()
    for r in range(1, sheet.nrows):
        row_data = dict()
        for c in range(sheet.ncols):
            if col_names[c] == 'nr':
                if val is None:
                    raise Exception("Value expected in sheet {0} r: {1}, {2}".format(sheet_name, r, c))
                row_data[col_names[c]] = int(sheet.cell(r,c).value)
            elif col_names[c].lower() == 'wert':
                if other_int_fields is not None:
                    if sheet.cell(r, c - 1).value in other_int_fields:
                        val = sheet.cell(r, c).value
                        if val is None:
                            raise Exception("Value expected in sheet {0} r: {1}, {2}".format(sheet_name, r, c))
                        row_data['value'] = int(sheet.cell(r, c).value)
                    else:    
                        row_data['value'] = sheet.cell(r, c).value  
                else:        
                    row_data['value'] = sheet.cell(r, c).value   
            else:    
                row_data[col_names[c]] = sheet.cell(r, c).value
            
        data.append(row_data)
        
    return data    

    
def excel_2_json(excel_file):
    global LOG
        
    wb = xlrd.open_workbook(excel_file)
    
    data = dict()
    data['material'] = read_sheet(wb, 'material')
    
    int_parms = ['AnzBefestigungBolzen',
                 'SelbstTrageK',
                 'STE_Anzahl',
                 'DH_Anzahl',
                 'LK_Anzahl',
                 'KH_Anzahl',
                 'PAL_Anzahl',
                 'AKH_Anzahl',
                 'SL_Anzahl',
                 'KL_Anzahl']
    
    data['params'] = read_sheet(wb, 'parameter', int_parms)
    
    wb.release_resources()
    del wb
    
    return json.dumps(data, indent=2, sort_keys=True)


def box_2_excel(excel_name, box):
    global LOG
    
    nr = 0
    dir_name = os.path.dirname(excel_name)
    base_name = os.path.basename(excel_name)
        
    if dir_name is not None:
        f_name = '{2}/r{0}-{1}'.format(nr, base_name, dir_name)
    else:    
        f_name = 'r{0}-{1}'.format(nr, base_name)
            
    while os.path.exists(f_name):
        nr += 1
        if dir_name is not None:
            f_name = '{2}/r{0}-{1}'.format(nr, base_name, dir_name)
        else:    
            f_name = 'r{0}-{1}'.format(nr, base_name)
            
    LOG.debug('Writing: ' + f_name)
    wb = xlsxwriter.Workbook(f_name)
    sheet = wb.add_worksheet('kiwi-box')
    try:
        row = 1
        for i in box:
            col = 0
            for k, v in i.items():
                sheet.write(row, col, v)
                col += 1
            row += 1    
            
        if len(box) > 0:
            bold = wb.add_format({'bold': 1})
            col = 0
            for k in box[0].keys():
                sheet.write(0, col, k, bold)
                col += 1        
    finally:
        wb.close()    
        
    return f_name    
    

def kiwi_engine(payload):
    global LOG, KIWI_CFG
    
    if payload is None or len(payload) == 0:
        LOG.error("No payload")
        raise Exception('No payload')
    
    url = KIWI_CFG['http.schema'] + "://" + KIWI_CFG['http.host'] + ":" + KIWI_CFG['http.port'] + KIWI_CFG['http.endpoint']
    LOG.debug("Engine url: {0}".format(url))
    
    headers = {'Accept'              : 'application/json',
               'Content-Type'        : 'application/json',
               'Content-Encoding'    : 'utf8',
               'Content-Length'      : str(len(payload)),
               'ISC_KIWI_ENGINE_KEY' : KIWI_CFG['kiwi.key'] }
    
    try:
        rsp = requests.post(url,
                            data=payload,
                            headers=headers,
                            verify=False)
        # rsp = requests.post(url,data=payload,headers=headers,verify=False,auth=(user_name,password))
        if rsp.status_code == requests.codes.ok:
           box = rsp.json()
           #LOG.debug('success')
           return box
        else:
           LOG.error(rsp.status_code)
           LOG.error(rsp.text)
           ret = {'status' : rsp.status_code}
           if rsp.status_code == 400:
               ret['message'] = 'Parameter error'
           elif rsp.status_code == 402:
               ret['message'] = 'Payment required / Invalid key'
           else:
               ret['message'] = 'General error'
           return [ ret ]
    except Exception as x:
        LOG.error(str(x))
        ret = {'status' : -1, 'message' : str(x)}
        return [ ret ]
        
        
def copy_2_default_result(result_file):
    dir_name = os.path.dirname(result_file)
    base_name = os.path.basename(result_file)
    if dir_name is not None:
        if not dir_name in ['', '/']:
            copyfile(result_file, dir_name + "/result.xlsx")
        else:
            copyfile(result_file, "result.xlsx")    
    else:         
        copyfile(result_file, "result.xlsx")
        
           
# ------------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------------            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--excel', type=str, const=True, nargs='?', default=False)
    parser.add_argument('-c', '--conf', type=str, const=True, nargs='?', default='kiwi.ini')
    parser.add_argument('-w', '--wait', type=bool, const=True, nargs='?', default=True)
    args = parser.parse_args()
    
    try:
        init(args.conf)
        
        if args.excel is None or args.excel == '' or not args.excel:
            raise Exception('Need a --excel parameter')
        
        LOG.info("Reading Excel data: {0} ...".format(args.excel))
        payload = excel_2_json(args.excel)
        LOG.debug(payload)
        
        LOG.info("Kiwi engine ....")
        box = kiwi_engine(payload)
        #LOG.debug(box)
        LOG.info("writing to Excel ...")
        res_file = box_2_excel(args.excel, box)
        LOG.info("Copy to default result workbook ...")
        copy_2_default_result(res_file)
        LOG.info("done.")
        
    except Exception as x:
        LOG.error(str(x))    
    finally:
        if args.wait:
            input("Press Enter to continue...")

