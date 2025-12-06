# 📁 Smart File Organizer

A Python-based file organization tool that automatically categorizes and organizes files by their extensions. Features a beautiful glassmorphic UI and a REST API for automation.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎨 **Beautiful Glassmorphic UI** - Modern, clean interface built with Tkinter
- 📂 **Browse & Select** - Choose any folder to organize with a folder browser
- 🔄 **Smart Categorization** - Automatically sorts files into 7 categories
- 🚀 **REST API** - Automate file organization via HTTP endpoints
- 🛡️ **Safe Operation** - Only processes root-level files, preserves subfolders
- ⚡ **Conflict Handling** - Automatically renames duplicate files
- 🧪 **Well Tested** - Comprehensive test suite included

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### UI Mode (Recommended)

Launch the graphical interface:
```bash
python main.py
```

1. Click **Browse** to select a folder
2. Click **Organize Now** to sort files
3. View the summary of organized files

### API Mode

Start the REST API server:
```bash
python main.py --api
```

API will be available at `http://localhost:8000`

#### API Endpoints

**Organize files:**
```bash
curl -X POST http://localhost:8000/organize
```

**With custom folder:**
```bash
curl -X POST http://localhost:8000/organize \
  -H "Content-Type: application/json" \
  -d '{"target_folder": "/path/to/folder"}'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

## 📋 File Categories

The organizer sorts files into these categories:

| Category | Extensions |
|----------|-----------|
| 📷 **Images** | .jpg, .jpeg, .png, .gif, .svg, .webp |
| 📄 **Documents** | .pdf, .docx, .txt, .pptx, .xlsx |
| 📦 **Archives** | .zip, .rar, .7z |
| 🎬 **Videos** | .mp4, .mkv, .mov |
| 🎵 **Audio** | .mp3, .wav |
| 💻 **Code Files** | .py, .js, .java, .html, .css |
| 📎 **Others** | Everything else |

## 🧪 Running Tests

Run the test suite:
```bash
python test_organizer.py
```

## 🏗️ Project Structure

```
smart-file-organizer/
├── organizer.py       # Core file organization logic
├── ui.py             # Glassmorphic Tkinter UI
├── api.py            # Flask REST API
├── main.py           # Entry point with mode selection
├── test_organizer.py # Test suite
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

## ⚙️ How It Works

1. **Scans** the target folder for files (root level only)
2. **Categorizes** each file based on its extension
3. **Creates** category folders if they don't exist
4. **Moves** files to their respective category folders
5. **Handles** naming conflicts by adding numeric suffixes

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

Created with ❤️ by [Your Name]

## ⚠️ Disclaimer

Always backup important files before organizing. While the tool is designed to be safe, it's best to test on non-critical folders first.
