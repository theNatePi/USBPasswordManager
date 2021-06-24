# USBPasswordManager
This is a script to encrypt and decrypt passwords stored on a USB drive to act as a login key

## Project Idea ##

For increased security you want to have a different password for every site you use. However, memorizing multiple long passwords is too much of a hassle for many people.

This python script is made to encrypt and decrypt files on a USB drive. The user will create a master passphrase which will be used both to create files with the password of a service and to retrieve these passwords later.
If the user wants to log into a website or application on a computer, all they have to do is:
- Insert the USB drive key
- Run the compiled script
- Input their master password
- Enter the name of the service
- Paste the password into the website or application

## Use ##

First the Python script can be compiled into an executable file using pyinstaller.
This executable file is put on a USB drive with a directory named "information" in the same directory as the executable file.

The user can create a passphrase which will be used to create a key and encrypt and decrypt files using symmetric encryption.
The passwords will be stored in encrypted files in the /information directory.
The name of each file will be the encrypted name of the service that the password is for, for example GitHub.
The contents of the file will just be the password, but this can also be adapted to store usernames.
