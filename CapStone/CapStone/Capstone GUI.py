from guizero import App, Text, PushButton, Picture, Window, Box, TextBox
from PIL import Image
import shutil
import os
from tkinter import filedialog
# loadining in images
trashcanPNG = Image.open("trashcan.png")
plusPNG = Image.open("plus.png")
secPNG = Image.open("securitySettings.png")
cancelPNG = Image.open("cancel.png")
renamePNG = Image.open("rename.png")
deletePNG = Image.open("delete.png")
# image sizes
iconsize = (140,140)
facesize = (175,175)
windowButtonSize = (80,80)
# image resizing
trashcanIcon = trashcanPNG.resize(iconsize)
plusIcon = plusPNG.resize(iconsize)
secIcon = secPNG.resize(iconsize)
app = App(title="guizero", bg = "black", height = 1080, width = 1920, layout= "grid" )

#faces
faceGrid = Box(app, grid=[0,1], layout="grid")
def faceFunction():
    #updates faces
    for widget in faceGrid.children:
        widget.destroy()
    #intializes for main loop
    fileArray = sorted(os.listdir("TestFolder"))
    count = 0
    xPosCount = 0
    yPosCount = 0

    def show_face_menu(face_name, image_path, face):
        #window setup
        menu = Window(app, title=f"Edit {face_name}", width=600, height=100, layout="grid", bg="black")
        Text(menu, text=f"Editing: {face_name}", color="white", grid=[0,0])

        def rename_face():
            rename_window = Window(menu, title="Rename Face", width=500, height=175, layout="grid", bg="#669cba")
            Text(rename_window, text="Enter new name:", grid=[0,0], size=20)
            name_box = TextBox(rename_window, grid=[1,0], width=15, height=15)
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
            PushButton(rename_window, text="Confirm", command=confirm_rename, grid=[1,2], width=10, height=2)

        def delete_face():
            os.remove(image_path)
            menu.hide()
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
            faceFunction()
            faceFunction()

        #image resizing
        cancelIcon = cancelPNG.resize(windowButtonSize)
        renameIcon = renamePNG.resize(windowButtonSize)
        deleteIcon = deletePNG.resize(windowButtonSize)
        #command buttons
        PushButton(menu, image=renameIcon, command=rename_face, grid=[1,0])
        PushButton(menu, image=deleteIcon, command=delete_face, grid=[2,0])
        PushButton(menu, image=cancelIcon, command=menu.hide, grid=[3,0])

    for x in fileArray:
        image_path = os.path.join("TestFolder", fileArray[count])
        removeFileTag = fileArray[count].replace(".jpg", "")
        faceOpen = Image.open(image_path)
        3
        finalFace = faceOpen.resize(facesize)

        # Create a container box for face + label
        faceBox = Box(faceGrid, grid=[xPosCount, yPosCount], layout="auto")
        face = PushButton(
            faceBox, 
            image=finalFace, 
            command=lambda name=removeFileTag, path=image_path: show_face_menu(name, path, finalFace)
        )
        name = Text(faceBox, text=removeFileTag, color="white")

        count += 1
        xPosCount += 1
        if xPosCount > 4:
            xPosCount = 0
            yPosCount += 2


    

# upload image
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
    faceFunction()

# inital setup
logo = Picture(app, image='logo.PNG', grid=[0,0])
plusButton = PushButton(app, image=plusIcon, grid=[1,0], command=uploadFunction)
secButton = PushButton(app, image=secIcon, grid =[3,0])
secButton.bg = "white"
faceFunction()

# test
app.display()
