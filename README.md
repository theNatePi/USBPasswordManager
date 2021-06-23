# USBPasswordManager
A script to encrypt and decrypt passwords stored on a USB drive to act as a login key

## General Idea ##

For increased security you want to have a different password for every site you use. However, memorizing multiple long passwords is too much of a hassle for many people.

This python script is made to encrypt and decrypt files on a USB drive. The user will create a master passphrase which will be used both to create files with the password of a service and to retrieve these passwords later.

## Use ##

First the Python script can be compiled into an executable file using pyinstaller.
This executable file is put on a USB drive with a directory named "information" in the same directory as the executable file.

On first boot, the user can input a passphrase, this passphrase will use symmetric encryption to encrypt the password and decrypt it later.
The encrypted passwords will be stored in the /information directory on the USB drive.

To get a password, the user can insert the USB drive and run the program. They can then enter the passphrase, type "copy", and then type the name of the service they want to get the password for.
The password will then be copied to their clipboard.

## Issues/Other Information ##

This has not been tested on Windows since Windows Defender really does not like unsigned .exe files (understandably).
Because of this if the code was not signed it would be difficult to use in the real world.
However, macOS and Linux do not have the same issue, meaning this USB login drive can be used for personal devices with these operating systems.
