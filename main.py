from pathlib import Path
import os

# Dedicated workspace directory so user-created files stay isolated from project code
# and are automatically ignored by Git via .gitignore.
WORKSPACE_DIR = Path("workspace")


def ensure_workspace():
    """Create the workspace directory if it doesn't already exist."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)


def list_files_and_folders():
    """Display all files and folders currently inside the workspace."""
    ensure_workspace()
    all_items = list(WORKSPACE_DIR.rglob("*"))

    if len(all_items) == 0:
        print("  (Workspace is empty - no files or folders found)")
        return

    for i, item in enumerate(all_items):
        # Display the path relative to the workspace folder
        rel_path = item.relative_to(WORKSPACE_DIR)
        label = "[DIR] " if item.is_dir() else "[FILE]"
        print(f"  {i + 1} : {label} {rel_path}")


def get_valid_int(prompt):
    """Prompt the user for an integer, returning None on invalid input."""
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def create_file():
    try:
        list_files_and_folders()
        name = input("Enter your file's name: ").strip()
        if name == "":
            print("File name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if not p.exists():
            # Create parent directories if a nested path is given (e.g. docs/notes.txt)
            p.parent.mkdir(parents=True, exist_ok=True)
            data = input("Write what you want: ")
            with open(p, "w") as fs:
                fs.write(data)
            print("FILE CREATED SUCCESSFULLY!!")
        else:
            print("This file already exists....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def read_file():
    try:
        list_files_and_folders()
        name = input("Type the name of the file: ").strip()
        if name == "":
            print("File name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if p.exists() and p.is_file():
            with open(p, "r") as fs:
                data = fs.read()
            print(data)
        else:
            print("The file doesn't exist....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def update_file():
    try:
        list_files_and_folders()
        name = input("Type the name of the file: ").strip()
        if name == "":
            print("File name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if p.exists() and p.is_file():
            print("1. Rename the file")
            print("2. Overwrite the file content")
            print("3. Append content to the file")

            response = get_valid_int("Enter an option: ")
            if response is None:
                return

            if response == 1:
                new_name = input("Enter the new name for your file: ").strip()
                if new_name == "":
                    print("New name cannot be empty.")
                    return
                new_path = WORKSPACE_DIR / new_name
                if new_path.exists():
                    print("A file with that name already exists.")
                    return
                new_path.parent.mkdir(parents=True, exist_ok=True)
                p.rename(new_path)
                print("FILE RENAMED SUCCESSFULLY!!")
            elif response == 2:
                data = input("Caution: This will overwrite your file content.\nWrite your content: ")
                with open(p, "w") as fs:
                    fs.write(data)
                print("FILE'S CONTENT OVERWRITTEN!!")
            elif response == 3:
                data = input("Write your content to add at the end of the file: ")
                with open(p, "a") as fs:
                    fs.write(" " + data)
                print("FILE'S CONTENT UPDATED SUCCESSFULLY!!")
            else:
                print("Enter a valid option....")
        else:
            print("The file doesn't exist....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def delete_file():
    try:
        list_files_and_folders()
        name = input("Which file do you want to delete?\n").strip()
        if name == "":
            print("File name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if p.exists() and p.is_file():
            # Require explicit confirmation before deleting
            confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
            if confirm == "y":
                os.remove(p)
                print("FILE DELETED SUCCESSFULLY!!")
            else:
                print("Deletion cancelled.")
        else:
            print("No such file exists....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def create_folder():
    try:
        list_files_and_folders()
        name = input("Enter the folder name to create: ").strip()
        if name == "":
            print("Folder name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if p.exists():
            print("A file or folder with that name already exists.")
            return
        os.makedirs(p, exist_ok=True)
        print("FOLDER CREATED SUCCESSFULLY!!")
    except Exception as err:
        print(f"An error occurred -> {err}")


def delete_folder():
    try:
        list_files_and_folders()
        name = input("Which folder do you want to delete?\n").strip()
        if name == "":
            print("Folder name cannot be empty.")
            return

        p = WORKSPACE_DIR / name
        if p.exists() and p.is_dir():
            # Check if the folder is empty; refuse to delete non-empty folders
            contents = os.listdir(p)
            if len(contents) > 0:
                print("Folder is not empty. Please remove its contents first.")
                return
            confirm = input(f"Are you sure you want to delete folder '{name}'? (y/n): ").strip().lower()
            if confirm == "y":
                os.rmdir(p)
                print("FOLDER DELETED SUCCESSFULLY!!")
            else:
                print("Deletion cancelled.")
        else:
            print("No such folder exists....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def show_menu():
    print("\n===== CLI File Manager =====")
    print("1. Create a file")
    print("2. Read a file")
    print("3. Update a file")
    print("4. Delete a file")
    print("5. Create a folder")
    print("6. Delete a folder")
    print("7. List all files and folders")
    print("0. Exit")


def main():
    ensure_workspace()
    while True:
        show_menu()
        choice = get_valid_int("Enter an option: ")
        if choice is None:
            continue

        if choice == 1:
            create_file()
        elif choice == 2:
            read_file()
        elif choice == 3:
            update_file()
        elif choice == 4:
            delete_file()
        elif choice == 5:
            create_folder()
        elif choice == 6:
            delete_folder()
        elif choice == 7:
            list_files_and_folders()
        elif choice == 0:
            print("Goodbye!")
            break
        else:
            print("Enter a valid option....")


main()