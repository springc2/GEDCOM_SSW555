"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
7/22/2018
Description: 
Reads a GEDCOM file, prints the Families and Individuals data in a easy to read format, and prints errors and anomalies found in the GEDCOM file
"""

#imports
import collections
from prettytable import PrettyTable
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import datetime

#global variables
INPUT_FILE = 'GEDCOM_Input.ged' #input file
OUTPUT_FILE = 'GEDCOM_Output.txt' #output file
try:
    F = open(OUTPUT_FILE,'w')
except IOError:
    print ('Error! Cannot open', OUTPUT_FILE)

FAMILIES = {} #empty dictionary for familie. The key is a families ID and the value is the a dict of  attribute pairs for that family
INDIVIDUALS = {} #empty dictionary for individuals. The key is an individuals ID and the value is the a dict of  attribute pairs for that individual

#main function
def main():
    
    try:
        with open(INPUT_FILE) as fp:
            invalidLines = []
            numLine = 0
            curEntityID = ''
            curEntityType = ''
            datePredecessor = ''
            for line in fp:
                numLine += 1
                #parse the GEDCOM line by whitespaces
                parsedLine = line.strip().split()
                #check to see if the line inputted is a valid one
                if (isSpecialCase(parsedLine)):
                    #new family or new individual
                    curEntityType = parsedLine[2] #this is either FAM or INDI
                    curEntityID = createEntity(parsedLine, curEntityType)
                elif (isValid(parsedLine)):
                    #either adding info to an existing family/individual or it is a comment
                    datePredecessor = updateEntity(parsedLine, curEntityID, curEntityType, datePredecessor, numLine)
                else:
                    #add error reporting to help user
                    invalidLines.append(numLine)
            
            if(len(invalidLines) > 0):
                #print 'Invalid GEDCOM format on lines:', invalidLines
                F.write('The following lines had an invalid format: ' + str(invalidLines) + '\n')
            #next we want to check for errors and anomalies
            additionalChecking()
            #print the individuals in order by their IDs
            printIndividuals(collections.OrderedDict(sorted(INDIVIDUALS.items())))
            #print the families in order by their IDs
            printFamilies(collections.OrderedDict(sorted(FAMILIES.items())))
            #next we want to print the lists for other user stories
            additionalLists()
    except IOError:
        #print 'ERROR: Cannot Open File:', INPUT_FILE
        F.write('ERROR: Cannot Open File: ' + INPUT_FILE + '\n')
    F.close()


#this fuction will create either a new family or a new individual
#returns the current entities ID
#(if it is not a uniquie ID, will return blanks so the info of this entity is not added)
def createEntity(pLine, entType):
    entID = pLine[1] #this is the ID of the entity
    if (entType == 'FAM'):
        #check if the ID is a unique ID
        if (checkUniqueIDs(entID,FAMILIES)):
            #the new entity is a family so we will create a new dictionary for it within the fam dictionary
            FAMILIES.update({entID: {'ID': entID}})
        else:
            #the ID is not unique so we will not add it and will not add any of it's info
            entID = ''
    elif (entType == 'INDI'):
        #check if the ID is a unique ID
        if (checkUniqueIDs(entID,INDIVIDUALS)):
            #the new entity is an individual so we will create a new dictionary for it within the indi dictionary
            INDIVIDUALS.update({entID: {'ID': entID}})
        else:
            #the ID is not unique so we will not add it and will not add any of it's info
            entID = ''
    else:
        entID = ''
        F.write('Unexpected error while creating a new entity! Entity type: ' + entType + 'is unknown.\n')
    return entID

#this fuction will update an entities information based on the given line info
def updateEntity(pLine, entID, entType, curDatePred, lineNumber):
    #if the level is 0, we will skip over everything becuase this function is only for level 1 or 2 items
    #also skipping over this function if there is no value for the entity ID
    validDatePredecessor = ['BIRT', 'DEAT', 'DIV', 'MARR'] #these are the only types that can come before the date tag
    nextDatePred = ''
    if (pLine[0] != '0' and entID != ''):
        if (entType == 'FAM'):
            #working within the family dict
            if (pLine[1] in validDatePredecessor):
                #need to store this tag because it will be followed by a date
                nextDatePred = pLine[1]
            elif (pLine[1] == 'DATE' and curDatePred in validDatePredecessor):
                #only add the date if it is a legitimate one
                if (checkIllegitimateDate(pLine[2:], lineNumber)):
                    #this date gets written for the previous tag
                    FAMILIES[entID].update({curDatePred: ' '.join(pLine[2:])})
                else:
                    #adding a basic date so the program doesn't crash
                    FAMILIES[entID].update({curDatePred: ' '.join(['01','JAN','2000'])})
            else:
                if (pLine[1] == 'CHIL' and 'CHIL' in FAMILIES[entID]):
                    #a family can have multiple children
                    FAMILIES[entID][pLine[1]].append(' '.join(pLine[2:]))
                else:
                    if (pLine[1] == 'CHIL'):
                        #CHIL must be stored differently since it can have multiple entries
                        FAMILIES[entID].update({pLine[1]: [' '.join(pLine[2:])]})
                    else:
                        #otherwise just write normally
                        FAMILIES[entID].update({pLine[1]: ' '.join(pLine[2:])})
        elif (entType == 'INDI'):
            #working within the indi dict
            #working within the family dict
            if (pLine[1] in validDatePredecessor):
                #need to store this tag because it will be followed by a date
                nextDatePred = pLine[1]
            elif (pLine[1] == 'DATE' and curDatePred in validDatePredecessor):
                #only add the date if it is a legitimate one
                if (checkIllegitimateDate(pLine[2:], lineNumber)):
                    #this date gets written for the previous tag
                    INDIVIDUALS[entID].update({curDatePred: ' '.join(pLine[2:])})
                else:
                    #adding a basic date so the program doesn't crash
                    INDIVIDUALS[entID].update({curDatePred: ' '.join(['01','JAN','2000'])})
            else:
                
                if ((pLine[1] == 'FAMS' or pLine[1] == 'FAMC') and (pLine[1] in INDIVIDUALS[entID])):
                    #an individual can be in multiple families (as a child or spouse)
                    INDIVIDUALS[entID][pLine[1]].append(' '.join(pLine[2:]))
                else:
                    if (pLine[1] == 'FAMS' or pLine[1] == 'FAMC'):
                        #FAMS and FAMC must be stored differently since they can have multiple entiries
                        INDIVIDUALS[entID].update({pLine[1]: [' '.join(pLine[2:])]})
                    else:
                        #otherwise just write normally
                        INDIVIDUALS[entID].update({pLine[1]: ' '.join(pLine[2:])})
        else:
            F.write('Unexpected error while updating an entity! Entity type ' + entType + ' is unknown.\n')
    return nextDatePred

#prints all the individuals and their info in the GEDCOM file by alphabetical order of their IDs
def printIndividuals(indi):
    rows = [] #initilize the row list
    rows.append(['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']) #add in header row
    for k, v in indi.iteritems():
        #check if they are still living
        alive = True
        if (v.get('DEAT') is not None):
            alive = False
        #get age
        if(alive):
            age = getAgeAlive([v['BIRT']])
        else:
            age = getAgeDead([v['BIRT']], [v['DEAT']])
        rows.append([v['ID'], v['NAME'], v['SEX'], v['BIRT'], age, alive, v.get('DEAT', 'NA'), v.get('FAMC', 'NA'), v.get('FAMS', 'NA')])
    prettyPrint('Individuals', rows)

#prints all the families and their info in the GEDCOM file by alphabetical order of their IDs
def printFamilies(fam):
    rows = [] #initilize the row list
    rows.append(['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']) #add in header row
    for k, v in fam.iteritems():
        rows.append([v['ID'], v['MARR'], v.get('DIV', 'NA'), v['HUSB'], INDIVIDUALS[v['HUSB']]['NAME'], v['WIFE'], INDIVIDUALS[v['WIFE']]['NAME'], v.get('CHIL', 'NA')])
    prettyPrint('Families', rows)

#this function is only for individuals who are alive
#returns the age of an individual given their birthdate based on today's date
#dates are in the format <day month year>
def getAgeAlive(birthDate):
    today = date.today()
    bDate = birthDate[0].split() #parse the birthday
    birthDay = int(bDate[0])
    months = {
            'JAN': 1,
            'FEB': 2,
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12,
            }
    if (bDate[1] in months):
        birthMonth = months[bDate[1]]
    else:
        F.write('Unexpected error with birthdate! ' + bDate[1] + ' is not in the correct format for a month.\n')
    birthYear = int(bDate[2])
    return today.year - birthYear - ((today.month, today.day) < (birthMonth, birthDay))

#this function is only for individuals who are dead
#returns the age of an individual given their birthdate based on their death date
#dates are in the format <day month year>
def getAgeDead(birthDate, deathDate):
    dDate = deathDate[0].split() #parse the deathday
    deathDay = int(dDate[0])
    
    bDate = birthDate[0].split() #parse the birthday
    birthDay = int(bDate[0])
    months = {
            'JAN': 1,
            'FEB': 2,
            'MAR': 3,
            'APR': 4,
            'MAY': 5,
            'JUN': 6,
            'JUL': 7,
            'AUG': 8,
            'SEP': 9,
            'OCT': 10,
            'NOV': 11,
            'DEC': 12,
            }
    if (dDate[1] in months):
        deathMonth = months[dDate[1]]
    else:
        F.write('Unexpected error with deathdate! ' + dDate[1] + ' is not in the correct format for a month.\n')
    if (bDate[1] in months):
        birthMonth = months[bDate[1]]
    else:
        F.write('Unexpected error with birthdate! ' + bDate[1] + ' is not in the correct format for a month.\n')
    deathYear = int(dDate[2])
    birthYear = int(bDate[2])
    return deathYear - birthYear - ((deathMonth, deathDay) < (birthMonth, birthDay))

# US12 -> Check if the dad is too old and returns false or true if he is or is not
def checkDadTooOld(dadBirth, childBirth):
    months = {'JAN': 1,
              'FEB': 2,
              'MAR': 3,
              'APR': 4,
              'MAY': 5,
              'JUN': 6,
              'JUL': 7,
              'AUG': 8,
              'SEP': 9,
              'OCT': 10,
              'NOV': 11,
              'DEC': 12
              }
    dadDiffInDays = (date(int(childBirth[2]),
                          months[childBirth[1]],
                          int(childBirth[0])) - date(int(dadBirth[2]),
                                                     months[dadBirth[1]],
                                                     int(dadBirth[0]))).days
    if(dadDiffInDays / 365.00 >= 80.00):
        return(True)
    else:
        return(False)

# US12 -> Checks if the mom is too old returns false or true if she is or is not
def checkMomTooOld(momBirth, childBirth):
    months = {'JAN': 1,
              'FEB': 2,
              'MAR': 3,
              'APR': 4,
              'MAY': 5,
              'JUN': 6,
              'JUL': 7,
              'AUG': 8,
              'SEP': 9,
              'OCT': 10,
              'NOV': 11,
              'DEC': 12
              }
    momDiffInDays = (date(int(childBirth[2]),
                          months[childBirth[1]],
                          int(childBirth[0])) - date(int(momBirth[2]),
                                                     months[momBirth[1]],
                                                     int(momBirth[0]))).days
    if(momDiffInDays / 365.00 >= 60.00):
        return(True)
    else:
        return(False)

#returns a date to compare to the current date
#input dates are in the format <day month year>
def getFormattedDateForCompare(date):
    _date = date.split() #parse the date
    
    workingDay = int(_date[0])    
    workingYear = int(_date[2])
    
    if (_date[1] == 'JAN'):
        workingMonth = 1
    elif (_date[1] == 'FEB'):
        workingMonth = 2
    elif (_date[1] == 'MAR'):
        workingMonth = 3
    elif (_date[1] == 'APR'):
        workingMonth = 4
    elif (_date[1] == 'MAY'):
        workingMonth = 5
    elif (_date[1] == 'JUN'):
        workingMonth = 6
    elif (_date[1] == 'JUL'):
        workingMonth = 7
    elif (_date[1] == 'AUG'):
        workingMonth = 8
    elif (_date[1] == 'SEP'):
        workingMonth = 9
    elif (_date[1] == 'OCT'):
        workingMonth = 10
    elif (_date[1] == 'NOV'):
        workingMonth = 11
    else:
        workingMonth = 12
    
    workingDate = datetime.date(workingYear, workingMonth, workingDay)
    return workingDate

#returns true if the line is in the correct format
#returns false otherwise
def isValid(pLine):    
    #note that INDI and FAM are not valid here, they are handled in the special case method
    validTags = {
            '0': ('HEAD', 'TRLR', 'NOTE'),
            '1': ('NAME', 'SEX', 'BIRT' , 'DEAT', 'FAMC', 'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV'),
            '2': ('DATE')
            }
    level = pLine[0]
    tag = pLine[1]
    isValid = False
    
    if (level in validTags and tag in validTags[level]):
        isValid = True
    
    return isValid

#returns true if the input is a special case in the correct format
#returns false otherwise
#special cases are:
#    0 <id> INDI
#    0 <id> FAM
def isSpecialCase(pLine):
    return (len(pLine) == 3) and (pLine[0] == '0') and (pLine[2] in ('INDI', 'FAM'))

# this fuction is to check if there are any errors or anomalies in the GEDCOM file
# note that some error checking happens while the information is being stored, 
# so this function will not recheck for errors that have already been covered earlier in the program
def additionalChecking():
    checkDatesBeforeCurrentDate(INDIVIDUALS, FAMILIES) #User Story 01
    checkBirthBeforeMarriage(INDIVIDUALS, FAMILIES) #User Story 02
    checkBirthBeforeDeath(INDIVIDUALS) #User Story 03
    checkMarriageBeforeDivorce(FAMILIES) #User Story 04
    checkMarriageBeforeDeath(INDIVIDUALS, FAMILIES) #User Story 05
    checkDivorceBeforeDeath(INDIVIDUALS, FAMILIES) #User Story 06
    checkLessThan150YearsOld(INDIVIDUALS) #User Story 07
    checkBirthBeforeMarriageOfParents(INDIVIDUALS, FAMILIES) #User Story 08
    checkBirthBeforeDeathOfParents(INDIVIDUALS, FAMILIES) #User Story 09
    checkMarriageAfter14(INDIVIDUALS, FAMILIES) #User Story 10
    checkNoBigamy(INDIVIDUALS, FAMILIES) #User Story 11
    checkParentsNotTooOld(INDIVIDUALS, FAMILIES) #User Story 12
    checkFewerThan15Siblings(FAMILIES) #User Story 15
    checkSiblingsShouldNotMarry(FAMILIES) #User Story 18
    checkCorrectGenderForRole(FAMILIES, INDIVIDUALS) #User Story 21
    checkUniqueNameAndBirthDate(INDIVIDUALS) #User Story 23
    checkUniqueFamiliesBySpouses(FAMILIES) #User Story 24
    checkUniqueFirstNamesInFamilies(INDIVIDUALS, FAMILIES) #User Story 25

# this fuction is to check if there are any errors or anomalies in the GEDCOM file
# note that some error checking happens while the information is being stored, 
# so this function will not recheck for errors that have already been covered earlier in the program
def additionalLists():
    prettyPrint('Individual\'s Age', listIndividualAges(collections.OrderedDict(sorted(INDIVIDUALS.items())))) #User Story 27
    prettyPrint('Siblings Ordered By Age', listSiblingsByAge()) #User Story 28
    prettyPrint('Deceased Individuals', listDeceased(collections.OrderedDict(sorted(INDIVIDUALS.items())))) #User Story 29
    prettyPrint('Living Married Individuals', listLivingMarried(collections.OrderedDict(sorted(INDIVIDUALS.items())),
                                                                collections.OrderedDict(sorted(FAMILIES.items())))) #User Story 30
    prettyPrint('Living Singles', listLivingSingles()) #User Story 31
    prettyPrint('Orphans', listOrphans()) #User Story 33
    prettyPrint('Large Age Differences', listLargeAgeDifferences()) #User Story 34
    prettyPrint('Recent Births', listRecentBirths(collections.OrderedDict(sorted(INDIVIDUALS.items())))) #User Story 35
    prettyPrint('Recent Deaths', listRecentDeaths(collections.OrderedDict(sorted(INDIVIDUALS.items())))) #User Story 36
    prettyPrint('Upcoming Birthdays', listUpcomingBirthdays()) #User Story 38
    prettyPrint('Upcoming Anniversaries', listUpcomingAnniversaries()) #User Story 39

# Checks User Story 01:
# Dates (birth, marriage, divorce, death) should not be after the current date
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkDatesBeforeCurrentDate(indi, fam):
    passesCheck = True
    
    currentDate = date.today() #today's date
    #look at the birth and death dates for individuals
    if(indi):
        for k, v in indi.iteritems():
            #looking at the birthdate if there is one
            if (v.get('BIRT', 'NA') != 'NA'):
                workingDate = getFormattedDateForCompare(v['BIRT'])
                if (workingDate > currentDate):
                    passesCheck = False
                    log('Error','US01','Individual ' + v.get('NAME', 'NA') + ' (' + v.get('ID', 'NA') + ') has a birth date after the current date.')

            #looking at the deathdate if there is one
            if (v.get('DEAT', 'NA') != 'NA'):
                workingDate = getFormattedDateForCompare(v['DEAT'])
                if (workingDate > currentDate):
                    passesCheck = False
                    log('Error','US01','Individual ' + v.get('NAME', 'NA') + ' (' + v.get('ID', 'NA') + ') has a death date after the current date.')

    #look at the marr and div dates for families
    if(fam):
        for k, v in fam.iteritems():
            #looking at the marriage date if there is one
            if (v.get('MARR', 'NA') != 'NA'):
                workingDate = getFormattedDateForCompare(v['MARR'])
                if (workingDate > currentDate):
                    passesCheck = False
                    log('Error','US01','Family ' + v.get('ID', 'NA') + ' has a marriage date after the current date.')

            #looking at the divorce if there is one
            if (v.get('DIV', 'NA') != 'NA'):
                workingDate = getFormattedDateForCompare(v['DIV'])
                if (workingDate > currentDate):
                    passesCheck = False
                    log('Error','US01','Family ' + v.get('ID', 'NA') + ' has a divorce date after the current date.')


    return passesCheck

# Checks User Story 02:
# Birth should occur before marriage of an individual
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkBirthBeforeMarriage(indi, fam):
    passesCheck = True

    #loop over all stored individuals
    for k, v in indi.iteritems():
        indi_id = v['ID']
        indi_name = v['NAME']

        for k1, v1 in fam.iteritems():
            husb_id = ''
            wife_id = ''

            if 'HUSB' in v1:
                husb_id = v1['HUSB']

            if 'WIFE' in v1:
                wife_id = v1['WIFE']

            if indi_id == husb_id or indi_id == wife_id:
                mDate = getFormattedDateForCompare(v1['MARR'])
                bDate = getFormattedDateForCompare(v['BIRT'])

                if bDate > mDate:
                    #there was a match, so we must print out the info
                    log('Error','US02','Individual ' + indi_name + ' (' + indi_id + ') has marriage date before birth date.')
                    passesCheck = False

    return passesCheck

# Checks User Story 03:
# Birth should occur before death of an individual
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkBirthBeforeDeath(indi):
    passesCheck = True

    #loop over all stored individuals
    for k, v in indi.iteritems():
        indi_id = v['ID']
        indi_name = v['NAME']
        if 'DEAT' in v:
            dDate = getFormattedDateForCompare(v['DEAT'])
            bDate = getFormattedDateForCompare(v['BIRT'])

            if bDate > dDate:
                #there was a match, so we must print out the info
                log('Error','US03','Individual ' + indi_name + ' (' + indi_id + ') has death date before birth date.')
                passesCheck = False

    return passesCheck

# Checks User Story 04:
# Marriage should occur before divorce of spouses, and divorce can only occur after marriage
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkMarriageBeforeDivorce(fam):
    passesCheck = True
    
    for k, v in fam.iteritems():
        if v.get('DIV') is None:
            continue
        coupleMarriageDate = getFormattedDateForCompare(v['MARR'])
        coupleDivorceDate = getFormattedDateForCompare(v['DIV'])

        if coupleDivorceDate < coupleMarriageDate:
            passesCheck = False
            log('Error','US04','Family (' + k +') has divorce before marriage.')
        
    return passesCheck

# Checks User Story 05:
# Marriage should occur before death of either spouse
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkMarriageBeforeDeath(ind, fam):
    passesCheck = True

    for k, v in fam.iteritems():
        coupleMarriageDate = getFormattedDateForCompare(v['MARR'])
        if(ind):
            if ind[v['HUSB']].get('DEAT') is not None:
                husbandDeathDate = getFormattedDateForCompare(ind[v['HUSB']]['DEAT'])
                if coupleMarriageDate > husbandDeathDate:
                    passesCheck = False
                    log('Error','US05','Family (' + k +') has death before marriage date for husband ('+v['HUSB']+ ').')
            if ind[v['WIFE']].get('DEAT') is not None:
                wifeDeathDate = getFormattedDateForCompare(ind[v['WIFE']]['DEAT'])
                if coupleMarriageDate > wifeDeathDate:
                    passesCheck = False
                    log('Error','US05','Family (' + k +') has death before marriage date for wife ('+v['WIFE']+ ').')
    return passesCheck

# Checks User Story 06:
# Divorce can only occur before death of both spouses
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkDivorceBeforeDeath(indi, fam):
    passesCheck = True
    for k, v in fam.iteritems():
        if v.get('DIV') is None:
            continue
        coupleDivorceDate = getFormattedDateForCompare(v['DIV'])
        if(indi):
            if indi[v['HUSB']].get('DEAT') is not None:
                husbandDeathDate = getFormattedDateForCompare(indi[v['HUSB']]['DEAT'])
                if coupleDivorceDate > husbandDeathDate:
                    passesCheck = False
                    log('Error','US06','Family (' + k +') has divorce after death date for husband ('+v['HUSB']+ ').')
            if indi[v['WIFE']].get('DEAT') is not None:
                wifeDeathDate = getFormattedDateForCompare(indi[v['WIFE']]['DEAT'])
                if coupleDivorceDate > wifeDeathDate:
                    passesCheck = False
                    log('Error','US06','Family (' + k +') has divorce after death date for wife ('+v['WIFE']+ ').')
    return passesCheck

# Checks User Story 07:
# Death should be less than 150 years after birth for dead people, and current date should be less than 150 years after birth for all living people
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkLessThan150YearsOld(indi):
    passesCheck = True

    for k, v in indi.iteritems():
        indi_id = v['ID']
        indi_name = v['NAME']

        #check if they are still living
        alive = True
        if (v.get('DEAT', 'NA') != 'NA'):
            alive = False
        #get age
        if(alive):
            age = getAgeAlive([v['BIRT']])
        else:
            age = getAgeDead([v['BIRT']], [v['DEAT']])

        if (age >= 150):
            #there was a match, so we must print out the info
            log('Error','US07', 'Individual' + indi_name + ' (' + indi_id + ') is not less than 150 years old.')
            passesCheck = False

    return passesCheck

# Checks User Story 08:
# Children should be born after marriage of parents (and not more than 9 months after their divorce)
# This is considered an Anomaly
# Returns True if the check is passed, and False if the check is failed
def checkBirthBeforeMarriageOfParents(indi, fam):
    passesCheck = True

    for k, v in fam.iteritems():
        #check against marr date if there is one
        if (v.get('MARR') is not None and v.get('CHIL') is not None):
            coupleMarriageDate = datetime.datetime.strptime(v['MARR'], '%d %b %Y').date()
            #loop over all children
            for i in range(0, len(v['CHIL'])):
                childAge = getFormattedDateForCompare(indi[v['CHIL'][i]].get('BIRT'))
                if coupleMarriageDate >= childAge:
                    log('Anomaly','US08','Individual ' + indi[v['CHIL'][i]].get('NAME') + ' (' + indi[v['CHIL'][i]].get('ID') + ') was born before marriage in Family (' + k +').')
                    passesCheck = False

        #check against div date if there is one
        if (v.get('DIV') is not None and v.get('CHIL') is not None):
            coupleDivorceDate = getFormattedDateForCompare(v['DIV'])
            #get the +9 months date for compairson
            plus9MonthDivDate = coupleDivorceDate + relativedelta(months=9)
            #loop over all children
            for i in range(0, len(v['CHIL'])):
                childAge = getFormattedDateForCompare(indi[v['CHIL'][i]].get('BIRT'))
                if plus9MonthDivDate < childAge:
                    log('Anomaly','US08','Individual ' + indi[v['CHIL'][i]].get('NAME') + ' (' + indi[v['CHIL'][i]].get('ID') + ') was born more than 9 months after divorce in Family (' + k +').')
                    passesCheck = False

    return passesCheck

# Checks User Story 09:
# Child should be born before death of mother and before 9 months after death of father
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkBirthBeforeDeathOfParents(indi, fam):
    passesCheck = True
    
    for k, v in fam.iteritems():
        #check against mother's death date if there is one
        if (indi[v['WIFE']].get('DEAT') is not None and v.get('CHIL') is not None):
            motherDeathDate = getFormattedDateForCompare(indi[v['WIFE']].get('DEAT'))
            #loop over all children
            for i in range(0, len(v['CHIL'])):
                childAge = getFormattedDateForCompare(indi[v['CHIL'][i]].get('BIRT'))
                if motherDeathDate <= childAge:
                    log('Error','US09','Individual ' + indi[v['CHIL'][i]].get('NAME') + ' (' + indi[v['CHIL'][i]].get('ID') + ') was born after death of mother ' + indi[v['WIFE']].get('NAME') + ' (' + indi[v['WIFE']].get('ID') + ') in Family (' + k +').')
                    passesCheck = False

        #check against father's death date if there is one
        if (indi[v['HUSB']].get('DEAT') is not None and v.get('CHIL') is not None):
            fatherDeathDate = getFormattedDateForCompare(indi[v['HUSB']].get('DEAT'))
            #get the +9 months date for compairson
            plus9MonthDeathDate = fatherDeathDate + relativedelta(months=9)
            #loop over all children
            for i in range(0, len(v['CHIL'])):
                childAge = getFormattedDateForCompare(indi[v['CHIL'][i]].get('BIRT'))
                if plus9MonthDeathDate <= childAge:
                    log('Error','US09','Individual ' + indi[v['CHIL'][i]].get('NAME') + ' (' + indi[v['CHIL'][i]].get('ID') + ') was born more than 9 months after death of father ' + indi[v['HUSB']].get('NAME') + ' (' + indi[v['HUSB']].get('ID') + ') in Family (' + k +').')
                    passesCheck = False
    
    return passesCheck

# Checks User Story 10:
# Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
# This is considered an Anomaly
# Returns True if the check is passed, and False if the check is failed
def checkMarriageAfter14(indi, fam):
    passesCheck = True
   
    for k, v in fam.iteritems():
        marriageDate = getFormattedDateForCompare(v['MARR'])
        if(indi):
            husbandBirthDate = getFormattedDateForCompare(indi[v['HUSB']]['BIRT'])
            wifeBirthDate = getFormattedDateForCompare(indi[v['WIFE']]['BIRT'])
            if ((marriageDate - husbandBirthDate).days / 365) < 14:
                passesCheck = False
                log('Anomaly', 'US10', 'Individual (' + v['HUSB'] + ') was younger than 14 when married')
            if ((marriageDate - wifeBirthDate).days / 365) < 14:
                passesCheck = False
                log('Anomaly', 'US10', 'Individual (' + v['WIFE'] + ') was younger than 14 when married')

    return passesCheck

# Checks User Story 11:
# Marriage should not occur during marriage to another spouse
# This is considered an Anomaly
# Returns True if the check is passed, and False if the check is failed
def checkNoBigamy(indi, fam):
    passesCheck = True
    
    return passesCheck

# Checks User Story 12:
# The mother and father in the family should be checked.
# Mothers age should be less than 60 years older than her children
# The fathers age should be less than 80 years older than his children
def checkParentsNotTooOld(indi, fam):
    passesCheck = True

    if(fam and indi):
        for k,v in fam.iteritems():                                 # Has to be husband and wife if its a family
            dadBirth = (indi[v['HUSB']].get('BIRT')).split()
            momBirth = (indi[v['WIFE']].get('BIRT')).split()
            if('CHIL' in v):                                        # Checks if family even has children
                for childID in v['CHIL']:
                    childBirth = (indi[childID].get('BIRT')).split()

                    if(checkMomTooOld(momBirth, childBirth) and checkDadTooOld(dadBirth, childBirth)):
                        passesCheck = False
                        log('Anomaly','US12','Family (' + k + ') mother is over 60 years older than child ' + childID + ' and father is over 80 years older than child ' + childID + '.')
                        break
                    elif(checkMomTooOld(momBirth, childBirth)):
                        passesCheck = False
                        log('Anomaly','US12','Family (' + k + ') mother is over 60 years older than child ' + childID + '.')
                        break
                    elif(checkDadTooOld(dadBirth, childBirth)):
                        passesCheck = False
                        log('Anomaly','US12','Family (' + k + ') father is over 80 years older than child ' + childID + '.')
                        break
    return passesCheck

# Checks User Story 15:
# In one family there must be fewer than 15 siblings
# This is considered an anomoly
# Returns true if the check is passed, and false if the check is failed
def checkFewerThan15Siblings(fam):
    passesCheck = True
    if(fam):
        for k, v in fam.iteritems():
            if('CHIL' in v and len(v['CHIL']) >= 15):
                log('Anomaly','US15','Family (' + k + ') has more than 15 siblings.')
                passesCheck = False

    return passesCheck

# Checks User Story 18:
# Siblings should not marry one another
# This is considered an anomoly
# Returns true if the check is passed, and false if the check is failed
def checkSiblingsShouldNotMarry(fam):
    passesCheck = True
    if(fam):
        for k, v in fam.iteritems():
            currentHusband = v.get('HUSB')
            currentWife = v.get('WIFE')
            for l, w in fam.iteritems():
                currentChildren = w.get('CHIL')
                if currentChildren and len(currentChildren) > 1 and currentHusband in currentChildren and \
                        currentWife in currentChildren:
                    log('Anomaly', 'US18', 'Family (' + k + ') has husband and wife as siblings.')
                    passesCheck = False
                    break
    return passesCheck

# Checks User Story 21:
# Husband in family should be male and wife in family should be female
# This is considered an anomoly
# Returns true if the check is passed, and false if the check is failed
def checkCorrectGenderForRole(fam, indi):
    passesCheck = True
    for k, v in fam.iteritems():
        currentWife = v.get('WIFE')
        currentHusband = v.get('HUSB')
        if(indi):
            if currentWife is not None and indi[currentWife]['SEX'] != 'F':
                log('Anomoly', 'US21', 'TRIGGER WARNING! ' + currentWife + ' is the wrong gender for wife.')
                passesCheck = False
            if currentHusband is not None and indi[currentHusband]['SEX'] != 'M':
                log('Anomoly', 'US21', 'TRIGGER WARNING! ' + currentHusband + ' is the wrong gender for husband.')
                passesCheck = False

    return passesCheck

# Checks User Story 22:
# All individual IDs should be unique and all family IDs should be unique
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkUniqueIDs(curID, dictionary):
    #NOTE that the name of an individual is not included in this error message
    #because families have no names but can run into the same error
    #and we want to keep the error message consistent for the both of them
    passesCheck = True
    if (curID in dictionary):
        #the ID is already in the dict, thus it is not unique
        log('Error','US22','ID ' + curID + ' is not a uniquie ID. Not including it or it\'s information!')
        passesCheck = False
    #otherwise the ID is unique
    return passesCheck

# Checks User Story 23:
# No more than one individual with the same name and birth date should appear in a GEDCOM file
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkUniqueNameAndBirthDate(indi):
    passesCheck = True
    all_IDs = [] #all the individual's IDs
    all_names = [] #all the individual's names
    all_bDays = [] #all the individual's birth days
    
    #loop over all stored individuals
    for k, v in indi.iteritems():
        indi_id = v['ID']
        indi_name = v['NAME']
        indi_bDay = v['BIRT']
        isNewNameAndBDay = True
        
        for i in range(0, len(all_IDs)):
            #look at the previously stored names and bdays
            if (indi_name == all_names[i] and indi_bDay == all_bDays[i]):
                #there was a match, so we must print out the info
                log('Error','US23','Individual ' + indi_name + ' (' + indi_id + ') and '+ all_names[i] + ' (' + all_IDs[i] + ') have the same name and birth date.')
                passesCheck = False
                isNewNameAndBDay = False
        
        if (isNewNameAndBDay):
            #after logic checking, store the values in the list so the next individual can check against them
            #no need to have duplicate individuals with the same BDay and Name...since we already included both their names in the print above,
            #we are still hitting the requirements of mentioning all individuals involved
            all_IDs.append(indi_id)
            all_names.append(indi_name)
            all_bDays.append(indi_bDay)
    return passesCheck

# Checks User Story 24:
# No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkUniqueFamiliesBySpouses(fam):
    passesCheck = True
    famIDs = []
    marHusWife = []

    if(fam):
        for k,v in fam.iteritems(): # Iterates through the dictionary and appends values into array
            s = (v['MARR'] + ' ' + v['HUSB'] + ' ' + v['WIFE'])
            if(s in marHusWife):
                i = marHusWife.index(s)
                passesCheck = False
                log('Error','US24','Family (' + k + ') has same spouses and marriage date as family (' + famIDs[i] + ').')
            else:
                famIDs.append(k)
                marHusWife.append(s)
    return passesCheck
    
# Checks User Story 25:
# No more than one child with the same name and birth date should appear in a family
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkUniqueFirstNamesInFamilies(indi, fam):
    passesCheck = True
    if(fam):
        for k, v in fam.iteritems():
            childrenArr = []
            if('CHIL' in v.keys()):
                for childId in v['CHIL']:
                    s = indi[childId]['NAME'] + ' ' + indi[childId]['BIRT']
                    if(s in childrenArr):
                        log('Error','US25','Family (' + k + ') child ' + indi[childId]['NAME'] + ' shares a name and birthday.')
                        passesCheck = False
                    else:
                        childrenArr.append(s)
    return passesCheck

# User Story 27:
# Include person's current age when listing individuals
# Returns a row of values to print as a pretty table (first row is the header)
def listIndividualAges(indi):
    rows = [] #initilize the row list
    rows.append(['Individual', 'Age']) #add in the header row
    #loop over all stored individuals
    for k, v in indi.iteritems():
        if (v.get('DEAT') is not None):
            #individual is dead
            age = getAgeDead([v['BIRT']], [v['DEAT']])
        else:
            #individual is alive
            age = getAgeAlive([v['BIRT']])
        rows.append([v['NAME'],age]) #append the data for the individual
    return rows

# User Story 28:
# List siblings in families by decreasing age, i.e. oldest siblings first
# Returns a row of values to print as a pretty table (first row is the header)
def listSiblingsByAge():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# User Story 29:
# List all deceased individuals in a GEDCOM file
# Returns a row of values to print as a pretty table (first row is the header)
def listDeceased(indi):
    rows = [] #initilize the row list
    rows.append(['Name', 'Date']) #add in the header row
    for k,v in indi.iteritems():
        if(v.get('DEAT') is not None):
            # Means individual is dead
            rows.append([v['NAME'], v['DEAT']])

    return rows
    
# User Story 30:
# List all living married people in a GEDCOM file
# Returns a row of values to print as a pretty table (first row is the header)
def listLivingMarried(indi, fam):
    rows = [] #initilize the row list
    rows.append(['Name', 'Family']) #add in the header row
    for k, v in indi.iteritems():
        if(v.get('DEAT') is None and v.get('FAMS') is not None):
            for f in v.get('FAMS'):
                if(fam[f].get('DIV') is None):
                    rows.append([v['NAME'], f])

    return rows

# User Story 31:
# List all living people over 30 who have never been married in a GEDCOM file
# Returns a row of values to print as a pretty table (first row is the header)
def listLivingSingles():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# User Story 33:
# List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
# Returns a row of values to print as a pretty table (first row is the header)
def listOrphans():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# User Story 34:
# List all couples who were married when the older spouse was more than twice as old as the younger spouse
# Returns a row of values to print as a pretty table (first row is the header)
def listLargeAgeDifferences():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# User Story 35:
# List all people in a GEDCOM file who were born in the last 30 days
# Returns a row of values to print as a pretty table (first row is the header)
def listRecentBirths(indi):
    rows = [] #initilize the row list
    rows.append(['Name', 'Date']) #add in the header row
    for k,v in indi.iteritems():
    	if(v.get('BIRT') is not None):
	        birthDate = getFormattedDateForCompare(v['BIRT'])
	        currentDate = date.today() #today's date
	        pastDate = currentDate - timedelta(days=30); #30 days ago

	        if(birthDate > pastDate and birthDate <= currentDate):
	        	# Means individual was born in the last 30 days
				rows.append([v['NAME'], v['BIRT']])

    return rows

# User Story 36:
# List all people in a GEDCOM file who died in the last 30 days
# Returns a row of values to print as a pretty table (first row is the header)
def listRecentDeaths(indi):
    rows = [] #initilize the row list
    rows.append(['Name', 'Date']) #add in the header row
    for k,v in indi.iteritems():
        if(v.get('DEAT') is not None):
			# Means individual is dead
			deathDate = getFormattedDateForCompare(v['DEAT'])
			currentDate = date.today() #today's date
			pastDate = currentDate - timedelta(days=30); #30 days ago

			if(deathDate > pastDate and deathDate <= currentDate):
				# Means individual has died in the last 30 days
				rows.append([v['NAME'], v['DEAT']])

    return rows

# User Story 38:
# List all living people in a GEDCOM file whose birthdays occur in the next 30 days
# Returns a row of values to print as a pretty table (first row is the header)
def listUpcomingBirthdays():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# User Story 39:
# List all living couples in a GEDCOM file whose marriage anniversaries occur in the next 30 days
# Returns a row of values to print as a pretty table (first row is the header)
def listUpcomingAnniversaries():
     rows = [] #initilize the row list
     rows.append(['Header0', 'Header1', 'Header2']) #add in the header row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     rows.append(['Data0', 'Data1', 'Data2']) #add in data row
     return rows

# Checks User Story 40:
# List line numbers from GEDCOM source file when reporting errors
def includeLineNumbers():
    return True

# Checks User Story 42:
# All dates should be legitimate dates for the months specified (e.g., 2/30/2015 is not legitimate)
# This is considered an Error
# Returns True if the check is passed, and False if the check is failed
def checkIllegitimateDate(date, line):
    passesCheck = True
    if len(date) != 3:
        log('Error','US42',str(line)+': The date entered is not in the correct format.')
        passesCheck = False
    else:
        try:
            months = {'JAN': 1,
                    'FEB': 2,
                    'MAR': 3,
                    'APR': 4,
                    'MAY': 5,
                    'JUN': 6,
                    'JUL': 7,
                    'AUG': 8,
                    'SEP': 9,
                    'OCT': 10,
                    'NOV': 11,
                    'DEC': 12}
            if (date[1] in months):
                datetime.datetime(year=int(date[2]),month=months[date[1]],day=int(date[0]))
            else:
                log('Error','US42',str(line)+': The date \'' + str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + '\' is not a legitimate date. A date of \'01 JAN 2000\' is being set for this date until it is fixed.')
                passesCheck = False
        except ValueError:
            log('Error','US42',str(line)+': The date \'' + str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + '\' is not a legitimate date. A date of \'01 JAN 2000\' is being set for this date until it is fixed.')
            passesCheck = False
    return passesCheck

# this function prints the error or anomaly message to the output file
# severity - Error or Anomaly
# userStory - the user story in which the error/anomaly failed
# message - detailed explination of the error/anomaly
def log(severity, userStory, message):
    F.write(severity + ': ' + userStory + ': ' + message + '\n')

# this function prints in a pretty table
# title is the title of the table (i.e. 'Individuals' or 'Families' or 'Recent Births')
# rows are the data to be printed (first row is the header)
def prettyPrint(title, rows):
    #printing using PrettyTable
    pt = PrettyTable()
    pt.field_names = rows[0] # header
    for i in range(1, len(rows)): #starting at 1 since 0 is the header
        pt.add_row(rows[i])
    F.write('\n') #spacing to make the output file easier to read
    F.write(title + ':\n') #print title
    F.write(str(pt) + '\n')

if __name__ == '__main__':
    main() #call to main function