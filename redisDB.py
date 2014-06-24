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
        self.dbc.setnx('currentSemester', 'Spring2014')
        self.dbc.setnx('numVTips', '0')
        self.dbc.setnx('numSTips', '0')
        self.dbc.setnx('numJTips', '0')
        self.dbc.setnx('numSubmissions', '0')
        self.dbc.setnx('schedule', ' <tr> <td>4:30pm</td> <td>Expo opens to the public</td> </tr> <tr> <td>5:00pm</td> <td>Optional tour of GT Invention Studio spaces at <a href="http://goo.gl/maps/K5vB3" target="_blank"> MRDC Building</a>, 2nd Floor Lobby near room 2211<br> <a href="http://www.capstone.gatech.edu/?page_id=2236#InventionStudioParking" target="_blank"> Invention Studio Tour Parking Information</a><br> A courtesy shuttle will take you to the Expo from MRDC and back</td> </tr> <tr> <td>5:30pm</td> <td>Expo judges preparation meeting at <a href="http://goo.gl/maps/xko7n" target="_blank">McCamish Pavilion</a><br> <a href="http://www.capstone.gatech.edu/?page_id=2236#McCamishPavilionParking" target="_blank">Expo Parking Information</a></td> </tr> <tr> <td>6:00pm</td> <td>Judging begins</td> </tr> <tr> <td>8:00pm</td> <td>Presentation of awards & prizes</td> </tr> <tr> <td>8:30pm</td> <td>Expo concludes</td> </tr> ')
        self.dbc.setnx('busSchedule', ' <tr> <td>5:30pm</td> <td>Bus will begin running from MRDC building to take visitors from Invention Studio tour to McCamish Pavilion</td> </tr> <tr> <td>6:00pm</td> <td>Bus is open to the public - route will run every 15 minutes from MRDC to McCamish Pavilion with no other stops along the way</td> </tr> <tr> <td>9:00pm</td> <td>Bus closes to the public</td> </tr>')
        self.dbc.setnx('schEnd','<a href="http://www.capstone.gatech.edu/wp-content/uploads/2014/03/Capstone-Design-Expo-Spring-2014.pdf" target="_blank">Click here</a> for a downloadable copy of the Expo, GT Invention Studio tour, and parking information.')

    def saveToDB(self, form, semester=None):
        self.init()
        if(semester == None):
            semester = self.getCurrentSemester()
        
        # Save the event in the database as a hash
        self.dbc.incr('numSubmissions')
        numSubmissions = int(self.dbc.get('numSubmissions'))
        if numSubmissions < 10:
            submission = semester + "submission00" + str(numSubmissions)
        elif numSubmissions < 100:
            submission = semester + "submission0" + str(numSubmissions)
        else:
            submission = semester +"submission" + str(numSubmissions)
        # We use this function to handle saving information of a varying
        # number of team members.
        info = self.compileTeamMemberData(form, submission, semester)

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

    def compileTeamMemberData(self, form, submission, semester=None):
        if(semester == None):
            semester = self.getCurrentSemester()
    
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

    def getAllEntries(self, semester=None):
        self.init()
        if(semester == None):
            semester = self.getCurrentSemester()
        listOfEntries = self.dbc.keys(semester + "submission*")
        listOfEntries.sort()
        entryList = []
        for x in listOfEntries:
            entryList.append(self.dbc.hgetall(x))
        return sorted(entryList, key=lambda k: k['projectName'])

    def getOneSubmission(self, submissionNum, semester=None):
        if(semester == None):
            semester = self.getCurrentSemester()
        submission = self.dbc.hgetall(semester + submissionNum)
        for x in range(1, 11):
            whichOne = "name" + `x`+"Major"
            if whichOne not in submission:
                break
            submission[whichOne] = self.MajorDict.get(submission[whichOne])
        submission['projectMajor'] = self.MajorDict.get(submission['projectMajor'])
        return submission

    def getAllEntriesWithSubmissionNums(self, semester=None):
        self.init()
        if(semester == None):
            semester = self.getCurrentSemester()
        listOfEntries = self.dbc.keys(semester + "submission*")
        listOfEntries.sort()
        entryList = []
        for x in listOfEntries:
            entryList.append([self.dbc.hgetall(x), x])
        return sorted(entryList, key=lambda k: k[0]['projectName'])

    def getAllNames(self, semester=None):
        self.init()
        if(semester == None):
            semester = self.getCurrentSemester()
        listOfEntries = self.dbc.keys(semester + "submission*")
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

    def search(self, string, semester=None):
        self.init()
        entryList = self.getAllEntriesWithSubmissionNums(semester)
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
    
    def getCurrentSemester(self):
        self.init()
        return self.dbc.get('currentSemester')
        
    def setCurrentSemester(self, newSemester):
        if(self.dbc.sismember('semesterSet', self.getCurrentSemester()) == 0):
            self.dbc.sadd('semesterSet', self.getCurrentSemester())
        self.dbc.set('currentSemester', newSemester)
        if(self.dbc.sismember('semesterSet', newSemester) == 0):
            self.dbc.sadd('semesterSet', newSemester)
        
    def getAllSemesters(self):
        return self.dbc.smembers('semesterSet')
        
  #  def removeSemester(self, semester):
  #      if(semester != getCurrentSemester()):
  #          self.dbc.srem('semesterSet', semester)
  #  
  #      return 0

