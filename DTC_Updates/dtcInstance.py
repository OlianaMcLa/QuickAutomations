import datetime

class DtcInstance:
    def __init__(self, uds_code, ECU='', description='',programme='', pf='', date=datetime.date.today(), vehicle='', slc='None', confi='None', pend='None', logsRoot='\\mal-plfile01\DataAcquisition'):
        self.__uds_code = uds_code
        self.ECU = ECU
        self.description = description
        self.programme = programme
        self.pf = pf
        self.date = date
        self.vehicle = vehicle
        self.slc = slc
        self.confi = confi
        self.pend = pend
        self.__logsRoot = '\\'+logsRoot+'\\'+programme+'\\Software_Validation\\'+pf+'\\02. Logs\\'+vehicle+'\\'+date.strftime("%Y%m%d")
        
    def get_sae_code(self):
        import UDStoSAE as tr
        return tr.uds_to_sae_convert(self.__uds_code)
    
    def get_uds_code(self):
        return self.__uds_code
    
    def get_dtc_ecu(self):
        return self.ECU+self.__uds_code
    
    def get_unique_code(self):
        return self.ECU+self.__uds_code+self.date.strftime("%Y%m%d")
    
    def get_log_path(self):
        return self.__logsRoot
    
    def set_confi(self, confi):
        if self.confi != 'None':
            self.confi += '&'+confi
        else:
            self.confi = confi
        return self
            
    def set_pend(self, pend):
        if self.pend != 'None':
            self.pend += '&'+pend
        else:
            self.pend = pend
        return self
            
    def set_slc(self, slc):
        if self.slc != 'None':
            self.slc += '&'+slc
        else:
            self.slc = slc
        return self
    
    def getDetails(self):
        res={}
        res['Date']=self.date
        res['Vehicle']=self.vehicle
        res['SLC']=self.slc
        res['Confi']=self.confi
        res['Pend']=self.pend
        res['Logs Path']=self.get_log_path()
        return res
    