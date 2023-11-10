from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import requests
import secrets
import base64
import time
import re

def get_obfuscated_variable_name():
    theNewName = "".join(re.findall(r'[a-zA-Z]+', base64.b64encode(get_random_bytes(32)).decode('utf-8') ))
    return theNewName

def obfuscate_code(code):
    # padd the code
    padded_code = code + ' ' * (16 - (len(code) % 16))
    # Generate key and iv and cipher
    iv = get_random_bytes(16)
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Encode the key and iv and code
    encrypted_code = cipher.encrypt(padded_code.encode('utf-8'))
    encoded_iv = base64.b64encode(iv).decode('utf-8')
    encoded_key = base64.b64encode(key).decode('utf-8')
    encoded_code = base64.b64encode(encrypted_code).decode('utf-8')
    # Obfuscate variable names
    encoded_code_variable_name = get_obfuscated_variable_name()
    encoded_key_variable_name = get_obfuscated_variable_name()
    encoded_iv_variable_name = get_obfuscated_variable_name()
    key_variable_name = get_obfuscated_variable_name()
    iv_variable_name =get_obfuscated_variable_name()
    encrypted_code_variable_name = get_obfuscated_variable_name()
    cipher_variable_name = get_obfuscated_variable_name()
    decrypted_code_variable_name = get_obfuscated_variable_name()
    
    # Create the obfuscated code
    obfuscated_code = f'''
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
{encoded_code_variable_name} = '{encoded_code}'
{encoded_key_variable_name} = '{encoded_key}'
{encoded_iv_variable_name} = '{encoded_iv}'
{key_variable_name} = base64.b64decode({encoded_key_variable_name})
{iv_variable_name} = base64.b64decode({encoded_iv_variable_name})
{encrypted_code_variable_name} = base64.b64decode({encoded_code_variable_name})
{cipher_variable_name} = AES.new({key_variable_name}, AES.MODE_CBC, {iv_variable_name})
{decrypted_code_variable_name} = {cipher_variable_name}.decrypt({encrypted_code_variable_name}).rstrip()
exec({decrypted_code_variable_name}.decode('utf-8'))
    '''
    return obfuscated_code


def obfuscate_times(code, times):

    theCode = code
    for i in range(times):
        theCode = obfuscate_code(theCode)
        time.sleep(0.1)
        print("Layer: ("+ str(i+1) + "/" + str(times) + ") " + str(round(((i + 1) / times) * 100)) + "%")


    return theCode

def show_disclaimer():
    try:
        Disclaimer = requests.get("https://raw.githubusercontent.com/IliyaBadri/HackSnips/main/API/APPDISCLAIMER")
        print(Disclaimer.text + "\n")
        Agree = input("Continue using the application? (Y/n): ")

        if Agree.lower() == "y":
            return
        elif Agree.lower() == "n":
            exit()
        else:
            print("please only respond with 'Y' or 'n'.")
            exit()

    except Exception() as e:
        print("You need to have access to the domain https://raw.githubusercontent.com/ before continueing.")
        # print(e)
        exit()

def main():
    show_disclaimer()
    
    print("Python Obfuscator")
    print("This is an free to use script provided by HackSnips repository and developed by EnterACE.")
    
    print("First you should provide a .py file like (test.py) to be obfuscated.")
    OriginalFileName = input("File name: ")
    
    OriginalFileContents = object()
    try:
        OriginalFile = open(OriginalFileName, "r")
        OriginalFileContents = OriginalFile.read()
    except:
        print("Couldn't open the provided file.")
        exit()
    
    print("Please provide a strength value for obfuscation.\nNote: going beyound 35 might have preformance issues. please make sure you have a decent amount of ram available.")
    
    Strength = input("Obfuscation strength value: ")
    
    if not Strength.isdigit() or Strength == 0:
        print("Your strength value was not valid.")
        exit()
    
    
    obfuscated_code = obfuscate_times(OriginalFileContents, int(Strength))
    print("Saving . . .")
    theoutputfile = open(file="out.py", mode="w")
    theoutputfile.write(obfuscated_code)

if __name__ == '__main__':
    main()

# This code has been published by the HackSnips repository at https://github.com/IliyaBadri/HackSnips.
