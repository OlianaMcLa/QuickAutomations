import datetime

class DtcIntance:
    def __init__(self, uds_code, ECU='', programme='', pf='', date=datetime.date.today(), vehicle='', slc=False, confi=False, pend=False, logsRoot='\\mal-plfile01\DataAcquisition'):
        self.__uds_code = uds_code
        self.ECU = ECU
        self.programme = programme
        self.pf = pf
        self.date = date
        self.vehicle = vehicle
        self.slc = slc
        self.confi = confi
        self.pend = pend
        self.__logsRoot = logsRoot+'\\'+programme+'\\Software_Validation\\'+pf+'\\02. Logs\\'+vehicle+'\\'+date
        
    def get_sae_code(self):
        import UDStoSAE as tr
        return tr.uds_to_sae_convert(self.__uds_code)
    
    def get_uds_code(self):
        return self.__uds_code
    
    def get_log_path(self):
        return self.__logsRoot
    
    def getDetails(self):
        res={}
        res['Date']=self.date
        res['Vehicle']=self.vehicle
        res['SLC']=self.slc
        res['Confi']=self.confi
        res['Pend']=self.pend
        res['Logs Path']=self.get_log_path()
        return res
        
    