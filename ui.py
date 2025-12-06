"""
Glassmorphic UI for Smart File Organizer using Tkinter.

This module provides a modern, glassmorphic-styled graphical user interface
for the Smart File Organizer. The UI allows users to organize files with a
single button click and displays the results in a summary area.

The interface features:
- Clean, modern glassmorphic design with soft colors
- Display of target folder path
- One-click file organization
- Real-time summary of organization results
"""
import tkinter as tk
from tkinter import scrolledtext, filedialog
from organizer import FileOrganizer


class GlassmorphicUI:
    """
    Tkinter-based glassmorphic user interface.
    
    This class creates and manages a modern UI with glassmorphic styling
    for organizing files. It integrates with the FileOrganizer class to
    provide file organization functionality.
    
    Attributes:
        target_folder (str): Path to the folder being organized.
        organizer (FileOrganizer): Instance of the file organizer.
        root (tk.Tk): Main Tkinter window.
        organize_btn (tk.Button): Button to trigger organization.
        log_area (scrolledtext.ScrolledText): Text area for displaying results.
    """
    
    def __init__(self, target_folder: str):
        """
        Initialize the UI.
        
        Creates the main window, initializes the file organizer, and sets up
        all UI components with glassmorphic styling.
        
        Args:
            target_folder (str): Path to the folder to organize.
        """
        self.target_folder = target_folder
        self.organizer = FileOrganizer(target_folder)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Smart File Organizer")
        self.root.geometry("500x600")
        self.root.configure(bg='#E8F4F8')
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        Create and layout UI components.
        
        Sets up all visual elements including title, folder display,
        organize button, and summary text area with glassmorphic styling.
        """
        
        # Title label at the top
        title = tk.Label(
            self.root,
            text="Smart File Organizer",
            font=("Segoe UI", 24, "bold"),
            bg='#E8F4F8',
            fg='#2C3E50'
        )
        title.pack(pady=20)
        
        # Target folder frame with glassmorphic effect
        folder_frame = tk.Frame(
            self.root,
            bg='#FFFFFF',
            relief=tk.FLAT,
            bd=0
        )
        folder_frame.pack(pady=10, padx=30, fill=tk.X)
        
        folder_label = tk.Label(
            folder_frame,
            text="Target Folder:",
            font=("Segoe UI", 11, "bold"),
            bg='#FFFFFF',
            fg='#34495E'
        )
        folder_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Folder path display and browse button container
        path_container = tk.Frame(folder_frame, bg='#FFFFFF')
        path_container.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.folder_path_label = tk.Label(
            path_container,
            text=self.target_folder,
            font=("Segoe UI", 9),
            bg='#FFFFFF',
            fg='#7F8C8D',
            wraplength=350,
            justify=tk.LEFT
        )
        self.folder_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(
            path_container,
            text="Browse",
            font=("Segoe UI", 9),
            bg='#95A5A6',
            fg='#FFFFFF',
            activebackground='#7F8C8D',
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.browse_folder
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Organize button with gradient effect
        button_frame = tk.Frame(self.root, bg='#E8F4F8')
        button_frame.pack(pady=20)
        
        self.organize_btn = tk.Button(
            button_frame,
            text="Organize Now",
            font=("Segoe UI", 14, "bold"),
            bg='#667EEA',
            fg='#FFFFFF',
            activebackground='#5A67D8',
            activeforeground='#FFFFFF',
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=12,
            cursor="hand2",
            command=self.organize_files
        )
        self.organize_btn.pack()
        
        # Summary/Log area
        log_label = tk.Label(
            self.root,
            text="Summary",
            font=("Segoe UI", 12, "bold"),
            bg='#E8F4F8',
            fg='#2C3E50'
        )
        log_label.pack(pady=(10, 5))
        
        self.log_area = scrolledtext.ScrolledText(
            self.root,
            font=("Consolas", 10),
            bg='#FFFFFF',
            fg='#2C3E50',
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=10,
            height=15,
            wrap=tk.WORD
        )
        self.log_area.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)
        self.log_area.insert(tk.END, "Click 'Organize Now' to start organizing files...\n")
        self.log_area.config(state=tk.DISABLED)
    
    def browse_folder(self):
        """
        Open folder browser dialog to select target folder.
        
        Updates the target folder path and reinitializes the organizer
        with the new path.
        """
        folder = filedialog.askdirectory(
            title="Select Folder to Organize",
            initialdir=self.target_folder
        )
        
        if folder:  # If user selected a folder (didn't cancel)
            self.target_folder = folder
            self.organizer = FileOrganizer(folder)
            self.folder_path_label.config(text=folder)
            
            # Update log area
            self.log_area.config(state=tk.NORMAL)
            self.log_area.delete(1.0, tk.END)
            self.log_area.insert(tk.END, f"Target folder changed to:\n{folder}\n\nClick 'Organize Now' to start organizing files...")
            self.log_area.config(state=tk.DISABLED)
    
    def organize_files(self):
        """
        Trigger file organization and display results.
        
        This method is called when the user clicks the "Organize Now" button.
        It disables the button during processing, runs the organization,
        displays results, and re-enables the button when complete.
        
        Errors during organization are caught and displayed in the log area.
        """
        # Disable button and update UI to show processing state
        self.organize_btn.config(state=tk.DISABLED, text="Organizing...")
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.insert(tk.END, "Starting organization...\n\n")
        self.root.update()  # Force UI update
        
        try:
            # Run the file organization
            results = self.organizer.organize()
            self.display_summary(results)
        except Exception as e:
            # Display any errors that occur
            self.log_area.insert(tk.END, f"\nError: {e}\n")
        finally:
            # Re-enable button and lock log area
            self.organize_btn.config(state=tk.NORMAL, text="Organize Now")
            self.log_area.config(state=tk.DISABLED)
    
    def display_summary(self, results: dict):
        """
        Display organization summary in the log area.
        
        Formats and displays the results of the file organization, showing
        the count of files moved to each category and the total count.
        
        Args:
            results (dict): Dictionary mapping category names to file counts.
        """
        # Calculate total files organized
        total = sum(results.values())
        
        # Display header
        self.log_area.insert(tk.END, "Organization Complete!\n")
        self.log_area.insert(tk.END, "=" * 40 + "\n\n")
        
        # Display count for each category that has files
        for category, count in results.items():
            if count > 0:
                self.log_area.insert(tk.END, f"  {category}: {count} file(s)\n")
        
        # Display footer with total
        self.log_area.insert(tk.END, "\n" + "=" * 40 + "\n")
        self.log_area.insert(tk.END, f"Total files organized: {total}\n")
    
    def run(self):
        """
        Start the UI main loop.
        
        This method starts the Tkinter event loop, displaying the window
        and handling user interactions.
        """
        self.root.mainloop()
