# main.py
import os
import random
import shutil
import string
from dataclasses import asdict
from pathlib import Path
from typing import List

from config import DEFAULT_CONFIG, GeneratorConfig
from gui import get_config_ui

debug = False


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

    return b"\x00" * size_bytes


def create_dummy_file(
    file_path: Path, fill_mode: str, min_kb: int, max_kb: int
) -> None:
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
    cfg: GeneratorConfig,
    stats: dict,
) -> None:
    """Recursively creates files and child folders up to max_depth."""
    current_dir.mkdir(parents=True, exist_ok=True)
    stats["total_folders"] += 1

    # 1. Generate files
    min_f = cfg.min_files_per_folder
    max_f = max(min_f, cfg.max_files_per_folder)
    file_count = random.randint(min_f, max_f)

    for i in range(1, file_count + 1):
        ext = random.choice(cfg.file_extensions)
        file_name = f"data_{i:03d}_{random.randint(1000, 9999)}{ext}"
        create_dummy_file(
            current_dir / file_name,
            cfg.fill_content,
            cfg.min_file_size_kb,
            cfg.max_file_size_kb,
        )
        stats["total_files"] += 1

    # 2. Base case
    if current_depth >= cfg.max_depth:
        return

    # 3. Generate child subfolders recursively
    min_sub = cfg.min_subfolders
    max_sub = max(min_sub, cfg.max_subfolders)
    subfolder_count = random.randint(min_sub, max_sub)

    for i in range(1, subfolder_count + 1):
        child_dir = (
            current_dir
            / f"level_{current_depth + 1}_sub_{i:02d}_{random.randint(100, 999)}"
        )
        populate_directory(
            current_dir=child_dir,
            current_depth=current_depth + 1,
            cfg=cfg,
            stats=stats,
        )


def compress_directory(
    directory_path: Path, delete_original: bool = True
) -> Path:
    """Compresses the given directory into a .zip archive and removes the original folder."""
    base_name = str(directory_path)
    print(f"[+] Compressing to: {base_name}.zip ...")

    zip_filepath = shutil.make_archive(
        base_name=base_name,
        format="zip",
        root_dir=directory_path.parent,
        base_dir=directory_path.name,
    )

    if delete_original:
        shutil.rmtree(directory_path)
        print(f"[✓] Removed original uncompressed directory: {directory_path}")

    print(f"[✓] Archive created at: {zip_filepath}")
    return Path(zip_filepath)


def generate_test_environment(cfg: GeneratorConfig) -> dict:
    """Entry point for generating a recursive test directory tree."""
    base_path = Path(cfg.root_dir).resolve()

    # Normalize extensions
    cfg.file_extensions = [
        ext if ext.startswith(".") else f".{ext}" for ext in cfg.file_extensions
    ] or [".dat"]

    stats = {"total_folders": 0, "total_files": 0}
    print(f"[+] Generating tree at: {base_path}")
    print(f"[+] Max Depth: {cfg.max_depth} | Fill Strategy: {cfg.fill_content}")

    populate_directory(
        current_dir=base_path,
        current_depth=0,
        cfg=cfg,
        stats=stats,
    )

    print(
        f"[✓] Done! Generated {stats['total_files']} files across {stats['total_folders']} folders."
    )

    zip_path = None
    if cfg.compress_to_zip:
        zip_path = str(compress_directory(base_path, delete_original=True))

    return {
        "root_path": str(base_path) if not cfg.compress_to_zip else None,
        "zip_path": zip_path,
        **stats,
    }


if __name__ == "__main__":
    config = get_config_ui()

    if config:
        if debug:
            print("User submitted:")
            for key, val in asdict(config).items():
                print(f"{key}: {val}")

        generate_test_environment(config)
    else:
        print("User closed the window without submitting.")
