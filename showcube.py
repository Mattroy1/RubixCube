from tkinter import *
from cube import Cube
from time import sleep
import os
from PIL import Image
import pyperclip as pc

#Get Images path
imagesFile = os.path.join(__file__,"..","Images")

#Delete extra image files
for i in os.listdir(imagesFile):
    if len(i)>3 and i[-3:]=="png":
        if i[:-4] not in ["randomizeButton512", "resetButton300"]:
            os.remove(os.path.join(imagesFile, i))

#Constants
SQUARE_SIZE = 312
RANDOM_BUTTON_SIZE = 200
FONT = ('Times', 14)
ROTATION_DIRECTION_INPUT = ['w','s','a','d']
#ROTATE_CUBE_INPUT = ['u','j','h','k']
ROTATION_SELECTION = ["<Up>","<Down>","<Left>","<Right>"]
CONTROLS = ["Click a Face > Rotates the Cube","                       to the clicked face", "", 
            "Arrow Keys > Highlight part of the ","                      cube you want to move", "",
            "WASD > Move highlighted part in ","               the selected direction"]

#Resize images
for i in os.listdir(imagesFile):
    image = Image.open(os.path.join(imagesFile,i))
    new_image = image.resize((RANDOM_BUTTON_SIZE, RANDOM_BUTTON_SIZE))
    tempname = i[:-7]+i[-4:]
    new_image.save(os.path.join(imagesFile,tempname))

# Create the tkinter window
window = Tk()
window.state('zoomed')
window.title("Rubix Cube")
frame = Frame(window)

#Initialize variables
randomize_button_image = PhotoImage(file=os.path.join(imagesFile,"randomizeButton.png"))
reset_button_image = PhotoImage(file=os.path.join(imagesFile,"resetButton.png"))
possible_highlights = [1, 3, 5, 7, 9, 11, 13, 15, 17]
canvases = []
current_side = 38
logs = []

