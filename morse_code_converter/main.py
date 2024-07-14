MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

def encrypt(message):
    cipher = ''
    for letter in message.upper():
        if letter != ' ':
            cipher += MORSE_CODE_DICT.get(letter, '') + ' '
        else:
            cipher += ' '
    return cipher.strip()

def decrypt(message):
    message += ' '
    decipher = ''
    cipherText = ''
    i = 0
    for letter in message:
        if letter != ' ':
            i = 0
            cipherText += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            elif cipherText:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(cipherText)]
                cipherText = ''
    return decipher

def main():
    message = "my name is zheer"
    result = encrypt(message)
    print(f"Original message: {message}")
    print(f"Encrypted message: {result}")
    decrypted = decrypt(result)
    print(f"Decrypted message: {decrypted}")

if __name__ == '__main__':
    main()