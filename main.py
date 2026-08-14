from pathlib import Path
import os

def ReadFileAndFolder():
    path = Path("")
    items = list(path.rglob("*"))
    for i, items in enumerate(items):
        print(f"{i + 1} : {items}")


def createfile():
    try:
        ReadFileAndFolder()
        name = input("Enter your file's name: ")
        p = Path(name)
        if not p.exists():
            with open(p, "w") as fs:
                data = input("Write what you want: ")
                fs.write(data)
                fs.close()

            print("FILE CREATED SUCCESSFULLY!!")
        else:
            print("This file already exists....")

    except Exception as err:
        print(f"An error occured -> {err}")


def readfile():
    try:
        ReadFileAndFolder()
        name = input("Type the name of the file: ")
        p = Path(name)
        if p.exists() and p.is_file():
            with open(p, "r") as fs:
                data = fs.read()
                print(data)
                fs.close()
        else:
            print("The file doesn't exist....")
    except Exception as err:
        print(f"An error occured -> {err}")


def updatefile():
    try:
        ReadFileAndFolder()
        name = input("Type the name of the file: ")
        p = Path(name)
        if p.exists() and p.is_file():
            print("Press 1 to change the name of your file: ")
            print("Press 2 to overwrite the data in your file: ")
            print("Press 3 to add content in your file: ")

            response = int(input("Enter an option:- "))

            if response == 1:
                new_name = input("Enter the new name for your file: ")
                new_path = Path(new_name)
                p.rename(new_path)
                print("FILE RENAMED SUCCESSFULLY!!")
            elif response == 2:
                with open(p, "w") as fs:
                    data = input("Caution: This will overwrite your file content.\nWrite your content: ")
                    fs.write(data)
                    fs.close()
                    print("FILE'S CONTENT OVERWRITTEN!!")
            elif response == 3:
                with open(p, "a") as fs:
                    data = input("Write your content to add at the end of the file: ")
                    fs.write(" " + data)
                    fs.close()
                    print("FILE'S CONTENT UPDATED SUCCESSFULLY!!")
            else:
                print("Enter a valid option....")

    except Exception as err:
        print(f"An error occured -> {err}")


def deletefile():
    try:
        ReadFileAndFolder()
        name = input("Which file do you want to delete?\n")
        p = Path(name)
        if p.exists() and p.is_file():
            os.remove(p)
            print("FILE DELETED SUCCESSFULLY!!")
        else:
            print("No such file exists....")

    except Exception as err:
        print(f"An error occured -> {err}")


print("Press 1 to create a file")
print("Press 2 to read a file")
print("Press 3 to update a file")
print("Press 4 to delete a file")

check = int(input("Enter an option:- "))

if check == 1:
    createfile()
elif check == 2:
    readfile()
elif check == 3:
    updatefile()
elif check == 4:
    deletefile()
else:
    print("Enter a valid option....")