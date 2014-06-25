from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, ValidationError, NumberRange, Email, Length


class teamForm(Form):
    majorChoices = [('interdisciplinary', 'Interdisciplinary'), ('ae', 'AE'), ('bme', 'BME'), ('chbe', 'CHBE'), ('ece', 'ECE'), ('pubp', 'PUBP'), ('id', 'ID'), ('isye', 'ISYE'), ('me', 'ME'), ('mse', 'MSE')]
    sectionChoices = [('mixed', 'Mixed (if you chose interdisciplinary)'), ('unknown', 'Don\'t know')]
    sectionChoices.extend([('ae4351-a', 'AE 4351-A'), ('ae4351-b', 'AE 4351-B'), ('ae4351-ip', 'AE 4351-IP')])
    sectionChoices.extend([('ae4357-a', 'AE 4357-A'), ('ae4357-b', 'AE 4357-B'),('ae4357-ip', 'AE 4357-IP'), ('ae4357-ip2', 'AE 4357-IP2')])
    sectionChoices.extend([('ae4359-a', 'AE 4359-A')])
    sectionChoices.extend([('bme4602-a', 'BME 4602-A'), ('bme4602-b', 'BME 4602-B'), ('bme4602-c', 'BME 4602-C'),('bme4602-d', 'BME 4602-D'), ('bme4602-e', 'BME 4602-E'), ('bme4602-ip', 'BME 4602-IP')])
    sectionChoices.extend([('chbe4505-a', 'CHBE 4505-A'), ('chbe4525-a', 'CHBE 4525-A')])
    sectionChoices.extend([('ece4012-ip', 'ECE 4012-IP'), ('ece4012-l1a', 'ECE 4012-L1A'), ('ece4012-l1b', 'ECE 4012-L1B'), ('ece4012-l1c', 'ECE 4012-L1C'), ('ece4012-l2a', 'ECE 4012-L2A'), ('ece4012-l2b', 'ECE 4012-L2B'),
                          ('ece4012-l3a', 'ECE 4012-L3A'), ('ece4012-l3b', 'ECE 4012-L3B'), ('ece4012-l4a', 'ECE 4012-L4A'), ('ece4012-l4b', 'ECE 4012-L4B'), ('ece4012-l4c', 'ECE 4012-L4C'), ('ece4012-vp1', 'ECE 4012-VP1'), ('ece4012-vpc', 'ECE 4012-VPC')])
    sectionChoices.extend([('gt4823-a', 'GT 4823-A'), ('gt4823-b', 'GT 4823-B')])
    sectionChoices.extend([('id4012-a', 'ID 4012-A'), ('id4012-me', 'ID 4012-ME'), ('id4012-mid', 'ID 4012-MID')])
    sectionChoices.extend([('isye4106-ad', 'ISYE 4106-AD'), ('isye4106-al', 'ISYE 4106-AL'), ('isye4106-cz', 'ISYE 4106-CZ'), ('isye4106-cs2', 'ISYE 4106-CS2'), ('isye4106-db1', 'ISYE 4106-DB1'), ('isye4106-db2', 'ISYE 4106-DB2'), ('isye4106-ip', 'ISYE 4106-IP'),
                          ('isye4106-js', 'ISYE 4106-JS'), ('isye4106-js1', 'ISYE 4106-JS1'), ('isye4106-lh', 'ISYE 4106-LH'), ('isye4106-oe', 'ISYE 4106-OE'), ('isye4106-pk', 'ISYE 4106-PK'), ('isye4106-rm', 'ISYE 4106-RM'), ('isye4106-sp1', 'ISYE 4106-SP1')])
    sectionChoices.extend([('me4182-a', 'ME 4182-A'), ('me4182-b', 'ME 4182-B'), ('me4182-c', 'ME 4182-C'), ('me4182-d', 'ME 4182-D'), ('me4182-e', 'ME 4182-E'),
                          ('me4182-f', 'ME 4182-F'), ('me4182-g', 'ME 4182-G'), ('me4182-h', 'ME 4182-H'), ('me4182-j', 'ME 4182-J'), ('me4182-id', 'ME 4182-ID')])
    sectionChoices.extend([('mse4402-a', 'MSE 4402-A')])
    sectionChoices.extend([('pubp4020-ki', 'PUBP 4020-KI')])

    setupChoices = [('tableTop', 'Table top setup (tables are 6\' x 3\')'), ('laptop', 'Laptop only (not provided)'), ('floor', 'Floor setup (area is 8\'x8\')'), (
        'large', 'Large demonstration area (these will be outside)'), ('vehicle', 'A vehicle is involved (these projects will be outside)')]

    tfs = [TextField("A","a"), TextField("B","b")]


    teamName = TextField("Team Name", [InputRequired("Please enter a team name.")])
    teamMemberCount = SelectField("Number of Team Members", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
    teamProjectMajor = SelectField("Project Major", choices=majorChoices)
    teamSection = SelectField("Section (you should see this information on T-square)", choices=sectionChoices)
    teamSponsor = TextField("Sponsor (type NA if you do not have a sponsor)", [InputRequired("Please enter a sponsor, or type NA if your team does not have a sponsor.")])
    teamNeedsPower = SelectField("Does your project require power? Please note that power cannot be added later.", choices=[('no', 'No'), ('yes', 'Yes')])
    teamHasDisplay = SelectField("Will your team have a poster or electronic display for your project? Please note that these will not be provided for you.", choices=[('no', 'No'), ('yes', 'Yes')])
    teamHasDanger = SelectField("Does your project involve heat, water, smoke, or fire of any kind? If it does, it will be set up outside the facility for safety.", choices=[('no', 'No'), ('yes', 'Yes')])
    teamSetup = SelectField("What kind of setup does your project require?", choices=setupChoices)
    teamProjectDescription = TextAreaField("Please describe your team's project in two to three sentences.", [InputRequired("Please enter a description of your team's project.")])
    teamEmail = TextField("Please enter one email address where we can get in contact with your team.", [InputRequired("Please enter a team email contact address."), Email("Please ensure that you have entered a valid email address.")])
    teamProjectName = TextField("Project Name (this may have been provided by your sponsor)", [InputRequired("Please enter a project name.")])
    teamSetupTime = SelectField("Please select the time which works best for your team to set up your project.", choices=[('1to2', '1pm to 2pm'), ('2to3', '2pm to 3pm'), ('3to4', '3pm to 4pm')])

    # Name, Major, and Shirt fields for 10 team members are created and are
    # only displayed according to the selection for number of team members
    TMNameStr = "Name of Team Member #"
    TMNameError = "Please enter the name of Team Member #"
    TMName1 = TextField(TMNameStr + "1", [InputRequired(TMNameError + "1")])
    TMName2 = TextField(TMNameStr + "2", [InputRequired(TMNameError + "2")])
    TMName3 = TextField(TMNameStr + "3", [InputRequired(TMNameError + "3")])
    TMName4 = TextField(TMNameStr + "4", [InputRequired(TMNameError + "4")])
    TMName5 = TextField(TMNameStr + "5", [InputRequired(TMNameError + "5")])
    TMName6 = TextField(TMNameStr + "6", [InputRequired(TMNameError + "6")])
    TMName7 = TextField(TMNameStr + "7", [InputRequired(TMNameError + "7")])
    TMName8 = TextField(TMNameStr + "8", [InputRequired(TMNameError + "8")])
    TMName9 = TextField(TMNameStr + "9", [InputRequired(TMNameError + "9")])
    TMName10 = TextField(TMNameStr + "10", [InputRequired(TMNameError + "10")])

    TMMajorStr = "Major of Team Member #"
    TMMajorError = "Please enter the major of Team Member #"
    TMMajorChoices = [('', ''), ('ae', 'Aerospace Engineering'), ('al', 'Applied Languages'), ('am', 'Applied Mathematics'), ('ap', 'Applied Physics'), ('arch', 'Architecture'), ('biochem', 'Biochemistry'), ('bme', 'Biomedical Engineering'), ('ba', 'Business Administration'), ('chbe', 'Chemical and Biomolecular Engineering'), ('chem', 'Chemistry'), ('civil', 'Civil Engineering'), ('ce', 'Computer Engineering'), ('cm', 'Computational Media'), ('cs', 'Computer Science'), ('dm', 'Discrete Mathematics'), ('eas', 'Earth and Atmospheric Sciences'), (
        'econ', 'Economics'), ('ee', 'Electrical Engineering'), ('environmental', 'Environmental Engineering'), ('global', 'Global Economics'), ('hts', 'History, Technology, and Society'), ('id', 'Industrial Design'), ('isye', 'Industrial Engineering'), ('inta', 'International Affairs'), ('me', 'Mechanical Engineering'), ('mse', 'Materials Science and Engineering'), ('ne', 'Nuclear Engineering'), ('physics', 'Physics'), ('psychology', 'Psychology'), ('pp', 'Public Policy'), ('stac', 'Science, Technology, and Culture')]
    TMMajor1 = SelectField(
        TMMajorStr + "1", [Length(min=1, message=TMMajorError + "1")], choices=TMMajorChoices)
    TMMajor2 = SelectField(
        TMMajorStr + "2", [Length(min=1, message=TMMajorError + "2")], choices=TMMajorChoices)
    TMMajor3 = SelectField(
        TMMajorStr + "3", [Length(min=1, message=TMMajorError + "3")], choices=TMMajorChoices)
    TMMajor4 = SelectField(
        TMMajorStr + "4", [Length(min=1, message=TMMajorError + "4")], choices=TMMajorChoices)
    TMMajor5 = SelectField(
        TMMajorStr + "5", [Length(min=1, message=TMMajorError + "5")], choices=TMMajorChoices)
    TMMajor6 = SelectField(
        TMMajorStr + "6", [Length(min=1, message=TMMajorError + "6")], choices=TMMajorChoices)
    TMMajor7 = SelectField(
        TMMajorStr + "7", [Length(min=1, message=TMMajorError + "7")], choices=TMMajorChoices)
    TMMajor8 = SelectField(
        TMMajorStr + "8", [Length(min=1, message=TMMajorError + "8")], choices=TMMajorChoices)
    TMMajor9 = SelectField(
        TMMajorStr + "9", [Length(min=1, message=TMMajorError + "9")], choices=TMMajorChoices)
    TMMajor10 = SelectField(
        TMMajorStr + "10", [Length(min=1, message=TMMajorError + "10")], choices=TMMajorChoices)

    TMShirtStr = "Shirt Size of Team Member #"
    TMShirtError = "Please enter the shirt size of Team Member #"
    TMShirtChoices = [('', ''), ('S', 'Small'), ('M', 'Medium'), (
        'L', 'Large'), ('XL', 'XLarge'), ('XXL', 'XXLarge'), ('XXXL', 'XXXLarge')]
    TMShirt1 = SelectField(
        TMShirtStr + "1", [Length(min=1, message=TMShirtError + "1")], choices=TMShirtChoices)
    TMShirt2 = SelectField(
        TMShirtStr + "2", [Length(min=1, message=TMShirtError + "2")], choices=TMShirtChoices)
    TMShirt3 = SelectField(
        TMShirtStr + "3", [Length(min=1, message=TMShirtError + "3")], choices=TMShirtChoices)
    TMShirt4 = SelectField(
        TMShirtStr + "4", [Length(min=1, message=TMShirtError + "4")], choices=TMShirtChoices)
    TMShirt5 = SelectField(
        TMShirtStr + "5", [Length(min=1, message=TMShirtError + "5")], choices=TMShirtChoices)
    TMShirt6 = SelectField(
        TMShirtStr + "6", [Length(min=1, message=TMShirtError + "6")], choices=TMShirtChoices)
    TMShirt7 = SelectField(
        TMShirtStr + "7", [Length(min=1, message=TMShirtError + "7")], choices=TMShirtChoices)
    TMShirt8 = SelectField(
        TMShirtStr + "8", [Length(min=1, message=TMShirtError + "8")], choices=TMShirtChoices)
    TMShirt9 = SelectField(
        TMShirtStr + "9", [Length(min=1, message=TMShirtError + "9")], choices=TMShirtChoices)
    TMShirt10 = SelectField(
        TMShirtStr + "10", [Length(min=1, message=TMShirtError + "10")], choices=TMShirtChoices)

    submit = SubmitField("Submit")



    def convertToDictionary(self):
        formDict = {}
        formDict['teamName'] = self.teamName.data.encode('utf-8')
        formDict['projectName'] = self.teamProjectName.data.encode('utf-8')
        formDict['memberCount'] = self.teamMemberCount.data.encode('utf-8')
        formDict['projectMajor'] = self.teamProjectMajor.data.encode('utf-8')
        formDict['section'] = self.teamSection.data.encode('utf-8')
        formDict['sponsor'] = self.teamSponsor.data.encode('utf-8')
        formDict['needsPower'] = self.teamNeedsPower.data.encode('utf-8')
        formDict['hasDisplay'] = self.teamHasDisplay.data.encode('utf-8')
        formDict['hasDanger'] = self.teamHasDanger.data.encode('utf-8')
        formDict['setup'] = self.teamSetup.data.encode('utf-8')
        formDict['projectDescription'] = self.teamProjectDescription.data.encode('utf-8')
        formDict['email'] = self.teamEmail.data.encode('utf-8')
        formDict['setupTime'] = self.teamSetupTime.data.encode('utf-8')
        formDict.update(self.compileTeamMemberData())
        return formDict



    # Takes the form data and figures out the list of names, majors, and shirt sizes
    # based on the number of team members

    def compileTeamMemberData(self):

        numMembers = int(self.teamMemberCount.data)
        info = {}
        shirts = {"S": 0, "M": 0, "L": 0, "XL": 0, "XXL": 0,
                "XXXL": 0}

        if numMembers > 0:
            shirts[self.TMShirt1.data] += 1
            info['name1'] = self.TMName1.data.encode('utf-8')
            info['name1Major'] = self.TMMajor1.data.encode('utf-8')
        if numMembers > 1:
            shirts[self.TMShirt2.data] += 1
            info['name2'] = self.TMName2.data.encode('utf-8')
            info['name2Major'] = self.TMMajor2.data.encode('utf-8')
        if numMembers > 2:
            shirts[self.TMShirt3.data] += 1
            info['name3'] = self.TMName3.data.encode('utf-8')
            info['name3Major'] = self.TMMajor3.data.encode('utf-8')
        if numMembers > 3:
            shirts[self.TMShirt4.data] += 1
            info['name4'] = self.TMName4.data.encode('utf-8')
            info['name4Major'] = self.TMMajor4.data.encode('utf-8')
        if numMembers > 4:
            shirts[self.TMShirt5.data] += 1
            info['name5'] = self.TMName5.data.encode('utf-8')
            info['name5Major'] = self.TMMajor5.data.encode('utf-8')
        if numMembers > 5:
            shirts[self.TMShirt6.data] += 1
            info['name6'] = self.TMName6.data.encode('utf-8')
            info['name6Major'] = self.TMMajor6.data.encode('utf-8')
        if numMembers > 6:
            shirts[self.TMShirt7.data] += 1
            info['name7'] = self.TMName7.data.encode('utf-8')
            info['name7Major'] = self.TMMajor7.data.encode('utf-8')
        if numMembers > 7:
            shirts[self.TMShirt8.data] += 1
            info['name8'] = self.TMName8.data.encode('utf-8')
            info['name8Major'] = self.TMMajor8.data.encode('utf-8')
        if numMembers > 8:
            shirts[self.TMShirt9.data] += 1
            info['name9'] = self.TMName9.data.encode('utf-8')
            info['name9Major'] = self.TMMajor9.data.encode('utf-8')
        if numMembers > 9:
            shirts[self.TMShirt10.data] += 1
            info['name10'] = self.TMName10.data.encode('utf-8')
            info['name10Major'] = self.TMMajor10.data.encode('utf-8')


        info["S"] = str(shirts["S"])
        info["M"] = str(shirts["M"])
        info["L"] = str(shirts["L"])
        info["XL"] = str(shirts["XL"])
        info["XXL"] = str(shirts["XXL"])
        info["XXXL"] = str(shirts["XXXL"])

        return info

