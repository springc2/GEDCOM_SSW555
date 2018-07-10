"""
Chris Springer, Dan Bekier, Dan Pecoraro, Mike Macari
SSW-555
7/22/2018
Description: 
Tests for the GEDCOM_Project.py file
"""
import collections
import unittest
import GEDCOM_Project
from datetime import date


class TestGEDCOM_Project(unittest.TestCase):

    # US01 - test the checkDatesBeforeCurrentDate function
    def test_checkDatesBeforeCurrentDate(self):
        currentDate = date.today()  # today's date

        if (currentDate.month == 1):
            currMonth = 'JAN'
        elif (currentDate.month == 2):
            currMonth = 'FEB'
        elif (currentDate.month == 3):
            currMonth = 'MAR'
        elif (currentDate.month == 4):
            currMonth = 'APR'
        elif (currentDate.month == 5):
            currMonth = 'MAY'
        elif (currentDate.month == 6):
            currMonth = 'JUN'
        elif (currentDate.month == 7):
            currMonth = 'JUL'
        elif (currentDate.month == 8):
            currMonth = 'AUG'
        elif (currentDate.month == 9):
            currMonth = 'SEP'
        elif (currentDate.month == 10):
            currMonth = 'OCT'
        elif (currentDate.month == 11):
            currMonth = 'NOV'
        else:
            currMonth = 'DEC'

        currdate = str(currentDate.day) + ' ' + currMonth + ' ' + str(currentDate.year)

        emptyIndiDict = {}
        emptyFamDict = {}

        test2IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976'}}
        test3IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 3000'}}
        test4IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': currdate}}
        test5IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976',
                                 'DEAT': '11 OCT 1996'}}
        test6IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976',
                                 'DEAT': '11 OCT 3000'}}
        test7IndiDict = {'I01': {'ID': 'I01',
                                 'NAME': 'John Doe',
                                 'BIRT': '12 MAY 1976',
                                 'DEAT': currdate}}
        test8FamDict = {'F01': {'ID': 'F01',
                                'MARR': '12 MAY 1976',
                                'HUSB': 'I01',
                                'WIFE': 'I02'}}
        test9FamDict = {'F01': {'ID': 'F01',
                                'MARR': '12 MAY 3000',
                                'HUSB': 'I01',
                                'WIFE': 'I02'}}
        test10FamDict = {'F01': {'ID': 'F01',
                                 'MARR': currdate,
                                 'HUSB': 'I01',
                                 'WIFE': 'I02'}}
        test11FamDict = {'F01': {'ID': 'F01',
                                 'MARR': '12 MAY 1976',
                                 'DIV': '10 OCT 1977',
                                 'HUSB': 'I01',
                                 'WIFE': 'I02'}}
        test12FamDict = {'F01': {'ID': 'F01',
                                 'MARR': '12 MAY 1976',
                                 'DIV': '10 OCT 3000',
                                 'HUSB': 'I01',
                                 'WIFE': 'I02'}}
        test13FamDict = {'F01': {'ID': 'F01',
                                 'MARR': '12 MAY 1976',
                                 'DIV': currdate,
                                 'HUSB': 'I01',
                                 'WIFE': 'I02'}}

        test1 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, emptyFamDict)  # empty dictionary check
        test2 = GEDCOM_Project.checkDatesBeforeCurrentDate(test2IndiDict,
                                                           emptyFamDict)  # birthday is before current date
        test3 = GEDCOM_Project.checkDatesBeforeCurrentDate(test3IndiDict,
                                                           emptyFamDict)  # birthday is after current date
        test4 = GEDCOM_Project.checkDatesBeforeCurrentDate(test4IndiDict, emptyFamDict)  # birthday is on current date
        test5 = GEDCOM_Project.checkDatesBeforeCurrentDate(test5IndiDict, emptyFamDict)  # death is before current date
        test6 = GEDCOM_Project.checkDatesBeforeCurrentDate(test6IndiDict, emptyFamDict)  # death is after current date
        test7 = GEDCOM_Project.checkDatesBeforeCurrentDate(test7IndiDict, emptyFamDict)  # death is on current date
        test8 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test8FamDict)  # marr is before current date
        test9 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test9FamDict)  # marr is after current date
        test10 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test10FamDict)  # marr is on current date
        test11 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test11FamDict)  # div is before current date
        test12 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test12FamDict)  # div is after current date
        test13 = GEDCOM_Project.checkDatesBeforeCurrentDate(emptyIndiDict, test13FamDict)  # div is on current date

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True (current date is supposed to pass)
        self.assertTrue(test5)  # True
        self.assertFalse(test6)  # False
        self.assertTrue(test7)  # True (current date is supposed to pass)
        self.assertTrue(test8)  # True
        self.assertFalse(test9)  # False
        self.assertTrue(test10)  # True (current date is supposed to pass)
        self.assertTrue(test11)  # True
        self.assertFalse(test12)  # False
        self.assertTrue(test13)  # True (current date is supposed to pass)

    # US02 - test the checkBirthBeforeMarriage function
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

        test1 = GEDCOM_Project.checkBirthBeforeMarriage(test1IndiDict, test1FamDict)  # empty dictionary
        test2 = GEDCOM_Project.checkBirthBeforeMarriage(test2IndiDict,
                                                        test2FamDict)  # Husband birth date post-dates marriage date
        test3 = GEDCOM_Project.checkBirthBeforeMarriage(test3IndiDict,
                                                        test3FamDict)  # Wife birth date post-dates marriage date
        test4 = GEDCOM_Project.checkBirthBeforeMarriage(test4IndiDict,
                                                        test4FamDict)  # Husband and Wife birth dates post-date marriage date
        test5 = GEDCOM_Project.checkBirthBeforeMarriage(test5IndiDict, test5FamDict)  # Marriage date after birth dates
        test6 = GEDCOM_Project.checkBirthBeforeMarriage(test6IndiDict,
                                                        test6FamDict)  # Marriage after wife birth, before husb birth
        test7 = GEDCOM_Project.checkBirthBeforeMarriage(test7IndiDict,
                                                        test7FamDict)  # Marriage after husb birth, before wife birth

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertFalse(test3)  # False
        self.assertFalse(test4)  # False
        self.assertTrue(test5)  # True
        self.assertFalse(test6)  # False
        self.assertFalse(test7)  # False

    # US03 - test the checkBirthBeforeDeath function
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

        test1 = GEDCOM_Project.checkBirthBeforeDeath(test1Dict)  # empty dictionary
        test2 = GEDCOM_Project.checkBirthBeforeDeath(test2Dict)  # death date pre-dates birth date
        test3 = GEDCOM_Project.checkBirthBeforeDeath(test3Dict)  # 2 persons death date pre-dates birth date
        test4 = GEDCOM_Project.checkBirthBeforeDeath(test4Dict)  # birth date pre-dates death date
        test5 = GEDCOM_Project.checkBirthBeforeDeath(test5Dict)  # birth date is same as death date

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True
        self.assertTrue(test5)  # True

    # US04 - test the checkMarriageBeforeDivorce function
    def test_checkMarriageBeforeDivorce(self):

        test1Dict = {'F01': {'MARR': '13 MAY 1986'}}
        test2Dict = {'F01': {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1987'}}
        test3Dict = {'F01': {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1984'}}
        test4Dict = {'F01': {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1988'},
                     'F02': {'MARR': '20 SEP 1986', 'DIV': '13 JUN 1988'}}
        test5Dict = {'F01': {'MARR': '13 MAY 1986', 'DIV': '13 MAY 1988'},
                     'F02': {'MARR': '20 SEP 1986', 'DIV': '13 JUN 1978'}}
        test6Dict = {}

        test1 = GEDCOM_Project.checkMarriageBeforeDivorce(test1Dict)  # No divorce
        test2 = GEDCOM_Project.checkMarriageBeforeDivorce(test2Dict)  # Marriage before divorce
        test3 = GEDCOM_Project.checkMarriageBeforeDivorce(test3Dict)  # Marriage after divorce
        test4 = GEDCOM_Project.checkMarriageBeforeDivorce(test4Dict)  # Marriage before divorce second family
        test5 = GEDCOM_Project.checkMarriageBeforeDivorce(test5Dict)  # Marriage after divorce second family
        test6 = GEDCOM_Project.checkMarriageBeforeDivorce(test6Dict)  # Empty dict

        self.assertTrue(test1)  # No divorce, True
        self.assertTrue(test2)  # Marriage before divorce TRUE
        self.assertFalse(test3)  # Marriage after divorce FALSE
        self.assertTrue(test4)  # Marriage before divorce second family TRUE
        self.assertFalse(test5)  # Marriage after divorce second family FALSE
        self.assertTrue(test6)  # Empty dict TRUE

    # US05 - test the checkMarriageBeforeDeath function
    def test_checkMarriageBeforeDeath(self):

        testDictFam = {'F01': {'MARR': '13 MAY 1986', 'HUSB': 'I01', 'WIFE': 'I02'}}
        test1DictInd = {'I01': {'ID': 'I01', 'DEAT': '8 OCT 1993'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1993'}}
        test2DictInd = {'I01': {'ID': 'I01', 'DEAT': '8 OCT 1900'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1993'}}
        test3DictInd = {'I01': {'ID': 'I01', 'DEAT': '8 OCT 1993'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1900'}}
        test4DictInd = {}
        test5DictInd = {'I01': {'ID': 'I01', 'DEAT': '8 OCT 1900'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1900'}}
        test6DictInd = {'I01': {'ID': 'I01'},
                        'I02': {'ID': 'I02'}}

        test1 = GEDCOM_Project.checkMarriageBeforeDeath(test1DictInd, testDictFam)  # deaths after marriage
        test2 = GEDCOM_Project.checkMarriageBeforeDeath(test2DictInd,
                                                        testDictFam)  # husb death before, wife after marriage
        test3 = GEDCOM_Project.checkMarriageBeforeDeath(test3DictInd,
                                                        testDictFam)  # husb death after, wife before marriage
        test4 = GEDCOM_Project.checkMarriageBeforeDeath(test4DictInd, testDictFam)  # empty dict
        test5 = GEDCOM_Project.checkMarriageBeforeDeath(test5DictInd,
                                                        testDictFam)  # both husb and wife died before marriage
        test6 = GEDCOM_Project.checkMarriageBeforeDeath(test6DictInd, testDictFam)  # both husb and wife still alive

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True
        self.assertFalse(test5)  # False
        self.assertTrue(test6)  # True

    # US06 - test the checkDivorceBeforeDeath function
    def test_checkDivorceBeforeDeath(self):

        testDictFam = {'F01': {'DIV': '13 MAY 1986', 'HUSB': 'I01', 'WIFE': 'I02'}}
        test1DictInd = {'I01': {'ID': 'I01', 'DEAT': '1 JUN 1993'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1993'}}
        test2DictInd = {'I01': {'ID': 'I01', 'DEAT': '2 JUN 1900'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1993'}}
        test3DictInd = {'I01': {'ID': 'I01', 'DEAT': '3 JUN 1993'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1900'}}
        test4DictInd = {}
        test5DictInd = {'I01': {'ID': 'I01', 'DEAT': '5 JUN 1900'},
                        'I02': {'ID': 'I02', 'DEAT': '16 JUN 1900'}}
        test6DictInd = {'I01': {'ID': 'I01'},
                        'I02': {'ID': 'I02'}}

        test1 = GEDCOM_Project.checkDivorceBeforeDeath(test1DictInd, testDictFam)  # deaths after divorce
        test2 = GEDCOM_Project.checkDivorceBeforeDeath(test2DictInd,
                                                       testDictFam)  # husb death before, wife after divorce
        test3 = GEDCOM_Project.checkDivorceBeforeDeath(test3DictInd,
                                                       testDictFam)  # husb death after, wife before divorce
        test4 = GEDCOM_Project.checkDivorceBeforeDeath(test4DictInd, testDictFam)  # empty dict
        test5 = GEDCOM_Project.checkDivorceBeforeDeath(test5DictInd,
                                                       testDictFam)  # both husb and wife died before divorce
        test6 = GEDCOM_Project.checkDivorceBeforeDeath(test6DictInd, testDictFam)  # both husb and wife still alive

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True
        self.assertFalse(test5)  # False
        self.assertTrue(test6)  # True

    # US07 - test the checkLessThan150YearsOld function
    def test_checkLessThan150YearsOld(self):
        test1Dict = {}

        test2Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '19 JUN 1850',
                             'DEAT': '15 AUG 2006'}}

        test3Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '19 JUN 1906',
                             'DEAT': '15 AUG 1986'}}

        test4Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '12 MAY 1850'}}

        test5Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '12 MAY 1950'}}

        test6Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '19 JUN 1850',
                             'DEAT': '19 JUN 2000'}}

        test7Dict = {'I01': {'ID': 'I01',
                             'NAME': 'John Doe',
                             'BIRT': '24 JUN 1868',
                             'DEAT': '24 JUN 2018'}}

        test1 = GEDCOM_Project.checkLessThan150YearsOld(test1Dict)  # Empty dic
        test2 = GEDCOM_Project.checkLessThan150YearsOld(test2Dict)  # Death more than 150 years after birth
        test3 = GEDCOM_Project.checkLessThan150YearsOld(test3Dict)  # Death less than 150 years after birth
        test4 = GEDCOM_Project.checkLessThan150YearsOld(test4Dict)  # Person is alive and birth more than 150 years ago
        test5 = GEDCOM_Project.checkLessThan150YearsOld(test5Dict)  # Person is alive and birth less than 150 years ago
        test6 = GEDCOM_Project.checkLessThan150YearsOld(test6Dict)  # Person died at 150 years old
        test7 = GEDCOM_Project.checkLessThan150YearsOld(test7Dict)  # Person is exactly 150 years old

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertTrue(test3)  # True
        self.assertFalse(test4)  # False
        self.assertTrue(test5)  # True
        self.assertFalse(test6)  # False
        self.assertFalse(test7)  # False

    # US08 - test the checkBirthBeforeMarriageOfParents function
    def test_checkBirthBeforeMarriageOfParents(self):

        emptyDictFam = {}
        testDictFam = {'F01': {'MARR': '13 MAY 1986',
                               'DIV': '20 MAY 2012',
                               'HUSB': 'I01',
                               'WIFE': 'I02',
                               'CHIL': ['I03']}}
        testDictFam['F01']['CHIL'].append('I04')  # adding I04 to the family

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

        test1 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(emptyDictInd, emptyDictFam)  # empty dicts
        test2 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test2DictInd,
                                                                 testDictFam)  # both children born after marr (and within 9 months of div)
        test3 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test3DictInd,
                                                                 testDictFam)  # one child born before marr
        test4 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test4DictInd,
                                                                 testDictFam)  # both children born before marr
        test5 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test5DictInd,
                                                                 testDictFam)  # one child born on date of marr (still false)
        test6 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test6DictInd,
                                                                 testDictFam)  # one child born after 9 months of div
        test7 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test7DictInd,
                                                                 testDictFam)  # both child born after 9 months of div
        test8 = GEDCOM_Project.checkBirthBeforeMarriageOfParents(test8DictInd,
                                                                 testDictFam)  # one child born 9 months after div

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False
        self.assertFalse(test6)  # False
        self.assertFalse(test7)  # False
        self.assertTrue(test8)  # True

    # US09 - test the checkBirthBeforeDeathOfParents function
    def test_checkBirthBeforeDeathOfParents(self):
        emptyDictFam = {}
        testDictFam = {'F01': {'MARR': '13 MAY 1986',
                               'HUSB': 'I01',
                               'WIFE': 'I02',
                               'CHIL': ['I03']}}
        testDictFam['F01']['CHIL'].append('I04')  # adding I04 to the family

        emptyDictInd = {}
        test2DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 MAY 1996',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test3DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'DEAT': '15 NOV 2031',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 MAY 1996',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test4DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '14 DEC 2035',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test5DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '14 DEC 2035',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '15 DEC 2036',
                                'FAMC': 'F01'}}
        test6DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 DEC 2035',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test7DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '14 FEB 2036',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test8DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '14 FEB 2037',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}
        test9DictInd = {'I01': {'ID': 'I01',
                                'NAME': 'Ed Doe',
                                'BIRT': '10 OCT 1970',
                                'DEAT': '13 DEC 2035',
                                'FAMS': 'F01'},
                        'I02': {'ID': 'I02',
                                'NAME': 'Karen Doe',
                                'BIRT': '16 JUN 1971',
                                'FAMS': 'F01'},
                        'I03': {'ID': 'I03',
                                'NAME': 'John Doe',
                                'BIRT': '13 SEP 2036',
                                'FAMC': 'F01'},
                        'I04': {'ID': 'I04',
                                'NAME': 'Jane Doe',
                                'BIRT': '25 MAY 1998',
                                'FAMC': 'F01'}}

        test1 = GEDCOM_Project.checkBirthBeforeDeathOfParents(emptyDictInd, emptyDictFam)  # empty dicts
        test2 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test2DictInd, testDictFam)  # parents are alive
        test3 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test3DictInd,
                                                              testDictFam)  # both kids are born well before their parents deaths
        test4 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test4DictInd,
                                                              testDictFam)  # one kid is born after mother's death date
        test5 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test5DictInd,
                                                              testDictFam)  # both kids are born after mother's death date
        test6 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test6DictInd,
                                                              testDictFam)  # one kid is born on the date of his mothers death
        test7 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test7DictInd,
                                                              testDictFam)  # one kid is born after -9months of father's death date
        test7 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test7DictInd,
                                                              testDictFam)  # one kid is born after father's death, but not more than 9 months after
        test8 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test8DictInd,
                                                              testDictFam)  # one kid is born after +9months of father's death
        test9 = GEDCOM_Project.checkBirthBeforeDeathOfParents(test9DictInd,
                                                              testDictFam)  # one kid is born on the +9months date of father's death

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertTrue(test3)  # True
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False
        self.assertFalse(test6)  # False
        self.assertTrue(test7)  # True
        self.assertFalse(test8)  # False
        self.assertFalse(test9)  # False

    # US10 - test the checkMarriageAfter14 function
    def test_checkMarriageAfter14(self):
        testDictFam = {'F01': {'MARR': '13 MAY 1986', 'HUSB': 'I01', 'WIFE': 'I02'}}
        test1DictInd = {'I01': {'ID': 'I01', 'BIRT': '1 JUN 1900'},
                        'I02': {'ID': 'I02', 'BIRT': '1 MAY 1900'}}
        test2DictInd = {'I01': {'ID': 'I01', 'BIRT': '2 JUN 1980'},
                        'I02': {'ID': 'I02', 'BIRT': '2 MAY 1900'}}
        test3DictInd = {'I01': {'ID': 'I01', 'BIRT': '3 JUN 1900'},
                        'I02': {'ID': 'I02', 'BIRT': '3 MAY 1980'}}
        test4DictInd = {}
        test5DictInd = {'I01': {'ID': 'I01', 'BIRT': '5 JUN 1980'},
                        'I02': {'ID': 'I02', 'BIRT': '5 MAY 1980'}}
        test6DictInd = {'I01': {'ID': 'I01', 'BIRT': '13 MAY 1972'},
                        'I02': {'ID': 'I02', 'BIRT': '13 MAY 1972'}}

        test1 = GEDCOM_Project.checkMarriageAfter14(test1DictInd, testDictFam)  # Both older than 14
        test2 = GEDCOM_Project.checkMarriageAfter14(test2DictInd, testDictFam)  # husband too young, wife okay
        test3 = GEDCOM_Project.checkMarriageAfter14(test3DictInd, testDictFam)  # wife too young husband okay
        test4 = GEDCOM_Project.checkMarriageAfter14(test4DictInd, testDictFam)  # empty dict
        test5 = GEDCOM_Project.checkMarriageAfter14(test5DictInd, testDictFam)  # both too young
        test6 = GEDCOM_Project.checkMarriageAfter14(test6DictInd, testDictFam)  # both are on 14th bday

        self.assertTrue(test1)  # True
        self.assertFalse(test2)  # False
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True
        self.assertFalse(test5)  # False
        self.assertTrue(test6)  # True

    # US12 test to check that mother and father aren't too old
    def test_checkParentsNotTooOld(self):
        test1fam = {}
        test1ind = {}

        test2fam = {'F01': {'HUSB': 'I01',
                            'WIFE': 'I02',
                            'CHIL': ['I03', 'I04']}}
        test2ind = {'I01': {'BIRT': '01 JAN 1920'},
                    'I02': {'BIRT': '01 JAN 1930'},
                    'I03': {'BIRT': '02 FEB 1952'},
                    'I04': {'BIRT': '02 FEB 1953'}}
        test3ind = {'I01': {'BIRT': '01 JAN 1920'},
                    'I02': {'BIRT': '01 JAN 1930'},
                    'I03': {'BIRT': '02 FEB 1990'},
                    'I04': {'BIRT': '02 FEB 1953'}}
        test4ind = {'I01': {'BIRT': '01 JAN 1910'},
                    'I02': {'BIRT': '01 JAN 1950'},
                    'I03': {'BIRT': '02 FEB 2000'},
                    'I04': {'BIRT': '02 FEB 1953'}}
        test5ind = {'I01': {'BIRT': '01 JAN 1920'},
                    'I02': {'BIRT': '01 JAN 1930'},
                    'I03': {'BIRT': '02 FEB 1931'},
                    'I04': {'BIRT': '02 FEB 2014'}}
        test6ind = {'I01': {'BIRT': '01 FEB 1900'},
                    'I02': {'BIRT': '01 FEB 1920'},
                    'I03': {'BIRT': '01 FEB 1950'},
                    'I04': {'BIRT': '01 FEB 1980'}}

        test1 = GEDCOM_Project.checkParentsNotTooOld(test1fam,
                                                     test1ind)  # Empty family and individuals, should pass true
        test2 = GEDCOM_Project.checkParentsNotTooOld(test2fam, test2ind)  # Neither parent is too old, should pass true
        test3 = GEDCOM_Project.checkParentsNotTooOld(test2fam, test3ind)  # Just the mom is too old
        test4 = GEDCOM_Project.checkParentsNotTooOld(test2fam, test4ind)  # Just the dad is too old
        test5 = GEDCOM_Project.checkParentsNotTooOld(test2fam, test5ind)  # Both parents are too old
        test6 = GEDCOM_Project.checkParentsNotTooOld(test2fam, test6ind)  # mom is exactly 60 years older, dad is exactly 80 years older

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False
        self.assertFalse(test6)  # False

    # US15 test check for greater than 15 siblings
    def test_checkFewerThan15Siblings(self):
        test1dic = {}  # Empty dictionary
        test2dic = {'F01': {'ID': 'F01'}}  # Tests family with 0 children
        test3dic = {'F01': {
            'CHIL': ['I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I14',
                     'I15']}}  # Tests family with 14 children
        test4dic = {'F01': {
            'CHIL': ['I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I14', 'I15',
                     'I16']}}  # Tests family with 15 children
        test5dic = {'F01': {
            'CHIL': ['I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I14', 'I15',
                     'I16', 'I17']}}  # Tests family with 16 children

        test1 = GEDCOM_Project.checkFewerThan15Siblings(test1dic)  # Empty dict
        test2 = GEDCOM_Project.checkFewerThan15Siblings(test2dic)  # 0 siblings
        test3 = GEDCOM_Project.checkFewerThan15Siblings(test3dic)  # 14 siblings
        test4 = GEDCOM_Project.checkFewerThan15Siblings(test4dic)  # 15 siblings
        test5 = GEDCOM_Project.checkFewerThan15Siblings(test5dic)  # 16 siblings

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertTrue(test3)  # True
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False

    # US18 - test the checkSiblingsShouldNotMarry function
    def test_checkSiblingsShouldNotMarry(self):
        self.assertTrue(True)  # True

    # US21 - test the checkCorrectGenderForRole function
    def test_checkCorrectGenderForRole(self):
        self.assertTrue(True)  # True

    # US22 - test the checkUniqueIDs funciton
    def test_checkUniqueIDs(self):
        test1Dict = {}
        test2Dict = {'I01': 'John Doe',
                     'I02': 'Jane Doe'}
        test3Dict = {'I01': 'John Doe',
                     'I02': 'Jane Doe',
                     'I03': 'Jake Doe'}

        test1 = GEDCOM_Project.checkUniqueIDs('I03', test1Dict)  # empty dictionary
        test2 = GEDCOM_Project.checkUniqueIDs('I03', test2Dict)  # unique IDs
        test3 = GEDCOM_Project.checkUniqueIDs('I03', test3Dict)  # not unique IDs

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False

    # US23 - test the checkUniqueNameAndBirthDate function
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

        test1 = GEDCOM_Project.checkUniqueNameAndBirthDate(test1Dict)  # empty dictionary
        test2 = GEDCOM_Project.checkUniqueNameAndBirthDate(test2Dict)  # no one has the same bday and name
        test3 = GEDCOM_Project.checkUniqueNameAndBirthDate(test3Dict)  # name and bday both match
        test4 = GEDCOM_Project.checkUniqueNameAndBirthDate(test4Dict)  # name matches, bday does not match
        test5 = GEDCOM_Project.checkUniqueNameAndBirthDate(test5Dict)  # name does not match, bday does match

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False
        self.assertTrue(test4)  # True
        self.assertTrue(test5)  # True

    # US24 - Tests checkUniqueFamiliesBySpouses function
    # Tests if there exists more than one family with the same spouses by name and marriage date
    def test_checkUniqueFamiliesBySpouses(self):
        # Test case for different families with different everything
        test1dic = {'F01': {'MARR': '13 MAY 1986',
                            'WIFE': 'I14',
                            'HUSB': 'I01'},
                    'F02': {'MARR': '14 JUNE 2002',
                            'WIFE': 'I11',
                            'HUSB': 'I02'}}

        # Tests empty dictionary case
        test2dic = {}

        # Test case for same marriage date but different spouses, should still be true
        test3dic = {'F04': {'MARR': '12 NOV 1999',
                            'WIFE': 'I05',
                            'HUSB': 'I03'},
                    'F05': {'MARR': '12 NOV 1999',
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

        test1 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test1dic)  # Valid family
        test2 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test2dic)  # Empty dictionary
        test3 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test3dic)  # Same marriage date but different spouses
        test4 = GEDCOM_Project.checkUniqueFamiliesBySpouses(
            test4dic)  # Families with identical spouses and marriage date false
        test5 = GEDCOM_Project.checkUniqueFamiliesBySpouses(
            test5dic)  # Families with identical spouses and marriage date one without false
        test6 = GEDCOM_Project.checkUniqueFamiliesBySpouses(
            test6dic)  # Same husband + wife and different date (divorced and remarried)
        test7 = GEDCOM_Project.checkUniqueFamiliesBySpouses(test7dic)  # husband marries two wives on same day

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertTrue(test3)  # True
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False
        self.assertTrue(test6)  # True
        self.assertTrue(test7)  # True

    # US25 - Tests checkUniqueFirstNamesInFamilies function
    # Tests if there is no more than one child with the same name and birth date in a family
    def test_checkUniqueFirstNamesInFamilies(self):

        test1famdic = {}  # Empty dictionary
        test1indidic = {}  # Empty dictionary

        test2famdic = {'F01': {'CHIL': ['I01']}}  # One child in family
        test2indidic = {'I01': {'NAME': 'Jack /Daniels/',  # Checks against list of individuals
                                'BIRT': '05 NOV 2001'}}

        test3famdic = {'F01': {'CHIL': ['I01', 'I02']},  # Two families with kids of all different names
                       'F02': {'CHIL': ['I03', 'I04']}}
        test3indidic = {'I01': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I02': {'NAME': 'Tyrone /Willis/',
                                'BIRT': '02 JUN 2001'},
                        'I03': {'NAME': 'Daron /Bonfooboo/',
                                'BIRT': '01 JAN 1999'},
                        'I04': {'NAME': 'John /Fosho/',
                                'BIRT': '22 NOV 1994'}}

        test4famdic = {'F01': {'CHIL': ['I01', 'I02']}}  # Tests false for two kids with same name and birth date
        test4indidic = {'I01': {'NAME': 'Michael /Flin/',
                                'BIRT': '04 NOV 1995'},
                        'I02': {'NAME': 'Michael /Flin/',
                                'BIRT': '04 NOV 1995'}}

        test5famdic = {'F01': {'CHIL': ['I01', 'I02']},
                       # Tests true for two different families with kids of same name and birthday
                       'F02': {'CHIL': ['I03', 'I04']}}
        test5indidic = {'I01': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I02': {'NAME': 'Tyrone /Willis/',
                                'BIRT': '02 JUN 2001'},
                        'I03': {'NAME': 'Taco /Salad/',
                                'BIRT': '05 JUN 2002'},
                        'I04': {'NAME': 'John /Fosho/',
                                'BIRT': '22 NOV 1994'}}

        test1 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test1indidic, test1famdic)  # Empty dictionaries
        test2 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test2indidic,
                                                               test2famdic)  # Two families with children of different names and birthday
        test3 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test3indidic,
                                                               test3famdic)  # One family with two children of same name
        test4 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test4indidic,
                                                               test4famdic)  # Two kids with same name and birthday in same family
        test5 = GEDCOM_Project.checkUniqueFirstNamesInFamilies(test5indidic,
                                                               test5famdic)  # Two different families with kids of same name and birthday

        self.assertTrue(test1)  # True
        self.assertTrue(test2)  # True
        self.assertTrue(test3)  # True
        self.assertFalse(test4)  # False
        self.assertTrue(test5)  # True

    # US27 - Tests listIndividualAges function
    def test_listIndividualAges(self):
        test1indidic = {}
        expected1 = [['Individual', 'Age']]
        
        test2indidic = {'I01': {'NAME': 'John /Doe/',
                                'BIRT': '08 OCT 1993'},
                        'I02': {'NAME': 'Jane /Doe/',
                                'BIRT': '16 JUN 1993'}}
        expected2 = [['Individual', 'Age'],
                    ['John /Doe/', 24],
                    ['Jane /Doe/', 25]]
        
        test3indidic = {'I01': {'NAME': 'John /Doe/',
                                'BIRT': '08 OCT 1993'},
                        'I02': {'NAME': 'Jane /Doe/',
                                'BIRT': '16 JUN 1993'},
                        'I04': {'NAME': 'Bob /Smith/',
                                'BIRT': '16 JUN 1993',
                                'DEAT': '20 JUN 2003'},
                        'I03': {'NAME': 'Sam /Doe/',
                                'BIRT': '16 JUN 2000'}}
        expected3 = [['Individual', 'Age'],
                    ['John /Doe/', 24],
                    ['Jane /Doe/', 25],
                    ['Sam /Doe/', 18],
                    ['Bob /Smith/', 10]]

        self.assertEqual(GEDCOM_Project.listIndividualAges(collections.OrderedDict(sorted(test1indidic.items()))), expected1) #empty dict
        self.assertEqual(GEDCOM_Project.listIndividualAges(collections.OrderedDict(sorted(test2indidic.items()))), expected2) #in order, all alive
        self.assertEqual(GEDCOM_Project.listIndividualAges(collections.OrderedDict(sorted(test3indidic.items()))), expected3) #not in order, not all alive

    # US29 - Tests listDeceased function
    def test_listDeceased(self):
        expected = [['Header1', 'Header2', 'Header3'],
                    ['Data1', 'Data2', 'Data3']]
        self.assertEqual(expected, GEDCOM_Project.listDeceased())

    # US30 - Tests listLivingMarried function
    def test_listLivingMarried(self):
        expected = [['Header1', 'Header2', 'Header3'],
                    ['Data1', 'Data2', 'Data3']]
        self.assertEqual(expected, GEDCOM_Project.listLivingMarried())

    # US35 - Tests listRecentBirths function
    def test_listRecentBirths(self):
        expected = [['Header1', 'Header2', 'Header3'],
                    ['Data1', 'Data2', 'Data3']]
        self.assertEqual(expected, GEDCOM_Project.listRecentBirths())

    # US36 - Tests listRecentDeaths function
    def test_listRecentDeaths(self):
        expected = [['Header1', 'Header2', 'Header3'],
                    ['Data1', 'Data2', 'Data3']]
        self.assertEqual(expected, GEDCOM_Project.listRecentDeaths())

    # US42 - test the checkIllegitimateDate function
    def test_checkIllegitimateDate(self):
        test1date = []
        test2date = ['30','JUN','2015']
        test3date = ['35','JUN','2015']
        test4date = ['-1','JUN','2015']
        test5date = ['29','FEB','2015']
        test6date = ['29','FEB','2012']
        test7date = ['30','JUN','0']
        test8date = ['30','JUN','-1']
        test9date = ['30','JUNE','2015']
        
        test1 = GEDCOM_Project.checkIllegitimateDate(test1date, 1)  # empty date
        test2 = GEDCOM_Project.checkIllegitimateDate(test2date, 1)  # valid date
        test3 = GEDCOM_Project.checkIllegitimateDate(test3date, 1)  # invalid day - over limit
        test4 = GEDCOM_Project.checkIllegitimateDate(test4date, 1)  # invalid day - neg
        test5 = GEDCOM_Project.checkIllegitimateDate(test5date, 1)  # invalid day - not a leap year
        test6 = GEDCOM_Project.checkIllegitimateDate(test6date, 1)  # valid day - leap year
        test7 = GEDCOM_Project.checkIllegitimateDate(test7date, 1)  # invalid year - 0
        test8 = GEDCOM_Project.checkIllegitimateDate(test8date, 1)  # invalid year - neg
        test9 = GEDCOM_Project.checkIllegitimateDate(test9date, 1)  # invalid month

        self.assertFalse(test1)  # False
        self.assertTrue(test2)  # True
        self.assertFalse(test3)  # False
        self.assertFalse(test4)  # False
        self.assertFalse(test5)  # False
        self.assertTrue(test6)  # True
        self.assertFalse(test7)  # False
        self.assertFalse(test8)  # False
        self.assertFalse(test9)  # False

if __name__ == '__main__':
    resultFile = 'Test_Results.txt'
    try:
        f = open(resultFile, "w")
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
        f.close()
    except IOError:
        print 'Error! Cannot open', resultFile
