# Dependencies
import os     # for enumerating directories
import nltk   # for NER
nltk.download('wordnet')
nltk.download('omw-1.4')
import spacy  # for NER
import re     # for regular expressions 
import glob   # for choosing file that can be accepted
from email.parser import Parser #  For opening the Emails using email parser
from nltk.stem import WordNetLemmatizer # lemmatizer
from nltk.corpus import wordnet # for synonyms set
import sys    # for writing stderr

# spacy - load nlp
nlp = spacy.load("en_core_web_md")

# Stats
# have some objects to keep track of redaction, a list in this case
locationRedaction = []
genderRedaction = []
emailprefRedaction = []
addressRedaction = []
# conceptsSentsList is to keep the sentences to be redacted
conceptsSentsList = []



# namesList contains the most 300 names each for male and female to catch the names that spacy does not catch
with open(os.getcwd()+'/project1/common_names.txt', 'r') as f2:  #input the names from common_names.txt
    names = f2.read()
    namesList = re.split(", ", names)

def main(input_ext, input_concepts, output_path, names_flag, dates_flag, genders_flag, phones_flag, address_flag, stats_type):
    
    # input
    globInput = input_ext
    for globType in globInput:
        #glob
        for file in glob.glob(f'*/emails/{globType}'):
        #for file in glob.glob(''):
            # opening a file into str object 'data'
            with open(file, "r") as f:
                data = f.read()
            f.close()
            
            # file name to be used for writing
            fileName = os.path.basename(file)
            
            #stats - stdOut
            stdOut = (f"stdout for {fileName}: \n")
            stdErr = (f"stderr for {fileName}: \n")

            if names_flag:
                # redact email prefixes
                data = emailPrefixRedactor(data)
                # stats
                stdOut += (f"{len(emailprefRedaction)} email prefix(s) redacted.\n")
                if len(emailprefRedaction) == 0:
                    stdErr += "0 email prefix redacted.\n"

            if input_concepts:
                # redact concepts
                data = conceptRedactor(data, input_concepts)
                # stats
                stdOut += (f"{len(conceptsSentsList)} sentence(s) containg concepts redacted.\n")
                if len(conceptsSentsList) == 0:
                    stdErr += "0 sentence containg concepts redacted.\n"

            if address_flag:
                # redact addresses
                data = addressRedactor(data)
                # stats
                stdOut += (f"{len(addressRedaction)} address(es) redacted.\n")
                if len(addressRedaction) == 0:
                    stdErr += "0 address redacted.\n"

            if names_flag:
                # redact names
                #nameRedaction = []
                data = nameRedactor(data)
                nameRedaction = data[1]
                data = data[0]
                # stats
                stdOut += (f"{len(nameRedaction)} name(s) redacted.\n")
                if len(nameRedaction) == 0:
                    stdErr += "0 name redacted.\n"

            if genders_flag:
                # redact gender specific terms
                data = genderRedactor(data)
                # stats
                stdOut += (f"{len(genderRedaction)} gender specific term(s) redacted.\n")
                if len(genderRedaction) == 0:
                    stdErr += "0 gender specific term redacted.\n"
        
            if phones_flag:
                # redact phone numbers
                data = phoneRedactor(data)
                phoneRedaction = data[1]
                data = data[0]
                # stats
                stdOut += (f"{len(phoneRedaction)} phone number(s) redacted.\n")
                if len(phoneRedaction) == 0:
                    stdErr += "0 phone number redacted.\n"
        
            if dates_flag:
                # redact dates
                data = dateRedactor(data)
                dateRedaction = data[1]
                data = data[0]
                # stats
                stdOut += (f"{len(dateRedaction)} date(s) redacted.\n")
                if len(dateRedaction) == 0:
                    stdErr += "0 date redacted.\n"
    
            
            # stats
            if stats_type == 'stdout':
                print(stdOut)
            elif stats_type == 'stderr':
                sys.stderr.write(stdErr)
            else:
                statPath = (f"./{output_path}/{stats_type}")
                os.makedirs(os.path.dirname(output_path), exist_ok=True) # to create the folder if not exist
                with open (statPath, 'a', encoding="utf-8") as s:
                    s.write(stdOut + "\n")
                    s.write(f"\nRedacted Terms for {fileName}\n")
                    if names_flag:
                        s.write(f"Redacted names are: ")
                        for name in nameRedaction:
                            s.write(f"{name}, ")
                        s.write("\n")
                        s.write(f"Redacted email prefixes are: ")
                        for name in emailprefRedaction:
                            s.write(f"{name}, ")
                        s.write("\n")
                    if input_concepts:
                        s.write(f"Redacted sentences (containing concepts) are: ")
                        for sentence in conceptsSentsList:
                            s.write(f"{sentence}, ")
                        s.write("\n")
                    if address_flag:
                        s.write(f"Redacted addresses are: ")
                        for address in addressRedaction:
                            s.write(f"{address}, ")
                        s.write("\n")
                    if genders_flag:
                        s.write(f"Redacted gender specific terms are: ")
                        for term in genderRedaction:
                            s.write(f"{term}, ")
                        s.write("\n")
                    if phones_flag:
                        s.write(f"Redacted phone numbers are: ")
                        for num in phoneRedaction:
                            s.write(f"{num}, ")
                        s.write("\n")
                    if dates_flag:
                        s.write(f"Redacted dates are: ")
                        for date in dateRedaction:
                            s.write(f"{date}, ")
                        s.write("\n\n")

                    s.close()

    
            # output
            os.makedirs(os.path.dirname(output_path), exist_ok=True) # to create the folder if not exist
            output = open("./"+output_path + fileName + ".redacted", "w", encoding="utf-8")
            output.write(data)
            output.close()

