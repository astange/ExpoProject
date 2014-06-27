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
        self.dbc.setnx(self.dbc.get('currentSemester') + 'seelioKey','52f3dfc042ae849b5e000097')
        self.dbc.setnx('numVTips', '0')
        self.dbc.setnx('numSTips', '0')
        self.dbc.setnx('numJTips', '0')
        self.dbc.setnx('numSubmissions', '0')
        self.dbc.setnx('schedule', ' <tr> <td>4:30pm</td> <td>Expo opens to the public</td> </tr> <tr> <td>5:00pm</td> <td>Optional tour of GT Invention Studio spaces at <a href="http://goo.gl/maps/K5vB3" target="_blank"> MRDC Building</a>, 2nd Floor Lobby near room 2211<br> <a href="http://www.capstone.gatech.edu/?page_id=2236#InventionStudioParking" target="_blank"> Invention Studio Tour Parking Information</a><br> A courtesy shuttle will take you to the Expo from MRDC and back</td> </tr> <tr> <td>5:30pm</td> <td>Expo judges preparation meeting at <a href="http://goo.gl/maps/xko7n" target="_blank">McCamish Pavilion</a><br> <a href="http://www.capstone.gatech.edu/?page_id=2236#McCamishPavilionParking" target="_blank">Expo Parking Information</a></td> </tr> <tr> <td>6:00pm</td> <td>Judging begins</td> </tr> <tr> <td>8:00pm</td> <td>Presentation of awards & prizes</td> </tr> <tr> <td>8:30pm</td> <td>Expo concludes</td> </tr> ')
        self.dbc.setnx('busSchedule', ' <tr> <td>5:30pm</td> <td>Bus will begin running from MRDC building to take visitors from Invention Studio tour to McCamish Pavilion</td> </tr> <tr> <td>6:00pm</td> <td>Bus is open to the public - route will run every 15 minutes from MRDC to McCamish Pavilion with no other stops along the way</td> </tr> <tr> <td>9:00pm</td> <td>Bus closes to the public</td> </tr>')
        self.dbc.setnx('schEnd','<a href="http://www.capstone.gatech.edu/wp-content/uploads/2014/03/Capstone-Design-Expo-Spring-2014.pdf" target="_blank">Click here</a> for a downloadable copy of the Expo, GT Invention Studio tour, and parking information.')

    def saveToDB(self, formDict, semester=None):
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
        for key, value in formDict.iteritems():
            self.dbc.hset(submission,key,value)
        return submission



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

    def getAllDataForSubmission(self, submissionNum):
        return self.dbc.hgetall(submissionNum)

    def getOneSubmission(self, submissionNum):
        submission = self.dbc.hgetall(submissionNum)
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
        
    def removeSemester(self, semester):
        if(semester != self.getCurrentSemester()):
            keys = self.dbc.keys(semester + '*')
            for x in keys:
                self.dbc.delete(x);
            self.dbc.srem('semesterSet', semester)
            return True;
        return False;

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
        
    def getCurrentSeelioKey(self, semester = None):
        if(semester == None):
            semester = self.getCurrentSemester()
        return self.dbc.get(semester + 'seelioKey')
        
    def setCurrentSeelioKey(self, newKey, semester = None):
        if(semester == None):
            semester = self.getCurrentSemester()
        self.dbc.set('seelioKey', newKey)
