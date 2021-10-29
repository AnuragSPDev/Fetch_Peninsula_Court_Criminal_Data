import pytest
from . import Criminal_Data

'''
Global list to contain scrapped data
'''
data = []

'''
Creating a fixture to make a call to the website and store resulant list 
into global data list
'''
@pytest.fixture
def setup():
    global data
    data = Criminal_Data.get_criminal_data()

'''
Test case to verify the data should not be empty
'''
def test_listNotEmpty(setup):
    global data
    assert len(data) != 0

'''
Test case to verify data 
'''
def test_lengthOfRows(setup):
    global data
    assert 11 == len(data)

'''
Test case to verify docket number of the first record
'''
def test_firstDocketNumber(setup):
    global data
    assert data[0]['DocketNumber'] == 'CP-67-CR-0007273-2009'

'''
Test case to verify docket number of the last record
'''
def test_lastDocketNumber(setup):
    global data
    assert data[10]['DocketNumber'] == 'MJ-19301-CR-0000360-2013'

'''
Negative test case to verify docket number of the second record
'''
def test_negativeTestSecondDocketNumber(setup):
    global data
    assert data[1]['DocketNumber'] != 'MJ-19301-CR-0000360-2013'