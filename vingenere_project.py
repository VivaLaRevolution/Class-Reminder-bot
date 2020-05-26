
charset = [chr(i) for i in range(32, 127)]
charset.remove('`')
charset.remove('"')

##def choose_method():
##    choice = input('To encrypt enter:1   To decrypt enter:0 ')
##    if choice == '1':
##        return 'encrypt'
##    else:
##        return 'decrypt'    

def encrypt(ptext,key):
    ptext = cleantext(ptext)
    keysize = len(key)
    ptextsize = len(ptext)
    ctext = ''
    for n in range(ptextsize):
        ptext_char = ptext[n]
        ptext_index = charset.index(ptext_char)
        key_char = key[n%keysize]
        key_index = charset.index(key_char)
        ctext_index = (ptext_index + key_index)%93
        ctext_char = charset[ctext_index]
        ctext = ctext + ctext_char
    return ctext

def decrypt(ctext,key):
    ctext = cleantext(ctext)
    keysize = len(key)
    ctextsize = len(ctext)
    dtext = ''
    for n in range(ctextsize):
        ctext_char = ctext[n]
        ctext_index = charset.index(ctext_char)
        key_char = key[n%keysize]
        key_index = charset.index(key_char)
        dtext_index = (ctext_index - key_index)%93
        dtext_char = charset[dtext_index]
        dtext = dtext + dtext_char
    return dtext

##def readtext(ptext_file):
##    with open(ptext_file, 'r') as infile:
##        ptext = infile.read()
##        cleanptext = cleantext(ptext)
##    return cleanptext
##
##def writetext(text, name):
##    with open('{}.txt'.format(name)), 'w') as outfile:
##        outfile.write(text)

def cleantext(text):
    cleantext = ''
    for character in text:
        if 31 < ord(character) < 127:
            cleantext += character
    return cleantext

##def main():
##    choice = choose_method()
##    if choice == 'encrypt':
##        ptext_file = 'ptext.txt'
##        ptext = readtext(ptext_file)
##        ctext = encrypt(ptext)
##        writetext(ctext, 'ctext')
##        print(ctext)
##    if choice == 'decrypt':
##        ctext_file = 'ctext.txt'
##        ctext = readtext(ctext_file)
##        dtext = decrypt(ctext)
##        writetext(dtext, 'dtext')
##        print(dtext)
        
##main()

##print(encrypt('water','water'))
    
    


