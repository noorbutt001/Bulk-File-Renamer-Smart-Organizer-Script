"""
utils.py
Helper functions for file validation and safety checks.
"""

import os


# =========================
# VALIDATE FOLDER
# =========================
def validate_folder(path: str) -> bool:
    """
    Check if folder exists and is valid.
    """
    if not path:
        print("❌ No path provided.")
        return False

    if not os.path.exists(path):
        print("❌ Folder does not exist.")
        return False

    if not os.path.isdir(path):
        print("❌ Path is not a folder.")
        return False

    return True


# =========================
# LIST FILES
# =========================
def get_files(folder: str):
    """
    Get all files inside a folder (not subfolders).
    """
    try:
        return [
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]
    except Exception as e:
        print(f"❌ Error reading folder: {e}")
        return []


# =========================
# UNIQUE FILE NAME
# =========================
def get_unique_name(folder: str, filename: str):

    base, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename

    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{base}({counter}){ext}"
        counter += 1

    return new_name


# =========================
# FORMAT SIZE (OPTIONAL USE)
# =========================
def format_size(size_bytes: int) -> str:

    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

    return f"{size_bytes:.2f} TB"