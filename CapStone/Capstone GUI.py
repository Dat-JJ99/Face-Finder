import json
from guizero import App, Text, PushButton, Picture, Window, Box, TextBox, CheckBox
from PIL import Image
import shutil
import os
from tkinter import filedialog
#Boolean file
security_file = "security_settings.json"

def load_security_settings():
    try:
        with open(security_file, "r") as f:
            data = f.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_security_settings():
    with open(security_file, "w") as f:
        json.dump(threat_status, f)
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

# main grid
app = App(title="guizero", bg="black", height=1080, width=1920, layout="grid")

# bounus boxes
scrollBox = Box(app, grid=[0, 1], layout="grid")
faceGrid = Box(scrollBox, grid=[0, 0], layout="grid")

scroll_position = 0
visible_faces = 10
num_columns = 5

def faceFunction():
    global scroll_position
    for widget in faceGrid.children:
        widget.destroy()

    fileArray = sorted(os.listdir("TestFolder"))
    total_faces = len(fileArray)

    # Ensure scroll_position is within bounds.
    if scroll_position >= total_faces:
        scroll_position = max(0, total_faces - visible_faces)

    start_index = scroll_position
    end_index = min(scroll_position + visible_faces, total_faces)

    # Display images in a local grid.
    for local_index, filename in enumerate(fileArray[start_index:end_index]):
        col = local_index % num_columns 
        row = local_index // num_columns

        image_path = os.path.join("TestFolder", filename)
        # Use the filename (without extension) as the face name/key.
        faceName = filename.replace(".jpg", "")

        # If no threat value exists yet, default it to the default_threat.
        if faceName not in threat_status:
            threat_status[faceName] = default_threat
            save_security_settings()

        faceOpen = Image.open(image_path)
        finalFace = faceOpen.resize(facesize)

        # Container for the face image and its label.
        faceBox = Box(faceGrid, grid=[col, row], layout="auto")
        PushButton(
            faceBox,
            image=finalFace,
            command=lambda name=faceName, path=image_path, face=finalFace: show_face_menu(name, path, face)
        )
        Text(faceBox, text=faceName, color="white")

def show_face_menu(face_name, image_path, face):
    """Display the editing window for a selected face (rename, delete, and threat toggle)."""
    menu = Window(app, title=f"Edit {face_name}", width=255, height=160, layout="grid", bg="black")
    Text(menu, text=f"Editing: {face_name}", color="white", grid=[0, 0, 4, 1])
    
    # Function to toggle the threat status for the selected face.
    def toggle_threat():
        threat_status[face_name] = threat_checkbox.value
        print(f"{face_name} threat status: {threat_status[face_name]}")
        save_security_settings()

    # Create the threat checkbox.
    threat_checkbox = CheckBox(menu, text="Threat", grid=[0, 1, 4, 1], command=toggle_threat)
    threat_checkbox.value = threat_status.get(face_name, False)
    threat_checkbox.text_color = "white"
    threat_checkbox.text_size = 20  # Increase the size of the checkbox text

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
                # Update threat_status key.
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
        # Remove threat status for the deleted face.
        if face_name in threat_status:
            del threat_status[face_name]
        save_security_settings()
        menu.hide()
        faceFunction()

    # Attach images to the menu (to avoid garbage collection issues).
    menu.rename_img = renamePNG.resize(windowButtonSize)
    menu.delete_img = deletePNG.resize(windowButtonSize)
    menu.cancel_img = cancelPNG.resize(windowButtonSize)

    # Create buttons using the attached images.
    PushButton(menu, image=menu.rename_img, command=rename_face, grid=[1, 3])
    PushButton(menu, image=menu.delete_img, command=delete_face, grid=[2, 3])
    PushButton(menu, image=menu.cancel_img, command=menu.hide, grid=[3, 3])

def scroll_up():
    global scroll_position
    if scroll_position - visible_faces >= 0:
        scroll_position -= visible_faces
    else:
        scroll_position = 0
    faceFunction()
    faceFunction()
    faceFunction()
    faceFunction()
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

def uploadFunction():
    filePath = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    if filePath:
        filename = os.path.basename(filePath)
        dest_path = os.path.join("TestFolder", filename)
        shutil.copy(filePath, dest_path)
        # Register the new face with the default threat status.
        faceName = filename.replace(".jpg", "")
        threat_status.setdefault(faceName, default_threat)
        save_security_settings()
        print(f"Uploaded {filename} to TestFolder.")
    faceFunction()

def security_settings_menu():
    """Opens a window to change the default threat setting and mass-update known faces."""
    global default_threat, threat_status
    sec_window = Window(app, title="Security Settings", width=650, height=200, layout="grid", bg="black")
    
    # Define callback functions first.
    def update_default_threat():
        global default_threat, threat_status
        default_threat = default_threat_checkbox.value
        threat_status["__default_threat__"] = default_threat
        save_security_settings()
    
    def set_all_faces(status):
        global threat_status
        # Update every key except the reserved default key.
        for key in list(threat_status.keys()):
            if key == "__default_threat__":
                continue
            threat_status[key] = status
        save_security_settings()
        faceFunction()  # Refresh the UI.
    
    # Create widgets with bigger text settings.
    Text(sec_window, text="Choose an action below:", grid=[0, 0, 3, 1], color="white", size=20)
    Text(sec_window, text="Default threat setting for unregistered faces:", grid=[0, 1, 2, 1], color="white", size=20)
    default_threat_checkbox = CheckBox(sec_window, text="Threat", grid=[2, 1], command=update_default_threat)
    default_threat_checkbox.value = default_threat
    default_threat_checkbox.text_color = "white"
    default_threat_checkbox.text_size = 20  # Increase checkbox text size
    
    PushButton(sec_window, text="Set All Faces to Threat", grid=[0, 2],
               command=lambda: set_all_faces(True), image=threatButton)
    PushButton(sec_window, text="Set All Faces to safe", grid=[1, 2],
               command=lambda: set_all_faces(False), image=safeButton)

logo = Picture(app, image="logo.PNG", grid=[0, 0])
plusButton = PushButton(app, image=plusIcon, grid=[1, 0], command=uploadFunction)
secButton = PushButton(app, image=secIcon, grid=[3, 0], command=security_settings_menu)
secButton.bg = "white"

# Scroll control buttons.
scrollUpButton = PushButton(app, text="Scroll Up", command=scroll_up, grid=[0, 2], image=upArrow)
scrollDownButton = PushButton(app, text="Scroll Down", command=scroll_down, grid=[0, 3], image=downArrow)

faceFunction()
app.display()
