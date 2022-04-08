# Author Nasri Binsaleh
#### See COLLABORATORS.txt for related links


# Activating pipenv in the project directory
I was trying to create an environment in 'cs5293sp22-project1' directory. But it seemed like after I updated to python 3.10, the pipenv was not usable. 
I had to reinstall pipenv, then try to activate an environment in the mentioned directory again. 
I activated pipenv using 'pipenv shell' in 'cs5293sp22-project1' directory. But I saw no Pipfile in the directory, so I tried to install it again using 'pipenv install' to create a pipfile. However, the Pipfile was still not there. I figured that the parent directory also has a Pipfile, so pipenv was actually inheriting from the parent directory at first, so I ran 'PIPENV_NO_INHERIT=True pipenv install' then the Pipfile was created in the working directory.


# How to install, directions on how to use the code, and some example of how to run.

## First, installation, simply clone the github ripository to your machine.
This github repository can be cloned using the following command:-  
    ```git clone "git repository link"```

## Prerequisites
    [packages]
    spacy = "*"
    nltk = "*"
    pytest = "*"

    [requires]
    python_version = "3.10"
You should be able to install above packages using pipenv install 'package'
  e.g. pipenv install spacy
The rest of the requirements will be import by the program. Also, make sure to create and use the environment with python 3.10


## Directories
    cs5293sp22-project1
    ├── COLLABORATORS.txt
    ├── LICENSE.txt
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── docs
    │   ├── common_names.txt
    │   └── emails
    │       ├── 1.txt
    │       ├── 2.txt
    │       ├── 3.txt
    │       └── test.txt
    ├── project1
    │   ├── common_names.txt
    │   └── main.py
    ├── redactor.py
    ├── setup.cfg
    ├── setup.py
    └── tests
        ├── glob_test.py
        ├── project1
        │   └── common_names.txt
        ├── spacy_test.py
        ├── test_address.py
        ├── test_concepts.py
        ├── test_dates.py
        ├── test_email.py
        ├── test_genders.py
        ├── test_names.py
        └── test_phones.py

The main files in this repository are `redactor.py` and `main.py`. `redactor.py` will drive the program, so this is the one to call. 

## To get the email dataset
In tmp directory, run the following command:- 
	wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
	tar xvzf enron_mail_20150507.tar.gz
The dataset was very large to inspect, so some samples are picked and put in cs5293sp22-project1/docs/emails folder as can be seen in the directory above.
### This program reads file from /cs5293sp22-project1/docs/emails directory.
#### please put any file you want the program to redact in that directory.

## Email dataset are not in .txt format
Since the downloaded dataset are not .txt files, I assumed that we should change the file type before running the program because 
running the program with the specified command line argument (in project description) should read all files given by the glob — 
in this case all the files ending in .txt in the current folder. So, the .txt files must already be present before running the program. 
But either way, the --input flag is going to specify which input type need to be read, and the program can handle it. 

## How to run
In the repository outer most directory (cs5293sp22-project1/ where redactor.py is located), you can call `redactor.py` to run the program by using the following command:- 

    pipenv run python redactor.py --input '*.txt' \
                        --names --dates --phones --genders --address\
                        --concept 'kids' \
                        --output 'files/' \
                        --stats stderr
Among the arguments, --input and --concept can take more than one arguments. For example, you might pass in --concept food --concept school for concept. 

# The functions
As mentioned, apart from redactor.py, main.py is another important file as this file host all the functions neccessary to this program. 

