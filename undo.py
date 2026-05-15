"""
undo.py
Reverts last rename/move batch operation.
"""

import os
import json
import shutil

UNDO_FILE = "undo_data.json"


# =========================
# SAVE UNDO DATA
# =========================
def save_undo_state(data):
    """
    Save operations so they can be reversed later.
    """
    with open(UNDO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================
# UNDO LAST OPERATION
# =========================
def undo_last_operation():

    if not os.path.exists(UNDO_FILE):
        print("\n📭 Nothing to undo.")
        return

    try:
        with open(UNDO_FILE, "r", encoding="utf-8") as f:
            operations = json.load(f)

        success = 0
        failed = 0

        for item in operations:

            action = item.get("action")
            src = item.get("from")
            dst = item.get("to")

            try:
                # =========================
                # UNDO RENAME
                # =========================
                if action == "rename":
                    if os.path.exists(src):
                        os.rename(src, dst)
                        success += 1

                # =========================
                # UNDO MOVE
                # =========================
                elif action == "move":
                    if os.path.exists(src):
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.move(src, dst)
                        success += 1

            except Exception as e:
                print(f"❌ Error undoing {src}: {e}")
                failed += 1

        # Delete undo file after use
        os.remove(UNDO_FILE)

        print("\n↩️ Undo Completed")
        print(f"✅ Success: {success}")
        print(f"❌ Failed: {failed}")

    except Exception as e:
        print(f"❌ Undo Error: {e}")