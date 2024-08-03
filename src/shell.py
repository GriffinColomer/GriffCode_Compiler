from lexical_parser import parseText

while True:
    text = input('basic > ')
    result, error = parseText(text)
    
    if error:
        print(error)
    else:
        print(result)