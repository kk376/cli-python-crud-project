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

Before each file or folder operation, the program lists the current contents of your workspace with numbers and `[FILE]` / `[DIR]` labels. You can select an item either by entering its number (e.g. `1`, `2`) or its relative path (e.g. `notes.txt`).

### Create a File

Prompts you for a filename (or nested path like `docs/notes.txt`) and content to write. If the file already exists, it warns you instead of overwriting.

### Read a File

Pick a file by number or name, and it prints the full contents to the terminal.

### Update a File

Pick a file by number or name, then choose from three sub-options:

1. **Rename** the file (checks that the new name does not collide with an existing file)
2. **Overwrite** the file contents entirely (with a warning prompt)
3. **Append** new content to the end of the file

### Delete a File

Pick a file by number or name. Asks for confirmation (`y/n`) before removing the file.

### Create a Folder

Creates a new directory inside your workspace. Checks for name collisions before creating.

### Delete a Folder

Pick a folder by number or name. Only deletes empty folders (warns you to clear the contents first if not empty). Asks for confirmation before removing.

### List Files and Folders

Shows every file and folder currently inside the workspace, sorted with directories first and files second, labeled `[FILE]` or `[DIR]`.

## Getting Started

### Prerequisites

- Python 3.7 or higher (standard library only)

No external dependencies required.

### Running It

```bash
git clone https://github.com/kk376/cli-python-crud-project.git
cd cli-python-crud-project
python main.py
```

Follow the prompts.

### Running Tests

Run the test suite using Python's built-in `unittest` runner:

```bash
python -m unittest discover tests
```

## Project Structure

```
cli-python-crud-project/
├── .gitignore             # Ignores workspace/ and bytecode cache
├── README.md
├── file_ops.py            # Core file operations, security validation, and domain models
├── main.py                # Interactive CLI loop, menus, and user I/O
├── tests/
│   └── test_file_ops.py   # Unit test suite using standard library unittest
└── workspace/             # Isolated user storage (untracked by git)
    ├── notes.txt
    └── docs/
```

### Module Breakdown

| Module / Component | Purpose |
|:--|:--|
| `file_ops.FileManager` | Encapsulates workspace path resolution, CRUD operations, deterministic listing, and dual selection |
| `file_ops.WorkspaceItem` | Readonly dataclass representing a workspace item (`path`, `rel_path`, `is_dir`) |
| `file_ops.FileOpsError` | Domain exception hierarchy (`PathSecurityError`, `InvalidTargetError`, `ItemAlreadyExistsError`, `ItemNotFoundError`, `DirectoryNotEmptyError`) |
| `main.py` | Handles terminal interaction, formatted menus, input validation, and signals |
| `tests/test_file_ops.py` | 16 automated test cases verifying CRUD behaviors, edge cases, and path security |

## Python Concepts Used

| Concept | Where It Shows Up |
|:--|:--|
| Variables | Storing user input, file paths, menu choices |
| Data types | Strings for filenames/content, integers for menu selection, booleans for checks |
| Dataclasses | `@dataclass(frozen=True)` for structured, immutable `WorkspaceItem` records |
| Custom exceptions | Subclassing `Exception` into a domain hierarchy (`PathSecurityError`, etc.) |
| Input/Output | `input()` for prompts, `print()` for feedback |
| String formatting | f-strings for error messages, confirmation prompts, and display |
| String methods | `.strip()` and `.lower()` for input sanitization |
| If/Elif/Else | Menu routing, file existence checks, update sub-menu, confirmation handling |
| Functions & classes | Modular separation between interactive CLI functions and domain class methods |
| While loop | Main menu loop that runs until the user exits |
| For loop | Iterating over directory contents with `enumerate()` |
| Exception handling | Structured `try/except` catching domain errors and gracefully intercepting `KeyboardInterrupt` / `EOFError` |
| File handling | `open()` with `"r"`, `"w"`, `"a"` modes inside `with` blocks |
| pathlib | `Path`, `.exists()`, `.is_file()`, `.is_dir()`, `.rglob()`, `.rename()`, `.relative_to()` |
| Unit testing | `unittest.TestCase` and `tempfile.TemporaryDirectory` for zero-dependency test isolation |
| Type conversion | `int()` for menu choices and dual selection resolution |
| Comparison operators | `==`, `>`, `and`, `not` for validation logic |

## Improvements in v2

- **Separation of Concerns**: Extracted filesystem CRUD logic and security validation into an independent `file_ops.py` domain module (`FileManager`). `main.py` is now purely dedicated to CLI interaction.
- **Dual Selection**: Whenever a file or directory needs to be selected, enter either the displayed item number (e.g. `1`, `2`) or the relative path string directly.
- **Path Traversal & Root Hardening**: Sanitized relative path resolution to neutralize root resets from leading slashes, and explicitly blocked targeting or modifying the workspace root directory itself.
- **Deterministic Listing**: Directories are listed first alphabetically, followed by files alphabetically. Hidden dotfiles and `__pycache__` directories are filtered out automatically.
- **Graceful Termination**: Intercepts Ctrl+C (`KeyboardInterrupt`) and Ctrl+D (`EOFError`) to exit cleanly without dumping stack traces.
- **Unit Test Coverage**: Added an automated test suite under `tests/test_file_ops.py` using Python's built-in `unittest` module, keeping zero external dependencies.

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
