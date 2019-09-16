from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter.ttk import Frame, Style
import time, os
import random
from winsound import *

class Game(Canvas):
    def __init__(self, parent, map, agent_learning, agent_logic):
        Canvas.__init__(self, width=420, height=420)
        self.map = map
        self.agent_learning = agent_learning
        self.agent_logic = agent_logic

        self.buttonMusic = Button(text="Music", fg="red", command= self.PlayMusic)
        self.buttonMusic.place(x=630, y=270)
        self.buttonRandom = Button(text="Random Map", fg="red", command=self.RandomMap)
        self.buttonRandom.place(x=630, y=300)
        self.buttonLearning = Button(text = "Use Learning", fg="red", command = self.ButtonLearning_Click)
        self.buttonLearning.place(x=630,y=240)
        self.buttonLogic = Button(text="Use Logic", fg="red", command=self.ButtonLogic_click)
        self.buttonLogic.place(x=630, y=210)
        self.State_label = Label(text = "NULL")
        self.State_label.place(x=630,y=180)

        self.Score = 0
        self.Score_label = Label(text = str(self.Score))
        self.Score_label.place(x=630,y=150)

        self.Inizaline_Map()
        self.parent = parent
        self.pack()
    def RandomMap(self):
        map = np.zeros(shape=(10, 10), dtype=int)
        pits = 8
        wumpus = 5
        gold = 13

        for i in range(pits):
            row = np.random.randint(0, 10)
            column = np.random.randint(0, 10)
            map[row][column] = 1
            SetCells(map, row, column, 2)

        for i in range(wumpus):
            row = np.random.randint(0, 10)
            column = np.random.randint(0, 10)
            map[row][column] = 3
            SetCells(map, row, column, 4)

        for i in range(gold):
            row = np.random.randint(0, 10)
            column = np.random.randint(0, 10)
            map[row][column] = 5

        self.map = map


    def ButtonLogic_click(self):
        self.delete(ALL)
        self.initGame_UseLogic()
    def ButtonLearning_Click(self):
        self.delete(ALL)
        self.initGame_UseLearning()

    def Inizaline(self):
        self.maps = Image.open("maps.jpg")
        self.maps.thumbnail((41, 41), Image.ANTIALIAS)
        self.maps_location = ImageTk.PhotoImage(self.maps)

        self.wind = Image.open("ani-win.gif")
        self.wind.thumbnail((30, 30), Image.ANTIALIAS)
        self.wind_location = ImageTk.PhotoImage(self.wind)

        self.windy = self.create_image((15, 15))
        self.playerRun = self.create_image((15, 15))

        self.layer = Image.open("ani-win.gif")
        self.layer.thumbnail((402, 406), Image.ANTIALIAS)
        self.layer_location = ImageTk.PhotoImage(self.layer)

        self.player = Image.open("mario.gif")
        self.player.thumbnail((40, 40), Image.ANTIALIAS)
        self.player_location = ImageTk.PhotoImage(self.player)

        self.wumpus = Image.open("wumpus-mario.gif")
        self.wumpus.seek(0)
        image1 = self.wumpus.transpose(Image.FLIP_LEFT_RIGHT)
        image1.thumbnail((30, 30), Image.ANTIALIAS)
        self.wumpus_location = ImageTk.PhotoImage(image1)

        self.lane = Image.open("lane.jpg")
        self.lane.thumbnail((40, 40), Image.ANTIALIAS)
        self.lane_location = ImageTk.PhotoImage(self.lane)

        self.pit = Image.open("pit.jpg")
        self.pit.thumbnail((30, 30), Image.ANTIALIAS)
        self.pit_locaion = ImageTk.PhotoImage(self.pit)

        self.gold = Image.open("gold-mario.gif")
        self.gold.thumbnail((30, 30), Image.ANTIALIAS)
        self.gold_location = ImageTk.PhotoImage(self.gold)

        self.smell = Image.open("smoke.gif")
        self.smell.thumbnail((30, 30), Image.ANTIALIAS)
        self.smell_location = ImageTk.PhotoImage(self.smell)

        self.hide = Image.open("hide.jpg")
        self.hide.thumbnail((30, 30), Image.ANTIALIAS)
        self.hide_location = ImageTk.PhotoImage(self.hide)

        self.imageObject = Image.open("mario.gif")
        self.imageObject.seek(0)
        image = self.imageObject.transpose(Image.FLIP_LEFT_RIGHT)
        image.thumbnail((40, 40), Image.ANTIALIAS)
        self.player_location1 = ImageTk.PhotoImage(image)

        self.YouWin = False
        self.GameOver = False
        self.checkPlayRun = False
        self.left = False
        self.right = False
        self.down = False
        self.up = False
        self.check = False
        self.checkgame = True
        self.checkWind = False
        self.checkSmell = False
        self.IsMusic = False
        self.row = 0
        self.column  = 9

    def PlayMusic(self):
        if self.IsMusic:
            self.IsMusic = False
            PlaySound(None,SND_FILENAME)
        else:
            self.IsMusic = True
            PlaySound("mario.wav",SND_FILENAME | SND_LOOP | SND_ASYNC)
    def Inizaline_Map(self):

        self.Inizaline()
        self.Maps()
        #self.Create_Object()
        self.create_map()

    def initGame_UseLearning(self):
        self.Inizaline_Map()

        current_row, current_column = self.agent_learning.get_position()
        self.x, self.y = self.Player_Location(10 + current_column * 40, 15 + 40 * current_row)

        self.agent_learning.training(self.map)
        while not self.agent_learning.done():
            row, column = self.agent_learning.get_action()
            self.agent_learning.move(row, column, self.map[row][column])
            self.Move(column, row)
            self.Score = self.agent_learning.get_total_rewards()
            self.Animation()
            self.IsGameOver()
            self.IsYouWin()
            time.sleep(0.1)
        #...............Code phan than Learning giong UseLogic
    def initGame_UseLogic(self):
        self.Inizaline_Map()
        current_row, current_column = self.agent_logic.get_position()
        self.x, self.y = self.Player_Location(10 + current_column * 40, 15 + 40 * current_row)

        while not self.agent_logic.done():
            row, column = self.agent_logic.get_action()
            if row is None or column is None:
                return

            self.agent_logic.move(row, column, self.map[row][column])
            self.Move(column, row)
            self.Score = self.agent_logic.get_total_rewards()
            self.Animation()
            self.IsGameOver()
            self.IsYouWin()
            time.sleep(0.5)

    def Game_Delete(self):
        self.delete(ALL)
    def Game_destroy(self):
        self.destroy()
    def IsGameOver(self):
        if self.GameOver == True:
            self.Animation_GameOver()
    def IsYouWin(self):
        if self.YouWin == True:
            self.Animation_Winner()
    def Animation(self):
        if self.check == True:
            return
        for i in range(0,16,1):
            self.ObjectAnimation(i)
    def Animation_Winner(self):
        self.delete(ALL)
        self.win = Image.open("winner.gif")
        self.win.thumbnail((410, 410), Image.ANTIALIAS)
        self.winner = ImageTk.PhotoImage(self.win)
        win = self.create_image(10, 10, image=self.winner, anchor=NW)
        i = 0
        while 1:
            self.win.seek(i % 2)
            image4 = self.win.transpose(Image.FLIP_LEFT_RIGHT)
            image4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
            image4.thumbnail((410, 410), Image.ANTIALIAS)
            frame4 = ImageTk.PhotoImage(image4)
            self.itemconfig(win, image=frame4)
            time.sleep(0.1)
            self.update()
            i=i+1
    def Animation_GameOver(self):
        self.delete(ALL)
        self.gameover = Image.open("gameover.gif")
        self.gameover.thumbnail((410,410), Image.ANTIALIAS)
        self.the_end = ImageTk.PhotoImage(self.gameover)
        gameover = self.create_image(10,10 , image = self.the_end, anchor = NW)
        i=0
        while 1:
            self.gameover.seek(i % 12)
            image4 = self.gameover.transpose(Image.FLIP_LEFT_RIGHT)
            image4 = image4.transpose(Image.FLIP_LEFT_RIGHT)
            image4.thumbnail((410,410), Image.ANTIALIAS)
            frame4 = ImageTk.PhotoImage(image4)
            self.itemconfig(gameover, image=frame4)
            time.sleep(0.1)
            self.update()
            i=i+1
    def ObjectAnimation(self,i):

        if self.checkWind == True:
            self.wind.seek(i%8)
            image4 = self.wind.transpose(Image.FLIP_LEFT_RIGHT)
            frame4 = ImageTk.PhotoImage(image4)
            self.itemconfig(self.windy, image=frame4)

        if self.checkSmell == True:
            self.smell.seek(i)
            image5 = self.smell.transpose(Image.FLIP_LEFT_RIGHT)
            image5.thumbnail((30,30), Image.ANTIALIAS)
            frame5 = ImageTk.PhotoImage(image5)
            self.itemconfig(self.sm, image=frame5)

        gold = self.find_withtag("gold")

        self.gold.seek(i)
        image = self.gold.transpose(Image.FLIP_LEFT_RIGHT)
        image.thumbnail((30, 30), Image.ANTIALIAS)
        frame = ImageTk.PhotoImage(image)
        for e in range(0,len(gold)):
            self.itemconfig(gold[e], image=frame)

        wumpus = self.find_withtag("wumpus")
        self.wumpus.seek(i)
        image1 = self.wumpus.transpose(Image.FLIP_LEFT_RIGHT)
        image1.thumbnail((30, 30), Image.ANTIALIAS)
        frame1 = ImageTk.PhotoImage(image1)
        for k in range(0, len(wumpus), 1):
            self.itemconfig(wumpus[k], image=frame1)
        time.sleep(0.05)
        self.update()

        self.DeleteWumpus()
        self.DeleteGold()

    def PlayerRun(self,x,y, str):
        i = 12
        k = 0
        gold = self.find_withtag("gold")
        wumpus = self.find_withtag("wumpus")
        while 1:
            if k == 10:
                break;
            i = (i + 1)
            if i >= 12:
                i = 0

            self.imageObject.seek(i)
            image2 = self.imageObject.transpose(Image.FLIP_LEFT_RIGHT)
            if str != "Left":
                image3 = image2.transpose(Image.FLIP_LEFT_RIGHT)
                image3.thumbnail((40,40), Image.ANTIALIAS)
                frame3 = ImageTk.PhotoImage(image3)
                self.itemconfig(self.playerRun, image=frame3)
                self.move(self.playerRun, x, y)
            else:
                image2.thumbnail((40, 40), Image.ANTIALIAS)
                frame2 = ImageTk.PhotoImage(image2)
                self.itemconfig(self.playerRun, image=frame2)
                self.move(self.playerRun, x, y)

            self.gold.seek(i)
            image = self.gold.transpose(Image.FLIP_LEFT_RIGHT)
            image.thumbnail((30, 30), Image.ANTIALIAS)
            frame = ImageTk.PhotoImage(image)
            for e in range(0, len(gold)):
                self.itemconfig(gold[e], image=frame)

            self.wumpus.seek(i)
            image1 = self.wumpus.transpose(Image.FLIP_LEFT_RIGHT)
            image1.thumbnail((30, 30), Image.ANTIALIAS)
            frame1 = ImageTk.PhotoImage(image1)
            for f in range(0, len(wumpus), 1):
                self.itemconfig(wumpus[f], image=frame1)
            time.sleep(0.02)
            k = k + 1
            self.update()
        self.DeleteWumpus()
        self.DeleteGold()

    def DeleteWumpus(self):
        wumpus = self.find_withtag("wumpus")
        for i in range(0,len(wumpus)):
            x,y = self.coords(wumpus[i])
            self.delete(wumpus[i])
            self.Create_Wumpus(x,y)

    def DeleteGold(self):
        gold = self.find_withtag("gold")
        for i in range(0, len(gold)):
            x, y = self.coords(gold[i])
            self.delete(gold[i])
            self.Create_Gold(x, y)

    def Create_Object(self):
        maps = open('aps.txt','r')
        for i in range(0,10):
            line = maps.readline()
            for k in range(0,len(line)):
                if line[k] == 'G':
                    count = line.count('.',0,k)
                    self.Create_Gold(15 + count*40, 15 + i*40)
                if line[k] == 'W':
                    count = line.count('.', 0, k)
                    self.Create_Wumpus(15 + count * 40, 15 + i * 40)
                if line[k] == 'P':
                    count = line.count('.', 0, k)
                    self.Create_Pit(15 + count * 40, 15 + i * 40)
                if line[k] == 'B':
                    count = line.count('.',0,k)
                    self.Create_Breeze(15 + count*40, 15 + i*40)
                if line[k] == 'S':
                    count = line.count('.', 0, k)
                    self.Create_Stench(20 + count*40,20 + i*40)
    def Color(self, x ,y):
        self.create_image((x,y), image = self.lane_location, anchor = NW, tag = "lane")
    def SwapLocation(self,column,row):
        column = 10 + 40 * column
        row = 15 + 40 * row
        return column, row

    def Maps(self):
        self.create_rectangle(10, 50, 50, 10)
        self.Create_tiles(10,10)
        for k in range(0, 361, 40):
            for i in range(0, 321, 40):
                self.create_rectangle(50 + i, 10 + k, 90 + i, 50 + k)
                self.Create_tiles(50+i,10+k)
        for i in range(0, 321, 40):
            self.create_rectangle(10, 50+i, 50, 90+i)
            self.Create_tiles(10,50+i)
        self.pack(fill = BOTH, expand = 1)

    def onKeyPressed(self,e):
        if e.keysym == "Left":
            if self.checkLocation(self.row - 1, self.column) == False:
                return
        if e.keysym == "Right":
            if self.checkLocation(self.row + 1, self.column) == False:
                return
        if e.keysym == "Up":
            if self.checkLocation(self.row, self.column - 1) == False:
                return
        if e.keysym == "Down":
            if self.checkLocation(self.row, self.column + 1) == False:
                return
        if self.check == True:
            return

        self.checkWind = False
        self.checkSmell = False
        self.check = True

        key = e.keysym
        list = ["Left", "Right", "Up", "Down"]
        if key not in list:
            return
        if key in list :
            self.delete(self.windy)
            location = self.find_withtag("player")
            if len(location) !=0:
                self.delete(location[0])

        if key == "Left":
            self.Move(self.row -1, self.column)
            self.checkCondision()
        if key == "Right":
            self.Move(self.row+1, self.column)
            self.checkCondision()
        if key == "Down":
            self.Move(self.row, self.column+1)
            self.checkCondision()

        if key == "Up":
            self.Move(self.row, self.column - 1)
            #self.Top(self.x,self.y-40)
            self.checkCondision()

        if key == "Escape":
            self.quit()
    def Move(self,x,y):
        self.checkWind = False
        self.checkSmell = False
        self.check = True

        x , y =self.SwapLocation(x,y)
        location = self.find_withtag("player")
        if len(location) != 0:
            self.delete(location[0])

        if self.x == x:
            if self.y > y:
                self.Top(x,y)
            else:
                self.Down(x,y)
        else:
            if self.y == y:
                if self.x > x:
                    self.Left(x,y)
                else:
                    self.Right(x,y)
    def Left(self,x,y):
        x= x+40
        self.playerRun = self.create_image(x + 15, y + 15, image=self.player_location)
        self.PlayerRun(-4, 0, "Left")
        self.check = False
        self.Color(self.x,self.y)
        self.row -=1
        self.x, self.y = self.Player_Location1(x - 40, y)
        self.checkCondision()
    def Top(self,x,y):
        y= y+40
        self.playerRun = self.create_image(x + 15, y + 15, image=self.player_location)
        self.PlayerRun(0, -4, "Up")
        self.check = False
        self.column -=1
        self.Color(self.x, self.y)
        self.x, self.y = self.Player_Location(x, y - 40)
        self.checkCondision()
    def Down(self,x,y):
        y=y-40
        self.playerRun = self.create_image(x + 15, y + 15, image=self.player_location)
        self.PlayerRun(0, 4, "Down")
        self.check = False
        self.column +=1
        self.Color(self.x, self.y)
        self.x, self.y = self.Player_Location(x, y + 40)
        self.checkCondision()
    def Right(self,x,y):
        x= x-40
        self.playerRun = self.create_image(x + 15,y + 15, image=self.player_location)
        self.PlayerRun(4, 0, "Right")
        self.check = False
        self.Color(self.x, self.y)
        self.row +=1
        self.x, self.y = self.Player_Location(x + 40, y)
        self.checkCondision()
    def checkLocation(self,row,column):
        if row < 0 or column < 0 or row > 9 or column > 9:
            return  False;
        return True;
    def Player_Location(self, x, y):
        if x < 0 or y < 0 or y > 411 or x > 411:
            self.create_image(self.x, self.y, image=self.player_location, anchor = NW, tag="player")
            return self.x, self.y
        self.create_image(x, y, image=self.player_location, anchor=NW, tag="player")
        return x, y

    def Player_Location1(self, x, y):
        if x < 0 or y < 0 or y > 411 or x > 411:
            self.create_image(self.x, self.y, image=self.player_location1, anchor = NW, tag="player")
            return self.x, self.y
        self.create_image(x, y, image=self.player_location1, anchor=NW, tag="player")
        return x, y
    def Create_tiles(self,x,y):
        self.create_image(x,y, image = self.maps_location, anchor = NW, tag = "tiles")
    def Create_Wumpus(self,x,y):
        self.create_image(x,y,image = self.wumpus_location, anchor = NW, tag = "wumpus")
    def Create_Pit(self,x,y):
        self.create_image(x,y, image = self.pit_locaion, anchor = NW, tag = "pit")
    def Create_Hide(self,x, y):
        self.create_image(x, y, image = self.hide_location, anchor = NW, tag = "hide")
    def Create_Gold(self,x,y):
        self.create_image(x,y, image = self.gold_location, anchor = NW, tag = "gold")
    def Create_Breeze(self,x,y):
        self.create_image(x,y, image=self.wind_location, anchor=NW, tag="breeze")
    def Create_Stench(self,x,y):
        self.create_image(x,y, image = self.smell_location, anchor = NW, tag = "stench")

    def create_map(self):
        for row in range(10):
            for column in range(10):
                if self.map[row][column] == 1:
                    self.Create_Pit(15 + column * 40, 15 + row * 40)
                if self.map[row][column] == 2:
                    self.Create_Breeze(15 + column * 40, 15 + row * 40)
                if self.map[row][column] == 3:
                    self.Create_Wumpus(15 + column * 40, 15 + row * 40)
                if self.map[row][column] == 4:
                    self.Create_Stench(15 + column * 40, 15 + row * 40)
                if self.map[row][column] == 5:
                    self.Create_Gold(15 + column * 40, 15 + row * 40)

    def checkCondision(self):
        wumpus = self.find_withtag("wumpus")
        pit = self.find_withtag("pit")
        gold = self.find_withtag("gold")
        player = self.find_withtag("player")
        breeze = self.find_withtag("breeze")
        smell = self.find_withtag("stench")
        x1, y1, x2, y2 = self.bbox(player)
        overlap = self.find_overlapping(x1,y1,x2,y2)
        self.State_label.destroy()
        self.State_label = Label(text="NULL")
        self.State_label.place(x=630, y=180)
        for over in overlap:
            for wum in wumpus:
                if wum == over:
                    self.State_label.destroy()
                    self.State_label = Label(text = "Wumpus")
                    self.State_label.place(x=630,y=180)
                    self.check = False
                    self.checkgame = False
                    self.GameOver = True
                    print("Game Over, You are killed by Wumpus")

            for pi in pit:
                if pi == over:
                    self.State_label.destroy()
                    self.State_label = Label(text="Pit")
                    self.State_label.place(x=630, y=180)
                    self.check = False
                    self.checkgame = False
                    self.GameOver = True
                    print("Game Over, You are falling into the pit")

            for go in gold:
                if go == over:
                    self.delete(go)
                    self.Score+=100

                    self.Score_label.destroy()
                    self.Score_label = Label(text=str(self.Score))
                    self.Score_label.place(x=630, y=150)

                    self.State_label.destroy()
                    self.State_label = Label(text="Gold")
                    self.State_label.place(x=630, y=180)
                    PlaySound("mario_coin.wav", SND_FILENAME | SND_ASYNC )
                    print("You got 100 point")
                    if len(gold) == 1:
                        print("You Win")
                        self.YouWin = True

            for be in breeze:
                if be == over:
                    print("WIND")
                    self.State_label.destroy()
                    self.State_label = Label(text="Breeze")
                    self.State_label.place(x=630, y=180)
                    x1,y1,x2,y2 = self.bbox(be)
                    self.windy = self.create_image((x1 + 20, y1), image=self.wind_location)
                    self.checkWind = True


            for sm in smell:
                if sm == over:
                    print("Stench")
                    self.State_label.destroy()
                    self.State_label = Label(text="Stench")
                    self.State_label.place(x=630, y=180)
                    x1, y1, x2, y2 = self.bbox(sm)
                    self.sm = self.create_image((x1+15, y1+15), image=self.smell_location)
                    self.checkSmell = True


