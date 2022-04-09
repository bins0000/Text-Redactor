def email_test():
    # email redaction
    data = "nick@jb.efr ---- kok@fahroo.com"
    data = re.sub('[a-zA-Z0-9_\-\.]*@', '█████@', data)
    expectedOutput = "█████ ---- █████"

    assert data == expectedOutput
