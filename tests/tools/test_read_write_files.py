import os
from unittest.mock import patch
from tools import read_write_files

@patch("builtins.input", return_value="y")
def test_write_file_create_file(mock_input, tmp_path, monkeypatch):
    monkeypatch.setattr(read_write_files, "BASE_DIR", str(tmp_path))
    read_write_files.write_file("test.txt", "hello")
    assert read_write_files.read_file("test.txt") == "hello"

@patch("builtins.input", return_value="y")
def test_write_file_blocks_path_traversal(mock_input, tmp_path, monkeypatch):
    monkeypatch.setattr(read_write_files, "BASE_DIR", str(tmp_path))
    read_write_files.write_file("../escape.txt", "malicious content")
    assert not os.path.exists(tmp_path.parent / "escape.txt")
    assert (tmp_path / "escape.txt").exists()

@patch("builtins.input", return_value="y")
def test_read_file(mock_input, tmp_path, monkeypatch):
    monkeypatch.setattr(read_write_files, "BASE_DIR", str(tmp_path))
    read_write_files.write_file("test.txt", "hello")
    assert read_write_files.read_file("test.txt") == "hello" 

@patch("builtins.input", return_value="y")
def test_read_file_not_exists(mock_input, tmp_path, monkeypatch):
    monkeypatch.setattr(read_write_files, "BASE_DIR", str(tmp_path))
    assert read_write_files.read_file("test.txt") == "File doesn't exist"