def GenerateMap(filename):
    map = np.zeros(shape=(10, 10), dtype=int)
    pits = 8
    wumpus = 5
    gold = 13
    gold_state = 0

    """for i in range(pits):
        row = np.random.randint(0, 10)
        column = np.random.randint(0, 10)
        map[row][column] = 1
        SetCells(map, row, column, 2)

    for i in range(wumpus):
        row = np.random.randint(0, 10)
        column = np.random.randint(0, 10)
        map[row][column] = 3
        SetCells(map, row, column, 4)

    for i in range(gold):
        row = np.random.randint(0, 10)
        column = np.random.randint(0, 10)
        map[row][column] = 5
        gold_state = row * 10 + column"""
    maps = open(filename, 'r')
    for i in range(0, 10):
        line = maps.readline()
        for k in range(0, len(line)):
            if line[k] == 'P':
                count = line.count('.', 0, k)
                map[i][count] = 1
                SetCells(map, i, count, 2)
            if line[k] == 'W':
                count = line.count('.', 0, k)
                map[i][count] = 3
                SetCells(map, i, count, 4)

            if line[k] == 'G':
                count = line.count('.',0,k)
                map[i][count] = 5

    temp = maps.readline()
    K = int(temp)
    init_row = np.random.randint(0, 10)
    init_column = np.random.randint(0, 10)

    while map[init_row][init_column] == 1 or map[init_row][init_column] == 3 or map[init_row][init_column] == 5:
        init_row = np.random.randint(0, 10)
        init_column = np.random.randint(0, 10)

    return map, init_row, init_column, K


