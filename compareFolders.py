import os
from pathlib import Path
from filecmp import dircmp
from typing import List, Tuple


def compare_directories(dir1, dir2) -> None:
    """
    Compare the contents of two directories and print the differences.
    Args:
    dir1 (str): The path to the first directory.
    dir2 (str): The path to the second directory.
    """

    def get_diff_files(dcmp) -> Tuple[List[Path], List[Path], List[Path]]:
        """
        Recursively get the paths of files that differ between two directories.
        Args:
        dcmp (dircmp): The dircmp object representing the comparison between two directories.
        Returns:
        Tuple[List[Path], List[Path], List[Path]]: A tuple containing lists of paths for files only in dir1, dir2, and files with different content.
        """
        left_path = Path(dcmp.left)
        right_path = Path(dcmp.right)

        diff_files_dir1 = [left_path / name for name in dcmp.left_only]
        diff_files_dir2 = [right_path / name for name in dcmp.right_only]
        diff_files = [left_path / name for name in dcmp.diff_files]

        for sub_dcmp in dcmp.subdirs.values():
            sub_diff_files_dir1, sub_diff_files_dir2, sub_diff_files = get_diff_files(
                sub_dcmp
            )
            diff_files_dir1.extend(sub_diff_files_dir1)
            diff_files_dir2.extend(sub_diff_files_dir2)
            diff_files.extend(sub_diff_files)

        return diff_files_dir1, diff_files_dir2, diff_files

    # Compare the directories
    dcmp = dircmp(dir1, dir2)
    diff_files_dir1, diff_files_dir2, diff_files = get_diff_files(dcmp)

    # Print the differences
    if diff_files_dir1:
        print("\nFiles only in {}:".format(dir1))
        for diff_file in diff_files_dir1:
            print(diff_file)

    if diff_files_dir2:
        print("\nFiles only in {}:".format(dir2))
        for diff_file in diff_files_dir2:
            print(diff_file)

    if diff_files:
        print("\nFiles with different content:")
        for name in diff_files:
            print(name)

    if not any([diff_files_dir1, diff_files_dir2, diff_files]):
        print("The two directories are identical.")


def is_valid_folder_path(path):
    """
    Check if the given path is a valid folder path.
    Args:
        path (str): The path to be checked.
    Returns:
        bool: True if the path is a valid folder path, False otherwise.
    """
    return os.path.isdir(path)


if __name__ == "__main__":
    dir1 = input("Enter path to first folder: ")
    dir2 = input("Enter path to second folder: ")
    if is_valid_folder_path(dir1) and is_valid_folder_path(dir2):
        compare_directories(dir1, dir2)
    else:
        print("Invalid path. Please enter a valid folder path.")
