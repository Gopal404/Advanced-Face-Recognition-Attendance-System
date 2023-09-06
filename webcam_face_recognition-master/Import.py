import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class FileCopier:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.option_add('*Dialog.msg.width', 20)
        self.root.option_add('*Dialog.msg.wrapLength', 300)

    def copy_files(self):
        try:
            # Ask the user to select files using the file dialog
            file_paths = filedialog.askopenfilenames(filetypes=[("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png")])

            # Check if the user selected any files
            if len(file_paths) < 10:
                messagebox.showwarning("Message", "Please select at least 10 image files.", parent=self.root)
                return

            # Ask the user for a new name to rename the files
            new_name = simpledialog.askstring("Rename Files", "Enter Photo ID:", parent=self.root)
            if not new_name:
                return

            # Specify the destination folder where you want to copy the selected files
            destination_folder = "G:\\Final project\\webcam_face_recognition-master\\webcam_face_recognition-master\\faces"

            for i, file_path in enumerate(file_paths):
                # Rename the file
                new_path = os.path.join(os.path.dirname(file_path), f"{new_name} ({i+1}).{file_path.split('.')[-1]}")
                os.rename(file_path, new_path)

                # Copy the renamed file to the destination folder
                shutil.copy(new_path, destination_folder)

            # Print a message to confirm that the files have been copied
            messagebox.showinfo("File Copied", f"{len(file_paths)} files have been imported.", parent=self.root)

        except TypeError:
            # User clicked cancel in the file dialog
            messagebox.showwarning("Message", "No Files Selected.", parent=self.root)


if __name__ == '__main__':
    copier = FileCopier()
    copier.copy_files()