## Names Redactor
`nameRedactor(data)` takes in a string of data (in this case, the string email) and redacts the names that appear in the data. This function employs SpaCy to tokenize the string into tokens and label them according there most suitable type. The entity type for names is 'PERSON'. So, in this function, any words that are categorized as 'PERSON' will be redacted. The redacted words will become █████████ (blocks) instead <-- This goes for every redaction through out the program. 
However, SpaCy alone cannot catch every name in the documents, and therefore some names are not redacted. I then use name-dataset published by [philipperemy](https://github.com/philipperemy/name-dataset) to generate more names to catch somemore names to be redacted. Thanks to philipperemy! I generated 1000 most common names in the US and put it in a file called `common_names.txt` to be passed on to this function.

## Email Prefix Redactor
`emailprefRedactor(data)` this function takes in the same string to redacts email prefix. This function will be called along with `nameRedactor(data)` when the flag for --names is passed. I considered redacting email prefix as well because most of the times, the prefix of the email contains names of the email owner. This function uses a regular expression below to redact the email prefixes.
    
    `'[a-zA-Z0-9_\-\.]*@'`
    
## Concepts Redactor
`conceptRedactor(data)` takes data of string in and redact any senctence that contains the exact words or other words related to the exact words passed in by --concept arguments. Since user can basically passed in any words they can think of, the function will normallize the input word by lemmatization to narrow down the word search. NLTK package is used in this function to lemmatize the words and also fine the synnonym of the input concepts to increase the amount of vocab related to the input concept. 
The collection of concepts are store in a dictionary format where the concept key have multiple related words in a list as its values. If a sentence in the document contain any word in the list, the whole sentence will be redacted with the blocks. 

## Addresses Redactor
`addressRedactor(data)` just like others, take in data string and redact the street address that appears in the text. This function uses multiple regular expression to try to catch as many formats of addresses including the street addresses, P.O. boxes, City, State, and Zip code. 
My regular expressions in this function are heavily inspired by the published CommonRegex module by [madisonmay](https://github.com/madisonmay/CommonRegex). Big thanks to this person as well! 

## Gender Specific Terms Redactor
`genderRedactor(data)` This function here redacts any terms that specify gender such as she, he, mother. In this function, I switch to use a list of words that are gender specific. Alongside SpaCy as a tokenizer, the tokenized words are then lemmatized are search to see if it exist in the list or not. If the word happens to be in the list of gender specific terms, then that word is redacted. 

## Phone Numbers Redactor
`phoneRedactor(data)` This function uses multitude of regular expression to redact various forms of phone numbers. Many regular expressions in this function are also inspired by madisonmay as well. If the text has any combination of numbers similar to the regular expression, then it will be redacted with the blocks. 

## Dates Redactor
`dateRedactor(data)` This function redacts dates in various forms using regular expressions as well. It can detect dates in the form such as 12 Aug 2020 or 11/12/1990. The dates redactor also redacts dates including days like Monday-Sunday and the words today, yesterday, and tomorrow. 

## Main Function
`main()` takes the arguments mentions earlier and calls the function coresponding to the what are being passed. It also keep tracks of the redaction and provide some statistics at the end of the redaction for each file.

# Assumptions & Bugs
## Assumptions
#### Times are not redacted.
- I assumed that time is not the sensitive information worth redacting. It can also provide a little bit of context. 

#### Phone number have too many forms
- I have assumed that my regular expression have the ability to detect most of the common phone number formats, but it might also unrecognize some unfamiliar patterns. 

#### SpaCy
- I have assumed that SpaCy will tokenize the words and label them accurately (but in reallity it is clearly not). 

#### Email Prefix
- I assumed that most of the email prefixes contain names. Therefore I generalized it and redact all the email prefixes. 

#### Names in Addresses
- It can be assumed that most of the street address would be someone's name, and that might cause a little bit of a confusion to the program. Thus, I decided to have the order of redaction to redact addresses first before names in the case that both categories are being redacted.

#### Dates in Phone Numbers
- It can also be assumed or observed that some patterns for date might be included in some of the phone numbers, therefore I order the redaction to have phone numbers redacted before dates in the case that both categories are being redacted. 

#### GLOB deals with input
 -  Since we are taking in an argument specifying which type(s) of files are being read. The program would only choose to read the specified file type and ignore the rest. Therefore I assumed that we do not need any 'input unable to read' handler. 

## Bugs
#### Not all the names are redacted
- NLTK and SpaCy are not being so accurates with names. Also, names are not detected if they are enclosed within other special characters. e.g. "Name LastName". 
- Some short names are not being detected and some common names are being mislabeled into GPE or ORG. 
- So, for the leftover names, I try to redact them with the nommon-names list. 
#### Some formats of phone number are not fully redacted.
#### "'s" and "\n" is categorized as PERSON
#### redacting dates accidentlly redacts some phone number
- So, phone number redaction will be done first. 
#### Dates that are not in the normal format are not redacted.
#### SpaCy also tokenize the string in a strange way where it separates every word at white space. 
- This then also stops SpaCy from recognizing the full pattern of dates.
#### The address regular expression catches some abbreviation of text like 15 min. or $100 million 
- Might be because this looks like an address. 
#### I had to create a new 'project1' folder in 'tests' folder to store common_names.txt
- without this, pytest could not find the common_names.txt file.


# Test
### 
    ├── glob_test.py
    ├── project1
    │   └── common_names.txt
    ├── spacy_test.py
    ├── test_address.py
    ├── test_concepts.py
    ├── test_dates.py
    ├── test_email.py
    ├── test_genders.py
    ├── test_names.py
    └── test_phones.py
As can be seen from the trees above, several test was done to check if a particular component is working. 
  
### glob_test.py
This test was done to check if glob can actually locate the file with the given extention. In this case, I simply want glob to look for common.names.txt in projext1 folder. 

### spacy_test.py
This function test SpaCy to see if it is tokenizing just fine. I let SpaCy tokenize a text string and compared to the expected list of tokens/words. 

### test_address.py
This function test if the address redactor function can detect and redact the address from the text. A string with several forms of address were redacted and compared with the expected output.

### test_concepts.py
In this test, I tried to test to see of the concepts are being recognized and of the whole sentence is being redacted by the concept redactor fucntion. 

### test_dates.py
Dates of various forms were being tested to see if the regualar expression in date redactor function can detect dates in its different forms. 

### test_email.py
This function simply tested to see if the email prefixes are being redacted by the email prefix redactor function. (The part in front of @ sign)

### test_genders.py
This test tests gender redactor function so see if the function can lemmatize the words and catch gender specific terms using the flags list. 

### test_names.py
This function test if name redactor function can redact different names in a string.  

### test_phones.py
Several phone numbers with unique patterns are given to test if phone redactor function can catch the phone numbers in these various patterns. 
