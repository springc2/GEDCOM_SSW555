"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
6/17/2018
Description: 
    Tests for the GEDCOM_Project.py file
"""

import unittest
import GEDCOM_Project

class TestGEDCOM_Project(unittest.TestCase):
    
    #test the checkUniqueIDs funciton
    def test_checkUniqueIDs(self):
        test1Dict = {}
        test2Dict = {'I01': 'John Doe',
                     'I02': 'Jane Doe'}
        test3Dict = {'I01': 'John Doe',
                     'I02': 'Jane Doe',
                     'I03': 'Jake Doe'}
        
        test1 = GEDCOM_Project.checkUniqueIDs('I03', test1Dict) #empty dictionary
        test2 = GEDCOM_Project.checkUniqueIDs('I03', test2Dict) #unique IDs
        test3 = GEDCOM_Project.checkUniqueIDs('I03', test3Dict) #not unique IDs
        
        self.assertTrue(test1) #True
        self.assertTrue(test2) #True
        self.assertFalse(test3) #False
    
    #test the checkUniqueNameAndBirthDate function
    def test_checkUniqueNameAndBirthDate(self):
        test1Dict = {}
        test2Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '8 OCT 1993'},
                     'I02': {'ID': 'I02',
                             'NAME': 'Jane Doe',
                             'BIRT': '16 JUN 1993'}}
        test3Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '8 OCT 1993'},
                     'I02': {'ID': 'I02',
                             'NAME': 'Jane Doe',
                             'BIRT': '16 JUN 1993'},
                     'I03': {'ID': 'I03',
                             'NAME': 'John Doe',
                             'BIRT': '8 OCT 1993'}}
        
        test4Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '8 OCT 1993'},
                     'I02': {'ID': 'I02',
                             'NAME': 'Jane Doe',
                             'BIRT': '16 JUN 1993'},
                     'I03': {'ID': 'I03',
                             'NAME': 'John Doe',
                             'BIRT': '15 NOV 1990'}}
        test5Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '8 OCT 1993'},
                     'I02': {'ID': 'I02',
                             'NAME': 'Jane Doe',
                             'BIRT': '16 JUN 1993'},
                     'I03': {'ID': 'I03',
                             'NAME': 'Jake Doe',
                             'BIRT': '8 OCT 1993'}}
        
        test1 = GEDCOM_Project.checkUniqueNameAndBirthDate(test1Dict) #empty dictionary
        test2 = GEDCOM_Project.checkUniqueNameAndBirthDate(test2Dict) #no one has the same bday and name
        test3 = GEDCOM_Project.checkUniqueNameAndBirthDate(test3Dict) #name and bday both match
        test4 = GEDCOM_Project.checkUniqueNameAndBirthDate(test4Dict) #name matches, bday does not match
        test5 = GEDCOM_Project.checkUniqueNameAndBirthDate(test5Dict) #name does not match, bday does match
        
        
        self.assertTrue(test1) #True
        self.assertTrue(test2) #True
        self.assertFalse(test3) #False
        self.assertTrue(test4) #True
        self.assertTrue(test5) #True

    #test the checkBirthBeforeMarriage function
    def test_checkBirthBeforeMarriage(self):
        test1IndiDict = {}
        test1FamDict = {}

        test2IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976'}}

        test2FamDict = {'F01': {'ID': 'F01',
                                'MARR': '19 AUG 1956',
                                'HUSB': 'I01'}}

        test3IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'Jane Doe',
                                 'BIRT': '23 JUN 1979'}}

        test3FamDict = {'F01': {'ID': 'F01',
                                'MARR': '19 AUG 1956',
                                'WIFE': 'I01'}}

        test4IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '23 JUN 1979'},
                        'I01': {'ID': 'I02',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976'}}

        test4FamDict = {'F01': {'ID': 'F01',
                                'MARR': '19 AUG 1956',
                                'HUSB': 'I01',
                                'WIFE': 'I02'}}

        test5IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976'}}

        test5FamDict = {'F01': {'ID': 'F01',
                                'MARR': '19 AUG 1996',
                                'HUSB': 'I01'}}

        
        test1 = GEDCOM_Project.checkBirthBeforeMarriage(test1IndiDict, test1FamDict) #empty dictionary
        test2 = GEDCOM_Project.checkBirthBeforeMarriage(test2IndiDict, test2FamDict) #Husband birth date post-dates marriage date
        test3 = GEDCOM_Project.checkBirthBeforeMarriage(test3IndiDict, test3FamDict) #Wife birth date post-dates marriage date
        test4 = GEDCOM_Project.checkBirthBeforeMarriage(test4IndiDict, test4FamDict) #Husband and Wife birth dates post-date marriage date
        test5 = GEDCOM_Project.checkBirthBeforeMarriage(test5IndiDict, test5FamDict) #Marriage date after birth dates
        
        self.assertTrue(test1) #True
        self.assertFalse(test2) #False
        self.assertFalse(test3) #False
        self.assertFalse(test4) #False
        self.assertTrue(test5) #True

    #test the checkBirthBeforeDeath function
    def test_checkBirthBeforeDeath(self):
        test1Dict = {}

        test2Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '12 MAY 1996',
                             'DEAT': '11 MAY 1996'}}

        test3Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '21 OCT 1985',
                             'DEAT': '18 JUN 1984'},
                     'I02': {'ID': 'I02',
                             'NAME': 'Jane Doe',
                             'BIRT': '8 OCT 1993',
                             'DEAT': '21 AUG 1973'}}

        test4Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '12 MAY 1984',
                             'DEAT': '21 OCT 1991'}}

        test5Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '21 OCT 1991',
                             'DEAT': '21 OCT 1991'}}

        
        test1 = GEDCOM_Project.checkBirthBeforeDeath(test1Dict) #empty dictionary
        test2 = GEDCOM_Project.checkBirthBeforeDeath(test2Dict) #death date pre-dates birth date
        test3 = GEDCOM_Project.checkBirthBeforeDeath(test3Dict) #2 persons death date pre-dates birth date
        test4 = GEDCOM_Project.checkBirthBeforeDeath(test4Dict) #birth date pre-dates death date
        test5 = GEDCOM_Project.checkBirthBeforeDeath(test5Dict) #birth date is same as death date
        
        
        self.assertTrue(test1) #True
        self.assertFalse(test2) #False
        self.assertFalse(test3) #False
        self.assertTrue(test4) #True
        self.assertTrue(test5) #True
    
if __name__ == '__main__':
   resultFile = 'Test_Results.txt'
   try:
       f = open(resultFile, "w")
       runner = unittest.TextTestRunner(f)
       unittest.main(testRunner=runner)
       f.close()
   except IOError:
       print 'Error! Cannot open', resultFile