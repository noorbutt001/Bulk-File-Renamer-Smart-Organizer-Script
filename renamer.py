"""
renamer.py
Rename files using prefix / suffix / replace / auto-numbering / date stamp.
"""

import os
from datetime import datetime


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
# UNIQUE FILE NAME
# =========================
def get_unique_name(folder, filename):
    base, ext = os.path.splitext(filename)

    counter = 1
    new_name = filename

    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{base}({counter}){ext}"
        counter += 1

    return new_name


# =========================
# PREVIEW CHANGES
# =========================
def show_preview(changes):
    print("\n" + "=" * 70)
    print(f"{'OLD NAME':<35} ➜ NEW NAME")
    print("=" * 70)

    for old, new in changes:
        print(f"{old:<35} ➜ {new}")

    print("=" * 70)

    confirm = input("\n✅ Apply changes? (y/n): ").lower()
    return confirm == "y"


# =========================
# BUILD NEW FILE NAME
# =========================
def build_new_name(original, options, index=1):
    base, ext = os.path.splitext(original)

    # Replace text
    if options.get("replace"):
        old_word, new_word = options["replace"]
        base = base.replace(old_word, new_word)

    # Auto numbering
    if options.get("auto_number"):
        base_name = options.get("number_base", "file")
        base = f"{base_name}_{index}"

    # Add date
    if options.get("add_date"):
        date_str = datetime.now().strftime("%Y%m%d")
        base = f"{base}_{date_str}"

    # Prefix
    if options.get("prefix"):
        base = f"{options['prefix']}{base}"

    # Suffix
    if options.get("suffix"):
        base = f"{base}{options['suffix']}"

    return f"{base}{ext}"


# =========================
# RENAME FILES
# =========================
def rename_files(folder, options):

    if not validate_folder(folder):
        print("❌ Invalid folder.")
        return

    files = get_files(folder)

    if not files:
        print("📭 No files found.")
        return

    changes = []

    for i, file in enumerate(files, start=1):
        new_name = build_new_name(file, options, i)

        if file != new_name:
            changes.append((file, new_name))

    if not changes:
        print("ℹ️ No changes needed.")
        return

    # Preview
    if not show_preview(changes):
        print("❌ Operation cancelled.")
        return

    success = 0
    failed = 0

    for old_name, new_name in changes:

        old_path = os.path.join(folder, old_name)

        safe_name = get_unique_name(folder, new_name)

        new_path = os.path.join(folder, safe_name)

        try:
            os.rename(old_path, new_path)

            print(f"✅ Renamed: {old_name} ➜ {safe_name}")

            success += 1

        except Exception as e:
            print(f"❌ Error renaming {old_name}: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"✅ Success: {success}")
    print(f"❌ Failed : {failed}")
    print("=" * 50)


# =========================
# USER INPUT OPTIONS
# =========================
def get_rename_options_from_user():

    print("\n🏷️ RENAME OPTIONS")
    print("-" * 40)

    options = {}

    prefix = input("Prefix: ").strip()
    if prefix:
        options["prefix"] = prefix

    suffix = input("Suffix: ").strip()
    if suffix:
        options["suffix"] = suffix

    replace = input("Replace text (old=new): ").strip()

    if "=" in replace:
        old, new = replace.split("=", 1)
        options["replace"] = (old.strip(), new.strip())

    auto = input("Enable auto numbering? (y/n): ").lower()

    if auto == "y":
        options["auto_number"] = True

        base = input("Base name (default=file): ").strip()

        options["number_base"] = base if base else "file"

    date_opt = input("Add date? (y/n): ").lower()

    if date_opt == "y":
        options["add_date"] = True

    return options