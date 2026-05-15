"""
logger.py
Handles logging and viewing file operations (rename/move/undo).
"""

import os
import csv
from datetime import datetime


# =========================
# LOG FILE PATH
# =========================
LOG_FILE = "operations_log.csv"


# =========================
# LOG OPERATION
# =========================
def log_operation(operation, old_path, new_path):

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Timestamp", "Operation", "Old Path", "New Path"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            operation,
            old_path,
            new_path
        ])


# =========================
# VIEW LOGS
# =========================
def view_logs():

    if not os.path.exists(LOG_FILE):
        print("\n📭 No logs found yet.")
        return

    print("\n" + "=" * 90)
    print("📜 OPERATION LOGS")
    print("=" * 90)

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0:
                print(f"{row[0]:<22} {row[1]:<12} {row[2]:<35} {row[3]}")
                print("-" * 90)
            else:
                print(f"{row[0]:<22} {row[1]:<12} {row[2]:<35} {row[3]}")

    print("=" * 90)
    