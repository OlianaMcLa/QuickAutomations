from requests.auth import HTTPBasicAuth
import json
import jiraAccess as ja

def searchDTCsInJira(jiraSession, jql):
    url = "https://your-domain.atlassian.net/rest/api/3/search/jql"

    auth = HTTPBasicAuth("email@example.com", "<api_token>")

    headers = {
    "Accept": "application/json"
    }

    query = {
    'jql': 'project = HSP',
    'nextPageToken': '<string>',
    'maxResults': 500,
    'fields': ['*navigable'],
    'expand': '<string>',
    'reconcileIssues': '{reconcileIssues}'
    }
    return jiraSession.searchIssues(jql)

def getcreatdDtcFromPfandProgramme(programme, pf, jiraSession):
    jquery='project = "SVDF" AND "programme[select list (multiple choices)]" = '+programme+' AND affectedversion = '+pf+' AND labels = DTC ORDER BY created DESC'
    return jiraSession.searchIssues(jquery)
jiratkn= r"C:\Users\oliana.cintasgrau\Desktop\token.txt"

jiraSession=ja.JiraStatus(tokenPath=jiratkn)
dtcs= getcreatdDtcFromPfandProgramme("P16MY27", "PF3.0", jiraSession)
print()