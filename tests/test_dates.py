import sys
sys.path.append('.')
from project1 import main

def test_dates():
    testText = "Today is a sunny day. However, tomorrow is Aug 20, 2022 and it will rain."
    expectedResult = "█████████ is a sunny day. However, █████████ is █████████ and it will rain."
    redactedText = main.dateRedactor(testText)
    redactedText = redactedText[0]


    assert expectedResult == redactedText