import numpy as np


class Cell:

    def __init__(self, row, column):
        self.row = row
        self.column = column


def SetCells(map, row, column, value):
    cells = []
    cells.append(Cell(row, column - 1))
    cells.append(Cell(row, column + 1))
    cells.append(Cell(row - 1, column))
    cells.append(Cell(row + 1, column))

    for cell in cells:
        if -1 < cell.row < 10 and -1 < cell.column < 10:
            map[cell.row][cell.column] = value


def GetCells(row, column):
    cells = []
    cells.append(Cell(row, column - 1))
    cells.append(Cell(row, column + 1))
    cells.append(Cell(row - 1, column))
    cells.append(Cell(row + 1, column))

    list = []

    for cell in cells:
        if -1 < cell.row < 10 and -1 < cell.column < 10:
            list.append(cell)

    return list

# 1 - Pit
# 2 - Breeze
# 3 - Wumpus
# 4 - Stench
# 5 - Gold



def UpdateRewardTable(rewards, row, column, value):
    cells = GetCells(row, column)

    for cell in cells:
        rowIndex = cell.row * 10 + cell.column
        columnIndex = row * 10 + column
        rewards[rowIndex][columnIndex] = value


def CreateRewardTable():
    rewards = np.zeros(shape=(100, 100), dtype=int)

    for row in range(10):
        for column in range(10):
            cells = GetCells(row, column)
            rowIndex = row * 10 + column

            for cell in cells:
                columnIndex = cell.row * 10 + cell.column
                rewards[rowIndex][columnIndex] = -1

    return rewards


