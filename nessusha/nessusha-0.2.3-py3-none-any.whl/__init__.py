from tkinter import filedialog
from bs4 import *
import re
from pprint import *
import pprint
import xlsxwriter
from tkinter import *
import os
from sys import platform
# from tkinter.filedialog import askopenfilename


# Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
#
#
# filename.replace("/", "\\\\")
#
# rawhtml = open(filename,
#                encoding="utf-8").readlines()


def openhtml():
    Tk().withdraw()
    filename =filedialog.askopenfilename()
    if platform =="win32":
        filename.replace("/", "\\\\")

    rawhtml = open(filename,
                   encoding="utf-8").readlines()
    return rawhtml, filename


def allhosts(rawhtml):
    myhosts =set()
    for i in range(len(rawhtml)):
        if re.findall('(?<=<h2 xmlns="">)((\d+\.)+(\d+))(?=(\(*.+)|(</h2>))', rawhtml[i]):
            # print(re.findall('(?<=<h2 xmlns="">)((\d+\.)+(\d+))(?=(\(*.+)|(</h2>))', rawhtml[i])[0][0])
            myhosts.add(re.findall('(?<=<h2 xmlns="">)((\d+\.)+(\d+))(?=(\(*.+)|(</h2>))', rawhtml[i])[0][0])

        else:
            continue
    return myhosts




def foo(hosts, rawhtml):
    dct = {}
    blah = []

    for host in hosts:
        dct[host] = {}

    for i in range(len(rawhtml)):

        if re.findall('(?<=font-weight: bold; font-size: 14px; line-height: 20px; color: #fff;">)(.*?)(?=<)',
                      rawhtml[i]):  # Look for check
            check = re.findall('(?<=font-weight: bold; font-size: 14px; line-height: 20px; color: #fff;">)(.*?)(?=<)',
                               rawhtml[i])[0]
            if "#d43f3a" in rawhtml[i]:
                compliance = "NC - "
            elif "#3fae49" in rawhtml[i]:
                compliance = "C - "
            elif "#ee9336" in rawhtml[i]:
                compliance = "NA - "

            # Add the default value into the dictionary
            for eachhost in dct:
                # dct[eachhost][check] ={"Policy Value": "NA", "Host Value": "NA",
                #                            "Compliance": "NA"}
                if check not in dct[eachhost].keys():
                    dct[eachhost][check] = {"Policy Value": "NA", "Host Value": "NA",
                                            "Compliance": "NA"}
                else:
                    continue

        elif 'Policy Value' in rawhtml[i]:  # Look for desired value
            polvalue = re.findall('(?<=>)(.*?)(?=<)', rawhtml[i + 2])[0]
            for eachhost in dct:
                dct[eachhost][check]["Policy Value"] =polvalue

        elif re.findall('(?<=<h2 xmlns="">)((\d+\.)+(\d+))(?=(\(*.+)|(</h2>))', rawhtml[i]):
            hostname = re.findall('(?<=<h2 xmlns="">)((\d+\.)+(\d+))(?=(\(*.+)|(</h2>))', rawhtml[i])[0][0]

            value =[]
            if re.findall('(?<=>)(.+?)(?=<div)', rawhtml[i + 2]):  # Look for host value
                value += re.findall('(?<=>)(.+?)(?=<div)', rawhtml[i + 2])

                if len(value) <=1:
                    dct[hostname][check]["Host Value"] =compliance +str(value[0])
                else:
                    addedvalue = "\n".join(map(str, value))
                    dct[hostname][check]["Host Value"] =compliance +str(addedvalue)

        else:
            continue

    return dct

def reformat(mydic):
    optdic = {}
    listofhosts =[]
    for host in mydic:
        listofhosts.append(host)
        if len(mydic[host]) == 0:
            continue
        else:
            for check in mydic[host]:
                if check not in optdic:
                    optdic[check] = {}
                    # print(mydic[host])
                    # print(mydic[host][check]['Host Value'])
                    optdic[check][host] = mydic[host][check]['Host Value']
                else:
                    optdic[check][host] = mydic[host][check]['Host Value']

    return optdic, listofhosts


def reformatforprint(newdic, hosts, filename):
    row = 1
    colum = 1
    dicofhosts = {}

    outputpath = re.findall("(?<=\/)(\w+)(?=\.\D+)", filename)[0]
    workbook = xlsxwriter.Workbook('%r_Output.xlsx' %outputpath)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 51)
    worksheet.set_column(1, len(hosts), 18)

    # Wrap content
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()

    # Light red fill with dark red text.
    formatr = workbook.add_format({'bg_color': '#FFC7CE',
                                   'font_color': '#9C0006'})
    # Green fill with dark green text.
    formatg = workbook.add_format({'bg_color': '#C6EFCE',
                                   'font_color': '#006100'})

    bold = workbook.add_format({'bold': 1})
    for host in hosts:
        worksheet.write(0, colum, host)
        dicofhosts[host] = colum
        colum +=1

    # print(dicofhosts)
    for check in newdic:
        # print(check)
        worksheet.write(row, 0, check, cell_format)
        # print(newdic[check])
        for thehost in newdic[check]:
            # print(dicofhosts[thehost])
            worksheet.write(row, dicofhosts[thehost], newdic[check][thehost], cell_format)
        row +=1

    worksheet.conditional_format('A1:Z999', {'type': 'text',
                                           'criteria': 'begins with',
                                           'value': 'NC - ',
                                           'format': formatr})

    worksheet.conditional_format('A1:Z999', {'type': 'text',
                                             'criteria': 'begins with',
                                             'value': 'C - ',
                                             'format': formatg})
    workbook.close()
    optpath =os.path.abspath('%r_Output.xlsx' %outputpath)
    optpathmc =os.path.abspath('%r_Output.xlsx' %("'" +outputpath +"'"))
    print("Output path: " + optpath)

    if platform =="win32":
        os.system("start " + optpath)

    elif platform =="linux":
        os.system("xdg-open " + optpath)

    else:
        os.system("open " +optpathmc)





def htmlparser():
    rawhtml, filename =openhtml()
    hhosts =allhosts(rawhtml)
    haha =foo(hhosts, rawhtml)

    a, b = reformat(haha)
    reformatforprint(a, b, filename)
    print("Done! Next!")




# hhosts =allhosts()
# haha =foo(hhosts)
# # print(type(haha))
# # print(haha)
# a, b =reformat(haha)
# # print(a)
# reformatforprint(a, b)
# print("Done! Next!")
# htmlparser()
