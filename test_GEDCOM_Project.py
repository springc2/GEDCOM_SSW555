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
        
if __name__ == '__main__':
    unittest.main()