def DictionaryMap(x):
    dictMap = {
        0: -1,
        1: -10000,
        2: -1,
        3: -10000,
        4: -1,
        5: 100
    }

    return dictMap[x]


rewardMap = {
        0: -10,
        1: -10000,
        2: -10,
        3: -10000,
        4: -10,
        5: -10
}


def ConvertMapToReward(map, reward):
    for row in range(10):
        for column in range(10):
            cells = GetCells(row, column)

            for cell in cells:
                rowIndex = cell.row * 10 + cell.column
                columnIndex = row * 10 + column
                reward[rowIndex][columnIndex] = DictionaryMap(map[row][column])


gamma = 0.4
alpha = 0.8
esilon = 0.1


class AgentLearning:
    def __init__(self, row, column, max_move):
        self.map = np.zeros(shape=(10, 10), dtype=int)
        self.current_row = row
        self.current_column = column
        self.current_state = row * 10 + column
        self.rewards_table = CreateRewardTable()
        self.q_table = np.array(np.zeros([100, 100]))
        self.max_move = max_move
        self.total_rewards = 0
        self.eposide = 35

    def move(self, row, column, value):
        temp = rewardMap[value]
        UpdateRewardTable(self.rewards_table, row, column, temp)
        self.current_row = row
        self.current_column = column
        self.current_state = self.current_row * 10 + self.current_column

        old_reward = self.total_rewards
        self.total_rewards += DictionaryMap(value)

        if old_reward - self.total_rewards > 1:
            self.eposide -= 1

        self.update_q_table(row, column)
        self.max_move -= 1

    def get_position(self):
        return self.current_row, self.current_column

    def get_action(self):
        action = self.evaluation()
        row = int(action / 10)
        column = int(action % 10)

        return row, column

    def update_q_table(self, row, column):
        next_state = row * 10 + column
        list = GetCells(row, column)

        for cell in list:
            current_state = cell.row * 10 + cell.column

            rewards_copy = self.rewards_table
            play_actions = []
            for m in range(100):
                if rewards_copy[next_state][m] != 0:
                    play_actions.append(m)

            max_next_state = self.q_table[next_state][play_actions[0]]
            action = play_actions[0]

            for item in play_actions:
                if self.q_table[next_state][item] > max_next_state:
                    max_next_state = self.q_table[next_state][item]
                    action = item
                elif self.q_table[next_state][item] == max_next_state:
                    if random.random() < 0.8:
                        action = item

            next_max = action

            TD = self.rewards_table[current_state, next_state] + gamma * self.q_table[next_state, next_max] - \
                 self.q_table[current_state, next_state]
            self.q_table[current_state, next_state] += alpha * TD

        rewards = self.rewards_table
        Q = self.q_table
        rewards_copy = np.copy(rewards)

        for i in range(10):
            current_state = np.random.randint(0, 100)
            total_reward = 0
            while -9999 < total_reward < 100:
                playable_actions = []

                for j in range(100):
                    if rewards_copy[current_state, j] != 0:
                        playable_actions.append(j)

                if np.random.uniform(0, 1) < esilon:
                    next_state = np.random.choice(playable_actions)
                else:
                    max = Q[current_state, playable_actions[0]]
                    action = playable_actions[0]
                    for item in playable_actions:
                        if Q[current_state, item] > max:
                            max = Q[current_state, item]
                            action = item
                        elif Q[current_state][item] == max:
                            if random.random() < 0.8:
                                action = item

                    next_state = action

                play_actions = []
                for m in range(100):
                    if rewards_copy[next_state][m] != 0:
                        play_actions.append(m)

                max_next_state = Q[next_state][play_actions[0]]
                action = play_actions[0]

                for item in play_actions:
                    if Q[next_state][item] > max_next_state:
                        max_next_state = Q[next_state][item]
                        action = item
                    elif Q[next_state][item] == max_next_state:
                        if random.random() < 0.8:
                            action = item

                next_max = action

                TD = rewards[current_state, next_state] + gamma * Q[next_state, next_max] - Q[current_state, next_state]
                Q[current_state, next_state] += alpha * TD
                Q[current_state, next_state] = round(Q[current_state, next_state])
                total_reward += rewards[current_state, next_state]
                current_state = next_state

        print("End training")
        self.q_table = Q

    def done(self):
        if self.max_move <= 0 or self.eposide <= 0:
            return True
        return False

    def training(self, map):
        ConvertMapToReward(map, self.rewards_table)
        rewards = self.rewards_table
        print("Begin training")
        gamma = 0.6
        alpha = 0.8
        esilon = 0.1
        Q = np.array(np.zeros([100, 100]))
        rewards_copy = np.copy(rewards)

        for i in range(10000):
            current_state = np.random.randint(0, 100)
            total_reward = 0
            while -9999 < total_reward < 100:
                playable_actions = []

                for j in range(100):
                    if rewards_copy[current_state, j] != 0:
                        playable_actions.append(j)

                if np.random.uniform(0, 1) < esilon:
                    next_state = np.random.choice(playable_actions)
                else:
                    max = Q[current_state, playable_actions[0]]
                    action = playable_actions[0]
                    for item in playable_actions:
                        if Q[current_state, item] > max:
                            max = Q[current_state, item]
                            action = item
                        elif Q[current_state][item] == max:
                            if random.random() < 0.8:
                                action = item

                    next_state = action

                play_actions = []
                for m in range(100):
                    if rewards_copy[next_state][m] != 0:
                        play_actions.append(m)

                max_next_state = Q[next_state][play_actions[0]]
                action = play_actions[0]

                for item in play_actions:
                    if Q[next_state][item] > max_next_state:
                        max_next_state = Q[next_state][item]
                        action = item
                    elif Q[next_state][item] == max_next_state:
                        if random.random() < 0.8:
                            action = item

                next_max = action

                TD = rewards[current_state, next_state] + gamma * Q[next_state, next_max] - Q[current_state, next_state]
                Q[current_state, next_state] += alpha * TD
                Q[current_state, next_state] = round(Q[current_state, next_state])
                total_reward += rewards[current_state, next_state]
                current_state = next_state

        print("End training")
        self.q_table = Q

    def get_total_rewards(self):
        return self.total_rewards

    def evaluation(self):
        Q = self.q_table
        rewards = self.rewards_table

        action = []
        for i in range(100):
            if rewards[self.current_state][i] != 0:
                action.append(i)

        max_action = action[0]
        for item in action:
            if Q[self.current_state][item] > Q[self.current_state][max_action]:
                max_action = item
            if Q[self.current_state][item] == Q[self.current_state][max_action]:
                k = random.random()
                if k < 0.5:
                    max_action = item

        self.current_state = max_action
        return max_action


