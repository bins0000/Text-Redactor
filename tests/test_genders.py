import sys
sys.path.append('..')
from project1 import main

def test_genders():
    testText = "Does he like her? Is she an actress?"
    expectedResult = "Does █████████ like █████████? Is █████████ an █████████?"
    redatedText = main.genderRedactor(testText)

    assert expectedResult == redatedText
