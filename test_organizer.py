"""Tests for FileOrganizer functionality"""
import os
import tempfile
import shutil
from pathlib import Path
from organizer import FileOrganizer


def test_scan_files():
    """Test that scan_files only returns files from root directory, not subdirectories"""
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Create files in root directory
        (test_dir / "file1.txt").touch()
        (test_dir / "file2.jpg").touch()
        (test_dir / "file3.pdf").touch()
        
        # Create a subdirectory with files (should be ignored)
        subdir = test_dir / "subdir"
        subdir.mkdir()
        (subdir / "nested_file.txt").touch()
        
        # Initialize organizer and scan
        organizer = FileOrganizer(str(test_dir))
        files = organizer.scan_files()
        
        # Verify results
        assert len(files) == 3, f"Expected 3 files, got {len(files)}"
        
        # Verify only root files are included
        file_names = {f.name for f in files}
        assert "file1.txt" in file_names
        assert "file2.jpg" in file_names
        assert "file3.pdf" in file_names
        assert "nested_file.txt" not in file_names, "Subdirectory files should not be included"
        
        # Verify subdirectory itself is not included
        assert "subdir" not in file_names, "Subdirectories should not be included"
        
        print("✓ scan_files() correctly scans only root directory files")
        print(f"✓ Found {len(files)} files in root directory")
        print(f"✓ Correctly excluded subdirectory and its contents")


def test_categorize_file():
    """Test that categorize_file correctly maps extensions to categories"""
    with tempfile.TemporaryDirectory() as tmpdir:
        organizer = FileOrganizer(tmpdir)
        
        # Test Images
        assert organizer.categorize_file("photo.jpg") == "Images"
        assert organizer.categorize_file("image.PNG") == "Images"  # Test case insensitivity
        assert organizer.categorize_file("graphic.svg") == "Images"
        
        # Test Documents
        assert organizer.categorize_file("report.pdf") == "Documents"
        assert organizer.categorize_file("essay.docx") == "Documents"
        assert organizer.categorize_file("notes.txt") == "Documents"
        
        # Test Archives
        assert organizer.categorize_file("backup.zip") == "Archives"
        assert organizer.categorize_file("data.rar") == "Archives"
        
        # Test Videos
        assert organizer.categorize_file("movie.mp4") == "Videos"
        assert organizer.categorize_file("clip.mkv") == "Videos"
        
        # Test Audio
        assert organizer.categorize_file("song.mp3") == "Audio"
        assert organizer.categorize_file("sound.wav") == "Audio"
        
        # Test Code Files
        assert organizer.categorize_file("script.py") == "Code Files"
        assert organizer.categorize_file("app.js") == "Code Files"
        
        # Test files without extensions (should go to Others)
        assert organizer.categorize_file("README") == "Others"
        assert organizer.categorize_file("Makefile") == "Others"
        
        # Test unknown extensions (should go to Others)
        assert organizer.categorize_file("data.xyz") == "Others"
        assert organizer.categorize_file("file.unknown") == "Others"
        
        print("✓ categorize_file() correctly maps extensions to categories")
        print("✓ Handles case-insensitive extensions")
        print("✓ Files without extensions go to 'Others'")
        print("✓ Unknown extensions go to 'Others'")


def test_organize():
    """Test that organize() creates folders, moves files, and returns correct counts"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Create test files in root directory
        (test_dir / "photo.jpg").touch()
        (test_dir / "image.png").touch()
        (test_dir / "report.pdf").touch()
        (test_dir / "notes.txt").touch()
        (test_dir / "backup.zip").touch()
        (test_dir / "script.py").touch()
        (test_dir / "song.mp3").touch()
        (test_dir / "video.mp4").touch()
        (test_dir / "README").touch()  # No extension - should go to Others
        
        # Initialize organizer and organize files
        organizer = FileOrganizer(str(test_dir))
        results = organizer.organize()
        
        # Verify category folders were created
        assert (test_dir / "Images").exists(), "Images folder should be created"
        assert (test_dir / "Documents").exists(), "Documents folder should be created"
        assert (test_dir / "Archives").exists(), "Archives folder should be created"
        assert (test_dir / "Code Files").exists(), "Code Files folder should be created"
        assert (test_dir / "Audio").exists(), "Audio folder should be created"
        assert (test_dir / "Videos").exists(), "Videos folder should be created"
        assert (test_dir / "Others").exists(), "Others folder should be created"
        
        # Verify files were moved to correct folders
        assert (test_dir / "Images" / "photo.jpg").exists()
        assert (test_dir / "Images" / "image.png").exists()
        assert (test_dir / "Documents" / "report.pdf").exists()
        assert (test_dir / "Documents" / "notes.txt").exists()
        assert (test_dir / "Archives" / "backup.zip").exists()
        assert (test_dir / "Code Files" / "script.py").exists()
        assert (test_dir / "Audio" / "song.mp3").exists()
        assert (test_dir / "Videos" / "video.mp4").exists()
        assert (test_dir / "Others" / "README").exists()
        
        # Verify files are no longer in root directory
        root_files = [f for f in test_dir.iterdir() if f.is_file()]
        assert len(root_files) == 0, "All files should be moved from root directory"
        
        # Verify results dictionary has correct counts
        assert results["Images"] == 2, f"Expected 2 images, got {results['Images']}"
        assert results["Documents"] == 2, f"Expected 2 documents, got {results['Documents']}"
        assert results["Archives"] == 1, f"Expected 1 archive, got {results['Archives']}"
        assert results["Code Files"] == 1, f"Expected 1 code file, got {results['Code Files']}"
        assert results["Audio"] == 1, f"Expected 1 audio file, got {results['Audio']}"
        assert results["Videos"] == 1, f"Expected 1 video file, got {results['Videos']}"
        assert results["Others"] == 1, f"Expected 1 other file, got {results['Others']}"
        
        print("✓ organize() creates category folders correctly")
        print("✓ Files are moved to appropriate category folders")
        print("✓ Files are removed from root directory")
        print("✓ Results dictionary contains correct counts")


def test_organize_name_conflicts():
    """Test that organize() handles file name conflicts by adding numeric suffixes"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        
        # Create multiple files with the same name
        (test_dir / "photo.jpg").write_text("file1")
        
        # Pre-create the Images folder with an existing photo.jpg
        images_folder = test_dir / "Images"
        images_folder.mkdir()
        (images_folder / "photo.jpg").write_text("existing")
        
        # Organize files
        organizer = FileOrganizer(str(test_dir))
        results = organizer.organize()
        
        # Verify both files exist with different names
        assert (images_folder / "photo.jpg").exists(), "Original file should exist"
        assert (images_folder / "photo_1.jpg").exists(), "Conflicting file should have suffix"
        
        # Verify content is preserved
        assert (images_folder / "photo.jpg").read_text() == "existing"
        assert (images_folder / "photo_1.jpg").read_text() == "file1"
        
        print("✓ organize() handles name conflicts with numeric suffixes")
        print("✓ Both original and conflicting files are preserved")


if __name__ == "__main__":
    test_scan_files()
    test_categorize_file()
    test_organize()
    test_organize_name_conflicts()
    print("\nAll tests passed!")
