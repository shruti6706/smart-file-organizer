"""
Main entry point for Smart File Organizer.
"""
import sys
import os
from pathlib import Path
from ui import GlassmorphicUI
from api import app

# Default target folder - uses user's home directory
TARGET_FOLDER = str(Path.home() / "Desktop")


def main():
    """Main entry point with mode selection."""
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == '--api':
            print("Starting API mode...")
            print(f"Target folder: {TARGET_FOLDER}")
            print("API available at: http://localhost:8000")
            print("Endpoint: POST /organize")
            app.run(debug=False, host='0.0.0.0', port=8000)
            
        elif mode == '--ui':
            print("Starting UI mode...")
            ui = GlassmorphicUI(TARGET_FOLDER)
            ui.run()
            
        else:
            print("Invalid mode. Use --ui or --api")
            sys.exit(1)
    else:
        # Default to UI mode
        print("Starting UI mode (default)...")
        ui = GlassmorphicUI(TARGET_FOLDER)
        ui.run()


if __name__ == '__main__':
    main()
