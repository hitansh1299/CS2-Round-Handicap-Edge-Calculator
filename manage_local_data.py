import os
import shutil
import glob

def move_and_symlink_dem_files(source_folder, destination_folder):
    """
    Moves all '.dem' files from 'source_folder' to 'destination_folder'
    and creates symbolic links in the source folder pointing to the
    new locations.
    """
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # List all items in the source folder
    for filepath in glob.glob(f'{source_folder}/*/*.dem', recursive=True):
        match_dir = filepath.split('\\')[-2]
        filename = filepath.split('\\')[-1]
        print(match_dir)
        print(filepath)

        if os.path.islink(filepath):
            print(f"Found symlink at {filepath}, skipping")
            continue

        os.makedirs(os.path.join(destination_folder, match_dir), exist_ok=True)
        src_path = filepath
        dst_path = os.path.join(destination_folder, match_dir, filename)
        print(dst_path)
        # Move the file to the destination folder
        shutil.move(src_path, dst_path)
        print(f"Moved: {src_path} -> {dst_path}")

        # Create a symlink in the original location
        # Points from old location (src_path) to new location (dst_path)
        try:
            os.symlink(dst_path, src_path)
            print(f"Created symlink: {src_path} -> {dst_path}")
        except OSError as e:
            print(f"Error creating symlink for {src_path}: {e}")
            print(f'Found error, undoing move')
            shutil.move(dst_path, src_path)
            print(f"Moved: {dst_path} -> {src_path}")
            exit()

def move_rar_files(source_folder, destination_folder):
    for filepath in glob.glob(f'{source_folder}/*.rar', recursive=True):
        filename = filepath.split('\\')[-1]
        src_path = filepath
        dst_path = os.path.join(destination_folder, filename)
        shutil.move(src_path, dst_path)
        print(f"Moved: {src_path} -> {dst_path}")


if __name__ == "__main__":
    # Example usage:
    # Replace these with your actual source and destination paths
    source_folder = r"demos"
    destination_folder = r"D:\CS2_Demos"

    # move_and_symlink_dem_files(source_folder, destination_folder)
    move_rar_files(source_folder=source_folder, destination_folder= destination_folder)

    # print()
