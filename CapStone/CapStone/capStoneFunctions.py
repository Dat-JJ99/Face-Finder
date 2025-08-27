import shutil
import os
from tkinter import filedialog

def uploadFunction():
    # Open file picker to select a JPG file
    filePath = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    
    if filePath:
        # Get the file name and destination path
        filename = os.path.basename(filePath)
        dest_path = os.path.join("TestFolder", filename)
        
        # Copy file to TestFolder
        shutil.copy(filePath, dest_path)
        print(f"Uploaded {filename} to TestFolder.")

