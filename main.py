"""
main.py
CLI menu-driven entry point for the Bulk Renamer & Smart Organizer.

Run:
    python main.py
"""

# =========================
# IMPORTS
# =========================
try:
    from renamer import rename_files, get_rename_options_from_user
    from organizer import organize_files
    from logger import view_logs
    from undo import undo_last_operation
    from utils import validate_folder
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("⚠️ Make sure all required .py files exist in the same folder.")
    input("\nPress Enter to exit...")
    raise


# =========================
# APP INFO
# =========================
APP_NAME = "Bulk File Renamer & Smart Organizer"
VERSION = "1.0.0"


# =========================
# BANNER
# =========================
def banner():
    print("\n" + "=" * 55)
    print(f"📁  {APP_NAME}")
    print(f"🚀  Version: {VERSION}")
    print("=" * 55)


# =========================
# MAIN MENU
# =========================
def print_menu(selected_folder=None):
    print("\n" + "-" * 55)

    if selected_folder:
        print(f"📂 Current Folder: {selected_folder}")
    else:
        print("📂 Current Folder: Not Selected")

    print("-" * 55)
    print("1. Select Folder")
    print("2. Rename Files")
    print("3. Organize Files")
    print("4. View Logs")
    print("5. Undo Last Operation")
    print("6. Launch GUI (Tkinter)")
    print("7. Exit")
    print("-" * 55)


# =========================
# ORGANIZE MENU
# =========================
def organize_menu(folder):
    print("\n🗂️ ORGANIZE FILES")
    print("-" * 40)
    print("1. By File Type")
    print("2. By Extension")
    print("3. By Date Modified")
    print("4. By File Size")
    print("-" * 40)

    choice = input("Choose option [1-4]: ").strip()

    mode_map = {
        "1": "type",
        "2": "extension",
        "3": "date",
        "4": "size"
    }

    if choice in mode_map:
        organize_files(folder, mode_map[choice])
    else:
        print("❌ Invalid organize option.")


# =========================
# MAIN APPLICATION LOOP
# =========================
def main():
    selected_folder = None

    banner()

    while True:
        try:
            print_menu(selected_folder)

            choice = input("Enter choice [1-7]: ").strip()

            # =========================
            # SELECT FOLDER
            # =========================
            if choice == "1":
                path = input("\n📂 Enter folder path: ").strip()

                # Remove quotes if pasted
                path = path.strip('"').strip("'")

                if validate_folder(path):
                    selected_folder = path
                    print(f"\n✅ Folder selected successfully!")
                else:
                    print("\n❌ Invalid folder path.")

            # =========================
            # RENAME FILES
            # =========================
            elif choice == "2":
                if not selected_folder:
                    print("\n⚠️ Please select a folder first.")
                    continue

                options = get_rename_options_from_user()

                if not options:
                    print("\n⚠️ No rename options selected.")
                    continue

                rename_files(selected_folder, options)

            # =========================
            # ORGANIZE FILES
            # =========================
            elif choice == "3":
                if not selected_folder:
                    print("\n⚠️ Please select a folder first.")
                    continue

                organize_menu(selected_folder)

            # =========================
            # VIEW LOGS
            # =========================
            elif choice == "4":
                view_logs()

            # =========================
            # UNDO LAST OPERATION
            # =========================
            elif choice == "5":
                undo_last_operation()

            # =========================
            # GUI MODE
            # =========================
            elif choice == "6":
                try:
                    from gui import launch_gui

                    print("\n🚀 Launching GUI...")
                    launch_gui()

                except ImportError as e:
                    print(f"\n❌ GUI Import Error: {e}")

                except Exception as e:
                    print(f"\n❌ GUI Error: {e}")

            # =========================
            # EXIT
            # =========================
            elif choice == "7":
                print("\n👋 Thank you for using the application.")
                print("✅ Exiting safely...\n")
                break

            # =========================
            # INVALID CHOICE
            # =========================
            else:
                print("\n❌ Invalid menu option. Please try again.")

        # =========================
        # CTRL + C HANDLING
        # =========================
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted by user.")
            print("👋 Exiting safely...\n")
            break

        # =========================
        # UNEXPECTED ERRORS
        # =========================
        except Exception as e:
            print(f"\n❌ Unexpected Error: {e}")


# =========================
# PROGRAM ENTRY POINT
# =========================
if __name__ == "__main__":
    main()