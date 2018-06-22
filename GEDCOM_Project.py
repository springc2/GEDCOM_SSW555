"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
6/24/2018
Description: 
    Reads a GEDCOM file, prints the Families and Individuals data in a easy to read format, and prints errors and anomalies found in the GEDCOM file
"""

#imports
import collections
import time
from prettytable import PrettyTable
from datetime import date

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
                    datePredecessor = updateEntity(parsedLine, curEntityID, curEntityType, datePredecessor)
                else:
                    #add error reporting to help user
                    invalidLines.append(numLine)
            
            if(len(invalidLines) > 0):
                #print 'Invalid GEDCOM format on lines:', invalidLines
                F.write('The following lines had an invalid format: ' + str(invalidLines) + '\n')
            #next we want to check for errors and anomalies
            additionalChecking()
            F.write('\n') #spacing to make the output file easier to read
            #print the individuals in order by their IDs
            printIndividuals(collections.OrderedDict(sorted(INDIVIDUALS.items())))
            F.write('\n') #spacing to make the output file easier to read
            #print the families in order by their IDs
            printFamilies(collections.OrderedDict(sorted(FAMILIES.items())))
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
        F.write('Unexpected error while creating a new entity!\n')
    return entID

#this fuction will update an entities information based on the given line info
def updateEntity(pLine, entID, entType, curDatePred):
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
                #this date gets written for the previous tag
                FAMILIES[entID].update({curDatePred: ' '.join(pLine[2:len(pLine)])})
            else:
                if (pLine[1] == 'CHIL' and 'CHIL' in FAMILIES[entID]):
                    #a family can have multiple children
                    FAMILIES[entID][pLine[1]].append(' '.join(pLine[2:len(pLine)]))
                else:
                    if (pLine[1] == 'CHIL'):
                        #CHIL must be stored differently since it can have multiple entries
                        FAMILIES[entID].update({pLine[1]: [' '.join(pLine[2:len(pLine)])]})
                    else:
                        #otherwise just write normally
                        FAMILIES[entID].update({pLine[1]: ' '.join(pLine[2:len(pLine)])})
        elif (entType == 'INDI'):
            #working within the indi dict
            #working within the family dict
            if (pLine[1] in validDatePredecessor):
                #need to store this tag because it will be followed by a date
                nextDatePred = pLine[1]
            elif (pLine[1] == 'DATE' and curDatePred in validDatePredecessor):
                #this date gets written for the previous tag
                INDIVIDUALS[entID].update({curDatePred: ' '.join(pLine[2:len(pLine)])})
            else:
                
                if ((pLine[1] == 'FAMS' or pLine[1] == 'FAMC') and (pLine[1] in INDIVIDUALS[entID])):
                    #an individual can be in multiple families (as a child or spouse)
                    INDIVIDUALS[entID][pLine[1]].append(' '.join(pLine[2:len(pLine)]))
                else:
                    if (pLine[1] == 'FAMS' or pLine[1] == 'FAMC'):
                        #FAMS and FAMC must be stored differently since they can have multiple entiries
                        INDIVIDUALS[entID].update({pLine[1]: [' '.join(pLine[2:len(pLine)])]})
                    else:
                        #otherwise just write normally
                        INDIVIDUALS[entID].update({pLine[1]: ' '.join(pLine[2:len(pLine)])})
        else:
            F.write('Unexpected error while updating an entity!\n')
    return nextDatePred

#prints all the individuals and their info in the GEDCOM file by alphabetical order of their IDs
def printIndividuals(indi):
    #printing using PrettyTable
    pt = PrettyTable()
    pt.field_names = ['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse']
    for k, v in indi.iteritems():
        #get age
        age = getAge([v['BIRT']])
        #check if they are still living
        alive = True
        if (v.get('DEAT', 'NA') != 'NA'):
            alive = False
        pt.add_row([v['ID'], v['NAME'], v['SEX'], v['BIRT'], age, alive, v.get('DEAT', 'NA'), v.get('FAMC', 'NA'), v.get('FAMS', 'NA')])
    F.write('Individuals:\n')
    F.write(str(pt) + '\n')

#prints all the families and their info in the GEDCOM file by alphabetical order of their IDs
def printFamilies(fam):
    #printing using PrettyTable
    pt = PrettyTable()
    pt.field_names = ['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
    for k, v in fam.iteritems():
        pt.add_row([v['ID'], v['MARR'], v.get('DIV', 'NA'), v['HUSB'], INDIVIDUALS[v['HUSB']]['NAME'], v['WIFE'], INDIVIDUALS[v['WIFE']]['NAME'], v.get('CHIL', 'NA')])
    F.write('Families:\n')
    F.write(str(pt) + '\n')

#returns the age of an individual given their birthdate
#dates are in the format <day month year>
def getAge(birthDate):
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
        F.write('Unexpected error with birthdate!\n')
    birthYear = int(bDate[2])
    return today.year - birthYear - ((today.month, today.day) < (birthMonth, birthDay))

#returns the a formatted string representation of a date
#input dates are in the format <day month year>
def getFormattedDateString(date):
    _date = date[0].split() #parse the date
    day = int(_date[0])
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
    if (_date[1] in months):
        month = months[_date[1]]
    else:
        F.write('Unexpected error with date!\n')
    year = int(_date[2])
    dateString = str(month) + "/" + str(day) + "/" + str(year)

    return dateString

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
    validTags = {
            '0': ('INDI', 'FAM')
            }

    isValid = False
    
    #check if the size of the line is 3 so we don't run into an index out of bounds error
    if (len(pLine) == 3):
        level = pLine[0]
        tag = pLine[2]
        if (level in validTags and tag in validTags[level]):
            isValid = True
    
    return isValid

#this fuction is to check if there are any errors or anomalies in the GEDCOM file
#note that some error checking happens while the information is being stored, 
#so this function will not recheck for errors that have already been covered earlier in the program
def additionalChecking():
    checkUniqueNameAndBirthDate(INDIVIDUALS) #User Story 23
    checkUniqueFamiliesBySpouses(FAMILIES) #User Story 24
    checkUniqueFirstNamesInFamilies(INDIVIDUALS, FAMILIES) #User Story 25
    checkBirthBeforeMarriage(INDIVIDUALS, FAMILIES) #User Story 02
    checkBirthBeforeDeath(INDIVIDUALS) #User Story 03
    checkMarriageBeforeDivorce(FAMILIES) #User Story 04
    checkMarriageBeforeDeath(FAMILIES,INDIVIDUALS) #User Story 05

#Checks User Story 02:
#Birth should occur before marriage of an individual
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
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
                mDateString = getFormattedDateString([v1['MARR']])
                bDateString = getFormattedDateString([v['BIRT']])

                mDate = time.strptime(mDateString, '%m/%d/%Y')
                bDate = time.strptime(bDateString, '%m/%d/%Y')

                if bDate > mDate:
                    #there was a match, so we must print out the info
                    F.write('Error US02: ' + indi_name + ' (' + indi_id + ') has marriage date before birth date.\n')
                    passesCheck = False

    return passesCheck

#Checks User Story 03:
#Birth should occur before death of an individual
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkBirthBeforeDeath(indi):
    passesCheck = True

    #loop over all stored individuals
    for k, v in indi.iteritems():
        indi_id = v['ID']
        indi_name = v['NAME']
        if 'DEAT' in v:
            dDateString = getFormattedDateString([v['DEAT']])
            bDateString = getFormattedDateString([v['BIRT']])

            dDate = time.strptime(dDateString, '%m/%d/%Y')
            bDate = time.strptime(bDateString, '%m/%d/%Y')

            if bDate > dDate:
                #there was a match, so we must print out the info
                F.write('Error US03: ' + indi_name + ' (' + indi_id + ') has death date before birth date.\n')
                passesCheck = False

    return passesCheck

#Checks User Story 04:
#Marriage should occur before divorce of spouses, and divorce can only occur after marriage
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkMarriageBeforeDivorce(fam):
    passesCheck = True
    
    for k, v in fam.iteritems():
        if v.get('DIV') is None:
            continue
        coupleMarriageDate = time.strptime(v['MARR'], '%d %b %Y')
        coupleDivorceDate = time.strptime(v['DIV'], '%d %b %Y')

        if coupleDivorceDate < coupleMarriageDate:
            passesCheck = False
            F.write('Error US04: Family[' + k +'] has divorce before marriage.\n')
        
    return passesCheck

#Checks User Story 05:
#Marriage should occur before death of either spouse
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkMarriageBeforeDeath(fam, ind):
    passesCheck = True

    for k, v in fam.iteritems():
        coupleMarriageDate = time.strptime(v['MARR'], '%d %b %Y')
        if(ind):
            if ind[v['HUSB']].get('DEAT') is not None:
                husbandDeathDate = time.strptime(ind[v['HUSB']]['DEAT'], '%d %b %Y')
                if coupleMarriageDate > husbandDeathDate:
                    passesCheck = False
                    F.write('Error US05: Family[' + k +'] has death before marriage date for husband ['+v['HUSB']+ '].\n')
            if ind[v['WIFE']].get('DEAT') is not None:
                wifeDeathDate = time.strptime(ind[v['WIFE']]['DEAT'], '%d %b %Y')
                if coupleMarriageDate > wifeDeathDate:
                    passesCheck = False
                    F.write('Error US05: Family[' + k +'] has death before marriage date for wife ['+v['WIFE']+ '].\n')
    return passesCheck

#Checks User Story 22:
#All individual IDs should be unique and all family IDs should be unique
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkUniqueIDs(curID, dictionary):
    #NOTE that the name of an individual is not included in this error message
    #because families have no names but can run into the same error
    #and we want to keep the error message consistent for the both of them
    passesCheck = True
    if (curID in dictionary):
        #the ID is already in the dict, thus it is not unique
        F.write('Error US22: ID ' + curID + ' is not a uniquie ID. (Not including it or it\'s information!)\n')
        passesCheck = False
    #otherwise the ID is unique
    return passesCheck

#Checks User Story 23:
#No more than one individual with the same name and birth date should appear in a GEDCOM file
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
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
                F.write('Error US23: ' + indi_name + ' (' + indi_id + ') and '+ all_names[i] + ' (' + all_IDs[i] + ') have the same name and birth date.\n')
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

#Checks User Story 24:
#No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkUniqueFamiliesBySpouses(fam):
    passesCheck = True
    famIDs = []
    marHusWife = []

    if(fam):
        for k,v in fam.iteritems():         # Iterates through the dictionary and appends values into array
            s = (v['MARR'] + ' ' + v['HUSB'] + ' ' + v['WIFE'])
            if(s in marHusWife):
                i = marHusWife.index(s)
                passesCheck = False
                F.write('Error US24: Family (' + k + ') has same spouses and marriage date as family (' + famIDs[i] + ').\n')
            else:
                famIDs.append(k)
                marHusWife.append(s)
    return passesCheck
    
#Checks User Story 25:
#No more than one child with the same name and birth date should appear in a family
#This is considered an Error
#Returns True if the check is passed, and False if the check is failed
def checkUniqueFirstNamesInFamilies(indi, fam):
    passesCheck = True
    if(fam):
        for k, v in fam.iteritems():
            childrenArr = []
            if('CHIL' in v.keys()):
                for childId in v['CHIL']:
                    s = indi[childId]['NAME'] + ' ' + indi[childId]['BIRT']
                    if(s in childrenArr):
                        F.write('Error US25: Family (' + k + ') child ' + indi[childId]['NAME'] + ' shares a name and birthday. \n')
                        passesCheck = False
                    else:
                        childrenArr.append(s)
    return passesCheck


if __name__ == '__main__':
    main() #call to main function