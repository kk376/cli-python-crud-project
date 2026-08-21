# CLI Python CRUD Project

A command-line file and folder manager built in Python. Create, read, update, and delete files and folders from your terminal through an interactive numbered menu that loops until you choose to exit.

All files and folders you create are isolated inside a dedicated `workspace/` directory, which is ignored by Git. This keeps your project root clean and prevents accidental modifications to project code.

I built this as a hands-on project while learning Python, specifically to put file handling, functions, exception handling, and `pathlib` into practice.

This project is part of my [AI/ML Journey](https://github.com/kk376/ai-ml-journey), where I'm documenting everything I learn from Python basics through to machine learning.

## What It Does

When you run the program, it creates a `workspace/` directory (if not already present) and displays a menu:

```
===== CLI File Manager =====
1. Create a file
2. Read a file
3. Update a file
4. Delete a file
5. Create a folder
6. Delete a folder
7. List all files and folders
0. Exit
```

The menu returns after each action until you choose `0` to exit.

Before each file or folder operation, the program lists the current contents of your workspace with `[FILE]` and `[DIR]` labels so you can see what you are working with.

### Create a File

Prompts you for a filename (or nested path like `docs/notes.txt`) and content to write. If the file already exists, it warns you instead of overwriting.

### Read a File

Pick a file by name, and it prints the full contents to the terminal.

### Update a File

Three sub-options:

1. **Rename** the file (checks that the new name does not collide with an existing file)
2. **Overwrite** the file contents entirely (with a warning prompt)
3. **Append** new content to the end of the file

### Delete a File

Asks for confirmation (`y/n`) before removing the file.

### Create a Folder

Creates a new directory inside your workspace. Checks for name collisions before creating.

### Delete a Folder

Only deletes empty folders (warns you to clear the contents first if not empty). Asks for confirmation before removing.

### List Files and Folders

Shows every file and folder currently inside the workspace, labeled `[FILE]` or `[DIR]`.

## Getting Started

### Prerequisites

- Python 3.6 or higher (for f-strings and `pathlib` support)

No external dependencies. Everything uses the standard library.

### Running It

```bash
git clone https://github.com/kk376/cli-python-crud-project.git
cd cli-python-crud-project
python main.py
```

Follow the prompts.

## Project Structure

```
cli-python-crud-project/
├── .gitignore         # Ignores workspace/ and bytecode cache
├── README.md
├── main.py            # All logic lives here
└── workspace/         # Isolated user storage (untracked by git)
    ├── notes.txt
    └── docs/
```

Single-file implementation organized into focused functions:

| Function | Purpose |
|:--|:--|
| `ensure_workspace()` | Creates the `workspace/` directory if missing |
| `list_files_and_folders()` | Recursively lists all items inside `workspace/` with `[FILE]`/`[DIR]` labels |
| `get_valid_int()` | Safely reads integer input, returning `None` on invalid input instead of crashing |
| `create_file()` | Creates a new file inside `workspace/` with user-provided content |
| `read_file()` | Reads and prints a file's contents from `workspace/` |
| `update_file()` | Rename, overwrite, or append to a file in `workspace/` |
| `delete_file()` | Deletes a file in `workspace/` after confirmation |
| `create_folder()` | Creates a new directory in `workspace/` |
| `delete_folder()` | Deletes an empty directory in `workspace/` after confirmation |
| `show_menu()` | Displays the main menu |
| `main()` | Initializes the workspace and runs the menu loop |

## Python Concepts Used

| Concept | Where It Shows Up |
|:--|:--|
| Variables | Storing user input, file paths, menu choices |
| Data types | Strings for filenames/content, integers for menu selection, booleans for checks |
| Input/Output | `input()` for prompts, `print()` for feedback |
| String formatting | f-strings for error messages, confirmation prompts, and display |
| String methods | `.strip()` and `.lower()` for input sanitization |
| If/Elif/Else | Menu routing, file existence checks, update sub-menu, confirmation handling |
| Functions | Each operation is its own function, plus helpers for input validation and menu display |
| While loop | Main menu loop that runs until the user exits |
| For loop | Iterating over directory contents with `enumerate()` |
| Exception handling | `try/except` wrapping every operation, plus targeted `ValueError` handling in input validation |
| File handling | `open()` with `"r"`, `"w"`, `"a"` modes inside `with` blocks |
| pathlib | `Path`, `.exists()`, `.is_file()`, `.is_dir()`, `.rglob()`, `.rename()`, `.relative_to()` |
| os module | `os.remove()`, `os.rmdir()`, `os.makedirs()`, `os.listdir()` |
| Type conversion | `int()` for menu choices with error handling |
| Comparison operators | `==`, `>`, `and`, `not` for validation logic |

## What Changed from v1

- **Workspace isolation**: All user files are stored in `workspace/`, which is ignored by Git. Your repository stays clean and project code (`main.py`, `README.md`) cannot be deleted or overwritten by the CLI tool.
- **Menu loop**: The program runs continuously until you choose option `0` to quit.
- **Input validation**: Typing letters or symbols at numeric prompts is caught safely via `get_valid_int()` instead of crashing with a `ValueError`.
- **Empty input handling**: Blank filenames and folder names are rejected.
- **Delete confirmation**: File and folder deletions require explicit `y/n` confirmation.
- **Folder CRUD**: Added support for creating folders and safely deleting empty folders.
- **Variable shadowing fix**: Fixed the loop variable shadowing bug in the listing function.
- **Consistent naming**: All functions use `snake_case`.
- **Redundant close calls removed**: Cleaned up manual `.close()` calls inside `with` context manager blocks.
- **Rename collision check**: Renaming checks for existing filenames before moving.
- **Directory labels**: `[FILE]` and `[DIR]` prefixes distinguish files from directories.

## What I Learned Building This

File handling was the primary goal, but this project touches almost every foundational Python concept. Managing file paths with `pathlib.Path` made manipulating nested files straightforward, while isolating user storage in a dedicated folder demonstrated how practical CLI tools separate application code from user data.

## License

Open source. Do whatever you want with it.
