import redis
import re


class RedisDB:
    # This is our connection to the DB.
    dbc = redis.StrictRedis(host='localhost', port=6379, db=0)
    # This is a dictionary we use to map abbreviations to full text.
    MajorDict = {'': '', 'interdisciplinary': 'Interdisciplinary', 'ae': 'Aerospace Engineering', 'al': 'Applied Languages', 'am': 'Applied Mathematics', 'ap': 'Applied Physics', 'arch': 'Architecture', 'biochem': 'Biochemistry', 'bme': 'Biomedical Engineering', 'ba': 'Business Administration', 'chbe': 'Chemical and Biomolecular Engineering', 'chem': 'Chemistry', 'civil': 'Civil Engineering', 'ce': 'Computer Engineering', 'cm': 'Computational Media', 'cs': 'Computer Science', 'dm': 'Discrete Mathematics', 'eas': 'Earth and Atmospheric Sciences',
                     'econ': 'Economics', 'ee': 'Electrical Engineering', 'environmental': 'Environmental Engineering', 'global': 'Global Economics', 'hts': 'History, Technology, and Society', 'id': 'Industrial Design', 'isye': 'Industrial Engineering', 'inta': 'International Affairs', 'me': 'Mechanical Engineering', 'mse': 'Materials Science and Engineering', 'ne': 'Nuclear Engineering', 'physics': 'Physics', 'psychology': 'Psychology', 'pubp': 'Public Policy', 'pp':'Public Policy', 'stac': 'Science, Technology, and Culture', 'ece': 'Electrical and Computer Engineering'}

    # If we're just starting the database and numSubmissions doesn't exist,
    # create it and set to 0
    def init(self):
        self.dbc.setnx('numSubmissions', '0')

    def saveToDB(self, form):
        self.init()
        # Save the event in the database as a hash
        self.dbc.incr('numSubmissions')
        numSubmissions = int(self.dbc.get('numSubmissions'))
        if numSubmissions < 10:
            submission = "submission00" + str(numSubmissions)
        elif numSubmissions < 100:
            submission = "submission0" + str(numSubmissions)
        else:
            submission = "submission" + str(numSubmissions)
        # We use this function to handle saving information of a varying
        # number of team members.
        info = self.compileTeamMemberData(form, submission)

        self.dbc.hset(submission, 'teamName', form.teamName.data)
        self.dbc.hset(submission, 'projectName', form.teamProjectName.data)
        self.dbc.hset(submission, 'memberCount', form.teamMemberCount.data)
        self.dbc.hset(submission, 'projectMajor', form.teamProjectMajor.data)
        self.dbc.hset(submission, 'section', form.teamSection.data)
        self.dbc.hset(submission, 'sponsor', form.teamSponsor.data)
        self.dbc.hset(submission, 'needsPower', form.teamNeedsPower.data)
        self.dbc.hset(submission, 'hasDisplay', form.teamHasDisplay.data)
        self.dbc.hset(submission, 'hasDanger', form.teamHasDanger.data)
        self.dbc.hset(submission, 'setup', form.teamSetup.data)
        self.dbc.hset(
            submission, 'projectDescription', form.teamProjectDescription.data)
        self.dbc.hset(submission, 'email', form.teamEmail.data)
        self.dbc.hset(submission, 'shirtsSmall', info["S"])
        self.dbc.hset(submission, 'shirtsMedium', info["M"])
        self.dbc.hset(submission, 'shirtsLarge', info["L"])
        self.dbc.hset(submission, 'shirtsXL', info["XL"])
        self.dbc.hset(submission, 'shirtsXXL', info["XXL"])
        self.dbc.hset(submission, 'shirtsXXXL', info["XXXL"])
        self.dbc.hset(submission, 'setupTime', form.teamSetupTime.data)

    # Takes the form data and figures out the list of names, majors, and shirt sizes
    # based on the number of team members

    def compileTeamMemberData(self, form, submission):
        numMembers = int(form.teamMemberCount.data)
        info = {"S": 0, "M": 0, "L": 0, "XL": 0, "XXL": 0,
                "XXXL": 0, "names": "", "majors": ""}

        if numMembers > 0:
            info[form.TMShirt1.data] += 1
            self.dbc.hset(submission, 'name1', form.TMName1.data)
            self.dbc.hset(submission, 'name1Major', form.TMMajor1.data)
        if numMembers > 1:
            info[form.TMShirt2.data] += 1
            self.dbc.hset(submission, 'name2', form.TMName2.data)
            self.dbc.hset(submission, 'name2Major', form.TMMajor2.data)
        if numMembers > 2:
            info[form.TMShirt3.data] += 1
            self.dbc.hset(submission, 'name3', form.TMName3.data)
            self.dbc.hset(submission, 'name3Major', form.TMMajor3.data)
        if numMembers > 3:
            info[form.TMShirt4.data] += 1
            self.dbc.hset(submission, 'name4', form.TMName4.data)
            self.dbc.hset(submission, 'name4Major', form.TMMajor4.data)
        if numMembers > 4:
            info[form.TMShirt5.data] += 1
            self.dbc.hset(submission, 'name5', form.TMName5.data)
            self.dbc.hset(submission, 'name5Major', form.TMMajor5.data)
        if numMembers > 5:
            info[form.TMShirt6.data] += 1
            self.dbc.hset(submission, 'name6', form.TMName6.data)
            self.dbc.hset(submission, 'name6Major', form.TMMajor6.data)
        if numMembers > 6:
            info[form.TMShirt7.data] += 1
            self.dbc.hset(submission, 'name7', form.TMName7.data)
            self.dbc.hset(submission, 'name7Major', form.TMMajor7.data)
        if numMembers > 7:
            info[form.TMShirt8.data] += 1
            self.dbc.hset(submission, 'name8', form.TMName8.data)
            self.dbc.hset(submission, 'name8Major', form.TMMajor8.data)
        if numMembers > 8:
            info[form.TMShirt9.data] += 1
            self.dbc.hset(submission, 'name9', form.TMName9.data)
            self.dbc.hset(submission, 'name9Major', form.TMMajor9.data)
        if numMembers > 9:
            info[form.TMShirt10.data] += 1
            self.dbc.hset(submission, 'name10', form.TMName10.data)
            self.dbc.hset(submission, 'name10Major', form.TMMajor10.data)

        return info

    def getAllEntries(self):
        self.init()
        listOfEntries = self.dbc.keys("submission*")
        listOfEntries.sort()
        entryList = []
        for x in listOfEntries:
            entryList.append(self.dbc.hgetall(x))
        return sorted(entryList, key=lambda k: k['projectName'])

    def getOneSubmission(self, submissionNum):
        submission = self.dbc.hgetall(submissionNum)
        for x in range(1, 11):
            whichOne = "name" + `x`+"Major"
            if whichOne not in submission:
                break
            submission[whichOne] = self.MajorDict.get(submission[whichOne])
        submission['projectMajor'] = self.MajorDict.get(submission['projectMajor'])
        return submission

    def getAllEntriesWithSubmissionNums(self):
        self.init()
        listOfEntries = self.dbc.keys("submission*")
        listOfEntries.sort()
        entryList = []
        for x in listOfEntries:
            entryList.append([self.dbc.hgetall(x), x])
        return sorted(entryList, key=lambda k: k[0]['projectName'])

    def getAllNames(self):
        self.init()
        listOfEntries = self.dbc.keys("submission*")
        listOfEntries.sort()
        entryList = []
        for x in listOfEntries:
            nameEntry = {}
            for y in range(1, 11):
                if self.dbc.hget(x, "name" + str(y)):
                    nameEntry = {}
                    nameEntry["name"] = self.dbc.hget(x, "name" + str(y))
                    nameEntry["major"] = self.dbc.hget(
                        x, "name" + str(y) + "Major")
                    nameEntry["teamName"] = self.dbc.hget(x, "teamName")
                    nameEntry["projectName"] = self.dbc.hget(x, "projectName")
                    nameEntry["projectMajor"] = self.dbc.hget(
                        x, "projectMajor")
                    nameEntry["section"] = self.dbc.hget(x, "section")
                    entryList.append(nameEntry)
        return entryList

    def search(self, string):
        self.init()
        entryList = self.getAllEntriesWithSubmissionNums()
        newEntryList = []
        searchTerms = string.lower().split()
        for x in entryList:
            addIt = True
            for searchTerm in searchTerms:
                pattern = r"\b%s\b" % searchTerm
                searchArea = x[0].get("projectDescription") + " " + x[0].get("projectName") + " " + x[0].get(
                    "teamName") + " " + x[0].get("projectMajor") + " " + self.MajorDict.get(x[0].get("projectMajor")) + " " + x[0].get("table") + " " 
                for y in range(1,11):
                    nameString = "name" + str(y)
                    if(x[0].get(nameString)!= None):
                        searchArea = searchArea + x[0].get(nameString) + " "
                if(x[0].get("sponsor") != None):
                    searchArea = searchArea + x[0].get("sponsor") + " "
                searchArea = searchArea.lower()
                if (re.search(pattern, searchArea) == None):
                    addIt = False
                    break
            if(addIt == True):
                newEntryList.append(x)
        return sorted(newEntryList, key=lambda k: k[0]['projectName'])
