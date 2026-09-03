from pathlib import Path

from file_ops import (
    DirectoryNotEmptyError,
    FileManager,
    InvalidTargetError,
    ItemAlreadyExistsError,
    ItemNotFoundError,
    PathSecurityError,
    WorkspaceItem,
)

# Dedicated workspace directory so user-created files stay isolated from project code
# and are automatically ignored by Git via .gitignore.
WORKSPACE_DIR = Path("workspace")
manager = FileManager(WORKSPACE_DIR)


def ensure_workspace() -> Path:
    """Create and return the resolved workspace directory."""
    return manager.ensure_workspace()


def resolve_safe_path(user_input: str) -> Path | None:
    """
    Resolve and validate that the requested path strictly resides within the workspace.
    Prevents path traversal vulnerabilities (CWE-22 / CWE-23) and protects workspace root.
    """
    try:
        return manager.resolve_safe_path(user_input)
    except PathSecurityError as err:
        print(f"Security Error: {err}")
        return None
    except InvalidTargetError as err:
        print(err)
        return None


def list_files_and_folders(mgr: FileManager = manager) -> list[WorkspaceItem]:
    """Display all files and folders currently inside the workspace."""
    items = mgr.list_items()
    if len(items) == 0:
        print("  (Workspace is empty - no files or folders found)")
        return items

    for i, item in enumerate(items):
        label = "[DIR] " if item.is_dir else "[FILE]"
        print(f"  {i + 1} : {label} {item.rel_path}")
    return items


def get_valid_int(prompt: str) -> int | None:
    """Prompt the user for an integer, returning None on invalid input."""
    raw = input(prompt)
    try:
        return int(raw)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def create_file(mgr: FileManager = manager):
    try:
        list_files_and_folders(mgr)
        name = input("Enter your file's name: ")
        data = input("Write what you want: ")
        mgr.create_file(name, data)
        print("FILE CREATED SUCCESSFULLY!!")
    except ItemAlreadyExistsError:
        print("This file already exists....")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred -> {err}")


def read_file(mgr: FileManager = manager):
    try:
        items = list_files_and_folders(mgr)
        name = input("Type the name or number of the file: ")
        content = mgr.read_file(name, items)
        if not content:
            print("(File is empty)")
        else:
            print(content)
    except ItemNotFoundError:
        print("The file doesn't exist....")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
    except UnicodeDecodeError:
        print("Unable to read file: file contains non-text or binary data.")
    except Exception as err:
        print(f"An error occurred -> {err}")


def update_file(mgr: FileManager = manager):
    try:
        items = list_files_and_folders(mgr)
        name = input("Type the name or number of the file: ")
        target = mgr.resolve_item_input(name, items)
        if not target.exists() or not target.is_file():
            print("The file doesn't exist....")
            return

        print("1. Rename the file")
        print("2. Overwrite the file content")
        print("3. Append content to the file")

        response = get_valid_int("Enter an option: ")
        if response is None:
            return

        if response == 1:
            new_name = input("Enter the new name for your file: ")
            mgr.rename_file(name, new_name, items)
            print("FILE RENAMED SUCCESSFULLY!!")
        elif response == 2:
            data = input("Caution: This will overwrite your file content.\nWrite your content: ")
            mgr.overwrite_file(name, data, items)
            print("FILE'S CONTENT OVERWRITTEN!!")
        elif response == 3:
            data = input("Write your content to add at the end of the file: ")
            mgr.append_file(name, data, items)
            print("FILE'S CONTENT UPDATED SUCCESSFULLY!!")
        else:
            print("Enter a valid option....")
    except ItemAlreadyExistsError:
        print("A file with that name already exists.")
    except ItemNotFoundError:
        print("The file doesn't exist....")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred -> {err}")


def delete_file(mgr: FileManager = manager):
    try:
        items = list_files_and_folders(mgr)
        name = input("Which file do you want to delete?\n")
        target = mgr.resolve_item_input(name, items)
        if not target.exists() or not target.is_file():
            print("No such file exists....")
            return

        confirm = input(f"Are you sure you want to delete '{target.name}'? (y/n): ").strip().lower()
        if confirm == "y":
            mgr.delete_file(name, items)
            print("FILE DELETED SUCCESSFULLY!!")
        else:
            print("Deletion cancelled.")
    except ItemNotFoundError:
        print("No such file exists....")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred -> {err}")


def create_folder(mgr: FileManager = manager):
    try:
        list_files_and_folders(mgr)
        name = input("Enter the folder name to create: ")
        mgr.create_folder(name)
        print("FOLDER CREATED SUCCESSFULLY!!")
    except ItemAlreadyExistsError:
        print("A file or folder with that name already exists.")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
    except Exception as err:
        print(f"An error occurred -> {err}")


def delete_folder(mgr: FileManager = manager):
    try:
        items = list_files_and_folders(mgr)
        name = input("Which folder do you want to delete?\n")
        target = mgr.resolve_item_input(name, items)
        if not target.exists() or not target.is_dir():
            print("No such folder exists....")
            return

        contents = list(target.iterdir())
        if len(contents) > 0:
            print("Folder is not empty. Please remove its contents first.")
            return

        confirm = input(f"Are you sure you want to delete folder '{target.name}'? (y/n): ").strip().lower()
        if confirm == "y":
            mgr.delete_folder(name, items)
            print("FOLDER DELETED SUCCESSFULLY!!")
        else:
            print("Deletion cancelled.")
    except DirectoryNotEmptyError:
        print("Folder is not empty. Please remove its contents first.")
    except ItemNotFoundError:
        print("No such folder exists....")
    except PathSecurityError as err:
        print(f"Security Error: {err}")
    except InvalidTargetError as err:
        print(err)
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
    manager.ensure_workspace()
    try:
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
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