def dateRedactor(data):
    # regex for dates
    dateregex = re.compile(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}|[\d]{1,2}-[\d]{1,2}-[\d]{2}|[\d]{1,2} [ADFJMNOS]\w* [\d]{4}|[\d]{1,2} [ADFJMNOS]\w* [\d]{4}")
    dayregex = re.compile(r"monday|tuesday|thursday|wednesday|friday|saturday|sunday|mon(\s|,)|tue(\s|,)|thu(\s|,)|wed(\s|,)|fri(\s|,)|sat(\s|,)|sun(\s|,)|today|tomorrow|yesterday", re.IGNORECASE)
    # from commonregex.py
    date = re.compile('(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}', re.IGNORECASE)
    time = re.compile('\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?', re.IGNORECASE)

    # stats for dates
    dateRedaction = re.findall(date, data)
    dateRedaction += re.findall(dayregex, data)

    # dates redaction on data
    data = re.sub(date, '█████████', data)
    data = re.sub(dayregex, '█████████', data)

    return(data, dateRedaction)  

    
def phoneRedactor(data):
    
    # regex for phone numbers
    phoneregex = re.compile(r"(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3} | (?:\+?\(?\d{2,3}?\)?\D?)?\d{4}\D?\d{4} | (?:\+\d{2})?\D?\d{2}\D?\d{4}\D?\d{4} | (?:\+\d{1,2})?\D?\d{2,3}\D?\d{3,4}\D?\d{3,4}")
    phoneregex2 = re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
    # from commonregex.py
    phone = re.compile('''((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))''')
    phones_with_exts = re.compile('((?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?(?:[2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?(?:[0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(?:\d+)?))', re.IGNORECASE)

    # find all the phone numbers in the text
    match1 = re.findall(phone, data)
    match2 = re.findall(phones_with_exts, data)
    match3 = re.findall(phoneregex, data)
    match4 = re.findall(phoneregex2, data)

    # combine the phone number founds from each regex
    matchCut = list(set(match1 + match2 + match3 + match4))

    # remove the numbers that are the substring of the same number
    for i in range(len(matchCut)):
        for j in range(i + 1, len(matchCut)):
            if matchCut[i] in matchCut[j]:
                matchCut[i] = matchCut[j]
            elif matchCut[j] in matchCut[i]:
                matchCut[j] = matchCut[i]

    # remove duplicates
    matchRedaction = []
    for word in matchCut:
        if word not in matchRedaction:
            matchRedaction.append(word)

    # strip the leading and trailing whitespaces
    for i in range(len(matchRedaction)):
        matchRedaction[i] = matchRedaction[i].strip()


    phoneRedaction = matchRedaction
    # redact phone numbers
    for token in phoneRedaction:
        data = data.replace(token, '█████████')

    return (data, phoneRedaction)
    
    
