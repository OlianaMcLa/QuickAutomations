import dtcInstance as di
import dtcexcelfinder as defi
import datetime as dt
import jiraAccess as ja
import jiraTableClass as jtc
import json
from dataclasses import asdict
import os

tokenPath=r"C:\Users\oliana.cintasgrau\Desktop\token.txt"
dtcPath = r'\\mal-plfile01\DataAcquisition\P28MY27\Software_Validation\PF7.0\01. DTCs'

def getAlldtcFiles(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xlsm') and not file.startswith('~$'):
                filePath = os.path.join(root, file)
                paths.append(filePath)
    return paths

def getTableFromDtcs(dtcs):
    table=jtc.headers_and_cells_to_v2_string(header=['Date','Car','SLC','CONF','PEND','Log Path'], cells=[[d.date.strftime("%Y-%m-%d"), d.vehicle, d.slc, d.confi, d.pend, d.get_log_path()] for d in dtcs])
    return table

def fromTableTov2String(table):
    
    return json.dumps(asdict(table))

dtcs=[]
# Get all DTCs from all files from path
for path in getAlldtcFiles(dtcPath):

    if 'efore' in path: ba='B'
    else: ba='A'

    all=defi.getAllDtc(path)
    baseName = os.path.splitext(os.path.basename(path))[0]
    baseName = path.split(sep='\\')
    for d in all:
        if not d[2].startswith('0x'): continue
        flag=False
        dtcinstance=di.DtcInstance(uds_code=d[2], ECU=d[1], description=d[3], programme=baseName[-7],pf=baseName[-5],date=dt.datetime.strptime(baseName[-2],"%Y%m%d"), vehicle=baseName[-3])
        for dtc in dtcs:
            if dtcinstance.get_unique_code()==dtc.get_unique_code():
                match d[4]:
                    case 'c':
                        dtc.set_confi(ba)
                    case 'p':
                        dtc.set_pend(ba)
                    case 's':
                        dtc.set_slc(ba)
                flag=True
                break
        if not flag:
            match d[4]:
                case 'c':
                    dtcs.append(dtcinstance.set_confi(ba))
                case 'p':
                    dtcs.append(dtcinstance.set_pend(ba))
                case 's':
                    dtcs.append(dtcinstance.set_slc(ba))

# Join same instances
ticketTable = {}
for dtc in dtcs:
    try:
        ticketTable[dtc.get_dtc_ecu()].append(dtc)
    except KeyError:
        ticketTable[dtc.get_dtc_ecu()] = [dtc]
print()

programme = {
                "self": "https://jira.task.mclaren.com/rest/api/3/customFieldOption/17292",
                "value": "P28MY27C",
                "id": "17292"
            }
#     programme={
#                 "self": "https://jira.task.mclaren.com/rest/api/2/customFieldOption/15084",
#                 "value": "P16MY27",
#                 "id": "15084"
#             }

js= ja.JiraStatus(tokenPath=tokenPath)
for key in ticketTable:
    unsortedDtc = ticketTable[key]
    dtcs = sorted(unsortedDtc, key=lambda x: x.date, reverse=True)
    try:
        summary=f"{dtcs[0].ECU} - {dtcs[0].get_uds_code()} - {dtcs[0].description}"
        description=getTableFromDtcs(dtcs)
        js.newTicket(projectKey='SVDF', summary=summary, description=description, labels=['DTC',dtcs[0].get_sae_code(),dtcs[0].get_uds_code(), dtcs[0].ECU],vehicle=[v.vehicle for v in dtcs] , programme=[programme], date= dtcs[dtcs.__len__()-1].date.strftime("%Y-%m-%d")+"T01:00:00.000+0100", nOccurrences=dtcs.__len__())
        print(f"Ticket created for DTC {dtcs[0].get_uds_code()}")
    except Exception as e:
        print(f"Error creating ticket for DTC {dtcs[0].get_uds_code()}: {e}")
