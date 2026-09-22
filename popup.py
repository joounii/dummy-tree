import dearpygui.dearpygui as dpg
from typing import Any, Callable, ContextManager, List, Optional, Tuple, cast

def as_ctx(item: Any) -> ContextManager[Any]:
    return item

TYPE_STYLES = {
    "info": ("INFO: ", (100, 180, 255)),
    "warning": ("WARNING: ", (255, 190, 60)),
    "error": ("ERROR: ", (255, 90, 90)),
}


def show_popup(
    title: str,
    message: str,
    popup_type: str = "warning",
    buttons: Optional[List[Tuple[str, Optional[Callable[[], None]]]]] = None,
    width: int = 420,
    height: int = 180,
):
    """
    Displays a modal popup dialog centered inside the Dear PyGui viewport.
    """
    prefix, color = TYPE_STYLES.get(popup_type.lower(), ("", (220, 220, 220)))
    window_title = f"{prefix}{title}"

    if not buttons:
        buttons = [("OK", None)]

    # Center relative to current viewport
    vp_w = dpg.get_viewport_client_width()
    vp_h = dpg.get_viewport_client_height()
    pos_x = max(0, int((vp_w - width) / 2))
    pos_y = max(0, int((vp_h - height) / 2))

    popup_tag = dpg.generate_uuid()

    # Generic button callback handler using DPG's user_data
    def _button_clicked(sender, app_data, user_callback):
        if dpg.does_item_exist(popup_tag):
            dpg.delete_item(popup_tag)
        if callable(user_callback):
            user_callback()

    with as_ctx(dpg.window(
        tag=popup_tag,
        label=window_title,
        modal=True,
        show=True,
        no_resize=True,
        no_move=True,
        width=width,
        height=height,
        pos=[pos_x, pos_y],
        on_close=lambda: _button_clicked(None, None, None),
    )):
        dpg.add_text(message, wrap=width - 30, color=color)
        dpg.add_spacer(height=15)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        # Buttons row
        with as_ctx(dpg.group(horizontal=True)):
            for label, cb in buttons:
                dpg.add_button(
                    label=label,
                    callback=_button_clicked,
                    user_data=cb,
                )


# ==========================================
# Standalone Test Harness
# ==========================================
if __name__ == "__main__":
    dpg.create_context()

    def on_generate_anyway():
        print("Action: User clicked 'Generate Anyway'")

    def on_select_new():
        print("Action: User clicked 'Select New Folder'")

    def on_cancel():
        print("Action: User clicked 'Cancel'")

    def test_warning_dialog():
        show_popup(
            title="Folder Not Empty",
            message="The selected folder already contains files. Are you sure you want to generate here?",
            popup_type="warning",
            buttons=[
                ("Generate Anyway", on_generate_anyway),
                ("Select New Folder", on_select_new),
                ("Cancel", on_cancel),
            ],
            width=460,
            height=180,
        )

    def test_error_dialog():
        show_popup(
            title="Path Not Found",
            message="The selected folder does not exist. Do you want to create it?",
            popup_type="error",
            buttons=[
                ("Create Path", lambda: print("Action: Create path")),
                ("Cancel", on_cancel),
            ],
        )

    def test_info_dialog():
        show_popup(
            title="Success",
            message="Dummy tree created successfully!",
            popup_type="info",
            buttons=[("OK", lambda: print("Action: Closed info"))],
        )

    with as_ctx(dpg.window(label="Popup Test Runner", width=400, height=200)):
        dpg.add_text("Click a button to test the popup styles:")
        dpg.add_button(label="Open Warning Popup", callback=test_warning_dialog)
        dpg.add_button(label="Open Error Popup", callback=test_error_dialog)
        dpg.add_button(label="Open Info Popup", callback=test_info_dialog)

    dpg.create_viewport(title="Popup Test Window", width=600, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()