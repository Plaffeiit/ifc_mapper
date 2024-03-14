import json
import shutil

# Erstelle zwei Beispieldaten
daten_vorlage = {
    "MapBlockName": [
        {"Name": "\\*Model_Space", "IfcExportAs": "IfcBuiltElement", "Export": True},
        {"Name": "\\*Paper_Space", "IfcExportAs": "IfcBuiltElement", "Export": True},
        {"Name": "\\*Paper_Space0", "IfcExportAs": "IfcBuiltElement", "Export": True},
    ],
    "MapCADLayerName": [
        {"Name": "0", "IfcExportAs": "", "Export": True},
        {"Name": "DO_01", "IfcExportAs": "", "Export": True},
        {"Name": "DO_02", "IfcExportAs": "", "Export": False},
        {"Name": "DO_03", "IfcExportAs": "ifcDonatschPartner", "Export": True},
        {"Name": "DO_04", "IfcExportAs": "ifcDonatschPartner", "Export": False},
        {"Name": "DO_11", "IfcExportAs": "ifcLandquart", "Export": True},
        {"Name": "DO_12", "IfcExportAs": "ifcLandquart", "Export": False},
        {"Name": "DO_21", "IfcExportAs": "ifcPoschiavo", "Export": True},
        {"Name": "DO_22", "IfcExportAs": "ifcPoschiavo", "Export": False},
        {"Name": "DO_42", "IfcExportAs": "", "Export": False},
    ],
}

daten_projekt = {
    "MapBlockName": [
        {"Name": "\\*Model_Space", "IfcExportAs": "IfcBuiltElement", "Export": True},
        {"Name": "\\*Paper_Space", "IfcExportAs": "IfcBuiltElement", "Export": True},
        {"Name": "\\*Paper_Space0", "IfcExportAs": "IfcBuiltElement", "Export": True},
    ],
    "MapCADLayerName": [
        {"Name": "0", "IfcExportAs": "", "Export": True},
        {"Name": "DO_01", "IfcExportAs": "", "Export": True},
        {"Name": "DO_02", "IfcExportAs": "", "Export": False},
        {"Name": "DO_03", "IfcExportAs": "ifcDonatschPartner", "Export": True},
        {"Name": "DO_04", "IfcExportAs": "ifcDonatschPartner", "Export": False},
        {
            "Name": "DO_11",
            "IfcExportAs": "ifcLandquart",
            "Export": False,
        },  # "Export": False
        {
            "Name": "DO_12",
            "IfcExportAs": "ifcLandquart",
            "Export": True,
        },  # "Export": True
        {
            "Name": "DO_21",
            "IfcExportAs": "",
            "Export": True,
        },  # "IfcExportAs": "ifcPoschiavo"
        {
            "Name": "DO_22",
            "IfcExportAs": "ifcLondon",
            "Export": True,
        },  # "IfcExportAs": "ifcLondon", "Export": False
        {
            "Name": "DO_31",
            "IfcExportAs": "ifBerlin",
            "Export": True,
        },  # nicht in Vorlage enthalten
        # {"Name": "DO_42", "IfcExportAs": "", "Export": False}, -> nicht in Project enthalten
    ],
}

# Pfade für die JSON-Dateien festlegen
pfad_zu_vorlage = "./testdata/datei_template.json"
pfad_zu_projekt = "./testdata/datei_project.json"

# JSON-Dateien schreiben
with open(pfad_zu_vorlage, "w", encoding="utf-8") as datei_a, open(
    pfad_zu_projekt, "w", encoding="utf-8"
) as datei_b:
    json.dump(daten_vorlage, datei_a, ensure_ascii=False, indent=4)
    json.dump(daten_projekt, datei_b, ensure_ascii=False, indent=4)

pfad_zu_vorlage, pfad_zu_projekt

# Kopiere IfcInfraExportMapping.json ind Hauptverzeichnis
shutil.copyfile(
    "./testdata/IfcInfraExportMapping_Testfile.json",
    "./testdata/IfcInfraExportMapping.json",
)

print("Erledigt.")
# Erledigt.

"""
Test-Output v20240311

0, , True
0, , True
DO_01, , True
DO_01, , True
DO_02, , False
DO_02, , False
DO_03, ifcDonatschPartner, True
DO_03, ifcDonatschPartner, True
DO_04, ifcDonatschPartner, False
DO_04, ifcDonatschPartner, False
DO_11, ifcLandquart, False
DO_11, ifcLandquart, True
DO_12, ifcLandquart, True
DO_12, ifcLandquart, False
DO_21, , True
DO_21, ifcPoschiavo, True
DO_22, ifcLondon, True
DO_22, ifcPoschiavo, False
DO_31, ifBerlin, True
DO_31, ifBerlin, True
Name DO_42 not in template
Name DO_42 new created
"""