def genderRedactor(data):
    # flags for genders
    genderFlags = ['he','him','his','she','her','hers','male','female','man','woman', 'father', 'mother', 'boy', 'girl', 'uncle', 'aunt', 'aunty', 'auntie', 'husband', 'wife', 'actor', 'actress', 'prince', 'princess', 'waiter', 'waitress', 'lady', 'gentleman', 'grandfather', 'grandmother', 'steward', 'stewardess', 'host', 'hostess', 'girlfriend', 'boyfriend', 'daughter', 'son', 'king', 'queen']
    # lemmatizer
    lemmatizer = WordNetLemmatizer()
    # a list to store redacted gender specific terms
    #nameRedaction = []
    # Opening the Emails using email parser
    emailData = Parser().parsestr(data)
    # get the headers of the email
    headers = emailData.items()
    # since, it is in a dictionary-like list, each key and value are joined to become a string with ': ' in between them
    for i in range(len(headers)):
        #str = ""
        delim = ': '
        header = delim.join(headers[i])
        #print(header)
        headers[i] = header
    # get the body string of the email
    body = emailData.get_payload(i=None, decode=False)
    # split the body string into a list separated by empty line(s) -- because some sentences are not stopped by SpaCy over empty lines
    bodySplitted = re.split("\n\n", body)
    # collects redaction in headers list
    for sentence in headers:
        document = nlp(sentence)
        for token in document:
            if (lemmatizer.lemmatize(token.text.lower()) in genderFlags):     # redacting the gender terms that could be caught by items in genderFlags
                genderRedaction.append(token.text)
    # collects redaction in body list
    for sentence in bodySplitted:
        document = nlp(sentence)
        for token in document:
            if (lemmatizer.lemmatize(token.text.lower()) in genderFlags):     # redacting the gender terms that could be caught by items in genderFlags
                genderRedaction.append(token.text)
    # using re.sub()
    for token in genderRedaction:
        data = re.sub(rf"\b(?=\w){token}\b(?!\w)", '█████████', data)
    return (data)
    
    
def nameRedactor(data):
    # a list to store redacted names
    nameRedaction = []
    # Opening the Emails using email parser
    emailData = Parser().parsestr(data)
    # get the headers of the email
    headers = emailData.items()
    # since, it is in a dictionary-like list, each key and value are joined to become a string with ': ' in between them
    for i in range(len(headers)):
        #str = ""
        delim = ': '
        header = delim.join(headers[i])
        #print(header)
        headers[i] = header
    #headers

    # get the body string of the email
    body = emailData.get_payload(i=None, decode=False)
    #print(body)
    # split the body string into a list separated by empty line(s) -- because some sentences are not stopped by SpaCy over empty lines
    bodySplitted = re.split("\n\n", body)
    #bodySplitted
    # collects redaction in headers list
    for sentence in headers:
        document = nlp(sentence)
        for token in document:
            if (token.ent_type_ == 'PERSON'):     # redacting 'name' token that was categorized as PERSON by SpaCy
                nameRedaction.append(token.text)
            elif (token.text in namesList):       # redacting the leftover names that could be caught by namesList
                nameRedaction.append(token.text)
            elif (token.ent_type_ == 'GPE'):      # redacting 'location' token that was categorized as GPE by SpaCy
                locationRedaction.append(token.text)
    # collects redaction in body list
    for sentence in bodySplitted:
        document = nlp(sentence)
        for token in document:
            if (token.ent_type_ == 'PERSON'):     # redacting 'name' token that was categorized as PERSON by SpaCy
                nameRedaction.append(token.text)
            elif (token.text in namesList):       # redacting the leftover names that could be caught by namesList
                nameRedaction.append(token.text)
            elif (token.ent_type_ == 'GPE'):      # redacting 'location' token that was categorized as GPE by SpaCy
                locationRedaction.append(token.text)
    # removing "'s'" and "\n"
    nameRedaction = [x for x in nameRedaction if x != "'s"]
    nameRedaction = [x for x in nameRedaction if x != "\n"]
    
    # using re.sub()
    for token in nameRedaction:
        data = re.sub(rf"\b(?=\w){token}\b(?!\w)", '█████████', data)
    for token in locationRedaction:
        data = re.sub(rf"\b(?=\w){token}\b(?!\w)", '█████████', data)
    return (data, nameRedaction)
    
    
def addressRedactor(data):
    # regex for address
    addressregex = re.compile('\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)', re.IGNORECASE)
    city_stateregex = re.compile(r"((?i)\d+((?!\d+).)*(AL|AK|AS|AZ|AR|CA|CO|CT|DE|DC|FM|FL|GA|GU|HI|ID|IL|IN|IA|KS|KY|LA|ME|MH|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|MP|OH|OK|OR|PW|PA|PR|RI|SC|SD|TN|TX|UT|VT|VI|VA|WA|WV|WI|WY)(, \d{5}|\d{5}|\b))")
    zipCoderegex = re.compile(r'\b\d{5}(?:[-\s]\d{4})?\b')
    poBoxregex = re.compile(r'P\.? ?O\.? Box \d+', re.IGNORECASE)
    
    # stats for address redaction
    # find all the address in the text
    addresses1 = re.findall(city_stateregex, data)
    addresses2 = re.findall(addressregex, data)
    addresses3 = re.findall(zipCoderegex, data)
    addresses4 = re.findall(poBoxregex, data)
    
    # address 1 gives tuples, let's get rid of tuple structure
    for i in range(len(addresses1)):
        addresses1[i] = list(addresses1[i])
        addresses1[i] = addresses1[i][0]
    # combine the addresses founds from each regex
    addressCut = list(set(addresses1 + addresses2 + addresses3 + addresses4))


    # remove the address that are the substring of the same address
    for i in range(len(addressCut)):
        for j in range(i + 1, len(addressCut)):
            if addressCut[i] in addressCut[j]:
                addressCut[i] = addressCut[j]
            elif addressCut[j] in addressCut[i]:
                addressCut[j] = addressCut[i]

    # remove duplicates
    for word in addressCut:
        if word not in addressRedaction:
            addressRedaction.append(word)
    
    # strip the leading and trailing whitespaces
    for i in range(len(addressRedaction)):
        addressRedaction[i] = addressRedaction[i].strip()
       
    # address redaction on data 
    data = re.sub(city_stateregex, '█████████', data)
    data = re.sub(addressregex, '█████████', data)
    data = re.sub(zipCoderegex, '█████████', data)
    data = re.sub(poBoxregex, '█████████', data)

    return (data)

    
