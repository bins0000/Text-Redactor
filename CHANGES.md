# Changes
- SpaCy web module was not auto downloading --- Added en_core_web_md = {file = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.2.0/en_core_web_md-3.2.0-py3-none-any.whl"} below spacy module in Pipfile for auto download when creating pipenv environment.
- Concepts redactor missed some input words bug --- Improved and fixed bugs with the concepts redaction function to include the input concepts.
- The program originally specify to put input files in docs/emails/ forder. --- Changed the location of where the input should be read to the root folder. 
- The stats file were also written into the same folder with all other redacted files --- Changed the location of where the stats file will be placed to the root folder. 
- stderr was not outputting the errors --- Changed stderr to output any error the code might run into.
- glob_test.py was run in tests/ folder when I ran pytest, and therefore, when you ran pytest in root directory it failed. --- updated the test file to be compatible with pytest running from root directory.
- Improve the way the program writes the stat file to make it easier to read.
- Please note that stdout print out the number of redactions on the console to convey only the important information and safe space, and if you want to check the terms/sentences that are redacted, it is going to be in a stat file when you pass an argument to create a new stat file.  
