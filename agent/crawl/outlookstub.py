from cybertools.agent.crawl.mail import MailCrawler

class OutlookCrawlerStub(MailCrawler):
    
    def __init__(self):
        pass
    
    def findOutlook(self):
        print "Returning reference to Outlook Application"
    
    def fetchCriteria(self):
        print "Retrieving Parameters"
    
    def crawlFolders(self):
        print "Crawling Folders"
        self.loadMailsFromFolder()
    
    def loadMailsFromFolder(self):
        print "loading mails from folder"
        self.createResource("SampleMail", "OutlookStubFolder", "OutlookStub")