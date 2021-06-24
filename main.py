import base64
import os
from os import system, name
import sys
import getpass
# must be installed
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

TITLE = r"""
__________                                                    .___ 
\______   \_____     ______  ________  _  __ ____ _______   __| _/ 
 |     ___/\__  \   /  ___/ /  ___/\ \/ \/ //  _ \\_  __ \ / __ |  
 |    |     / __ \_ \___ \  \___ \  \     /(  <_> )|  | \// /_/ |  
 |____|    (____  //____  >/____  >  \/\_/  \____/ |__|   \____ |  
   _____        \/      \/      \/    ____                     \/  
  /     \  _____     ____  _____     / ___\   ____ _______         
 /  \ /  \ \__  \   /    \ \__  \   / /_/  >_/ __ \\_  __ \        
/    Y    \ / __ \_|   |  \ / __ \_ \___  / \  ___/ |  | \/        
\____|__  /(____  /|___|  /(____  //_____/   \___  >|__|           
        \/      \/      \/      \/               \/         

Version 2.0
Created 6/21/21
------------------------------------------------------------------
"""

password_input = getpass.getpass('Input Password: ')
password_bytes = bytes(password_input, 'utf-8')

SALT = b"This is the salt"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=SALT,
    iterations=100000,
)
key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
encryption = Fernet(key)


# Encrypt provided bytes with the key created
def encrypt(given_bytes):
    encrypted = encryption.encrypt(given_bytes)
    return encrypted


# Decrypt provided bytes with the key created
def decrypt(given_bytes):
    decrypted = encryption.decrypt(given_bytes)
    return decrypted


# A function to clear the terminal window depending on the operating system
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux
    else:
        _ = system('clear')


# Function to create a new file with encrypted password
def create_file():
    # This this the name of the service the password is for, for example github
    given_name = input('Input Service Name: ')
    # Inputting the password for that service
    given_pass = input('Input Desired Password: ')
    # Turning the name of the service into bytes and encrypting it
    encrypted_name = encrypt(bytes(given_name, 'utf-8'))
    # This takes the encrypted name for the file,
    # takes away the b'' added to indicate it is bytes in python 3.9,
    # and adds .utf8 for the file extension
    final_name = str(encrypted_name).removeprefix("b'").removesuffix("'") + '.utf8'

    """
    Side note for the above operation. The names of each file are encrypted using the same
    key as its content. Something with a random encrypted name will make less sense to someone
    who may find the USB than say "github.utf8" meaning if someone finds the USB stick, they wont
    be able to know what each of the files are
    """

    # Renaming given_pass to content_format
    content_format = given_pass
    # This turns the password that the user gave into bytes and then encrypts it using the same key
    encrypted_information = encrypt(bytes(content_format, 'utf-8'))

    # Getting the current directory path of the program
    if getattr(sys, 'frozen', False):
        path = sys.executable
    else:
        path = os.path.dirname(os.path.abspath(__file__))

    # The above path will be something like "/usb_drive_name/main"
    # Since the program is named "main" this will replace it with "/information" since /information is where all of the passwords will be
    path = path.replace('/main', '/information')
    """
    Note, this may not work on windows if compiled into an exe file, it was only tested on macOS
    """

    # Finally the file is created in the information directory
    with open(path + '/' + final_name, 'wb') as new_file:
        new_file.write(encrypted_information)


# Function to retrieve correct file and decrypt the password
def retrieve_password(service):
    # Same operation to get the path
    if getattr(sys, 'frozen', False):
        path = sys.executable
    else:
        path = os.path.dirname(os.path.abspath(__file__))

    path = path.replace('/main', '/information')

    # The following block does the following things
    #   Gets a list of all files in the /information directory
    #   For every file, the name has the .utf8 removed from the end
    #   The name is converted into bytes and decrypted
    #   If the decrypted name matches the service the user is looking for, it saves the file as the correct file
    """
    The file names are decrypted using the key used to create the file
    This means that the same password must be used
    If the wrong password is used then the wrong key will be made and no file will be found
    """
    service_in_files = False
    password_files = os.listdir(path)
    file_found = ""
    for file in password_files:
        service_name = file.removesuffix(".utf8")
        bytes_name = bytes(service_name, 'utf-8')
        try:
            decrypted_name = decrypt(bytes_name)
        except:
            decrypted_name = ""
        if decrypted_name == bytes(service, 'utf-8'):
            service_in_files = True
            file_found = file

    # If the file is found
    if service_in_files:
        service_file = path + "/" + file_found
        with open(service_file) as service_open_file:
            # Decrypts the contents
            content = service_open_file.read()
            decrypted_content = decrypt(bytes(content, 'utf-8'))
            decrypted_password = decrypted_content.decode('utf-8')
            pyperclip.copy(decrypted_password)
            sys.exit('Copied to clipboard')
    if not service_in_files:
        print('Service could not be found')


# This loop will prompt the user to either make a new file or get the password from an existing one
clear()
while True:
    print(TITLE)
    print('Would you like to Add or Copy a password')
    user_initial_input = input('add/copy: ')
    if user_initial_input == 'add':
        create_file()
    elif user_initial_input == 'copy':
        service_to_retrieve = input('Input the service to retrieve: ')
        retrieve_password(service_to_retrieve)
