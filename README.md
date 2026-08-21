# CLI Python CRUD Project

A command-line file and folder manager built in Python. Create, read, update, and delete files and folders from your terminal through a numbered menu that loops until you choose to exit.

I built this as a hands-on project while learning Python, specifically to put file handling, functions, exception handling, and `pathlib` into practice.

This project is part of my [AI/ML Journey](https://github.com/kk376/ai-ml-journey), where I'm documenting everything I learn from Python basics through to machine learning.

## What It Does

When you run the program, you get a persistent menu:

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

You can perform as many operations as you want in a single session. The menu returns after each action until you choose `0` to exit.

Before each file or folder operation, the program lists everything in the current directory tree with `[FILE]` and `[DIR]` labels so you can see what you're working with.

### Create a File

Prompts you for a filename and the content to write. If the file already exists, it tells you instead of overwriting.

### Read a File

Pick a file by name, and it prints the full contents to the terminal.

### Update a File

Three sub-options:

1. **Rename** the file (checks that the new name doesn't collide with an existing file)
2. **Overwrite** the file's contents entirely (with a warning)
3. **Append** new content to the end of the file

### Delete a File

Asks for confirmation (`y/n`) before removing the file.

### Create a Folder

Creates a new directory. Checks for name collisions before creating.

### Delete a Folder

Only deletes empty folders (tells you to clear the contents first if not empty). Asks for confirmation before removing.

### List Files and Folders

Shows every file and folder in the current directory tree, labeled `[FILE]` or `[DIR]`.

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
├── main.py        # All logic lives here
└── README.md
```

Single-file project. The code is organized into focused functions:

| Function | Purpose |
|:--|:--|
| `list_files_and_folders()` | Recursively lists all items in the current directory with `[FILE]`/`[DIR]` labels |
| `get_valid_int()` | Safely reads integer input, returns `None` on invalid input instead of crashing |
| `create_file()` | Creates a new file with user-provided content |
| `read_file()` | Reads and prints a file's contents |
| `update_file()` | Rename, overwrite, or append to a file |
| `delete_file()` | Deletes a file after confirmation |
| `create_folder()` | Creates a new directory |
| `delete_folder()` | Deletes an empty directory after confirmation |
| `show_menu()` | Displays the main menu |
| `main()` | Runs the menu loop |

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
| pathlib | `Path`, `.exists()`, `.is_file()`, `.is_dir()`, `.rglob()`, `.rename()` |
| os module | `os.remove()`, `os.rmdir()`, `os.makedirs()`, `os.listdir()` |
| Type conversion | `int()` for menu choices with proper error handling |
| Comparison operators | `==`, `>`, `and`, `not` for validation logic |

## What Changed from v1

The original version had several issues that are now fixed:

- **Menu loop**: The program no longer exits after a single operation. It keeps running until you choose to quit.
- **Input validation**: Typing a non-integer at any prompt no longer crashes the program with a `ValueError`.
- **Empty input handling**: Blank filenames and folder names are caught and rejected.
- **Delete confirmation**: Both file and folder deletion now require a `y/n` confirmation.
- **Folder support**: You can now create and delete folders, not just files.
- **Variable shadowing fix**: `ReadFileAndFolder()` had a bug where `items` was used as both the list and the loop variable. Fixed.
- **Consistent naming**: All functions now use `snake_case` instead of a mix of `PascalCase` and `lowercase`.
- **Redundant close calls removed**: `fs.close()` inside `with` blocks was unnecessary (the context manager handles it).
- **Rename collision check**: Renaming a file now checks if the target name already exists.
- **Hidden files filtered**: Directory listing ignores hidden files and directories (like `.git`) and `__pycache__` so the menu only shows relevant project files.
- **Directory labels**: The listing function marks entries with `[FILE]` or `[DIR]` so you can tell them apart.
- **Typo fix**: "occured" corrected to "occurred".

## What I Learned Building This

File handling was the main goal, but this project ended up touching almost every concept I'd studied. The update function with its sub-menu was probably the trickiest part, juggling multiple file modes (`"w"` vs `"a"`) and making sure `Path.rename()` worked correctly.

The `pathlib` module turned out to be cleaner than raw `os.path` calls for most things, though I still needed `os.remove()`, `os.rmdir()`, and `os.makedirs()` for operations `pathlib` doesn't cover directly.

Adding input validation taught me how `try/except` with specific exception types (`ValueError`) is more useful than blanket `Exception` catches, and how returning `None` from a helper function can signal "bad input" to the caller without crashing.

## License

Open source. Do whatever you want with it.
