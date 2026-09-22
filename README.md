# Mock Environment Generator

A lightweight desktop utility to quickly generate nested dummy folder structures and test files with customizable depths, counts, sizes, and content types.

---

## Features

- **Custom Directory Depth**: Control how deep subfolder hierarchies can go.
- **Randomized File & Folder Counts**: Set minimum and maximum ranges for folders and files per level.
- **Configurable Extensions**: Specify file formats (e.g., `.txt`, `.log`, `.dat`, `.bin`).
- **Flexible Content Strategies**:
  - `Zero Bytes (Instant)`: Fast allocation using sparse/null bytes.
  - `Random Bytes`: Generates raw random byte sequences.
  - `Repeated ASCII Text`: Fills files with readable alphanumeric text.
- **Archive Export**: Option to compress the generated directory structure directly into a `.zip` archive.
- **GUI Interface**: Easy-to-use graphical interface powered by Dear PyGui.

---

## Installation

### 1. Requirements

- **Python 3.8+** installed on your system.

### 2. Install Dependencies

Install the required GUI dependency via pip:

```bash
pip install dearpygui
```

*(All other modules used (`os`, `random`, `string`, `pathlib`, `typing`, `zipfile`) are built into Python standard libraries).*

### 3. File Setup

Ensure your project files are in the same folder:

```text
├── config.py        # Configuration data structures and defaults
├── gui.py           # GUI interface module (Dear PyGui layout & inputs)
├── main.py          # Application entry point and generation logic
└── popup.py         # Modal dialogs and status popup windows
```

---

## How to Run

Launch the script from your terminal or command prompt:

```bash
python main.py
```

1. The configuration window will pop up.
2. Adjust your settings:
   - **Root Directory**: Where the generated folders and files will be placed.
   - **Max Depth**: How deep the folder nesting should go.
   - **Subfolder Range (Min / Max)**: How many subfolders to create inside each folder.
   - **Files Per Folder (Min / Max)**: Range of dummy files to place in each directory.
   - **File Size (Min / Max in KB)**: Target size range for generated files.
   - **File Extensions**: Extensions to randomly assign to created files.
   - **Fill Content**: How the dummy data should be populated.
   - **Compress to ZIP**: Toggle to package output into a ZIP archive.
3. Click the submit button to begin generation.
4. Watch the progress dialog and status popups for generation completion.

---

## License

This project is open-source and free to use for testing, benchmarking, and development purposes.