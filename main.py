
import os

from integrity import (
    scan_files,
    save_baseline,
    load_baseline,
    compare_files
)

FOLDER = "monitored_files"
BASELINE = "baseline.json"


def main():

    print("\n===== FILE INTEGRITY MONITOR =====")

    os.makedirs(FOLDER, exist_ok=True)

    baseline = load_baseline(BASELINE)

    print("\n1. Create Baseline")
    print("2. Scan and Detect Changes")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        current_files = scan_files(FOLDER)
        save_baseline(current_files, BASELINE)

        print("\nBaseline created successfully!")

    elif choice == "2":

        if not os.path.exists(BASELINE):
            print("\nPlease create a baseline first!")
            return

        old_files = load_baseline(BASELINE)
        new_files = scan_files(FOLDER)

        print("\nScanning files...\n")

        compare_files(old_files, new_files)

        print("\nScan completed!")

    else:
        print("\nInvalid choice!")


if __name__ == "__main__":
    main()
