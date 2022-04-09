import sys
sys.path.append('..')
from project1 import main

def test_concepts():
    testText = "I will visit a prison tomorrow. Will you come with? How about you kids go eat something at home."
    expectedResult = "█████████ Will you come with? █████████"
    redatedConcept = main.conceptRedactor(testText, ['prisons', 'kids'])

    assert expectedResult == redatedConcept
