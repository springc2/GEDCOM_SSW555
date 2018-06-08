"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
6/10/2018
Project03 - save info about families and individuals, print info in nice format
"""

#imports
import collections
from prettytable import PrettyTable
from datetime import date

#global variables
INPUT_FILE = 'GEDCOM_Input.ged' #input file
OUTPUT_FILE = 'GEDCOM_Output.txt' #output file
try:
    F = open(OUTPUT_FILE,'w')
except IOError:
    print 'Error! Cannot open', OUTPUT_FILE

FAMILIES = {} #empty dictionary for families, will be a dict of dicts
INDIVIDUALS = {} #empty dictionary for individuals, will be a dict of dicts

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
            
            #print the individuals in order by their IDs
            printIndividuals(collections.OrderedDict(sorted(INDIVIDUALS.items())))
            #print the families in order by their IDs
            printFamilies(collections.OrderedDict(sorted(FAMILIES.items())))
    except IOError:
        #print 'ERROR: Cannot Open File:', INPUT_FILE
        F.write('ERROR: Cannot Open File: ' + INPUT_FILE + '\n')
    F.close()


#this fuction will create either a new fmily or a new individual
#returns the current entities ID
#(if it is not a uniquie ID, will return blanks so the info of this entity is not added)
def createEntity(pLine, entType):
    entID = pLine[1] #this is the ID of the entity
    if (entType == 'FAM'):
        #check if the ID is a unique ID
        if (entID not in FAMILIES):
            #the new entity is a family so we will create a new dictionary for it within the fam dictionary
            FAMILIES.update({entID: {'ID': entID}})
        else:
            entID = ''
            F.write('Error: not a uniquie Family ID, not adding it or it\'s info!\n')
    elif (entType == 'INDI'):
        #check if the ID is a unique ID
        if (entID not in INDIVIDUALS):
            #the new entity is an individual so we will create a new dictionary for it within the indi dictionary
            INDIVIDUALS.update({entID: {'ID': entID}})
        else:
            entID = ''
            F.write('Error: not a uniquie Family ID, not adding it or it\'s info!\n')
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


main() #call to main function