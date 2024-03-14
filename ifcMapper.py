# import tkinter as tk
import pathlib

# import IfcInfraExportMapping as ifcm


def check_file_exists(path: str) -> bool:
    """Check if file exists."""
    extensions = [".json"]
    try:
        return pathlib.Path(path).exists() and pathlib.Path(path).suffix in extensions
    except Exception as e:
        print(f"Fehler: {e}")
        return False


print(check_file_exists("IfcInfraExportMapping.json"))

"""
path_template = "./testdata/IfcInfraExportMapping_Template.json"
path_project = "IfcInfraExportMapping.json"

# intro
print(dp())
print("IfcInfraExportMapping . . .")

# 1) load json template and project file
template = ifcm.open_json_file(path_template)
project_file = ifcm.open_json_file(path_project)

# 2) map files
ifcm.mapping(project_file, template, ifcm.mapping_categories)

# 3) save project file
ifcm.save_json_file(path_project, project_file)

# outro
print("Erledigt.")
"""
