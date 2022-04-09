# This test is to test if my nameRedactor function
import re
import spacy
nlp = spacy.load("en_core_web_sm")

def test_names():
    testText = "I met John a while ago. Everyday, Nash goes jogging."
    expectedResult = "I met █████████ a while ago. Everyday, █████████ goes jogging."
    
    nameRedaction = []
    document = nlp(testText)
    for token in document:
        if (token.ent_type_ == 'PERSON'):     # redacting 'name' token that was categorized as PERSON by SpaCy
            nameRedaction.append(token.text)
        elif (token.ent_type_ == 'GPE'):      # redacting 'location' token that was categorized as GPE by SpaCy
            nameRedaction.append(token.text)


    for token in nameRedaction:
        testText = re.sub(rf"\b(?=\w){token}\b(?!\w)", '█████████', testText)

    assert expectedResult == testText

