import os

def rename_files_in_directory(directory, skip_filename="rename.py"):
    files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f != skip_filename
    ]
    files.sort()  # Optional: sort alphabetically before renaming

    for index, filename in enumerate(files, start=1):
        old_path = os.path.join(directory, filename)
        _, ext = os.path.splitext(filename)
        new_filename = f"Q{index}{ext}"
        new_path = os.path.join(directory, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed '{filename}' to '{new_filename}'")

# Example usage:
directory_path = "Inputs/test"
rename_files_in_directory(directory_path)
