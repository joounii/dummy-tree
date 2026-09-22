from pathlib import Path
from typing import Any, ContextManager, Optional, cast
import dearpygui.dearpygui as dpg
from config import DEFAULT_CONFIG, GeneratorConfig
from popup import show_popup


def get_config_ui() -> Optional[GeneratorConfig]:
    """Opens configuration UI and returns the user inputs as a GeneratorConfig instance."""
    result_config: Optional[GeneratorConfig] = None

    def browse_native_windows_folder():
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_directory = filedialog.askdirectory(
            title="Select Root Directory",
            initialdir=dpg.get_value("root_dir"),
        )
        root.destroy()

        if selected_directory:
            dpg.set_value("root_dir", selected_directory.replace("/", "\\"))

    def sync_from_slider(sender, app_data):
        dpg.set_value("max_depth_input", app_data)

    def sync_from_input(sender, app_data):
        clamped = max(0, min(20, app_data))
        dpg.set_value("max_depth_slider", clamped)
        dpg.set_value("max_depth_input", clamped)

    def commit_and_exit():
        """Builds the final GeneratorConfig object and closes Dear PyGui."""
        nonlocal result_config
        raw_exts = dpg.get_value("f_extensions")
        parsed_exts = [
            ext.strip() if ext.strip().startswith(".") else f".{ext.strip()}"
            for ext in raw_exts.split(",")
            if ext.strip()
        ]

        result_config = GeneratorConfig(
            root_dir=dpg.get_value("root_dir"),
            max_depth=dpg.get_value("max_depth_slider"),
            min_subfolders=dpg.get_value("min_subfolders"),
            max_subfolders=dpg.get_value("max_subfolders"),
            min_files_per_folder=dpg.get_value("min_files"),
            max_files_per_folder=dpg.get_value("max_files"),
            file_extensions=parsed_exts,
            min_file_size_kb=dpg.get_value("min_size"),
            max_file_size_kb=dpg.get_value("max_size"),
            fill_content=dpg.get_value("fill_content"),
            compress_to_zip=dpg.get_value("compress_to_zip"),
        )

        dpg.stop_dearpygui()

    def on_submit():
        root_dir_str = dpg.get_value("root_dir").strip()

        # Check 1: Is the path valid (non-empty, absolute path with a root/drive)?
        target_path = Path(root_dir_str)
        is_valid = DEFAULT_CONFIG.debug or (bool(root_dir_str) and target_path.is_absolute())

        if not is_valid:
            show_popup(
                title="Invalid Path",
                message=(
                    f"'{root_dir_str}' is not a valid absolute directory path.\n\n"
                    "Please provide a complete absolute path (e.g. 'C:\\dummy_folder')."
                ),
                popup_type="error",
                buttons=[
                    ("Change Path", browse_native_windows_folder),
                    ("Cancel", None),
                ],
                width=460,
                height=180,
            )
            return

        # Check 2: Does the path exist?
        if not target_path.exists():
            def create_path_and_continue():
                try:
                    target_path.mkdir(parents=True, exist_ok=True)
                    commit_and_exit()
                except OSError as err:
                    show_popup(
                        title="Permission Error",
                        message=f"Failed to create directory:\n{err}",
                        popup_type="error",
                        buttons=[("OK", None)],
                    )

            show_popup(
                title="Path Does Not Exist",
                message=(
                    f"The provided path does not exist:\n'{root_dir_str}'\n\n"
                    "Would you like to create this path, choose a new one, or cancel?"
                ),
                popup_type="warning",
                buttons=[
                    ("Create Path", create_path_and_continue),
                    ("Select New Path", browse_native_windows_folder),
                    ("Cancel", None),
                ],
                width=480,
                height=190,
            )
            return

        # Check 3: Is the existing folder empty?
        if target_path.is_dir():
            has_files = any(target_path.iterdir())
            if has_files:
                show_popup(
                    title="Folder Not Empty",
                    message=(
                        f"The selected root folder is not empty:\n'{root_dir_str}'\n\n"
                        "Are you sure you want to generate the files here?"
                    ),
                    popup_type="warning",
                    buttons=[
                        ("Generate Anyway", commit_and_exit),
                        ("Select New Folder", browse_native_windows_folder),
                        ("Cancel", None),
                    ],
                    width=480,
                    height=190,
                )
                return

        # Path is valid, exists, and is empty
        commit_and_exit()

    dpg.create_context()
    dpg.create_viewport(
        title="Mock Environment Generator Setup",
        width=540,
        height=530,
        resizable=False,
    )

    with cast(ContextManager[Any], dpg.window(tag="PrimaryWindow")):
        dpg.add_text("Directory & Subfolders", color=(100, 200, 255))

        with cast(ContextManager[Any], dpg.group(horizontal=True)):
            dpg.add_input_text(
                tag="root_dir",
                default_value=DEFAULT_CONFIG.root_dir,
                width=340,
            )
            dpg.add_button(
                label="Browse...", callback=browse_native_windows_folder
            )
            dpg.add_text("Root Dir")

        with cast(ContextManager[Any], dpg.group(horizontal=True)):
            dpg.add_slider_int(
                tag="max_depth_slider",
                default_value=DEFAULT_CONFIG.max_depth,
                min_value=0,
                max_value=20,
                clamped=True,
                width=240,
                callback=sync_from_slider,
            )
            dpg.add_input_int(
                tag="max_depth_input",
                default_value=DEFAULT_CONFIG.max_depth,
                min_value=0,
                min_clamped=True,
                step=0,
                step_fast=0,
                width=60,
                callback=sync_from_input,
            )
            dpg.add_text("Max Depth (0 - 20)")

        dpg.add_input_int(
            label="Min Subfolders",
            tag="min_subfolders",
            default_value=DEFAULT_CONFIG.min_subfolders,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max Subfolders",
            tag="max_subfolders",
            default_value=DEFAULT_CONFIG.max_subfolders,
            min_value=0,
            min_clamped=True,
        )

        dpg.add_spacer(height=6)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        dpg.add_text("Files & Sizes", color=(100, 200, 255))
        dpg.add_input_int(
            label="Min Files / Folder",
            tag="min_files",
            default_value=DEFAULT_CONFIG.min_files_per_folder,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max Files / Folder",
            tag="max_files",
            default_value=DEFAULT_CONFIG.max_files_per_folder,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_text(
            label="File Extensions",
            tag="f_extensions",
            default_value=DEFAULT_CONFIG.file_extensions_str,
        )
        dpg.add_input_int(
            label="Min File Size (KB)",
            tag="min_size",
            default_value=DEFAULT_CONFIG.min_file_size_kb,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max File Size (KB)",
            tag="max_size",
            default_value=DEFAULT_CONFIG.max_file_size_kb,
            min_value=0,
            min_clamped=True,
        )

        dpg.add_spacer(height=6)
        dpg.add_separator()
        dpg.add_spacer(height=6)

        dpg.add_text("Output Strategy", color=(100, 200, 255))
        dpg.add_combo(
            items=[
                "Zero Bytes (Instant)",
                "Random Bytes",
                "Repeated ASCII Text",
            ],
            label="Fill Content",
            tag="fill_content",
            default_value=DEFAULT_CONFIG.fill_content,
        )
        dpg.add_checkbox(
            label="Compress output to ZIP",
            tag="compress_to_zip",
            default_value=DEFAULT_CONFIG.compress_to_zip,
        )

        dpg.add_spacer(height=12)
        dpg.add_button(
            label="Run Generator", callback=on_submit, width=-1, height=35
        )

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("PrimaryWindow", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

    return result_config


if __name__ == "__main__":
    result = get_config_ui()
    print("Direct run output:", result)