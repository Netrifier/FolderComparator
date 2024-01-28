from pathlib import Path
from filecmp import dircmp
import tkinter as tk
from tkinter import filedialog, scrolledtext
import shutil
from typing import List, Tuple


class DirectoryComparatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Folder Comparator")

        app_width = 680
        app_height = 500

        # Get screen dimensions
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Center the window on the screen
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        # Set window size and position
        self.master.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
        self.master.resizable(False, False)

        # Directory 1 input
        self.dir1_label = tk.Label(master, text="Directory 1:")
        self.dir1_label.grid(row=0, column=0, padx=10, pady=10)

        self.dir1_entry = tk.Entry(master, width=50)
        self.dir1_entry.grid(row=0, column=1, padx=10, pady=10)
        self.dir1_entry.insert(0, "D:/Study")

        self.dir1_button = tk.Button(master, text="Browse", command=self.browse_dir1)
        self.dir1_button.grid(row=0, column=2, padx=10, pady=10)

        # Directory 2 input
        self.dir2_label = tk.Label(master, text="Directory 2:")
        self.dir2_label.grid(row=1, column=0, padx=10, pady=10)

        self.dir2_entry = tk.Entry(master, width=50)
        self.dir2_entry.grid(row=1, column=1, padx=10, pady=10)
        self.dir2_entry.insert(0, "E:/Study")

        self.dir2_button = tk.Button(master, text="Browse", command=self.browse_dir2)
        self.dir2_button.grid(row=1, column=2, padx=10, pady=10)

        # Compare button
        self.compare_button = tk.Button(
            master, text="Compare", command=self.compare_directories
        )
        self.compare_button.grid(row=2, column=1, pady=10)

        # Output text area
        self.output_text = scrolledtext.ScrolledText(master, width=80, height=20)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Copy button
        self.copy_button = tk.Button(
            master, text="Copy Selected Files", command=self.copy_selected_items
        )
        self.copy_button.grid(row=2, column=2, pady=5)

    def browse_dir1(self):
        """Browse for a directory and update dir1_entry with the selected directory path."""
        directory = filedialog.askdirectory()
        self.dir1_entry.delete(0, tk.END)
        self.dir1_entry.insert(0, directory)

    def browse_dir2(self):
        """Browse for a directory and update dir2_entry with the selected directory path."""
        directory = filedialog.askdirectory()
        self.dir2_entry.delete(0, tk.END)
        self.dir2_entry.insert(0, directory)

    def copy_selected_items(self):
        """Copy selected items from source directory to destination directory. NOT from destination directory to source directory YET."""
        # Get source and destination directories from entry widgets
        source_dir: Path = Path(self.dir1_entry.get())
        destination_dir: Path = Path(self.dir2_entry.get())

        if source_dir and destination_dir:
            # Get selected items from Checkbutton widgets
            selected_items: List[Path] = [
                Path(widget.file_path)
                for widget in self.output_text.winfo_children()
                if isinstance(widget, tk.Checkbutton) and widget.var.get() == 1
            ]

            # Copy selected items to destination directory
            for item_path in selected_items:
                try:
                    # Generate destination path from source and item paths
                    dest_path: Path = destination_dir / item_path.relative_to(
                        source_dir
                    )
                    # Copy file or directory to destination
                    if item_path.is_file():
                        shutil.copy(str(item_path), str(dest_path))
                    elif item_path.is_dir():
                        shutil.copytree(str(item_path), str(dest_path))

                    # Remove widget of copied item from display
                    for widget in self.output_text.winfo_children():
                        if (
                            hasattr(widget, "file_path")
                            and Path(widget.file_path) == item_path
                        ):
                            widget.destroy()
                except Exception as e:
                    print(f"Error copying {item_path}: {e}")

    def compare_directories(self):
        """
        Compares the contents of two directories and displays the differences in the GUI.
        """
        # Get the paths of the directories from the entry widgets
        dir1_path = self.dir1_entry.get()
        dir2_path = self.dir2_entry.get()

        # Define labels for the different types of differences
        labels = {
            "diff_files_dir1": "Files Only in Directory 1",
            "diff_files_dir2": "Files Only in Directory 2",
            "diff_files": "Files Having Different Content But Same Name",
        }

        # Check if both directory paths are provided
        if dir1_path and dir2_path:
            # Compare the directories and get the result
            result = compare_directories(dir1_path, dir2_path)
            # Clear the output text area
            self.output_text.delete(1.0, tk.END)

            # Iterate through the result and display the differences in the GUI
            for result_key, diff_items in result.items():
                if diff_items:
                    # Display the header for the type of difference
                    header = f"\n{labels[result_key]}:\n"
                    self.output_text.insert(tk.END, header)
                    # Display the differing items and add a copy button for each
                    for diff_item in diff_items:
                        var = tk.IntVar(value=0)
                        checkbox = tk.Checkbutton(
                            self.output_text, text=diff_item, variable=var
                        )
                        checkbox.var = var
                        checkbox.file_path = diff_item
                        self.output_text.window_create(tk.END, window=checkbox)

                        copy_button = tk.Button(
                            self.output_text,
                            text="Copy",
                            command=lambda item_path=diff_item: self.copy_item(
                                item_path
                            ),
                        )
                        copy_button.file_path = diff_item
                        self.output_text.window_create(tk.END, window=copy_button)

                        self.output_text.insert(tk.END, "\n")

            # If there are no differences, indicate that the directories are identical
            if not any(result.values()):
                self.output_text.insert(tk.END, "The two directories are identical.\n")

    def copy_item(self, item_path):
        """
        Copy the specified item from one directory to another.
        Args:
            item_path (str): The path of the item to be copied.
        Returns:
            None
        """
        # Get the source and destination directories
        source_dir = Path(self.dir1_entry.get())
        destination_dir = Path(self.dir2_entry.get())
        item_path = Path(item_path)

        # Try to perform the copy operation
        try:
            # Calculate the destination path
            dest_path = destination_dir / item_path.relative_to(source_dir)

            # Resolve the paths
            item_path = item_path.resolve()
            dest_path = dest_path.resolve()

            # Convert paths to string
            item_path = item_path.as_posix()
            dest_path = dest_path.as_posix()

            # Copy file or directory
            if Path(item_path).is_file():
                shutil.copy(str(item_path), str(dest_path))
            elif Path(item_path).is_dir():
                shutil.copytree(str(item_path), str(dest_path))

            # Remove the widget from the UI if it exists
            for widget in self.output_text.winfo_children():
                if (
                    hasattr(widget, "file_path")
                    and Path(widget.file_path).resolve().as_posix() == item_path
                ):
                    widget.destroy()

            # Print success message
            print(f"Item {item_path} copied to {dest_path}")
        except Exception as e:
            # Print error message
            print(f"Error copying {item_path}: {e}")


def compare_directories(dir1, dir2) -> dict:
    """
    Compare the contents of two directories and print the differences.
    Args:
    dir1 (str): The path to the first directory.
    dir2 (str): The path to the second directory.
    Returns:
    dict: A dictionary containing lists of paths for files only in dir1, dir2, and files with different content.
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

    # Return the differences
    return {
        "diff_files_dir1": diff_files_dir1,
        "diff_files_dir2": diff_files_dir2,
        "diff_files": diff_files,
    }


if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryComparatorGUI(root)
    root.mainloop()
