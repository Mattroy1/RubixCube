from random import randint, choice
import os

class Cube:
    def __init__(self):
        #ZYX: Where current face is white, and top face is orange
        self.position = [
            [['RYG','RY','RYB'], ['GY','Y','BY'], ['OYG','OY','OYB']], 
            [['RG' ,'R' ,'RB' ], ['G' ,' ','B' ], ['OG' ,'O' ,'OB' ]],
            [['RWG','RW','RWB'], ['GW','W','BW'], ['OWG','OW','OWB']]]
        self.logs = []
        self.randomizing = False

    #returns the colors on each of the faces
    def getFace(self, face:int) -> list:
        #left to right, up to down
        facecolors = []
        if face not in [1,2,3,4]:
            if face == 5:
                face=2
            for i in self.position[face]:
                for j in i:
                    if len(j) > 1:
                        facecolors.append(j[1])
                    else:
                        facecolors.append(j)
        elif face in [1,3]:
            face-=1
            for i in range(3):
                for j in range(3):
                    if j != 1:
                        facecolors.append(self.position[i][j][face][-1])
                    else:
                        facecolors.append(self.position[i][j][face][0])
        elif face in [2,4]:
            face-=2
            for i in range(3):
                for j in self.position[i][face]:
                    facecolors.append(j[0])
        return facecolors
    
    #switches the front face, does not do anything if the front or back is selected
    def changeFace(self, newFace:int) -> None:
        if newFace in [0,5]:
            return
        self.logRotation(newFace)
        faces = []
        for i in range(6):
            faces.append(self.getFace(i))
        if newFace == 1:
            faces = [faces[3], faces[0], faces[2], faces[5], faces[4], faces[1]]
        if newFace == 3:
            faces = [faces[1], faces[5], faces[2], faces[0], faces[4], faces[3]]
        if newFace == 2:
            faces = [faces[4], faces[1], faces[0], faces[3], faces[5], faces[2]]
        if newFace == 4:
            faces = [faces[2], faces[1], faces[5], faces[3], faces[0], faces[4]]
        newpos = [[['','',''],['','',''],['','','']],[['','',''],['','',''],['','','']],[['','',''],['','',''],['','','']]]
        for i in range(3):
            for j in range(3):
                newpos[i][0][j] += faces[2].pop(0)
                newpos[i][2][j] += faces[4].pop(0)
        for i in range(3):
            for j in range(3):
                newpos[0][i][j] += faces[0].pop(0)
                newpos[2][i][j] += faces[5].pop(0)
        for i in range(3):
            for j in range(3): 
                if j != 1:
                    newpos[i][j][0] += faces[1].pop(0)
                    newpos[i][j][2] += faces[3].pop(0)
                else:
                    newpos[i][j][0] = faces[1].pop(0) + newpos[i][j][0] 
                    newpos[i][j][2] = faces[3].pop(0) + newpos[i][j][2] 
        self.position = newpos
                        
    #works in reference to current face
    def rotateface(self, face:int, direction:str) -> None:
        if direction not in ["left", "right"]:
            return
        self.logTurn(face, direction)
        p = self.position
        if face in [0,5]:
            ranges = {"left":[range(3),range(2,-1,-1)], "right":[range(2,-1,-1),range(3)]}[direction]
            if face == 5:
                face = 2
            else:
                ranges = ranges[::-1]
            final = []
            for i in ranges[0]:
                for j in ranges[1]:
                    final.append(p[face][j][i])
            for i in [0,2,6,8]:
                final[i] = final[i][::-1]
            for i in range(3):
                self.position[face][i] = [final.pop(0),final.pop(0),final.pop(0)]
        elif face in [1,3]:
            ranges = [range(2,-1,-1),range(3)]
            if direction == "right":
                ranges = ranges[::-1]
            if face == 3:
                ranges = ranges[::-1]
            face -= 1
            final = []
            for i in ranges[0]:
                for j in ranges[1]:
                    final.append(p[j][i][face])
            for i in range(len(final)):
                j = final[i]
                switchColors = [*j]
                if len(j) > 1:
                    switchColors[0], switchColors[1] = switchColors[1], switchColors[0]
                final[i] = ''.join(switchColors)
            for i in range(3):
                for j in range(3):
                    self.position[i][j][face] = final.pop(0)
        elif face in [2,4]:
            ranges = [range(2,-1,-1),range(3)]
            if direction == "right":
                ranges = ranges[::-1]
            if face == 2:
                ranges = ranges[::-1]
            face -= 2
            final = []
            for i in ranges[0]:
                for j in ranges[1]:
                    final.append(p[j][face][i])
            for i in range(len(final)):
                j = final[i]
                switchColors = [*j]
                if len(j) > 2:
                    switchColors[1], switchColors[2] = switchColors[2], switchColors[1]
                final[i] = ''.join(switchColors)
            for i in range(3):
                for j in range(3):
                    self.position[i][face][j] = final.pop(0)
    
    #for front face only
    def verticalRotate(self, side:str, direction:str) -> None:
        if direction not in ["up","down"]:
            return
        if side == "left":
            if direction == "up":
                self.rotateface(1, "left")
            if direction == "down":
                self.rotateface(1, "right")
        if side == "right":
            if direction == "up":
                self.rotateface(3, "right")
            if direction == "down":
                self.rotateface(3, "left")
            
    #for front face only
    def horizontalRotate(self, side:str, direction:str) -> None:
        if direction not in ["right","left"]:
            return
        if side == "up":
            self.rotateface(4, direction)
        if side == "down":
            self.rotateface(2, direction)

    def randomize(self):
        self.randomizing = True
        for i in range(1000):
            move = randint(1,16)
            direction = move%2
            leftright = {0:"left",1:"right"}[direction]
            updown = {0:"up",1:"down"}[direction]
            if move <= 4:
                self.changeFace(move)
            elif move <= 6:
                self.horizontalRotate("left", updown)
            elif move <= 8:
                self.horizontalRotate("right",updown)
            elif move <= 10:
                self.verticalRotate("up", leftright)
            elif move <= 12:
                self.verticalRotate("down", leftright)
            elif move <= 14:
                self.rotateface(5, leftright)
            elif move <= 16:
                self.verticalRotate(0, leftright)
        self.randomizing = False

    #appends which side was rotated using cube notation
    def logTurn(self, face:int, direction:str) -> None:
        if self.randomizing:
            return
        getlogentry = {0:'B',1:'L',2:'D',3:'R',4:'U',5:'F'}[face] + {"left":"'","right":" "}[direction]
        self.logs.append(getlogentry)
    
    #appends any time the cube itself is rotated using cube notiation(note 1: The cube in this program cannot rotate in the Z direction)
    # (note 2:This is not the same ZYX of self.position, I couldnt make it match without extra effort)
    def logRotation(self, newFace:int) -> None:
        if self.randomizing:
            return
        getlogentry = {1:"Y'",2:"X ",3:"Y ",4:"X'"}[newFace]
        self.logs.append(getlogentry)
    
    #resets all positions of the cube to the original solved version, creates a trial.txt file in the Logs Folder, then clears the logs variable
    def reset(self) -> None:
        self.position =  [
            [['RYG','RY','RYB'], ['GY','Y','BY'], ['OYG','OY','OYB']], 
            [['RG' ,'R' ,'RB' ], ['G' ,' ','B' ], ['OG' ,'O' ,'OB' ]],
            [['RWG','RW','RWB'], ['GW','W','BW'], ['OWG','OW','OWB']]]
        
        '''new_log_num = 1
        for i in os.listdir(os.path.join(__file__,"..","Logs")):
            current_log_num = ''
            for j in i:
                if j.isdigit():
                    current_log_num += j
            if int(current_log_num) > new_log_num:
                new_log_num = int(current_log_num)
        txtPath = os.path.join(__file__,"..","Logs", f"trial{new_log_num}"+'.txt')
        format_logs = ""
        count = 0
        for i in self.logs:
            format_logs += i
            count += 1
            if count == 8:
                count = 0
                format_logs += "\n"
        with open(txtPath, 'w') as f:
            f.write(format_logs)'''
            
        self.logs = []
        
    def clearLogFolder(): 
        for i in os.listdir("Logs"):
            os.remove(os.path.join("Logs",i))


    #create of a list of colors for tkinter
    def tkinterDisplay(self) -> None:
        allcolors = []
        for i in range(6):
            f = self.getFace(i)
            correct = []
            if i in [0,5]:
                correct = self.tkinterFlip(f)
            elif i in [1,3]:
                correct=[f[2],f[5],f[8],f[1],f[4],f[7],f[0],f[3],f[6]]
                if i == 3:
                    correct = correct[::-1]
                    correct = self.tkinterFlip(correct)
            elif i in [2,4]:
                if i == 2:
                    correct = self.tkinterFlip(f)
                else:
                    correct = f
            for j in correct:
                allcolors.append(j)
        return allcolors
    
    def tkinterFlip(self, flippy:list) -> list:
        flipped = []
        for i in range(2,-1,-1):
            i *= 3
            flipped.append(flippy[i])
            flipped.append(flippy[i+1])
            flipped.append(flippy[i+2])
        return flipped