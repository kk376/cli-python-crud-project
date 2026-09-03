from dataclasses import dataclass
from pathlib import Path


class FileOpsError(Exception):
    """Base exception for file operations."""
    pass


class PathSecurityError(FileOpsError):
    """Raised when an operation attempts path traversal outside the workspace."""
    pass


class ItemNotFoundError(FileOpsError):
    """Raised when a requested file or directory does not exist."""
    pass


class ItemAlreadyExistsError(FileOpsError):
    """Raised when an item already exists at the target path."""
    pass


class DirectoryNotEmptyError(FileOpsError):
    """Raised when attempting to delete a non-empty directory."""
    pass


class InvalidTargetError(FileOpsError):
    """Raised when targeting the workspace root itself or an invalid path."""
    pass


@dataclass(frozen=True)
class WorkspaceItem:
    """Represents a file or directory inside the workspace."""
    path: Path
    rel_path: Path
    is_dir: bool


class FileManager:
    """Manages file and directory CRUD operations safely isolated inside a workspace directory."""

    def __init__(self, workspace_dir: Path | str = "workspace"):
        self.workspace_dir = Path(workspace_dir).resolve()
        self.ensure_workspace()

    def ensure_workspace(self) -> Path:
        """Create and return the resolved workspace directory."""
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        return self.workspace_dir

    def resolve_safe_path(self, user_input: str) -> Path:
        """
        Resolve and validate that the requested path strictly resides within the workspace.
        Prevents path traversal vulnerabilities (CWE-22 / CWE-23) and protects workspace root.
        """
        cleaned = user_input.strip()
        if not cleaned:
            raise InvalidTargetError("Path cannot be empty.")

        # Strip leading slashes and backslashes to avoid absolute filesystem root resets
        stripped = cleaned.lstrip("/\\")
        if not stripped:
            raise InvalidTargetError("Cannot target the workspace root itself.")

        target = (self.workspace_dir / stripped).resolve()

        try:
            target.relative_to(self.workspace_dir)
        except ValueError:
            raise PathSecurityError("Path traversal outside workspace is forbidden.")

        if target == self.workspace_dir:
            raise InvalidTargetError("Cannot target the workspace root itself.")

        return target

    def list_items(self) -> list[WorkspaceItem]:
        """
        Return all files and directories inside the workspace, filtering out hidden
        items (.git, .gitignore, etc.) and __pycache__, sorted deterministically.
        """
        self.ensure_workspace()
        items: list[WorkspaceItem] = []

        for p in self.workspace_dir.rglob("*"):
            rel = p.relative_to(self.workspace_dir)
            # Filter hidden entries and python bytecode caches
            if any(part.startswith(".") or part == "__pycache__" for part in rel.parts):
                continue
            items.append(WorkspaceItem(path=p, rel_path=rel, is_dir=p.is_dir()))

        # Sort: directories first alphabetically, then files alphabetically
        items.sort(key=lambda item: (not item.is_dir, str(item.rel_path).lower()))
        return items

    def resolve_item_input(self, user_input: str, items: list[WorkspaceItem] | None = None) -> Path:
        """
        Resolve user input either from a 1-based index (e.g. '1', '2') or a path string.
        """
        cleaned = user_input.strip()
        if not cleaned:
            raise InvalidTargetError("Input cannot be empty.")

        if items is None:
            items = self.list_items()

        # Check if user entered a valid 1-based index
        if cleaned.isdigit():
            idx = int(cleaned)
            if 1 <= idx <= len(items):
                return items[idx - 1].path

        # Otherwise resolve as relative path
        return self.resolve_safe_path(cleaned)

    def create_file(self, target_input: str, content: str) -> Path:
        """Create a new file with the specified content inside the workspace."""
        p = self.resolve_safe_path(target_input)
        if p.exists():
            raise ItemAlreadyExistsError(f"File or folder already exists: {p.name}")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return p

    def read_file(self, target_input: str, items: list[WorkspaceItem] | None = None) -> str:
        """Read and return text content from an existing file."""
        p = self.resolve_item_input(target_input, items)
        if not p.exists() or not p.is_file():
            raise ItemNotFoundError(f"File does not exist: {p.name}")
        return p.read_text(encoding="utf-8")

    def rename_file(self, source_input: str, new_name_input: str, items: list[WorkspaceItem] | None = None) -> tuple[Path, Path]:
        """Rename an existing file to a new safe path."""
        source = self.resolve_item_input(source_input, items)
        if not source.exists() or not source.is_file():
            raise ItemNotFoundError(f"Source file does not exist: {source.name}")

        dest = self.resolve_safe_path(new_name_input)
        if dest.exists():
            raise ItemAlreadyExistsError(f"A file or folder with that name already exists: {dest.name}")

        dest.parent.mkdir(parents=True, exist_ok=True)
        source.rename(dest)
        return source, dest

    def overwrite_file(self, target_input: str, content: str, items: list[WorkspaceItem] | None = None) -> Path:
        """Overwrite an existing file's contents entirely."""
        p = self.resolve_item_input(target_input, items)
        if not p.exists() or not p.is_file():
            raise ItemNotFoundError(f"File does not exist: {p.name}")
        p.write_text(content, encoding="utf-8")
        return p

    def append_file(self, target_input: str, content: str, items: list[WorkspaceItem] | None = None) -> Path:
        """Append text to the end of an existing file."""
        p = self.resolve_item_input(target_input, items)
        if not p.exists() or not p.is_file():
            raise ItemNotFoundError(f"File does not exist: {p.name}")
        with open(p, "a", encoding="utf-8") as f:
            f.write(" " + content)
        return p

    def delete_file(self, target_input: str, items: list[WorkspaceItem] | None = None) -> Path:
        """Delete an existing file."""
        p = self.resolve_item_input(target_input, items)
        if not p.exists() or not p.is_file():
            raise ItemNotFoundError(f"File does not exist: {p.name}")
        p.unlink()
        return p

    def create_folder(self, target_input: str) -> Path:
        """Create a new folder inside the workspace."""
        p = self.resolve_safe_path(target_input)
        if p.exists():
            raise ItemAlreadyExistsError(f"A file or folder with that name already exists: {p.name}")
        p.mkdir(parents=True, exist_ok=True)
        return p

    def delete_folder(self, target_input: str, items: list[WorkspaceItem] | None = None) -> Path:
        """Delete an empty directory."""
        p = self.resolve_item_input(target_input, items)
        if not p.exists() or not p.is_dir():
            raise ItemNotFoundError(f"Folder does not exist: {p.name}")

        contents = list(p.iterdir())
        if len(contents) > 0:
            raise DirectoryNotEmptyError(f"Folder '{p.name}' is not empty. Remove its contents first.")

        p.rmdir()
        return p
