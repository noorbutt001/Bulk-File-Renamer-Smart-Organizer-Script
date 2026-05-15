"""
organizer.py
Organize files into folders by:
- file type
- extension
- date
- size
"""

import os
import shutil
from datetime import datetime


# =========================
# FILE TYPE CATEGORIES
# =========================
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".html", ".css", ".js"],
}


# =========================
# VALIDATE FOLDER
# =========================
def validate_folder(folder):
    return os.path.exists(folder) and os.path.isdir(folder)


# =========================
# GET FILES
# =========================
def get_files(folder):
    return [
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f))
    ]


# =========================
# GET TYPE CATEGORY
# =========================
def get_type_category(extension):

    extension = extension.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Others"


# =========================
# GET EXTENSION CATEGORY
# =========================
def get_extension_category(extension):

    extension = extension.replace(".", "").upper()

    if extension:
        return extension

    return "NO_EXTENSION"


# =========================
# GET DATE CATEGORY
# =========================
def get_date_category(filepath):

    timestamp = os.path.getmtime(filepath)

    return datetime.fromtimestamp(timestamp).strftime("%Y-%m")


# =========================
# GET SIZE CATEGORY
# =========================
def get_size_category(filepath):

    size = os.path.getsize(filepath)

    if size < 1024 * 1024:
        return "Small Files"

    elif size < 50 * 1024 * 1024:
        return "Medium Files"

    elif size < 500 * 1024 * 1024:
        return "Large Files"

    else:
        return "Huge Files"


# =========================
# SHOW PREVIEW
# =========================
def show_preview(changes):

    print("\n" + "=" * 70)
    print(f"{'FILE':<35} ➜ DESTINATION")
    print("=" * 70)

    for old, new in changes:
        print(f"{old:<35} ➜ {new}")

    print("=" * 70)

    confirm = input("\n✅ Apply organization? (y/n): ").lower()

    return confirm == "y"


# =========================
# ORGANIZE FILES
# =========================
def organize_files(folder, mode):

    if not validate_folder(folder):
        print("❌ Invalid folder.")
        return

    files = get_files(folder)

    if not files:
        print("📭 No files found.")
        return

    plan = []

    # =========================
    # BUILD ORGANIZATION PLAN
    # =========================
    for file in files:

        filepath = os.path.join(folder, file)

        _, extension = os.path.splitext(file)

        # Organize by type
        if mode == "type":
            category = get_type_category(extension)

        # Organize by extension
        elif mode == "extension":
            category = get_extension_category(extension)

        # Organize by date
        elif mode == "date":
            category = get_date_category(filepath)

        # Organize by size
        elif mode == "size":
            category = get_size_category(filepath)

        else:
            print("❌ Invalid organize mode.")
            return

        plan.append((file, category))

    # =========================
    # SHOW PREVIEW
    # =========================
    preview = []

    for file, category in plan:
        preview.append((file, f"{category}/{file}"))

    if not show_preview(preview):
        print("❌ Operation cancelled.")
        return

    # =========================
    # MOVE FILES
    # =========================
    success = 0
    failed = 0

    for file, category in plan:

        source = os.path.join(folder, file)

        destination_folder = os.path.join(folder, category)

        try:
            os.makedirs(destination_folder, exist_ok=True)

            destination = os.path.join(destination_folder, file)

            shutil.move(source, destination)

            print(f"✅ Moved: {file} ➜ {category}")

            success += 1

        except Exception as e:
            print(f"❌ Error moving {file}: {e}")

            failed += 1

    print("\n" + "=" * 50)
    print(f"✅ Success: {success}")
    print(f"❌ Failed : {failed}")
    print("=" * 50)