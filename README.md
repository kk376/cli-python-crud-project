# CLI Python CRUD Project

A command-line file manager built in Python. It lets you create, read, update, and delete files right from your terminal — all through a simple numbered menu.

I built this as a hands-on project while learning Python, specifically to put file handling, functions, exception handling, and `pathlib` into practice.

This project is part of my [AI/ML Journey](https://github.com/Kk376/ai-ml-journey), where I'm documenting everything I learn from Python basics through to machine learning. You can follow along there to see what I've covered and where I'm headed next.

## What It Does

When you run the program, you get four options:

```
Press 1 to create a file
Press 2 to read a file
Press 3 to update a file
Press 4 to delete a file
```

Each option walks you through the operation step by step. Before every action, the program lists all files and folders in the current directory so you can see what you're working with.

### Create

Prompts you for a filename and the content you want to write. If the file already exists, it tells you so instead of overwriting it.

### Read

Pick a file by name, and it prints the full contents to the terminal.

### Update

Three sub-options here:

1. **Rename** the file
2. **Overwrite** the file's contents entirely (with a warning)
3. **Append** new content to the end of the file

### Delete

Removes the file after confirming it exists. Uses `os.remove()` under the hood.

## Getting Started

### Prerequisites

- Python 3.6 or higher (for f-strings and `pathlib` support)

No external dependencies — everything uses the standard library.

### Running It

```bash
git clone https://github.com/Kk376/cli-python-crud-project.git
cd cli-python-crud-project
python main.py
```

That's it. Follow the prompts.

## Project Structure

```
cli-python-crud-project/
├── main.py        # All the logic lives here
└── README.md
```

Single-file project. The code is organized into four functions (`createfile`, `readfile`, `updatefile`, `deletefile`) plus a helper (`ReadFileAndFolder`) that lists directory contents.

## Python Concepts Used

This project pulls together most of what I've covered so far in my Python learning:

| Concept | Where It Shows Up |
|---|---|
| Variables | Storing user input, file paths, menu choices |
| Data types | Strings for filenames/content, integers for menu selection |
| Input/Output | `input()` for prompts, `print()` for feedback |
| String formatting | f-strings throughout for error messages and display |
| If/Else | Menu routing, file existence checks, update sub-menu |
| Functions | Each CRUD operation is its own function |
| For loops | Iterating over directory contents with `enumerate()` |
| Exception handling | Every function is wrapped in `try/except` |
| File handling | `open()` with `"r"`, `"w"`, `"a"` modes, `pathlib.Path` |
| Type conversion | `int(input(...))` for menu choices |
| Operators | Comparison (`==`, `not`), logical checks |

## Limitations

A few things this doesn't handle yet:

- No loop back to the menu after an operation — the program exits after one action
- Typing a non-integer at the menu prompt will crash with a `ValueError`
- Works on files in the current directory only (no absolute path support)
- Folder creation/deletion isn't supported

These are all things I could revisit later, especially once I get into OOP and can restructure the code with classes.

## What I Learned Building This

File handling was the main goal, but I ended up touching almost every concept I'd studied before. Writing the update function with its sub-menu was probably the trickiest part — juggling multiple file modes (`"w"` vs `"a"`) and making sure `Path.rename()` worked correctly took some trial and error.

The `pathlib` module turned out to be cleaner than raw `os.path` calls for most things, though I still needed `os.remove()` for deletion.

## License

Open source. Do whatever you want with it.