#in order to make the webpage edittable, we will store certain text information here so it can easily be editted.

    def addVisTip(self, tip):
		self.dbc.incr('numVTips')
		numVTips = int(self.dbc.get('numVTips'))
		name = 'VTips'+str(numVTips)
		self.dbc.hset(name, "tip", tip) 
		self.dbc.hset(name, "num", str(numVTips)) 

    def addJudTip(self, tip):

		self.dbc.incr('numJTips')
		numJTips = int(self.dbc.get('numJTips'))
		name = 'JTips'+str(numJTips)
		self.dbc.hset(name, "tip",tip) 
		self.dbc.hset(name, "num", str(numJTips)) 


    def addStuTip(self, tip):

		self.dbc.incr('numSTips')
		numSTips = int(self.dbc.get('numSTips'))
		name = 'STips'+str(numSTips)
		self.dbc.hset(name, "tip", tip) 
		self.dbc.hset(name, "num", str(numSTips)) 

    def getAllVTips(self):
		keys = self.dbc.keys('VTips*')
		vTips = [];
		for x in keys:
			vTips.append((self.dbc.hget(x,"tip"),self.dbc.hget(x,"num")))
		return vTips


    def getAllSTips(self):
		keys = self.dbc.keys('STips*')
		sTips = [];
		for x in keys:
			sTips.append((self.dbc.hget(x,"tip"),self.dbc.hget(x,"num")))
		return sTips



    def getAllJTips(self):
		keys = self.dbc.keys('JTips*')
		jTips = [];
		for x in keys:
			jTips.append((self.dbc.hget(x,"tip"),self.dbc.hget(x,"num")))
		return jTips

    def editVTip(self,newTip,numKey):
        name = "VTips"+numKey
        self.dbc.hset(name, "tip", newTip)

    def editJTip(self,newTip,numKey):
        name = "JTips"+numKey
        self.dbc.hset(name, "tip", newTip)

    def editSTip(self,newTip,numKey):
        name = "STips"+numKey
        self.dbc.hset(name, "tip", newTip)

    def delJTip(self,key):
        self.dbc.delete("JTips"+key)

    def delVTip(self,key):
        self.dbc.delete("VTips"+key)

    def delSTip(self,key):
        self.dbc.delete("STips"+key)

    def deleteAllTips(self):
		keys = self.dbc.keys('VTips*')+self.dbc.keys('JTips*')+self.dbc.keys('STips*')
		for x in keys:
			self.dbc.delete(x);


    def editSchedule(self, text):
        self.dbc.set("schedule", text)

    def editBusSchedule(self, text):
        self.dbc.set("busSchedule", text)

    def editSchEnd(self, text):
        self.dbc.set("schEnd", text)

    def getSchEnd(self):
        return self.dbc.get("schEnd")

    def getSchedule(self):
        return self.dbc.get("schedule")


    def getBusSchedule(self):
        return self.dbc.get("busSchedule")
