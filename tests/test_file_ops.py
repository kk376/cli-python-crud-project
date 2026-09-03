import tempfile
import unittest
from pathlib import Path

from file_ops import (
    DirectoryNotEmptyError,
    FileManager,
    InvalidTargetError,
    ItemAlreadyExistsError,
    ItemNotFoundError,
    PathSecurityError,
)


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace_path = Path(self.temp_dir.name) / "workspace"
        self.mgr = FileManager(self.workspace_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_ensure_workspace_creates_directory(self):
        self.assertTrue(self.workspace_path.exists())
        self.assertTrue(self.workspace_path.is_dir())

    def test_create_and_read_file(self):
        created = self.mgr.create_file("hello.txt", "Hello World")
        self.assertTrue(created.exists())
        content = self.mgr.read_file("hello.txt")
        self.assertEqual(content, "Hello World")

    def test_create_nested_file_creates_parents(self):
        created = self.mgr.create_file("docs/deep/notes.txt", "Deep content")
        self.assertTrue(created.exists())
        self.assertEqual(self.mgr.read_file("docs/deep/notes.txt"), "Deep content")

    def test_create_file_already_exists(self):
        self.mgr.create_file("existing.txt", "v1")
        with self.assertRaises(ItemAlreadyExistsError):
            self.mgr.create_file("existing.txt", "v2")

    def test_read_file_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.mgr.read_file("missing.txt")

    def test_overwrite_file(self):
        self.mgr.create_file("overwrite.txt", "initial")
        self.mgr.overwrite_file("overwrite.txt", "overwritten")
        self.assertEqual(self.mgr.read_file("overwrite.txt"), "overwritten")

    def test_append_file(self):
        self.mgr.create_file("log.txt", "start")
        self.mgr.append_file("log.txt", "finish")
        self.assertEqual(self.mgr.read_file("log.txt"), "start finish")

    def test_rename_file(self):
        self.mgr.create_file("old.txt", "data")
        self.mgr.rename_file("old.txt", "new.txt")
        self.assertFalse((self.workspace_path / "old.txt").exists())
        self.assertTrue((self.workspace_path / "new.txt").exists())
        self.assertEqual(self.mgr.read_file("new.txt"), "data")

    def test_rename_collision_fails(self):
        self.mgr.create_file("file1.txt", "a")
        self.mgr.create_file("file2.txt", "b")
        with self.assertRaises(ItemAlreadyExistsError):
            self.mgr.rename_file("file1.txt", "file2.txt")

    def test_delete_file(self):
        self.mgr.create_file("delete_me.txt", "bye")
        self.mgr.delete_file("delete_me.txt")
        self.assertFalse((self.workspace_path / "delete_me.txt").exists())

    def test_create_and_delete_empty_folder(self):
        folder = self.mgr.create_folder("my_folder")
        self.assertTrue(folder.exists())
        self.assertTrue(folder.is_dir())
        self.mgr.delete_folder("my_folder")
        self.assertFalse(folder.exists())

    def test_delete_non_empty_folder_fails(self):
        self.mgr.create_folder("parent_dir")
        self.mgr.create_file("parent_dir/child.txt", "inside")
        with self.assertRaises(DirectoryNotEmptyError):
            self.mgr.delete_folder("parent_dir")

    def test_list_items_filtering_and_sorting(self):
        # Create directories and files, plus hidden files and pycache
        self.mgr.create_folder("beta_dir")
        self.mgr.create_folder("alpha_dir")
        self.mgr.create_file("beta_dir/zebra.txt", "z")
        self.mgr.create_file("alpha.txt", "a")

        # Create hidden directory and files directly on filesystem
        hidden_dir = self.workspace_path / ".hidden_folder"
        hidden_dir.mkdir()
        (hidden_dir / "secret.txt").write_text("secret")
        (self.workspace_path / ".DS_Store").write_text("mac")

        pycache_dir = self.workspace_path / "__pycache__"
        pycache_dir.mkdir()
        (pycache_dir / "cache.pyc").write_text("pyc")

        items = self.mgr.list_items()
        rel_paths = [str(item.rel_path) for item in items]

        # Ensure hidden files and pycache are excluded
        self.assertNotIn(".hidden_folder", rel_paths)
        self.assertNotIn(".DS_Store", rel_paths)
        self.assertNotIn("__pycache__", rel_paths)

        # Ensure directories come first, sorted alphabetically, followed by files
        self.assertEqual(rel_paths[0], "alpha_dir")
        self.assertEqual(rel_paths[1], "beta_dir")
        self.assertIn("alpha.txt", rel_paths)
        self.assertIn("beta_dir/zebra.txt", rel_paths)

    def test_dual_selection_by_index_and_name(self):
        self.mgr.create_file("item_a.txt", "A")
        self.mgr.create_file("item_b.txt", "B")
        items = self.mgr.list_items()

        # By name
        read_a = self.mgr.read_file("item_a.txt", items)
        self.assertEqual(read_a, "A")

        # By 1-based index
        read_idx_1 = self.mgr.read_file("1", items)
        self.assertEqual(read_idx_1, "A")

        read_idx_2 = self.mgr.read_file("2", items)
        self.assertEqual(read_idx_2, "B")

    def test_path_traversal_outside_workspace_rejected(self):
        with self.assertRaises(PathSecurityError):
            self.mgr.resolve_safe_path("../escaped.txt")

        with self.assertRaises(PathSecurityError):
            self.mgr.resolve_safe_path("../../etc/passwd")

    def test_workspace_root_protection(self):
        # Prevent user from operating on the workspace root itself
        with self.assertRaises(InvalidTargetError):
            self.mgr.resolve_safe_path(".")

        with self.assertRaises(InvalidTargetError):
            self.mgr.resolve_safe_path("./")

        with self.assertRaises(InvalidTargetError):
            self.mgr.resolve_safe_path("")

        with self.assertRaises(InvalidTargetError):
            self.mgr.delete_folder(".")


if __name__ == "__main__":
    unittest.main()
