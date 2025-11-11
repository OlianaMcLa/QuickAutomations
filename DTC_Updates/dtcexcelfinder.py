import pandas as pd

#testPath= r'\\mal-plfile01\DataAcquisition\DataAcquisition_New\DataAcquisition\Software Integration Validation\Programs\P16\PF4.7\03. DTCs\VIN65\20230308\P16_DTCs_VIN65_20230308_AfterRun.xlsx'

class ExcelDtcInfo(object):
    def __init__(self, excelPath):
        self.excel = pd.ExcelFile(excelPath)
        self.sheetNames = self.excel.sheet_names

    def findTheRightSheet(self, name):
        for i, sheet in enumerate(self.sheetNames):
            if name.lower() in sheet.lower():
                return i
        return -1

    def getDtcFromSheet(self, sheetName):
        dataFrame = pd.read_excel(self.excel, sheet_name=sheetName, skiprows=2, na_values='n/a', keep_default_na=False)
        data = dataFrame.set_index(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'])
        data = list(data.axes[0].T)
        return [list(e) for e in data]

class ExcelToUpdateInfo(object):
    def __init__(self, filePath):
        self.excel = pd.ExcelFile(filePath)
        self.sheetNames = self.excel.sheet_names
        self.writer=pd.ExcelWriter(filePath)

    def writeOnLastRow(self, column, sheet, dataFrame):#TODO: testear si funciona...
        dataNumber= pd.read_excel(self.excel, sheet_name=sheet, na_values='n/a', keep_default_na=False)
        dataNumber= dataNumber.set_index(column)
        dataNumber= list(dataNumber.axes[0].T)
        dataFrame.to_excel(self.writer, sheet_name=sheet, startrow=len(dataNumber), startcol=column,)

    def close(self):
        self.writer.close()
    
def getDtc(excelPath, ecus=[], sheet='conf'):
    dtcExcel = ExcelDtcInfo(excelPath=excelPath)
    data = dtcExcel.getDtcFromSheet(dtcExcel.findTheRightSheet(sheet))
    if len(ecus)==0:
        return data
    else:
        ecusData=list()
        for ecu in ecus:
            ecusData.extend([e for e in data if ecu in e[1]])
        return ecusData
    
def getAllDtc(excelPath, ecus=[]):
    data=[]
    dtcExcel = ExcelDtcInfo(excelPath=excelPath)
    datac=[]
    datap=[]
    datas=[]
    if dtcExcel.findTheRightSheet('conf')!=-1:datac = dtcExcel.getDtcFromSheet(dtcExcel.findTheRightSheet('conf'))
    for c in datac:
        c.append('c')
        data.append(c)
    if dtcExcel.findTheRightSheet('pend')!=-1:datap = dtcExcel.getDtcFromSheet(dtcExcel.findTheRightSheet('pend'))
    for p in datap:
        p.append('p')
        data.append(p)
    if dtcExcel.findTheRightSheet('slc')!=-1:datas = dtcExcel.getDtcFromSheet(dtcExcel.findTheRightSheet('slc'))
    for s in datas:
        s.append('s')
        data.append(s)
    if len(ecus)==0:
        return data
    else:
        ecusData=list()
        for ecu in ecus:
            ecusData.extend([e for e in data if ecu in e[1]])
        return ecusData

def getConfirmedDtc(excelPath, ecus=[]):
    return getDtc(excelPath=excelPath, ecus=ecus, sheet='conf')

def getPendingDtc(excelPath, ecus=[]):
    return getDtc(excelPath=excelPath, ecus=ecus, sheet='pend')

def getSlcdDtc(excelPath, ecus=[]):
    return getDtc(excelPath=excelPath, ecus=ecus, sheet='slc')
