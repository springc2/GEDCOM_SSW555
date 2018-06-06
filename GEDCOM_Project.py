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
#inputGEDCOM = 'Bekier_Project01.txt'; #project01's GED file
#inputGEDCOM = 'proj02test.ged'; #sample GED file
inputGEDCOM = 'sample.txt'; #sample GED file
#outputfile = 'Bekier_Project01_output.txt'; #project01's output file
#outputfile = 'proj02test_output.txt'; #sample output file
outputfile = 'sample_output.txt'; #sample output file
f = open(outputfile,'w');

level0Tags = [ #all the valid level 0 tags
              'INDI',
              'FAM',
              'HEAD',
              'TRLR',
              'NOTE'
              ];

level1Tags = [ #all the valid level 1 tags
              'NAME',
              'SEX',
              'BIRT',
              'DEAT',
              'FAMC',
              'FAMS',
              'MARR',
              'HUSB',
              'WIFE',
              'CHIL',
              'DIV'
              ];

level2Tags = [ #all the valid level 3 tags
              'DATE'
              ];

#main function
def main():

    with open(inputGEDCOM) as fp:
        for line in fp:
            #print the line as it is
            f.write("--> " + ' '.join(line.split()[0:len(line.split())]) + "\n");
            #print with the correct format
            formattedPrint(line)
    f.close()



#this fuction will print the GEDCOM lines in the correct format
def formattedPrint(line):
    #parse the GEDCOM line by whitespaces
    parsedLine = line.split();
    
    #check if the line's format is valid
    validLine = isValid(parsedLine);
    #check if the line is a valid special case
    validSpecialCase = isSpecialCase(parsedLine);

    if (validLine or validSpecialCase):
        validFlag = 'Y';
    else:
        validFlag = 'N';
    
    if(validSpecialCase):
        #special case format
        f.write("<-- " + parsedLine[0] + "|" + parsedLine[2] + "|" + validFlag + "|" + parsedLine[1] + '\n');
    else:
        #normal case format
        f.write("<-- " + parsedLine[0] + "|" + parsedLine[1] + "|" + validFlag + "|" + ' '.join(parsedLine[2:len(parsedLine)]) + '\n');

#returns true if the line is in the correct format
#returns false otherwise
def isValid(pLine):
    level = pLine[0];
    tag = pLine[1];
    isValid = True;
    
    if (level == '0'):
        #level 0
        if tag not in level0Tags :
            isValid = False;
        else:
            #if INDI or FAM is in the tag location, then it is invalid
            if (tag == 'INDI' or tag == 'FAM'):
                isValid = False;
    elif (level == '1'):
        #level 1
        if tag not in level1Tags :
            isValid = False;
    elif (level == '2'):
        #level 2
        if tag not in level2Tags :
            isValid = False;
    else:
        #the level is not a valid level
        isValid = False;
    
    return isValid;

#returns true if the input is a special case in the correct format
#returns false otherwise
#special cases are:
#    0 <id> INDI
#    0 <id> FAM
def isSpecialCase(pLine):
    isValid = True;
    specialTags = [ #all the valid special tags
                   'INDI',
                   'FAM'
                   ];

    #check if the size of the line is 3
    if (len(pLine) != 3):
        isValid = False;
    else:
        #check if the level is 0
        if (pLine[0] != '0'):
            isValid = False;
        else:
            #check if the 'tag' is a special tag
            if pLine[2] not in specialTags :
                isValid = False;
    return isValid;


main(); #call to main function