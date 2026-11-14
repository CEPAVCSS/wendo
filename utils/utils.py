import sys
from pathlib import Path


class Utils:
    @staticmethod
    def resource_path(relative_path):
        base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
        return base_path / relative_path

    @staticmethod
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    