from jira import JIRA

# tokenLocation = r"C:\Users\armand.solermarti\Documents\Code\JiraToken.txt"
# tokenLocation = r"C:\Users\oliana.cintasgrau\Desktop\token.txt"

class JiraStatus:
    def __init__(self, user, tokenPath):
        with open(tokenPath, 'r') as f:
            token=f.readline()
        self.jiraSession=JIRA(server= 'https://mclaren-automotive.atlassian.net',basic_auth=(user,token.rstrip()))
        
    def jquery(self, jql):
        return self.jiraSession.search_issues(jql)
        
    def getIssue(self, issueId):
        return self.jiraSession.issue(issueId)
    
    def uploadFile(self, issue, filePath):
        self.jiraSession.add_attachment(issue=issue, attachment=filePath)

    def newComment(self, issueId, comment):
        self.jiraSession.add_comment(issueId, comment)

    def modifyField(self, issue, key, data):
        issue.update(fields={key:data})

    def getComments(self, issue):
        return self.jiraSession.comments(issue)
    
    def searchIssues(self, search):
        return self.jiraSession.search_issues(search)

    def uploadFileOnIssue(self, issueId, filePath):
        self.uploadFile(self.getIssue(issueId=issueId), filePath)

    def commentIssue(self,issueId, comment):
        self.newComment(issueId=issueId, comment=comment)

    def addNewOccurrence(self, issueId, comment):
        issue=self.getIssue(issueId=issueId)
        if 'customfield_11202' in issue.raw['fields']:
            occurrences = issue.raw['fields']['customfield_11202']
            if occurrences == None: occurrences=0
            self.modifyField(issue=issue, key='customfield_11202', data=occurrences+1)
        if 'NO_enough' in issue.fields.labels: print('NO ENOUGH')
        else:
            # print('PUT DATA')
            self.newComment(issueId=issueId, comment=comment)

    def addLabel(self,issueId=str, newLabels=list):
        issue = self.getIssue(issueId=issueId)
        if 'labels' in issue.raw['fields']:
            self.modifyField(issue=issue, key='labels', data= issue.raw['fields']['labels'] + newLabels)

    def getLastComment(self,issueId):
        issue=self.getIssue(issueId)
        return self._lastComment(issue, self)

    def _lastComment(issue, session):
        comments = list(session.getComments(issue))
        if len(comments)==0:
            return ''
        else:
            return comments[len(comments)-1]

    def getLastComentFromEveryOpenedIssue(self):
        issuesList=self.searchIssues('resolution = Unresolved AND reporter = currentUser()')
        comments=[]
        for issue in issuesList:
            desc=issue.key+': '+issue.fields.summary+'\n'
            lastComment=self._lastComment(issue=issue, session=self)
            if lastComment=='':
                desc+='No Comments'
            else:
                desc+=lastComment.updated[:10]+' '+lastComment.author.displayName
            comments.append(desc)
        return comments

    def _getListOfIssues(self,issuesId=[]):
        issues=[]
        for id in issuesId:
            issue=self.getIssue(id)
            issues.append(issue)
        return issues

    def getTitlesFromIssues(self,issuesId=[]):
        titles=[]
        issues=self._getListOfIssues(issuesId=issuesId)
        for issue in issues:
            titles.append([issue.key,issue.fields.summary])
        return titles

    def getAssigneeFromIssue(self,issueId=''):
        issue=self.getIssue(issueId)
        return issue.fields.assignee
    
    def newTicket(self, projectKey, summary, description, labels=[], programme='', date='', vehicle=''):
        newIssue=self.jiraSession.create_issue(project={'key':projectKey}, summary=summary, description=description, issuetype={'name':'Fault'}, labels=labels, customfield_10037=programme, customfield_10669=date, customfield_10687=vehicle)
        return newIssue.key