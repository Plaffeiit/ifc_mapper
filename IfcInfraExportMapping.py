import json

DEBUG = False


def dp(text: str = "Donatsch + Partner AG", space: int = 1) -> str:
    """Return a white string with a green background."""
    _color = "\033[37m\033[42m"
    _reset = "\033[0m"
    _space = " "
    return _color + (space * _space) + text + (space * _space) + _reset


def open_json_file(path: str) -> dict:
    """Open a json file and return the content as a dictionary."""
    with open(path, "r", encoding="utf-8") as datei:
        return json.load(datei)


def save_json_file(path: str, data: dict) -> None:
    """Save a dictionary as a json file."""
    with open(path, "w", encoding="utf-8") as datei:
        json.dump(data, datei, ensure_ascii=False, indent=4)


def mapping(file: dict, template: dict, categories: list) -> str:
    """Map the entries from the template to the project file."""
    output_str = ""
    try:
        for category in categories:
            name_list_template = []  # list of names in template
            for entry in template[category]:
                name_list_template.append(entry["Name"])

            output_str += f"{category}\n"

            # check if entry is in project file but not in template
            for entry in file[category]:
                if DEBUG:
                    output_str += (
                        f'{entry["Name"]}, {entry["IfcExportAs"]}, {entry["Export"]}\n'
                    )

                if entry["Name"] in name_list_template:
                    template_entry = next(
                        (t for t in template[category] if t["Name"] == entry["Name"]),
                        None,
                    )
                    if template_entry:
                        entry["IfcExportAs"] = template_entry["IfcExportAs"]
                        entry["Export"] = template_entry["Export"]

                    output_str += f"..\"{entry['Name']}\" wurde abgeglichen\n"
                else:
                    output_str += f"..\"{entry['Name']}\" bleibt unverändert\n"
                if DEBUG:
                    output_str += (
                        f'{entry["Name"]}, {entry["IfcExportAs"]}, {entry["Export"]}\n'
                    )

            name_list_project = []  # list of names in project file
            for entry in file[category]:
                name_list_project.append(entry["Name"])

            # check if entry is in template but not in project file
            for name in name_list_template:
                if name not in name_list_project:
                    file[category].append(
                        {"Name": name, "IfcExportAs": "", "Export": True}
                    )
                    output_str += f'.."{name}" neu hinzugefügt\n'

            # ToDo: sort all entries alphabetically

    except KeyError as e:
        output_str += f"KEY_ERROR: {e} nicht gefunden!\nMapping abgebrochen . . .\n"

    return output_str[:-1]


if __name__ == "__main__":
    DEBUG = False

    if DEBUG:
        mapping_categories = (
            "MapBlockName",
            "MapCADLayerName",
        )

    else:
        mapping_categories = (
            "MapBlockName",
            "MapCADLayerName",
            "MapAlignmentStyleName",
            "MapAssemblyStyleName",
            "MapCorridorStyleName",
            "MapFeatureLineStyleName",
            "MapLinkStyleName",
            "MapPipeStyleName",
            "MapPointStyleName",
            "MapPressureAppurtenanceStyleName",
            "MapPressureFittingStyleName",
            "MapPressurePipeStyleName",
            "MapProfileStyleName",
            "MapShapeStyleName",
            "MapStructureStyleName",
            "MapSurfaceStyleName",
            "MapSubassemblyName",
            "MapShapeCode",
            "MapLinkCode",
            "MapPointCode",
            "MapFolderName",
        )

    # paths
    path_template = "./testdata/IfcInfraExportMapping_Template.json"
    path_project = "./testdata/IfcInfraExportMapping.json"

    if DEBUG:
        path_template = "./testdata/datei_template.json"
        path_project = "./testdata/datei_project.json"

    # intro
    print(dp())
    print("IfcInfraExportMapping . . .")

    # 1) load json template and project file
    template = open_json_file(path_template)
    project_file = open_json_file(path_project)

    # 2) map files
    log_str = mapping(project_file, template, mapping_categories)
    print(log_str)

    # 3) save project file
    save_json_file(path_project, project_file)

    # outro
    print("Erledigt.")

"""
Debug output:

[…]
MapCADLayerName
.."0" wurde abgeglichen
.."DO_1" wurde abgeglichen
.."DO_2" wurde abgeglichen
.."DO_4" wurde abgeglichen
.."DO_5" bleibt unverändert
.."DO_6" wurde abgeglichen
.."DO_7" wurde abgeglichen
.."DO_3" neu hinzugefügt
.."DO_8" neu hinzugefügt
[…]
"""
