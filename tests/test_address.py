import sys
sys.path.append('..')
from project1 import main

def test_address():
    testText = "I don't live at 5990 Ginnie Street, Norman, OK, 12345."
    expectedResult = "I don't live at █████████."
    redactedText = main.addressRedactor(testText)


    assert expectedResult == redactedText