def ConvertList(list):
    temp = []
    for cell in list:
        cell.row = 9 - cell.row
        temp.append(cell)
    return temp

impliesRule = {
    'O': 'O',
    'S': 'W',
    'B': 'P',
    'W': 'S',
    'P': 'B'
}

level = {
    'O': 5,
    'S': 5,
    'B': 5,
    'W': 1,
    'P': 1,
    'N': 0,
    'BS': 5,
    'G': 4
}

states = {
    'N': -1,
    'O': 0,
    'P': 1,
    'B': 2,
    'W': 3,
    'S': 4,
    'G': 5,
    'BS': 6
}

states_reverse = {
    -1: 'N',
    0: 'O',
    1: 'P',
    2: 'B',
    3: 'W',
    4: 'S',
    5: 'G',
    6: 'BS'
}


class Fact:
    def __init__(self, text):
        self.text = text

    def get_state(self):
        row = int(self.text[1])
        column = int(self.text[2])
        state = self.text[0]

        return state, row, column

    def implies(self):
        list = []
        state, row, column = self.get_state()

        if state == 'G':
            return list

        adjCell = GetCells(row, column)

        for cell in adjCell:
            new_state = impliesRule[state]
            new_state += str(cell.row) + str(cell.column)
            list.append(InferenceRule(new_state))

        return list


