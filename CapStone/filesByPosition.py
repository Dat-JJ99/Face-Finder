import json
import os
import shutil
from datetime import datetime
from tkinter import filedialog

from guizero import App, Text, PushButton, Picture, Window, Box, TextBox, CheckBox
from PIL import Image

# ---------------------------
# Helper Functions & Globals
# ---------------------------

# File where the threat statuses are stored.
security_file = "security_settings.json"


def load_security_settings():
    """Load security settings from file."""
    try:
        with open(security_file, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_security_settings():
    """Save threat statuses to file."""
    with open(security_file, "w") as f:
        json.dump(threat_status, f)


# Global dictionary storing threat status for each face.
# The reserved key "__default_threat__" gives the default for new/unregistered faces.
threat_status = load_security_settings()
default_threat = threat_status.get("__default_threat__", False)


# Load images.
trashcanPNG = Image.open("trashcan.png")
plusPNG = Image.open("plus.png")
secPNG = Image.open("securitySettings.png")
cancelPNG = Image.open("cancel.png")
renamePNG = Image.open("rename.png")
deletePNG = Image.open("delete.png")
upPNG = Image.open("upArrow.png")
downPNG = Image.open("downArrow.png")
threatPNG = Image.open("threat.png")
safePNG = Image.open("safe.png")

# Image sizes.
iconsize = (140, 140)
facesize = (175, 175)
windowButtonSize = (80, 80)
arrowSize = (50, 50)
securitySettingsSize = (180, 90)

# Resize images.
trashcanIcon = trashcanPNG.resize(iconsize)
plusIcon = plusPNG.resize(iconsize)
secIcon = secPNG.resize(iconsize)
upArrow = upPNG.resize(arrowSize)
downArrow = downPNG.resize(arrowSize)
threatButton = threatPNG.resize(securitySettingsSize)
safeButton = safePNG.resize(securitySettingsSize)

# Global scrolling parameters.
scroll_position = 0          # Index of the first face shown.
visible_faces = 10           # Number of faces to display at one time.
num_columns = 5              # Number of columns in the face grid.


def update_log():
    """
    Refresh the log panel with information from the currently visible faces.
    Each entry includes a timestamp, face name, and threat status.
    """
    # Remove all widgets except the header (first child) from logBox.
    for widget in logBox.children[1:]:
        widget.destroy()

    fileArray = sorted(os.listdir("TestFolder"))
    start_index = scroll_position
    end_index = min(scroll_position + visible_faces, len(fileArray))
    visible_files = fileArray[start_index:end_index]

    for filename in visible_files:
        faceName = filename.replace(".jpg", "")
        if faceName in threat_status:
            status = "Threat" if threat_status[faceName] else "Safe"
        else:
            status = "Threat" if default_threat else "Safe"
        time_stamp = datetime.now().strftime("%H:%M:%S")
        Text(logBox, text=f"[{time_stamp}] Detected: {faceName} - {status}", color="white", size=14)


def faceFunction():
    """
    Display a subset of the faces from the TestFolder in the face grid.
    """
    global scroll_position
    # Clear previous widgets from the face grid.
    for widget in faceGrid.children:
        widget.destroy()

    fileArray = sorted(os.listdir("TestFolder"))
    total_faces = len(fileArray)

    if scroll_position >= total_faces:
        scroll_position = max(0, total_faces - visible_faces)

    start_index = scroll_position
    end_index = min(scroll_position + visible_faces, total_faces)

    for local_index, filename in enumerate(fileArray[start_index:end_index]):
        col = local_index % num_columns
        row = local_index // num_columns

        image_path = os.path.join("TestFolder", filename)
        faceName = filename.replace(".jpg", "")

        # Ensure a threat status exists for new (unregistered) faces.
        if faceName not in threat_status:
            threat_status[faceName] = default_threat
            save_security_settings()

        faceOpen = Image.open(image_path)
        finalFace = faceOpen.resize(facesize)

        # Create a container for the face image and its label.
        faceBox = Box(faceGrid, grid=[col, row], layout="auto")
        PushButton(
            faceBox,
            image=finalFace,
            command=lambda name=faceName, path=image_path, face=finalFace: show_face_menu(name, path, face)
        )
        Text(faceBox, text=faceName, color="white", size=14)

    update_log()


def show_face_menu(face_name, image_path, face):
    """
    Open a window to allow editing options for a selected face:
    rename, delete, or toggle its threat status.
    """
    menu = Window(app, title=f"Edit {face_name}", width=255, height=160, layout="grid", bg="black")
    Text(menu, text=f"Editing: {face_name}", color="white", grid=[0, 0, 4, 1])

    def toggle_threat():
        threat_status[face_name] = threat_checkbox.value
        print(f"{face_name} threat status: {threat_status[face_name]}")
        save_security_settings()
        update_log()

    threat_checkbox = CheckBox(menu, text="Threat", grid=[0, 1, 4, 1], command=toggle_threat)
    threat_checkbox.value = threat_status.get(face_name, False)
    threat_checkbox.text_color = "white"
    threat_checkbox.text_size = 20

    def rename_face():
        rename_window = Window(menu, title="Rename Face", width=500, height=175, layout="grid", bg="#669cba")
        Text(rename_window, text="Enter new name:", grid=[0, 0], size=20)
        name_box = TextBox(rename_window, grid=[1, 0], width=15)
        name_box.bg = "white"
        name_box.text_size = 20

        def confirm_rename():
            new_name = name_box.value.strip()
            if new_name:
                new_path = os.path.join("TestFolder", new_name + ".jpg")
                os.rename(image_path, new_path)
                if face_name in threat_status:
                    threat_status[new_name] = threat_status.pop(face_name)
                else:
                    threat_status[new_name] = default_threat
                save_security_settings()
                rename_window.hide()
                menu.hide()
                faceFunction()

        PushButton(rename_window, text="Confirm", command=confirm_rename, grid=[1, 2], width=10, height=2)

    def delete_face():
        os.remove(image_path)
        if face_name in threat_status:
            del threat_status[face_name]
        save_security_settings()
        menu.hide()
        faceFunction()

    # Attach images to the menu (to avoid garbage collection issues).
    menu.rename_img = renamePNG.resize(windowButtonSize)
    menu.delete_img = deletePNG.resize(windowButtonSize)
    menu.cancel_img = cancelPNG.resize(windowButtonSize)

    PushButton(menu, image=menu.rename_img, command=rename_face, grid=[1, 3])
    PushButton(menu, image=menu.delete_img, command=delete_face, grid=[2, 3])
    PushButton(menu, image=menu.cancel_img, command=menu.hide, grid=[3, 3])


def scroll_up():
    """Scroll upward through the list of faces."""
    global scroll_position
    if scroll_position - visible_faces >= 0:
        scroll_position -= visible_faces
    else:
        scroll_position = 0
    faceFunction()


def scroll_down():
    """Scroll downward through the list of faces."""
    global scroll_position
    files = sorted(os.listdir("TestFolder"))
    if scroll_position + visible_faces < len(files):
        scroll_position += visible_faces
    faceFunction()


def uploadFunction():
    """Upload a new JPG file into the TestFolder and register it with the default threat status."""
    filePath = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if filePath:
        filename = os.path.basename(filePath)
        dest_path = os.path.join("TestFolder", filename)
        shutil.copy(filePath, dest_path)
        faceName = filename.replace(".jpg", "")
        threat_status.setdefault(faceName, default_threat)
        save_security_settings()
        print(f"Uploaded {filename} to TestFolder.")
    faceFunction()


def security_settings_menu():
    """
    Open a window to change the default threat setting for new/unregistered faces
    and allow a mass update for all known faces.
    """
    global default_threat, threat_status
    sec_window = Window(app, title="Security Settings", width=650, height=200, layout="grid", bg="black")

    def update_default_threat():
        global default_threat, threat_status
        default_threat = default_threat_checkbox.value
        threat_status["__default_threat__"] = default_threat
        save_security_settings()

    def set_all_faces(status):
        global threat_status
        for key in list(threat_status.keys()):
            if key == "__default_threat__":
                continue
            threat_status[key] = status
        save_security_settings()
        faceFunction()  # Refresh the UI.

    Text(sec_window, text="Choose an action below:", grid=[0, 0, 3, 1], color="white", size=20)
    Text(sec_window, text="Default threat setting for unregistered faces:", grid=[0, 1, 2, 1], color="white", size=20)
    default_threat_checkbox = CheckBox(sec_window, text="Threat", grid=[2, 1], command=update_default_threat)
    default_threat_checkbox.value = default_threat
    default_threat_checkbox.text_color = "white"
    default_threat_checkbox.text_size = 20

    PushButton(sec_window, text="Set All Faces to Threat", grid=[0, 2],
               command=lambda: set_all_faces(True), image=threatButton)
    PushButton(sec_window, text="Set All Faces to Non-threat", grid=[1, 2],
               command=lambda: set_all_faces(False), image=safeButton)


# ---------------------------
# GUI Creation & Initialization
# ---------------------------

# Create the main app using a grid layout.
app = App(title="Face Detection Dashboard", width=1920, height=1080, layout="grid", bg="black")

# Header Section (row 0)
headerBox = Box(app, grid=[0, 0], width=1920, height=150, layout="grid")
Picture(headerBox, image="logo.PNG", grid=[0, 0])
PushButton(headerBox, image=plusIcon, grid=[1, 0], command=uploadFunction)
secButton = PushButton(headerBox, image=secIcon, grid=[2, 0], command=security_settings_menu)
secButton.bg = "white"

# Main Content: Face Grid (left) and Log Panel (right)
mainBox = Box(app, grid=[0, 1], width=1920, height=800, layout="grid")
faceContainer = Box(mainBox, grid=[0, 0], width=1500, height=800, layout="grid")
faceGrid = Box(faceContainer, grid=[0, 0], layout="grid")

# Log Panel (right). 'bg' isn’t supported in the constructor so we set it after.
logBox = Box(mainBox, grid=[1, 0], width=400, height=800, layout="grid", border=True)
logBox.bg = "black"
Text(logBox, text="Live Detection Log", color="white", size=16)

# Scroll Control Section (row 2)
scrollBox = Box(app, grid=[0, 2], width=1920, height=100, layout="grid")
PushButton(scrollBox, text="Scroll Up", command=scroll_up, grid=[0, 0], image=upArrow)
PushButton(scrollBox, text="Scroll Down", command=scroll_down, grid=[1, 0], image=downArrow)

# Initialize the face grid.
faceFunction()
app.display()
