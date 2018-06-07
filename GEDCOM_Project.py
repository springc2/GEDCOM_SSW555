"""
Dan Bekier
SSW-555
6/3/2018
Project02 - GEDCOM file reader, quick error checker

This script will:
    1) Read each line of a GEDCOM file
    2) Print "--> <input line>"
    3) Print "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
        <level> - level of the input line
        <tag> - tag associated with the line
        <valid?> - value 'Y' if the tag is a supported tag or 'N' otherwise.
        <arguments> - rest of the line beyond the level and tag.

(The output will be a seperate text file)
"""

#global variables
#INPUTGEDCOM = 'Bekier_Project01.txt' #project01's GED file
INPUTGEDCOM = 'proj02test.ged' #sample GED file
#INPUTGEDCOM = 'sample.txt' #sample GED file
#OUTPUTFILE = 'Bekier_Project01_output.txt' #project01's output file
OUTPUTFILE = 'proj02test_output.txt' #sample output file
#OUTPUTFILE = 'sample_output.txt' #sample output file
try:
    F = open(OUTPUTFILE,'w')
except IOError:
    print 'cannot open', OUTPUTFILE


#main function
def main():

    try:
        with open(INPUTGEDCOM) as fp:
            for line in fp:
                #print the line as it is
                F.write("--> " + line)
                #print with the correct format
                formattedPrint(line)
        F.close()
    except IOError:
        print 'ERROR: Cannot Open File:', INPUTGEDCOM


#this fuction will print the GEDCOM lines in the correct format
def formattedPrint(line):
    #parse the GEDCOM line by whitespaces
    parsedLine = line.strip().split()
    
    #check if the line's format is valid
    validLine = isValid(parsedLine)
    #check if the line is a valid special case
    validSpecialCase = isSpecialCase(parsedLine)

    if (validLine or validSpecialCase):
        validFlag = 'Y'
    else:
        validFlag = 'N'
    
    if(validSpecialCase):
        #special case format
        F.write("<-- " + parsedLine[0] + "|" + parsedLine[2] + "|" + validFlag + "|" + parsedLine[1] + '\n')
    else:
        #normal case format
        F.write("<-- " + parsedLine[0] + "|" + parsedLine[1] + "|" + validFlag + "|" + ' '.join(parsedLine[2:len(parsedLine)]) + '\n')

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