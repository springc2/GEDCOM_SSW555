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
    
    #test the checkUniqueNameAndBirthDate funciton
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


    # Michael Macari - Test Cases
    # Tests checkUniqueFamiliesBySpouses function
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


        test1 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test1dic)   # Valid family
        test2 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test2dic)   # Empty dictionary
        test3 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test3dic)   # Same marriage date but different spouses
        test4 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test4dic)   # Families with identical spouses and marriage date false
        test5 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test5dic)   # Families with identical spouses and marriage date one without false

        self.assertTrue(test1) # True
        self.assertTrue(test2) # True
        self.assertTrue(test3) # True
        self.assertFalse(test4) # False
        self.assertFalse(test5) # False

    # Tests checkUniqueFirstNamesInFamilies function
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