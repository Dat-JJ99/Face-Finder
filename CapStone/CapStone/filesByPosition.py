from guizero import App, Text, PushButton, Picture, Window, Box, TextBox
from PIL import Image
import shutil
import os
from tkinter import filedialog

# Load images
trashcanPNG = Image.open("trashcan.png")
plusPNG = Image.open("plus.png")
secPNG = Image.open("securitySettings.png")
cancelPNG = Image.open("cancel.png")
renamePNG = Image.open("rename.png")
deletePNG = Image.open("delete.png")

# Image sizes
iconsize = (140, 140)
facesize = (175, 175)
windowButtonSize = (80, 80)

# Resize images
trashcanIcon = trashcanPNG.resize(iconsize)
plusIcon = plusPNG.resize(iconsize)
secIcon = secPNG.resize(iconsize)

# Initialize the app with grid layout
app = App(title="guizero", bg="black", height=1080, width=1920, layout="grid")

# Create a container for the scrolling section; grid reference added.
scrollBox = Box(app, grid=[0, 1], layout="grid")
# Create the face grid inside scrollBox
faceGrid = Box(scrollBox, grid=[0, 0], layout="grid")

# Global scrolling parameters
scroll_position = 0
visible_faces = 10  # Number of images to show at one time
num_columns = 5     # Number of columns in the grid

def faceFunction():
    """Displays a portion of faces from TestFolder, re-indexing the grid each time."""
    global scroll_position
    # Clear previous widgets from the face grid
    for widget in faceGrid.children:
        widget.destroy()

    fileArray = sorted(os.listdir("TestFolder"))
    total_faces = len(fileArray)

    # Make sure scroll_position is within bounds
    if scroll_position >= total_faces:
        scroll_position = max(0, total_faces - visible_faces)

    start_index = scroll_position
    end_index = min(scroll_position + visible_faces, total_faces)

    # Use a local index for grid placement so the grid always starts at [0,0]
    for local_index, filename in enumerate(fileArray[start_index:end_index]):
        # Calculate column and row for the current face.
        col = local_index % num_columns                
        row = local_index // num_columns               

        image_path = os.path.join("TestFolder", filename)
        removeFileTag = filename.replace(".jpg", "")
        faceOpen = Image.open(image_path)
        finalFace = faceOpen.resize(facesize)

        # Create a container for the face image and its label (grid: [column, row])
        faceBox = Box(faceGrid, grid=[col, row], layout="auto")
        PushButton(
            faceBox,
            image=finalFace,
            command=lambda name=removeFileTag, path=image_path: show_face_menu(name, path, finalFace)
        )
        Text(faceBox, text=removeFileTag, color="white")

def show_face_menu(face_name, image_path, face):
    """Show editing window for a selected face (rename or delete)."""
    menu = Window(app, title=f"Edit {face_name}", width=600, height=100, layout="grid", bg="black")
    Text(menu, text=f"Editing: {face_name}", color="white", grid=[0, 0])

    def rename_face():
        rename_window = Window(menu, title="Rename Face", width=500, height=175, layout="grid", bg="#669cba")
        Text(rename_window, text="Enter new name:", grid=[0, 0], size=20)
        name_box = TextBox(rename_window, grid=[1, 0], width=15)
        name_box.bg = 'white'
        name_box.text_size = 20

        def confirm_rename():
            new_name = name_box.value.strip()
            if new_name:
                new_path = os.path.join("TestFolder", new_name + ".jpg")
                os.rename(image_path, new_path)
                rename_window.hide()
                menu.hide()
                faceFunction()
        PushButton(rename_window, text="Confirm", command=confirm_rename, grid=[1, 2], width=10, height=2)

    def delete_face():
        os.remove(image_path)
        menu.hide()
        faceFunction()

    cancelIcon = cancelPNG.resize(windowButtonSize)
    renameIcon = renamePNG.resize(windowButtonSize)
    deleteIcon = deletePNG.resize(windowButtonSize)

    PushButton(menu, image=renameIcon, command=rename_face, grid=[1, 0])
    PushButton(menu, image=deleteIcon, command=delete_face, grid=[2, 0])
    PushButton(menu, image=cancelIcon, command=menu.hide, grid=[3, 0])

def scroll_up():
    global scroll_position
    # Scroll up by one page if possible
    if scroll_position - visible_faces >= 0:
        scroll_position -= visible_faces
    else:
        scroll_position = 0
    faceFunction()

def scroll_down():
    global scroll_position
    files = sorted(os.listdir("TestFolder"))
    if scroll_position + visible_faces < len(files):
        scroll_position += visible_faces
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()

def uploadFunction():
    filePath = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if filePath:
        filename = os.path.basename(filePath)
        dest_path = os.path.join("TestFolder", filename)
        shutil.copy(filePath, dest_path)
        print(f"Uploaded {filename} to TestFolder.")
    faceFunction()

# Static header items
logo = Picture(app, image='logo.PNG', grid=[0, 0])
plusButton = PushButton(app, image=plusIcon, grid=[1, 0], command=uploadFunction)
secButton = PushButton(app, image=secIcon, grid=[3, 0])
secButton.bg = "white"

# Scroll control buttons
scrollUpButton = PushButton(app, text="Scroll Up", command=scroll_up, grid=[0, 2])
scrollDownButton = PushButton(app, text="Scroll Down", command=scroll_down, grid=[0, 3])

faceFunction()
app.display()