class InferenceRule:
    def __init__(self, text):
        self.text = text

    def get_state(self):
        state = self.text[0]
        row = int(self.text[1])
        column = int(self.text[2])

        return state, row, column

    def set_states(self, map):
        state, row, column = self.get_state()
        old_state = states_reverse[map[row][column]]
        old_level = level[old_state]
        new_level = level[state]

        if new_level > old_level:
            map[row][column] = states[state]
            return True
        elif state != 'W' and state != 'P' and old_state == 'O':
            map[row][column] = states[state]
            return True
        return False


class KB:
    def __init__(self):
        self.facts = []
        self.inferences = []
        self.states = []
        self.visited = []

        """
        -1: Null, 0: OK, 1: Pit, 2: Breeze, 3: Wumpus, 4:Stench, 5: Gold
        """
        self.map = np.full((10, 10), -1, dtype=int)

    def add_fact(self, text):
        if len(text) == 3:
            fact = Fact(text)
            self.facts.append(fact)
            state, row, column = fact.get_state()
            self.map[row][column] = states[state]

            print(text)
            list = fact.implies()
            for clause in list:
                self.inferences.append(clause)
        else:
            self.add_fact(text[0] + text[2] + text[3])
            self.add_fact(text[1] + text[2] + text[3])
            row = int(text[2])
            column = int(text[3])
            self.map[row][column] = 6

    def show_clauses(self):
        print('FACT:')
        for fact in self.facts:
            print(fact.text)

        print('INFERENCES RULE:')
        for clause in self.inferences:
            print(clause.text)

    def tell(self):
        for clause in self.inferences:
            valid = clause.set_states(self.map)

        self.inferences.clear()
        for row in range(10):
            for column in range(10):
                if self.map[row][column] == 0:
                    state = str(row) + str(column)
                    self.states.append(state)
        self.states = list(dict.fromkeys(self.states))
        for row in range(10):
            for column in range(10):
                if self.map[row][column] == 3:
                    fact = Fact('W%s%s' % (row, column))
                    list123 = fact.implies()

                    for clause in list123:
                        state_clause, row_clause, column_clause = clause.get_state()
                        old_state = states_reverse[self.map[row_clause, column_clause]]
                        statement = old_state + str(row_clause) + str(column_clause)
                        for fact in self.facts:
                            if statement == fact.text:

                                if state_clause not in old_state and old_state != 'N':
                                    self.map[row][column] = 0
                                    self.states.append(str(row) + str(column))
                                    break
                if self.map[row][column] == 1:
                    fact = Fact('P%s%s' % (row, column))
                    list123 = fact.implies()

                    for clause in list123:
                        state_clause, row_clause, column_clause = clause.get_state()
                        old_state = states_reverse[self.map[row_clause, column_clause]]
                        statement = old_state + str(row_clause) + str(column_clause)

                        for fact in self.facts:
                            if statement == fact.text:

                                if state_clause not in old_state and old_state != 'N':
                                    self.map[row][column] = 0
                                    self.states.append(str(row) + str(column))
                                    break

    def ask(self):
        if len(self.states) > 0:
            while len(self.states) > 0:
                action = self.states.pop()
                if action not in self.visited:
                    self.visited.append(action)
                    return action
        else:
            for row in range(10):
                for column in range(10):
                    if self.map[row][column] == 0:
                        action = str(row) + str(column)
                        if action not in self.visited:
                            self.visited.append(action)

            if len(self.states) > 0:
                action = self.states.pop()
                return action
            else:
                return None

    def show_map(self):
        for row in range(10):
            print(self.map[9 - row])


