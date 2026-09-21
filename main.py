import os
import random
import string
from pathlib import Path
from typing import List
from gui import get_config_ui

debug = False

# ==========================================
# DEFAULT VARIABLES
# ==========================================
ROOT_DIR: str = r"./mock_environment"

# Subfolder Structure
MAX_DEPTH: int = 4                # 0 = only root folder, 1 = root + direct children, etc.
MIN_SUBFOLDERS: int = 1           # Min subfolders created inside each directory
MAX_SUBFOLDERS: int = 3           # Max subfolders created inside each directory

# Files
MIN_FILES_PER_FOLDER: int = 2     # Min files placed inside each directory
MAX_FILES_PER_FOLDER: int = 6     # Max files placed inside each directory
FILE_EXTENSIONS: List[str] = [".txt", ".log", ".dat", ".bin"]
MIN_FILE_SIZE_KB: int = 4         # Min file size
MAX_FILE_SIZE_KB: int = 64        # Max file size

# Content strategy
FILL_CONTENT: str = "Zero Bytes (Instant)"  # Options: "Zero Bytes (Instant)", "Random Bytes", "Repeated ASCII Text"

# ==========================================
# CORE LOGIC
# ==========================================
def generate_file_content(fill_mode: str, size_bytes: int) -> bytes:
    """Generates file content based on the chosen fill mode."""
    if size_bytes <= 0:
        return b""

    if fill_mode == "Random Bytes":
        return os.urandom(size_bytes)

    elif fill_mode == "Repeated ASCII Text":
        charset = string.ascii_letters + string.digits + " \n"
        sample_chars = "".join(random.choices(charset, k=1024)).encode("utf-8")
        repeats = (size_bytes // len(sample_chars)) + 1
        return (sample_chars * repeats)[:size_bytes]

    # Default: "Zero Bytes (Instant)"
    return b"\x00" * size_bytes


def create_dummy_file(file_path: Path, fill_mode: str, min_kb: int, max_kb: int) -> None:
    """Writes a dummy file with a randomized size between min_kb and max_kb."""
    min_size = max(0, min_kb)
    max_size = max(min_size, max_kb)
    target_bytes = random.randint(min_size, max_size) * 1024

    if fill_mode == "Zero Bytes (Instant)":
        with open(file_path, "wb") as f:
            if target_bytes > 0:
                f.seek(target_bytes - 1)
                f.write(b"\x00")
            else:
                f.write(b"")
    else:
        content = generate_file_content(fill_mode, target_bytes)
        file_path.write_bytes(content)


def populate_directory(
    current_dir: Path,
    current_depth: int,
    max_depth: int,
    min_subfolders: int,
    max_subfolders: int,
    min_files: int,
    max_files: int,
    file_extensions: List[str],
    min_size_kb: int,
    max_size_kb: int,
    fill_mode: str,
    stats: dict,
) -> None:
    """Recursively creates files and child folders up to max_depth."""
    current_dir.mkdir(parents=True, exist_ok=True)
    stats["total_folders"] += 1

    # 1. Generate files in the current directory
    file_count = random.randint(min_files, max(min_files, max_files))
    for i in range(1, file_count + 1):
        ext = random.choice(file_extensions)
        file_name = f"data_{i:03d}_{random.randint(1000, 9999)}{ext}"
        create_dummy_file(current_dir / file_name, fill_mode, min_size_kb, max_size_kb)
        stats["total_files"] += 1

    # 2. Base case: stop creating subfolders if max depth reached
    if current_depth >= max_depth:
        return

    # 3. Generate child subfolders recursively
    subfolder_count = random.randint(min_subfolders, max(min_subfolders, max_subfolders))
    for i in range(1, subfolder_count + 1):
        child_dir = current_dir / f"level_{current_depth + 1}_sub_{i:02d}_{random.randint(100, 999)}"
        populate_directory(
            current_dir=child_dir,
            current_depth=current_depth + 1,
            max_depth=max_depth,
            min_subfolders=min_subfolders,
            max_subfolders=max_subfolders,
            min_files=min_files,
            max_files=max_files,
            file_extensions=file_extensions,
            min_size_kb=min_size_kb,
            max_size_kb=max_size_kb,
            fill_mode=fill_mode,
            stats=stats,
        )


def generate_test_environment(
    root_dir: str,
    max_depth: int,
    min_subfolders: int,
    max_subfolders: int,
    min_files_per_folder: int,
    max_files_per_folder: int,
    file_extensions: List[str],
    min_file_size_kb: int,
    max_file_size_kb: int,
    fill_content: str,
) -> dict:
    """Entry point for generating a recursive test directory tree."""
    base_path = Path(root_dir).resolve()

    clean_exts = [ext if ext.startswith(".") else f".{ext}" for ext in file_extensions]
    if not clean_exts:
        clean_exts = [".dat"]

    stats = {"total_folders": 0, "total_files": 0}

    print(f"[+] Generating tree at: {base_path}")
    print(f"[+] Max Depth: {max_depth} | Fill Strategy: {fill_content}")

    populate_directory(
        current_dir=base_path,
        current_depth=0,
        max_depth=max_depth,
        min_subfolders=min_subfolders,
        max_subfolders=max_subfolders,
        min_files=min_files_per_folder,
        max_files=max_files_per_folder,
        file_extensions=clean_exts,
        min_size_kb=min_file_size_kb,
        max_size_kb=max_file_size_kb,
        fill_mode=fill_content,
        stats=stats,
    )

    print(f"[✓] Done! Generated {stats['total_files']} files across {stats['total_folders']} folders.")
    return {
        "root_path": str(base_path),
        **stats,
    }


# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":

    config = get_config_ui()

    if config:
        if debug:
            print("User submitted:")
            print("Root dir: " + config["ROOT_DIR"])
            print("max depth: " + config["MAX_DEPTH"])
            print("min subfolders: " + config["MIN_SUBFOLDERS"])
            print("max sub folders: " + config["MAX_SUBFOLDERS"])
            print("max files per folder: " + config["MAX_FILES_PER_FOLDER"])
            print("file extensions: " + config["FILE_EXTENSIONS"])
            print("min file size: " + config["MIN_FILE_SIZE_KB"])
            print("max file size: " + config["MAX_FILE_SIZE_KB"])
            print("fill content: " + config["FILL_CONTENT"])
            print("compress to zip: " + config["COMPRESS_TO_ZIP"])

        generate_test_environment(
            root_dir=config["ROOT_DIR"],
            max_depth=config["MAX_DEPTH"],
            min_subfolders=config["MIN_SUBFOLDERS"],
            max_subfolders=config["MAX_SUBFOLDERS"],
            min_files_per_folder=config["MIN_FILES_PER_FOLDER"],
            max_files_per_folder=config["MAX_FILES_PER_FOLDER"],
            file_extensions=config["FILE_EXTENSIONS"],
            min_file_size_kb=config["MIN_FILE_SIZE_KB"],
            max_file_size_kb=config["MAX_FILE_SIZE_KB"],
            fill_content=config["FILL_CONTENT"],
        )
    else:
        print("User closed the window without submitting.")

    