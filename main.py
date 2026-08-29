from pathlib import Path
import os

# Dedicated workspace directory so user-created files stay isolated from project code
# and are automatically ignored by Git via .gitignore.
WORKSPACE_DIR = Path("workspace")


def ensure_workspace() -> Path:
    """Create and return the resolved workspace directory."""
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    return WORKSPACE_DIR.resolve()


def resolve_safe_path(user_input: str) -> Path | None:
    """
    Resolve and validate that the requested path strictly resides within the workspace.
    Prevents path traversal vulnerabilities (CWE-22 / CWE-23).
    """
    cleaned = user_input.strip()
    if not cleaned:
        print("Path cannot be empty.")
        return None

    workspace_root = ensure_workspace()
    # Normalize and resolve absolute target path
    target_path = (workspace_root / cleaned).resolve()

    try:
        target_path.relative_to(workspace_root)
        return target_path
    except ValueError:
        print("Security Error: Path traversal outside workspace is forbidden.")
        return None


def list_files_and_folders():
    """Display all files and folders currently inside the workspace."""
    workspace_root = ensure_workspace()
    all_items = list(workspace_root.rglob("*"))

    if len(all_items) == 0:
        print("  (Workspace is empty - no files or folders found)")
        return

    for i, item in enumerate(all_items):
        # Display the path relative to the workspace folder
        rel_path = item.relative_to(workspace_root)
        label = "[DIR] " if item.is_dir() else "[FILE]"
        print(f"  {i + 1} : {label} {rel_path}")


def get_valid_int(prompt: str) -> int | None:
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
        name = input("Enter your file's name: ")
        p = resolve_safe_path(name)
        if p is None:
            return

        if not p.exists():
            # Create parent directories if a nested path is given (e.g. docs/notes.txt)
            p.parent.mkdir(parents=True, exist_ok=True)
            data = input("Write what you want: ")
            with open(p, "w", encoding="utf-8") as fs:
                fs.write(data)
            print("FILE CREATED SUCCESSFULLY!!")
        else:
            print("This file already exists....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def read_file():
    try:
        list_files_and_folders()
        name = input("Type the name of the file: ")
        p = resolve_safe_path(name)
        if p is None:
            return

        if p.exists() and p.is_file():
            with open(p, "r", encoding="utf-8") as fs:
                data = fs.read()
            print(data)
        else:
            print("The file doesn't exist....")
    except Exception as err:
        print(f"An error occurred -> {err}")


def update_file():
    try:
        list_files_and_folders()
        name = input("Type the name of the file: ")
        p = resolve_safe_path(name)
        if p is None:
            return

        if p.exists() and p.is_file():
            print("1. Rename the file")
            print("2. Overwrite the file content")
            print("3. Append content to the file")

            response = get_valid_int("Enter an option: ")
            if response is None:
                return

            if response == 1:
                new_name = input("Enter the new name for your file: ")
                new_path = resolve_safe_path(new_name)
                if new_path is None:
                    return
                if new_path.exists():
                    print("A file with that name already exists.")
                    return
                new_path.parent.mkdir(parents=True, exist_ok=True)
                p.rename(new_path)
                print("FILE RENAMED SUCCESSFULLY!!")
            elif response == 2:
                data = input("Caution: This will overwrite your file content.\nWrite your content: ")
                with open(p, "w", encoding="utf-8") as fs:
                    fs.write(data)
                print("FILE'S CONTENT OVERWRITTEN!!")
            elif response == 3:
                data = input("Write your content to add at the end of the file: ")
                with open(p, "a", encoding="utf-8") as fs:
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
        name = input("Which file do you want to delete?\n")
        p = resolve_safe_path(name)
        if p is None:
            return

        if p.exists() and p.is_file():
            confirm = input(f"Are you sure you want to delete '{p.name}'? (y/n): ").strip().lower()
            if confirm == "y":
                p.unlink()
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
        name = input("Enter the folder name to create: ")
        p = resolve_safe_path(name)
        if p is None:
            return

        if p.exists():
            print("A file or folder with that name already exists.")
            return
        p.mkdir(parents=True, exist_ok=True)
        print("FOLDER CREATED SUCCESSFULLY!!")
    except Exception as err:
        print(f"An error occurred -> {err}")


def delete_folder():
    try:
        list_files_and_folders()
        name = input("Which folder do you want to delete?\n")
        p = resolve_safe_path(name)
        if p is None:
            return

        if p.exists() and p.is_dir():
            contents = list(p.iterdir())
            if len(contents) > 0:
                print("Folder is not empty. Please remove its contents first.")
                return
            confirm = input(f"Are you sure you want to delete folder '{p.name}'? (y/n): ").strip().lower()
            if confirm == "y":
                p.rmdir()
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


if __name__ == "__main__":
    main()