class LogicAgent:
    def __init__(self, row, column, value, max_moves):
        self.kb = KB()
        self.max_moves = max_moves
        self.row = int(row)
        self.column = int(column)
        self.init_state = states_reverse[value]
        self.total_rewards = 0

        self.move(row, column, value)

    def get_position(self):
        return self.row, self.column

    def done(self):
        if self.max_moves <= 0:
            return True

        return False

    def move(self, row, column, value):
        state = states_reverse[value]
        state += str(row) + str(column)
        self.kb.add_fact(state)
        self.kb.tell()
        self.total_rewards += DictionaryMap(value)

    def get_action(self):
        action =  self.kb.ask()
        if action is not None:
            self.row = int(action[0])
            self.column = int(action[1])
            return int(action[0]), int(action[1])
        else:
            return None, None

    def show_map(self):
        self.kb.show_map()

    def get_total_rewards(self):
        return self.total_rewards

class Wumpus(Frame):

    def __init__(self, parent, map, row, column, K):
        Frame.__init__(self, parent)
        self.parent = parent
        parent.title("Wumpus")

        agent_learning = AgentLearning(row, column, K)
        agent_logic = LogicAgent(row, column, map[row][column], K)
        self.game = Game(self.parent, map, agent_learning, agent_logic)
        self.pack()


map, init_row, init_column, K = GenerateMap('map5.txt')
App = Tk()
App.geometry("840x420")
wumpus = Wumpus(App, map, init_row, init_column, K)
App.mainloop()

