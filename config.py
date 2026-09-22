# config.py
from dataclasses import dataclass, field
from typing import List, Literal

FillContentMode = Literal[
    "Zero Bytes (Instant)",
    "Random Bytes",
    "Repeated ASCII Text",
]

EnvironmentMode = Literal["dev", "prod"]


@dataclass
class GeneratorConfig:
    # Environment & Validation Mode
    environment: EnvironmentMode = "dev"
    """Execution environment ('dev' or 'prod'). When 'dev', strict validations like absolute path requirements are relaxed."""

    # Console Output / Logging
    verbose: bool = False
    """Controls console output verbosity. When True, extra runtime information is printed to stdout."""

    # Directory & Storage
    root_dir: str = r"./mock_environment"
    """The root directory path where mock folders will be generated."""

    compress_to_zip: bool = False
    """Whether to automatically compress the generated output folder into a .zip file."""

    # Subfolder Structure
    max_depth: int = 4
    """Recursion depth limit: 0 = only root folder, 1 = root + direct children, etc."""

    min_subfolders: int = 1
    """Minimum number of subfolders created inside each directory."""

    max_subfolders: int = 3
    """Maximum number of subfolders created inside each directory."""

    # Files & Sizing
    min_files_per_folder: int = 2
    """Minimum number of dummy files placed inside each directory."""

    max_files_per_folder: int = 6
    """Maximum number of dummy files placed inside each directory."""

    file_extensions: List[str] = field(
        default_factory=lambda: [".txt", ".log", ".dat", ".bin"]
    )
    """List of file extensions to choose from randomly (e.g. ['.txt', '.bin'])."""

    min_file_size_kb: int = 4
    """Minimum generated file size in Kilobytes (KB)."""

    max_file_size_kb: int = 64
    """Maximum generated file size in Kilobytes (KB)."""

    # Content Strategy
    fill_content: FillContentMode = "Zero Bytes (Instant)"
    """Fill strategy: 'Zero Bytes (Instant)', 'Random Bytes', or 'Repeated ASCII Text'."""

    @property
    def is_dev(self) -> bool:
        """Helper to quickly check if dev validation rules apply."""
        return self.environment == "dev"

    @property
    def file_extensions_str(self) -> str:
        """Helper to format extensions as a comma-separated string for GUI inputs."""
        return ", ".join(self.file_extensions)


DEFAULT_CONFIG = GeneratorConfig()
"""Default configuration settings for mock folder and file generation.

Available Attributes:
- environment (str): 'dev' or 'prod'. In 'dev', relative paths are allowed.
- verbose (bool): Verbose console logging flag.
- root_dir (str): Base destination directory (default: './mock_environment').
- compress_to_zip (bool): Compress folder to .zip on completion (default: False).
- max_depth (int): Max directory recursion depth (0 = root only) (default: 4).
- min_subfolders (int): Min subdirectories per folder (default: 1).
- max_subfolders (int): Max subdirectories per folder (default: 3).
- min_files_per_folder (int): Min files per directory (default: 2).
- max_files_per_folder (int): Max files per directory (default: 6).
- file_extensions (list[str]): Target file extensions (default: ['.txt', '.log', '.dat', '.bin']).
- min_file_size_kb (int): Min dummy file size in KB (default: 4).
- max_file_size_kb (int): Max dummy file size in KB (default: 64).
- fill_content (str): Mode: 'Zero Bytes (Instant)', 'Random Bytes', 'Repeated ASCII Text'.
- file_extensions_str (str): Comma-separated representation of file extensions.
"""