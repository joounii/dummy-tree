from typing import Any, Dict, Optional
import dearpygui.dearpygui as dpg


def get_config_ui() -> Optional[Dict[str, Any]]:
    """Opens the configuration UI and returns the user inputs as a dictionary.

    Returns:
        dict: The parsed configuration if submitted.
        None: If the user closed the window without submitting.
    """
    config: Dict[str, Any] = {}

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

    def on_submit():
        raw_exts = dpg.get_value("f_extensions")
        parsed_exts = [
            ext.strip() if ext.strip().startswith(".") else f".{ext.strip()}"
            for ext in raw_exts.split(",")
            if ext.strip()
        ]

        config["ROOT_DIR"] = dpg.get_value("root_dir")
        config["MAX_DEPTH"] = dpg.get_value("max_depth_slider")
        config["MIN_SUBFOLDERS"] = dpg.get_value("min_subfolders")
        config["MAX_SUBFOLDERS"] = dpg.get_value("max_subfolders")
        config["MIN_FILES_PER_FOLDER"] = dpg.get_value("min_files")
        config["MAX_FILES_PER_FOLDER"] = dpg.get_value("max_files")
        config["FILE_EXTENSIONS"] = parsed_exts
        config["MIN_FILE_SIZE_KB"] = dpg.get_value("min_size")
        config["MAX_FILE_SIZE_KB"] = dpg.get_value("max_size")
        config["FILL_CONTENT"] = dpg.get_value("fill_content")
        config["COMPRESS_TO_ZIP"] = dpg.get_value("compress_to_zip")

        dpg.stop_dearpygui()

    # Initialize Dear PyGui lifecycle
    dpg.create_context()
    dpg.create_viewport(
        title="Mock Environment Generator Setup",
        width=540,
        height=530,
        resizable=False,
    )

    with dpg.window(tag="PrimaryWindow"):
        dpg.add_text("Directory & Subfolders", color=(100, 200, 255))

        with dpg.group(horizontal=True):
            dpg.add_input_text(
                tag="root_dir", default_value=r".\mock_environment", width=340
            )
            dpg.add_button(
                label="Browse...", callback=browse_native_windows_folder
            )
            dpg.add_text("Root Dir")

        with dpg.group(horizontal=True):
            dpg.add_slider_int(
                tag="max_depth_slider",
                default_value=4,
                min_value=0,
                max_value=20,
                clamped=True,
                width=240,
                callback=sync_from_slider,
            )
            dpg.add_input_int(
                tag="max_depth_input",
                default_value=4,
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
            default_value=1,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max Subfolders",
            tag="max_subfolders",
            default_value=3,
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
            default_value=2,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max Files / Folder",
            tag="max_files",
            default_value=6,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_text(
            label="File Extensions",
            tag="f_extensions",
            default_value=".txt, .log, .dat, .bin",
        )
        dpg.add_input_int(
            label="Min File Size (KB)",
            tag="min_size",
            default_value=4,
            min_value=0,
            min_clamped=True,
        )
        dpg.add_input_int(
            label="Max File Size (KB)",
            tag="max_size",
            default_value=64,
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
            default_value="Zero Bytes (Instant)",
        )
        dpg.add_checkbox(
            label="Compress output to ZIP",
            tag="compress_to_zip",
            default_value=False,
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

    return config if config else None


if __name__ == "__main__":
    result = get_config_ui()
    print("Direct run output:", result)