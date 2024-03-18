import configparser
import pathlib
import tkinter as tk
from tkinter import filedialog, scrolledtext

import IfcInfraExportMapping as ifcm


class IfcMapper_GUI:
    def __init__(self, window: tk.Tk) -> None:
        global path_template
        global file_directory
        global file_name

        self.root = window
        self.root.title("IFC Mapper")
        self.root.geometry("800x600")
        # self.root.resizable(width=False, height=True)
        ico_file = pathlib.Path("dp.ico")
        self.root.iconbitmap(ico_file)

        # Frame
        self.frame = tk.Frame(self.root)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=2)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=2)
        self.frame.grid_configure(row=0, column=0, sticky="nsew")
        self.frame.pack(
            fill="both",
            padx=5,
            pady=5,
        )

        # Template file
        self.label_template_text = tk.Label(self.frame, text="Vorlage:")
        self.label_template_text.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.label_template_path = tk.Label(self.frame, text=f"{path_template}")
        self.label_template_path.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.button_template = tk.Button(
            self.frame,
            text="Vorlage öffnen",
            command=self.open_template,
        )
        self.button_template.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # Working file
        self.label_file_text = tk.Label(self.frame, text="Datei:")
        self.label_file_text.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.label_file_path = tk.Label(self.frame, text=f"[{file_name}]", foreground="red")
        self.label_file_path.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.button_file = tk.Button(
            self.frame,
            text="Datei öffnen",
            command=self.open_file,
        )
        self.button_file.grid(row=1, column=2, sticky="e", padx=5, pady=5)

        # Map file
        self.button_map = tk.Button(
            self.frame, text="Datei mappen", command=self.map_file
        )
        self.button_map.config(state="disabled")
        self.button_map.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # Log text
        self.text_log = scrolledtext.ScrolledText(self.frame, wrap="word")
        self.text_log.grid(row=3, column=0, columnspan=3, sticky="nswe", padx=5, pady=5)

    def open_template(self) -> None:
        global path_template
        path = filedialog.askopenfilename(
            title="Vorlage auswählen",
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")],
            initialdir=path_template.parent,
        )
        if check_file_exists(path):
            path_template = pathlib.Path(path)
            short_path = self.shorten_path(path_template)
            self.label_template_path.config(text=f"{short_path}", foreground="black")
            if check_both_files_exists():
                self.button_map.config(state="normal")
            else:
                self.button_map.config(state="disabled")
        else:
            self.label_template_path.config(
                text="FEHLER: Datei nicht gefunden oder falsches Format.",
                foreground="red",
            )
            self.button_map.config(state="disabled")

    def open_file(self) -> None:
        global path_file
        path = filedialog.askopenfilename(
            title="Datei auswählen",
            filetypes=[("JSON-Dateien", "*.json"), ("Alle Dateien", "*.*")],
            initialdir=path_file.parent,
        )
        if check_file_exists(path):
            path_file = pathlib.Path(path)
            short_path = self.shorten_path(path_file)
            self.label_file_path.config(text=f"{short_path}", foreground="black")
            if check_both_files_exists():
                self.button_map.config(state="normal")
            else:
                self.button_map.config(state="disabled")
        else:
            self.label_file_path.config(
                text="FEHLER: Datei nicht gefunden oder falsches Format.",
                foreground="red",
            )
            self.button_map.config(state="disabled")

    def shorten_path(self, path: str, max_length: int = 80) -> str:
        full_path = str(path)
        if len(full_path) <= max_length:
            return full_path

        parts = list(path.parts)
        short_path = "..." + parts[-1]

        for part in parts[-2::-1]:
            if len(short_path) + len(part) + 1 <= max_length:
                short_path = ".../" + part + "/" + short_path[3:]
            else:
                break

        return short_path

    def map_file(self) -> None:
        global path_template
        global path_file
        global mapping_categories
        global DEBUG

        # 1) load json template and project file
        template_data = ifcm.open_json_file(path_template)
        file_data = ifcm.open_json_file(path_file)

        # 2) map files
        log_str = ifcm.mapping(file_data, template_data, mapping_categories)
        if DEBUG:
            print(log_str)
        self.text_log.delete(1.0, tk.END)
        self.text_log.insert(tk.END, log_str)

        # 3) save project file
        ifcm.save_json_file(path_file, file_data)


def check_file_exists(path: str) -> bool:
    """Check if file exists."""
    extensions = [".json"]
    try:
        return pathlib.Path(path).exists() and pathlib.Path(path).suffix in extensions
    except Exception as e:
        print(f"Fehler: {e}")
        return False


def check_directory_exists(path: str) -> bool:
    """Check if directory exists."""
    try:
        return pathlib.Path(path).exists() and pathlib.Path(path).is_dir()
    except Exception as e:
        print(f"Fehler: {e}")
        return False


def check_both_files_exists() -> bool:
    if check_file_exists(path_template) and check_file_exists(path_file):
        return True
    else:
        return False


if __name__ == "__main__":
    # Load configuration
    config_file = pathlib.Path("ifcMapper.ini")
    config = configparser.ConfigParser()
    config.read(config_file)

    # Set preferences
    path_template = pathlib.Path(config["Preferences"]["template"])

    file_directory = pathlib.Path(config["Preferences"]["filepath"])
    file_name = config["Preferences"]["filename"]
    path_file = file_directory / "file_does_not_exist.json"

    categories_string = config["Preferences"]["categories"]
    mapping_categories = [category.strip() for category in categories_string.split(",")]

    DEBUG = config.getboolean("Debug", "debug")

    if DEBUG:
        print(f"{pathlib.Path.cwd() = }")
        print(
            f"path_template {path_template} exists: {check_file_exists(path_template)}"
        )
        print(
            f"file_directory {file_directory} exists: {check_directory_exists(file_directory)}"
        )
        print(f"path_file {path_file} exists: {check_file_exists(path_file)}")
        print(f"{len(mapping_categories)} mapping_categories: {mapping_categories}")

    # Start GUI
    root = tk.Tk()
    app = IfcMapper_GUI(root)
    root.mainloop()
