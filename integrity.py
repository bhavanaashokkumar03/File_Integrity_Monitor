
import hashlib
import os
import json
from datetime import datetime


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (FileNotFoundError, PermissionError):
        return None


def scan_files(folder):
    file_hashes = {}

    for root, dirs, files in os.walk(folder):
        for filename in files:
            path = os.path.join(root, filename)
            file_hash = calculate_hash(path)

            if file_hash:
                file_hashes[path] = file_hash

    return file_hashes


def save_baseline(data, baseline_file):
    with open(baseline_file, "w") as file:
        json.dump(data, file, indent=4)


def load_baseline(baseline_file):
    try:
        with open(baseline_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def log_changes(message):
    with open("logs.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] {message}\n")


def compare_files(old_data, new_data):
    for path, new_hash in new_data.items():

        if path not in old_data:
            message = f"NEW FILE DETECTED: {path}"
            print(message)
            log_changes(message)

        elif old_data[path] != new_hash:
            message = f"FILE MODIFIED: {path}"
            print(message)
            log_changes(message)

    for path in old_data:

        if path not in new_data:
            message = f"FILE DELETED: {path}"
            print(message)
            log_changes(message)
