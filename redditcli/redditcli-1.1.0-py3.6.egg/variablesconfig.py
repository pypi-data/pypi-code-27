class variables:
    def initialize(self):
        self.links = []
        self.listed = False
        self.listofsubmissions = []
        self.listofcomments = []
        self.listofsubreddits = []
        self.countlist = 0
        self.countcomments = 0
        self.tempvar = 0
        self.nextprevious = False
        self.nextpreviousnormal = False
        self.nextprevioussubreddits = False
        self.commands = []

    def getvarables(self):
        return (self.links, self.listed, self.listofsubmissions, self.listofcomments, self.listofsubreddits, self.countlist,
                self.countcomments, self.tempvar, self.nextprevious, self.nextpreviousnormal, self.nextprevioussubreddits, self.commands)

    def setlinks(self, links):
        self.links.append(links)
    def emptylinks(self):
        del self.links[:]
    def setlisted(self, listed):
        self.listed = listed
    def setlistofsubmissions(self, listofsubmissions):
        self.listofsubmissions.append(listofsubmissions)
    def emptylistofsubmissions(self):
        del self.listofsubmissions[:]
    def setlistofcomments(self, listofcomments):
        self.listofcomments.append(listofcomments)
    def emptylistofcomments(self):
        del self.listofcomments[:]
    def listofsubreddits(self, listofsubreddits):
        self.listofsubreddits.append(listofsubreddits)
    def emptylistofsubreddits(self):
        del self.listofsubreddits[:]
    def setcountlist(self, countlist):
        self.countlist = countlist
    def setcountcomments(self, countcomments):
        self.countcomments = countcomments
    def settempvar(self, tempvar):
        self.tempvar = tempvar
    def setnextprevious(self, nextprevious):
        self.nextprevious = nextprevious
    def setnextpreviousnormal(self, nextpreviousnormal):
        self.nextpreviousnormal = nextpreviousnormal
    def setnextprevioussubreddits(self, nextprevioussubreddits):
        self.nextprevioussubreddits = nextprevioussubreddits
    def setcommands(self, commands):
        self.commands = commands


