import spacy
nlp = spacy.load("en_core_web_sm")


def test_spacy():
    text = "Hello, one day I walked into the jungle."
    doc = nlp(text)
    words = []
    for token in doc:
        words.append(token.text)

    assert ['Hello', ',', 'one', 'day', 'I', 'walked', 'into', 'the', 'jungle', '.'] == words
