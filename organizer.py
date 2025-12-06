"""
Core file organization logic for Smart File Organizer.

This module provides the FileOrganizer class which handles:
- Scanning files in a target directory
- Categorizing files based on their extensions
- Organizing files into category-specific folders

The organizer only processes files in the root directory and ignores subdirectories.
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List


class FileOrganizer:
    """
    Handles file scanning, categorization, and organization.
    
    This class provides methods to scan a directory for files, categorize them
    based on their extensions, and organize them into category-specific folders.
    
    Attributes:
        CATEGORIES (dict): Mapping of category names to lists of file extensions.
        target_folder (Path): The directory path to organize.
    """
    
    # File extension to category mapping
    CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'],
        'Documents': ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
        'Archives': ['.zip', '.rar', '.7z'],
        'Videos': ['.mp4', '.mkv', '.mov'],
        'Audio': ['.mp3', '.wav'],
        'Code Files': ['.py', '.js', '.java', '.html', '.css'],
    }
    
    def __init__(self, target_folder: str):
        """
        Initialize the file organizer.
        
        Args:
            target_folder (str): Path to the folder to organize.
            
        Raises:
            ValueError: If the target folder does not exist.
        """
        self.target_folder = Path(target_folder)
        if not self.target_folder.exists():
            raise ValueError(f"Target folder does not exist: {target_folder}")
    
    def scan_files(self) -> List[Path]:
        """
        Scan only the root directory for files (ignore subdirectories).
        
        This method iterates through items in the target folder and collects
        only files, ignoring any subdirectories.
        
        Returns:
            List[Path]: List of file paths in the root directory.
            
        Note:
            Permission errors are caught and printed but don't stop execution.
        """
        files = []
        try:
            # Iterate through all items in the target folder
            for item in self.target_folder.iterdir():
                # Only include files, not directories
                if item.is_file():
                    files.append(item)
        except PermissionError as e:
            print(f"Permission denied: {e}")
        return files
    
    def categorize_file(self, filename: str) -> str:
        """
        Categorize a file based on its extension.
        
        Files are categorized by matching their extension against the CATEGORIES
        mapping. Files without extensions or with unrecognized extensions are
        placed in the 'Others' category.
        
        Args:
            filename (str): Name of the file to categorize.
            
        Returns:
            str: Category name (e.g., 'Images', 'Documents', 'Others').
        """
        # Extract file extension and convert to lowercase for case-insensitive matching
        ext = Path(filename).suffix.lower()
        
        # Check each category for a matching extension
        for category, extensions in self.CATEGORIES.items():
            if ext in extensions:
                return category
        
        # Default to 'Others' for unrecognized or missing extensions
        return 'Others'
    
    def organize(self) -> Dict[str, int]:
        """
        Organize files into category folders.
        
        This method scans the target folder, categorizes each file, creates
        category folders as needed, and moves files to their appropriate
        category folders. If a file with the same name already exists in the
        destination, a numeric suffix is added to avoid conflicts.
        
        Returns:
            Dict[str, int]: Dictionary mapping category names to the count of
                           files moved to each category.
                           
        Note:
            Errors during file operations are caught and printed but don't
            stop the overall organization process.
        """
        # Scan for files in the root directory
        files = self.scan_files()
        
        # Initialize results dictionary with all categories
        results = {category: 0 for category in self.CATEGORIES.keys()}
        results['Others'] = 0
        
        # Process each file
        for file_path in files:
            try:
                # Determine which category this file belongs to
                category = self.categorize_file(file_path.name)
                
                # Create category folder if it doesn't exist
                category_folder = self.target_folder / category
                category_folder.mkdir(exist_ok=True)
                
                # Prepare destination path
                destination = category_folder / file_path.name
                
                # Handle name conflicts by adding numeric suffix
                if destination.exists():
                    base = file_path.stem  # Filename without extension
                    ext = file_path.suffix  # File extension
                    counter = 1
                    # Keep incrementing counter until we find an available name
                    while destination.exists():
                        destination = category_folder / f"{base}_{counter}{ext}"
                        counter += 1
                
                # Move the file to its category folder
                shutil.move(str(file_path), str(destination))
                results[category] += 1
                
            except Exception as e:
                # Log error but continue processing other files
                print(f"Error moving {file_path.name}: {e}")
                continue
        
        return results
