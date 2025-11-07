import jiraAccess as ja

def getcreatdDtcFromPfandProgramme(programme, pf, jiraSession):
    jquery='project = "SVDF" AND "programme[select list (multiple choices)]" = '+programme+' AND affectedversion = '+pf+' AND labels = DTC ORDER BY created DESC'
    return jiraSession.searchIssues(jquery)

jiraSession=ja.JiraStatus(tokenPath=r"C:\Users\oliana.cintasgrau\Desktop\token.txt")
dtcs= getcreatdDtcFromPfandProgramme("P16MY27", "PF3.0", jiraSession)
print()