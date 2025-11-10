import dtcInstance as di
import dtcexcelfinder as defi
import os

dtcPath = r'\\mal-plfile01\DataAcquisition\P28MY27\Software_Validation\PF7.0\01. DTCs'

def getAlldtcFiles(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xlsm') and not file.startswith('~$'):
                filePath = os.path.join(root, file)
                paths.append(filePath)
    return paths
dtcs=[]

for path in getAlldtcFiles(dtcPath):
    dtcs.extend(defi.getAllDtc(path))
    print