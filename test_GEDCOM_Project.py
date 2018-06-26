"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
6/24/2018
Description: 
    Tests for the GEDCOM_Project.py file
"""

import unittest
import GEDCOM_Project

class TestGEDCOM_Project(unittest.TestCase):
    
    #US01 - test the checkDatesBeforeCurrentDate function
    def test_checkDatesBeforeCurrentDate(self):
        test1 = True
        self.assertTrue(test1)

    #US02 - test the checkBirthBeforeMarriage function
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
                        'I02': {'ID': 'I02',
                                 'NAME': 'Jane Doe',
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
        
        test6IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '14 MAY 1976'},
                        'I02': {'ID': 'I02',
                                 'NAME': 'Jane Doe',
                                 'BIRT': '10 MAY 1976'}}

        test6FamDict = {'F01': {'ID': 'F01',
                                'MARR': '12 MAY 1976',
                                'HUSB': 'I01',
                                'WIFE': 'I02'}}
        
        test7IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '10 MAY 1976'},
                        'I02': {'ID': 'I02',
                                 'NAME': 'Jane Doe',
                                 'BIRT': '14 MAY 1976'}}

        test7FamDict = {'F01': {'ID': 'F01',
                                'MARR': '12 MAY 1976',
                                'HUSB': 'I01',
                                'WIFE': 'I02'}}

        
        test1 = GEDCOM_Project.checkBirthBeforeMarriage(test1IndiDict, test1FamDict) #empty dictionary
        test2 = GEDCOM_Project.checkBirthBeforeMarriage(test2IndiDict, test2FamDict) #Husband birth date post-dates marriage date
        test3 = GEDCOM_Project.checkBirthBeforeMarriage(test3IndiDict, test3FamDict) #Wife birth date post-dates marriage date
        test4 = GEDCOM_Project.checkBirthBeforeMarriage(test4IndiDict, test4FamDict) #Husband and Wife birth dates post-date marriage date
        test5 = GEDCOM_Project.checkBirthBeforeMarriage(test5IndiDict, test5FamDict) #Marriage date after birth dates
        test6 = GEDCOM_Project.checkBirthBeforeMarriage(test6IndiDict, test6FamDict) #Marriage after wife birth, before husb birth
        test7 = GEDCOM_Project.checkBirthBeforeMarriage(test7IndiDict, test7FamDict) #Marriage after husb birth, before wife birth
        
        self.assertTrue(test1) #True
        self.assertFalse(test2) #False
        self.assertFalse(test3) #False
        self.assertFalse(test4) #False
        self.assertTrue(test5) #True
        self.assertFalse(test6) #False
        self.assertFalse(test7) #False

    #US03 - test the checkBirthBeforeDeath function
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

    #US04 - test the checkMarriageBeforeDivorce function
    def test_checkMarriageBeforeDivorce(self):

        test1Dict = {'F01' : {'MARR': '13 MAY 1986'}}
        test2Dict = {'F01' : {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1987'}}
        test3Dict = {'F01' : {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1984'}}		
        test4Dict = {'F01' : {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1988'},
                     'F02' : {'MARR': '20 SEP 1986', 'DIV': '13 JUN 1988'}}
        test5Dict = {'F01' : {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1988'},
                     'F02' : {'MARR': '20 SEP 1986', 'DIV': '13 JUN 1978'}}			
        test6Dict = {}			 

        test1 = GEDCOM_Project.checkMarriageBeforeDivorce(test1Dict) #No divorce
        test2 = GEDCOM_Project.checkMarriageBeforeDivorce(test2Dict) #Marriage before divorce
        test3 = GEDCOM_Project.checkMarriageBeforeDivorce(test3Dict) #Marriage after divorce
        test4 = GEDCOM_Project.checkMarriageBeforeDivorce(test4Dict) #Marriage before divorce second family
        test5 = GEDCOM_Project.checkMarriageBeforeDivorce(test5Dict) #Marriage after divorce second family
        test6 = GEDCOM_Project.checkMarriageBeforeDivorce(test6Dict) #Empty dict

        self.assertTrue(test1) #No divorce, True
        self.assertTrue(test2) #Marriage before divorce TRUE
        self.assertFalse(test3) #Marriage after divorce FALSE
        self.assertTrue(test4) #Marriage before divorce second family TRUE
        self.assertFalse(test5) #Marriage after divorce second family FALSE
        self.assertTrue(test6) #Empty dict TRUE

    #US05 - test the checkMarriageBeforeDeath function
    def test_checkMarriageBeforeDeath(self):

        testDictFam = {'F01' : {'MARR': '13 MAY 1986', 'HUSB': 'I01', 'WIFE': 'I02'}}
        test1DictInd = {'I01': {'ID': 'I01','DEAT': '8 OCT 1993'},
                        'I02': {'ID': 'I02','DEAT': '16 JUN 1993'}}
        test2DictInd = {'I01': {'ID': 'I01','DEAT': '8 OCT 1900'},
                        'I02': {'ID': 'I02','DEAT': '16 JUN 1993'}}
        test3DictInd = {'I01': {'ID': 'I01','DEAT': '8 OCT 1993'},
                        'I02': {'ID': 'I02','DEAT': '16 JUN 1900'}}
        test4DictInd = {}
        test5DictInd = {'I01': {'ID': 'I01','DEAT': '8 OCT 1900'},
                        'I02': {'ID': 'I02','DEAT': '16 JUN 1900'}}
        test6DictInd = {'I01': {'ID': 'I01'},
                        'I02': {'ID': 'I02'}}
        

        test1 = GEDCOM_Project.checkMarriageBeforeDeath(test1DictInd, testDictFam) #deaths after marriage
        test2 = GEDCOM_Project.checkMarriageBeforeDeath(test2DictInd, testDictFam) #husb death before, wife after marriage
        test3 = GEDCOM_Project.checkMarriageBeforeDeath(test3DictInd, testDictFam) #husb death after, wife before marriage
        test4 = GEDCOM_Project.checkMarriageBeforeDeath(test4DictInd, testDictFam) #empty dict
        test5 = GEDCOM_Project.checkMarriageBeforeDeath(test5DictInd, testDictFam) #both husb and wife died before marriage
        test6 = GEDCOM_Project.checkMarriageBeforeDeath(test6DictInd, testDictFam) #both husb and wife still alive

        self.assertTrue(test1) #True
        self.assertFalse(test2) #False
        self.assertFalse(test3) #False
        self.assertTrue(test4) #True
        self.assertFalse(test5) #False
        self.assertTrue(test6) #True

    #US06 - test the checkDivorceBeforeDeath function
    def test_checkDivorceBeforeDeath(self):
        test1 = True
        self.assertTrue(test1)

    #US07 - test the checkLessThan150YearsOld function
    def test_checkLessThan150YearsOld(self):
        test1 = True
        self.assertTrue(test1)

    #US08 - test the checkBirthBeforeMarriageOfParents function
    def test_checkBirthBeforeMarriageOfParents(self):
        
        emptyDictFam = {}
        testDictFam = {'F01' : {'MARR': '13 MAY 1986', 
                                'DIV' : '20 MAY 2012',
                                'HUSB': 'I01', 
                                'WIFE': 'I02',
                                'CHIL': ['I03']}}
        testDictFam['F01']['CHIL'].append('I04') #adding I04 to the family
        
        emptyDictInd = {}
        test2DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 MAY 1996',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 2012',
                                'FAMC': 'F01'}}
        test3DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '10 MAY 1986',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '13 MAY 1996',
                                'FAMC': 'F01'}}
        test4DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '10 MAY 1986',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '11 MAY 1986',
                                'FAMC': 'F01'}}
        test5DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 MAY 1986',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '22 MAY 1996',
                                'FAMC': 'F01'}}
        test6DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 MAY 1996',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 2020',
                                'FAMC': 'F01'}}
        test7DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '25 MAY 2020',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '20 FEB 2020',
                                'FAMC': 'F01'}}
        test8DictInd = {'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '25 MAY 2000',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '20 FEB 2013',
                                'FAMC': 'F01'}}

        test1 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(emptyDictInd, emptyDictFam) #empty dicts
        test2 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test2DictInd, testDictFam) #both children born after marr (and within 9 months of div)
        test3 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test3DictInd, testDictFam) #one child born before marr
        test4 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test4DictInd, testDictFam) #both children born before marr
        test5 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test5DictInd, testDictFam) #one child born on date of marr (still false)
        test6 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test6DictInd, testDictFam) #one child born after 9 months of div
        test7 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test7DictInd, testDictFam) #both child born after 9 months of div
        test8 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test8DictInd, testDictFam) #one child born 9 months after div


        self.assertTrue(test1) #True
        self.assertTrue(test2) #True
        self.assertFalse(test3) #False
        self.assertFalse(test4) #False
        self.assertFalse(test5) #False
        self.assertFalse(test6) #False
        self.assertFalse(test7) #False
        self.assertTrue(test8) #True

    #US09 - test the checkBirthBeforeDeathOfParents function
    def test_checkBirthBeforeDeathOfParents(self):
        test1 = True
        self.assertTrue(test1)

    #US10 - test the checkMarriageAfter14 function
    def test_checkMarriageAfter14(self):
        test1 = True
        self.assertTrue(test1)

    #US12 - test the checkParentsNotTooOld function
    def test_checkParentsNotTooOld(self):
        test1 = True
        self.assertTrue(test1)

    #US15 - test the checkFewerThan15Siblings function
    def test_checkFewerThan15Siblings(self):
        test1 = True
        self.assertTrue(test1)

    #US22 - test the checkUniqueIDs funciton
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
    
    #US23 - test the checkUniqueNameAndBirthDate function
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

    # US24 - Tests checkUniqueFamiliesBySpouses function
    # Tests if there exists more than one family with the same spouses by name and marriage date
    def test_checkUniqueFamiliesBySpouses(self):
        # Test case for different families with different everything
        test1dic = {'F01' : {'MARR': '13 MAY 1986',
                             'WIFE': 'I14',
                             'HUSB': 'I01'},
                    'F02' : {'MARR': '14 JUNE 2002',
                             'WIFE': 'I11',
                             'HUSB': 'I02'}}

        # Tests empty dictionary case
        test2dic = {}

        # Test case for same marriage date but different spouses, should still be true
        test3dic = {'F04': {'MARR': '12 NOV 1999',
                            'WIFE': 'I05',
                            'HUSB': 'I03'},
                    'F05' : {'MARR': '12 NOV 1999',
                             'WIFE': 'I06',
                             'HUSB': 'I07'}}

        # Test case for two families with identical everything should return false
        test4dic = {'F01': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'},
                    'F02': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'}}

        # One valid family and two identical families should return false
        test5dic = {'F01': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'},
                    'F05': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'},
                    'F03': {'MARR': '16 JUN 2001',
                            'WIFE': 'I04',
                            'HUSB': 'I05'}}

        # Same husband + wife and different date (divorced and remarried) should return true
        test6dic = {'F01': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'},
                    'F05': {'MARR': '12 MAY 2010',
                            'WIFE': 'I01',
                            'HUSB': 'I02'}}
        
        # husband marries two wives on same day should return true
        test7dic = {'F01': {'MARR': '12 MAY 2000',
                            'WIFE': 'I01',
                            'HUSB': 'I02'},
                    'F05': {'MARR': '12 MAY 2000',
                            'WIFE': 'I03',
                            'HUSB': 'I01'}}

        test1 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test1dic)   # Valid family
        test2 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test2dic)   # Empty dictionary
        test3 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test3dic)   # Same marriage date but different spouses
        test4 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test4dic)   # Families with identical spouses and marriage date false
        test5 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test5dic)   # Families with identical spouses and marriage date one without false
        test6 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test6dic)   # Same husband + wife and different date (divorced and remarried)
        test7 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test7dic)   # husband marries two wives on same day

        self.assertTrue(test1) # True
        self.assertTrue(test2) # True
        self.assertTrue(test3) # True
        self.assertFalse(test4) # False
        self.assertFalse(test5) # False
        self.assertTrue(test6) # True
        self.assertTrue(test7) # True

    # US25 - Tests checkUniqueFirstNamesInFamilies function
    # Tests if there is no more than one child with the same name and birth date in a family
    def test_checkUniqueFirstNamesInFamilies(self):

        test1famdic = {}   # Empty dictionary
        test1indidic = {}  # Empty dictionary

        test2famdic = {'F01': {'CHIL': ['I01']}}            # One child in family
        test2indidic = {'I01': {'NAME': 'Jack /Daniels/',   # Checks against list of individuals
                                'BIRT': '05 NOV 2001'}}

        test3famdic = {'F01': {'CHIL': ['I01', 'I02']},     # Two families with kids of all different names
                       'F02': {'CHIL': ['I03', 'I04']}}
        test3indidic = {'I01': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I02': {'NAME': 'Tyrone /Willis/',
                                'BIRT': '02 JUN 2001'},
                        'I03': {'NAME': 'Daron /Bonfooboo/',
                                'BIRT': '01 JAN 1999'},
                        'I04': {'NAME': 'John /Fosho/',
                                'BIRT': '22 NOV 1994'}}

        test4famdic = {'F01': {'CHIL': ['I01', 'I02']}}     # Tests false for two kids with same name and birth date
        test4indidic = {'I01': {'NAME': 'Michael /Flin/',
                                'BIRT': '04 NOV 1995'},
                        'I02': {'NAME': 'Michael /Flin/',
                                'BIRT': '04 NOV 1995'}}

        test5famdic = {'F01': {'CHIL': ['I01', 'I02']},     # Tests true for two different families with kids of same name and birthday
                       'F02': {'CHIL': ['I03', 'I04']}}
        test5indidic = {'I01': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I02': {'NAME': 'Tyrone /Willis/',
                                'BIRT': '02 JUN 2001'},
                        'I03': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I04': {'NAME': 'John /Fosho/',
                                'BIRT': '22 NOV 1994'}}

        test1 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test1indidic, test1famdic)   # Empty dictionaries
        test2 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test2indidic, test2famdic)   # Two families with children of different names and birthday
        test3 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test3indidic, test3famdic)   # One family with two children of same name
        test4 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test4indidic, test4famdic)   # Two kids with same name and birthday in same family
        test5 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test5indidic, test5famdic)   # Two different families with kids of same name and birthday

        self.assertTrue(test1)   # True
        self.assertTrue(test2)   # True
        self.assertTrue(test3)   # True
        self.assertFalse(test4)  # False
        self.assertTrue(test5)   # True

if __name__ == '__main__':
   resultFile = 'Test_Results.txt'
   try:
       f = open(resultFile, "w")
       runner = unittest.TextTestRunner(f)
       unittest.main(testRunner=runner)
       f.close()
   except IOError:
       print 'Error! Cannot open', resultFile