def emailPrefixRedactor(data):
    # stats for email
    emailprefList = re.findall('[a-zA-Z0-9_\-\.]*@', data)
    for pref in emailprefList:
        emailprefRedaction.append(pref)
    # email redaction
    data = re.sub('[a-zA-Z0-9_\-\.]*@', '█████@', data)
    return (data)

def conceptRedactor(data, input_concepts):

    # lemmatizing the input concept to normalize the term for comparison
    #from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    concept_input = []
    #lemmatize the inputs
    for term in input_concepts:
        concept_input.append(lemmatizer.lemmatize(term.lower()))

    # concept 2D list 
    concepts = [['kid', 'child', 'girl', 'boy', 'toy', 'playground', 'games', 'boardgames', 'baby'],
                ['prison', 'jail', 'incarcerated', 'bar', 'con', 'lockup', 'prisoner', 'warden', 'crime'],
                ['woman', 'lady', 'fierce', 'beauty', 'female', 'girl'],
                ['business', 'rich', 'welthy', 'money', 'economy', 'bill', 'cash', 'payment'],
                ['academic','school', 'university', 'student', 'teacher', 'textbook', 'computer', 'learn','campus'],
                ['food','utensil','spoon','fork','breakfast','lunch','dinner','knife']
               ]
    
    # conceptRedactingWords collects the related words
    conceptRedactingWords = []
    for term in concept_input:
        for relatedWords in concepts:
            if term in relatedWords:
                conceptRedactingWords += relatedWords

    # conceptRedactingTerms collects the related words
    conceptRedactingTerms = []
    # using nltk synsets
    for term in conceptRedactingWords:
        concept_list = []
        synSet = wordnet.synsets(term)
        # for each of the synonym, put it in a list
        for syn in synSet:
            temp = syn.lemma_names()
            for elm in temp:
                if elm not in concept_list:
                    concept_list.append(elm)
        for word in concept_list:
            word = word.replace("_", " ")   # replace "_" with a space
            conceptRedactingTerms.append(word) 

    # Opening the Emails using email parser
    emailData = Parser().parsestr(data)
    # get the headers of the email
    headers = emailData.items()
    # since, it is in a dictionary-like list, each key and value are joined to become a string with ': ' in between them
    for i in range(len(headers)):
        #str = ""
        delim = ': '
        header = delim.join(headers[i])
        #print(header)
        headers[i] = header
    # get the body string of the email
    body = emailData.get_payload(i=None, decode=False)
    #print(body)
    # split the body string into a list separated by empty line(s) -- because some sentences are not stopped by SpaCy over empty lines
    bodySplitted = re.split("\n\n", body)
    #bodySplitted

    # collect sentences with the concept in the headers
    for sentence in headers:
        document = nlp(sentence)
        for token in document:
            if (lemmatizer.lemmatize(token.text.lower()) in conceptRedactingTerms):
                conceptsSentsList.append(str(token.sent)) # append the sentence that has the related word
            elif(lemmatizer.lemmatize(token.text.lower()) in conceptRedactingWords):
                conceptsSentsList.append(str(token.sent))

    # collect sentences with the concept in the body
    for sentence in bodySplitted:
        document = nlp(sentence)
        for token in document:
            if (lemmatizer.lemmatize(token.text.lower()) in conceptRedactingTerms):
                conceptsSentsList.append(str(token.sent))
            elif(lemmatizer.lemmatize(token.text.lower()) in conceptRedactingWords):
                conceptsSentsList.append(str(token.sent))

    # redact the sentences with the concepts
    for token in conceptsSentsList:
        data = re.sub(token, '█████████', data)

    return(data)
    
    
    
    
    
    
