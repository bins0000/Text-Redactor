import sys
sys.path.append('.')
from project1 import main

def test_phones():
    testText = "405-897-5589.  281/932-5145.   +39-06-3600-4741.    485 698 4578"
    expectedResult = "█████████.  █████████.   █████████.    █████████"
    redatedText = main.phoneRedactor(testText)
    redatedText = redatedText[0]

    assert expectedResult == redatedText