# Create the nine squares and add them to the frame
show = ['01','10','11','12','13','21']
colors = {'W':"white",'G':"green",'O':"#FF7900",'B':"blue",'R':"red",'Y':"yellow"}
rubix = Cube()
def showCube(event):
    global logs_listbox
    while len(rubix.logs) > len(logs) and len(rubix.logs)>0:
        current_log = rubix.logs[len(logs)]
        logs.append(current_log)
        logs_listbox.insert(0, current_log+"- "+str(len(logs)))
    colorgrabber = 0
    canvas_title = 0
    faces = rubix.tkinterDisplay()
    for i in range(3):
        for j in range(4):
            if ((str(i) + str(j)) in show):
                square = Canvas(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, bg='gray', name=str(canvas_title))
                square.bind("<Button-1>", chooseCanvas)
                square.grid(row=i, column=j)
                canvases.append(square)
                canvas_title += 1
                for row in range(3):
                    for col in range(3):
                        x1 = ((col + 1) * 18 + 2) + (col * 80)
                        y1 = ((row + 1) * 18 + 2) + (row * 80)
                        x2 = x1 + 80
                        y2 = y1 + 80
                        rectobj = square.create_rectangle(col*98+2, row*98+2, col*98+100+18, row*98+100+18, fill="", outline="")
                        square.create_rectangle(x1, y1, x2, y2, fill=colors[faces[colorgrabber]])
                        colorgrabber += 1
            if event == '1':
                if ((str(i) + str(j))) == '00':
                    controls_area = Frame(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, name="controls_box")
                    controls_label = Label(controls_area, text="Controls", width=30, font=FONT)
                    controls_listbox = Listbox(controls_area, font=FONT)
                    for control in CONTROLS:
                        controls_listbox.insert(END, control)
                    controls_label.pack(anchor='c')
                    controls_listbox.pack(anchor='c', fill=X, expand=YES)
                    controls_area.grid(row=i, column=j)
                if ((str(i) + str(j))) == '02':
                    logs_area = Frame(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, name="logs_box")
                    logs_label = Label(logs_area, text="Logs   ", font=FONT)
                    logs_scrollbar = Scrollbar(logs_area)
                    logs_listbox = Listbox(logs_area, font=FONT, width=8, yscrollcommand=logs_scrollbar.set, selectmode=EXTENDED)
                    logs_selectall_button = Button(logs_area, text="Copy \nHighlight", font=("Times",7), command=lambda:copyNotation("highlight"))
                    logs_selecthighlight_button = Button(logs_area, text="Copy \nAll", font=("Times",7), command=lambda:copyNotation("all"))
                    logs_label.grid(row=1, column=1, columnspan=4, sticky='NSEW')
                    logs_listbox.grid(row=2, column=1, rowspan=5, columnspan=2, sticky='NSE')
                    logs_scrollbar.grid(row=2, column=3, rowspan=5, columnspan=2, sticky='NSW')
                    logs_selecthighlight_button.grid(row=7, column=1, sticky='NSEW')
                    logs_selectall_button.grid(row=7, column=2, sticky='NSEW')
                    logs_scrollbar.config(command=logs_listbox.yview)
                    logs_area.grid(row=i, column=j)
                if ((str(i) + str(j))) == '03':
                    cubemovement_area = Frame(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, name="cubemovement_box")
                    cubemovement_button_options = [["F ","B ","X ","Y "],["F'","B'","X'","Y'"],["L ","R ","U ","D "],["L'","R'","U'","D'"]]
                    cubemovement_buttons1 =  Button(cubemovement_area, text="F" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("F "))
                    cubemovement_buttons2 =  Button(cubemovement_area, text="B" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("B "))
                    cubemovement_buttons3 =  Button(cubemovement_area, text="X" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("X "))
                    cubemovement_buttons4 =  Button(cubemovement_area, text="Y" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("Y "))
                    cubemovement_buttons5 =  Button(cubemovement_area, text="F'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("F'"))
                    cubemovement_buttons6 =  Button(cubemovement_area, text="B'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("B'"))
                    cubemovement_buttons7 =  Button(cubemovement_area, text="X'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("X'"))
                    cubemovement_buttons8 =  Button(cubemovement_area, text="Y'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("Y'"))
                    cubemovement_buttons9 =  Button(cubemovement_area, text="L" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("L "))
                    cubemovement_buttons10 = Button(cubemovement_area, text="R" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("R "))
                    cubemovement_buttons11 = Button(cubemovement_area, text="U" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("U "))
                    cubemovement_buttons12 = Button(cubemovement_area, text="D" , font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("D "))
                    cubemovement_buttons13 = Button(cubemovement_area, text="L'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("L'"))
                    cubemovement_buttons14 = Button(cubemovement_area, text="R'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("R'"))
                    cubemovement_buttons15 = Button(cubemovement_area, text="U'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("U'"))
                    cubemovement_buttons16 = Button(cubemovement_area, text="D'", font=FONT, width=3, height=2, command=lambda:moveCubeFromButton("D'"))
                    cubemovement_buttons1.grid (row=1, column=1, sticky='NSEW')
                    cubemovement_buttons2.grid (row=1, column=2, sticky='NSEW')
                    cubemovement_buttons3.grid (row=1, column=3, sticky='NSEW')
                    cubemovement_buttons4.grid (row=1, column=4, sticky='NSEW')
                    cubemovement_buttons5.grid (row=2, column=1, sticky='NSEW')
                    cubemovement_buttons6.grid (row=2, column=2, sticky='NSEW')
                    cubemovement_buttons7.grid (row=2, column=3, sticky='NSEW')
                    cubemovement_buttons8.grid (row=2, column=4, sticky='NSEW')
                    cubemovement_buttons9.grid (row=3, column=1, sticky='NSEW')
                    cubemovement_buttons10.grid(row=3, column=2, sticky='NSEW')
                    cubemovement_buttons11.grid(row=3, column=3, sticky='NSEW')
                    cubemovement_buttons12.grid(row=3, column=4, sticky='NSEW')
                    cubemovement_buttons13.grid(row=4, column=1, sticky='NSEW')
                    cubemovement_buttons14.grid(row=4, column=2, sticky='NSEW')
                    cubemovement_buttons15.grid(row=4, column=3, sticky='NSEW')
                    cubemovement_buttons16.grid(row=4, column=4, sticky='NSEW')
                    cubemovement_area.grid(row=i, column=j)
                if ((str(i) + str(j))) == '22':
                    randomize_area = Frame(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, name="randomize_box")
                    randomize_button = Button(randomize_area, image=randomize_button_image, bg='gray', activebackground="#D0D0D0", command=onRandomButton)
                    randomize_button.pack(anchor='c')
                    randomize_area.grid(row=i, column=j)
                if ((str(i) + str(j))) == '23':
                    reset_area = Frame(frame, width=SQUARE_SIZE, height=SQUARE_SIZE, name="reset_box")
                    reset_button = Button(reset_area, image=reset_button_image, bg='gray', activebackground="#D0D0D0", command=onResetButton)
                    reset_button.pack(anchor='c')
                    reset_area.grid(row=i, column=j)
    rowSelect(current_side)
    
def rowSelect(event):
    global current_side
    #Clears all highlights
    for i in possible_highlights:
        canvases[-1].itemconfig(i, fill='')
        canvases[0].itemconfig(i, fill='')
    #Checks whether event is an int input or event input
    if type(event) == int:
        side = event
    else:
        side = event.keycode
    #Intilizaes highlight to top row upon startup
    if side == 0:
        canvases[-1].itemconfig(1, fill="black")
        canvases[-1].itemconfig(3, fill="black")
        canvases[-1].itemconfig(5, fill="black")
        current_side = 38
    #Sets the highlight to the entire front face
    elif (current_side == 37 and side == 39) or (current_side == 39 and side == 37) or (current_side == 38 and side == 40) or (current_side == 40 and side == 38) or (side == 1):
        for i in possible_highlights:
            canvases[-1].itemconfig(i, fill="black")
        current_side = 1
    #Sets the highlight to the entire back face
    elif ((current_side == side) and (type(event) != int)) or (side == 2):
        for i in possible_highlights:
            canvases[0].itemconfig(i, fill="black")
        current_side = 2
    #left
    elif side == 37:
        canvases[-1].itemconfig(1, fill="black")
        canvases[-1].itemconfig(7, fill="black")
        canvases[-1].itemconfig(13, fill="black")
        current_side = 37
    #top
    elif side == 38:
        canvases[-1].itemconfig(1, fill="black")
        canvases[-1].itemconfig(3, fill="black")
        canvases[-1].itemconfig(5, fill="black")
        current_side = 38
    #right
    elif side == 39:
        canvases[-1].itemconfig(5, fill="black")
        canvases[-1].itemconfig(11, fill="black")
        canvases[-1].itemconfig(17, fill="black")
        current_side = 39
    #down
    elif side == 40:
        canvases[-1].itemconfig(13, fill="black")
        canvases[-1].itemconfig(15, fill="black")
        canvases[-1].itemconfig(17, fill="black")
        current_side = 40

#chooses which face to rotate based on what side is currently highlighted and what button was just pressed
def chooseRotate(event):
    direction = {ROTATION_DIRECTION_INPUT[0]:'up',ROTATION_DIRECTION_INPUT[1]:'down',ROTATION_DIRECTION_INPUT[2]:'left',ROTATION_DIRECTION_INPUT[3]:'right'}
    if current_side == 1:
        rubix.rotateface(5, direction[event.char])
    if current_side == 2:
        rubix.rotateface(0, direction[event.char])
    if current_side == 37:
        rubix.verticalRotate('left', direction[event.char])
    if current_side == 39:
        rubix.verticalRotate('right', direction[event.char])
    if current_side == 38:
        rubix.horizontalRotate('up', direction[event.char])
    if current_side == 40:
        rubix.horizontalRotate('down', direction[event.char])
    showCube('none')

#Takes the logs and simplifies it a little bit, then copies it to the clipboard
def copyNotation(selection):
    full_notation = []
    to_clipboard = ''
    count = 1
    if selection == "highlight":
        for i in logs_listbox.curselection():
            i = (i+1)*-1
            full_notation.append(logs[i])
            full_notation = full_notation[::-1]
    if selection == "all":
        full_notation = logs
    
    if len(full_notation) == 0:
        return
    combined_notiation = []
    count = 0
    for i in range(len(full_notation)-1):
        if full_notation[i] != full_notation[i+1]:
            combined_notiation.append(''.join(full_notation[count:i+1]))
            count = i+1
        if i == len(full_notation)-2:
            combined_notiation.append(''.join(full_notation[count:]))
    for i in range(len(combined_notiation)):
        in_a_row = len(combined_notiation[i])/2
        if in_a_row % 4 == 0:
            times = '4'
        elif in_a_row % 4 == 2:
            times = '2'
        elif in_a_row % 4 == 3:
            times = '3'
        else:
            times = ''
        to_clipboard += times+combined_notiation[i][:2]
        if combined_notiation[i][1] == "'":
            to_clipboard += " "
        
    if to_clipboard[-1] == ' ':
        to_clipboard = to_clipboard[:-1]
    pc.copy(to_clipboard)

#Move the cube based on the button pressed
def moveCubeFromButton(notation):
    if notation[0] in "BLDRUF":
        face_to_rotate = {"B":0,"L":1,"D":2,"R":3,"U":4,"F":5}[notation[0]]
        direction = {" ":"right","'":"left"}[notation[1]]
        rubix.rotateface(face_to_rotate, direction)
    else:
        face_to_change = {"Y'":1,"X ":2,"Y ":3,"X'":4}[notation]
        rubix.changeFace(face_to_change)
    showCube('none')

#Rotates the cube based on which face was clicked
def chooseCanvas(event):
    rubix.changeFace(int(str(event.widget)[-1]))
    showCube('none')

#When the randomize button is clicked it makes 1000 random moves
def onRandomButton():
    rubix.randomize()
    showCube('none')

#When the reset button is clicked is resets the cube and the logs
def onResetButton():
    rubix.reset()
    logs = []
    logs_listbox.delete(0,END)
    showCube('none')
    

# Pack the frame into the window and start the main loop
showCube('1')
rowSelect(0)
frame.pack()
#window.bind(ROTATE_CUBE_INPUT[0], showCube)
#window.bind(ROTATE_CUBE_INPUT[2], showCube)
#window.bind(ROTATE_CUBE_INPUT[1], showCube)
#window.bind(ROTATE_CUBE_INPUT[3], showCube)
window.bind(ROTATION_DIRECTION_INPUT[0], chooseRotate)
window.bind(ROTATION_DIRECTION_INPUT[2], chooseRotate)
window.bind(ROTATION_DIRECTION_INPUT[1], chooseRotate)
window.bind(ROTATION_DIRECTION_INPUT[3], chooseRotate)
window.bind(ROTATION_SELECTION[0], rowSelect)
window.bind(ROTATION_SELECTION[2], rowSelect)
window.bind(ROTATION_SELECTION[1], rowSelect)
window.bind(ROTATION_SELECTION[3], rowSelect)
window.mainloop()

#Make a tool that gives directions to solve the cube, with formulas or ?optimally
#Make a menu to configure where tools go and their visibility
#Make a bot that solves the cube with common formulas
#Make an AI that solves the cube optimally
#Make an AI that get can start with a solved cube and get into any predetermined cube state