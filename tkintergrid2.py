#Nicky Gundersen
#CS440 Intro to AI
#create_world.py reads a txt file containing a map and start/end coordinates. then displays is using tkinter
#Each 'number' in the file becomes a cell, with a value of that numbber determining the color based on my color
#dictionary.
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
import numpy as np
import os

def mapMaker():
    #make a directory out of the HeuristicSearch fold
    directory = os.listdir('../CS440_HeuristicSearch/')
    #search for files in directory, if file eneds with .txt, open it
    for File in directory:
        if File.endswith('.txt'):
            with open(File, "r") as mapFile:
                #make two lists out of the first two lines in .txt. split them(put them in a list and have each item in
                #line be its own element). Then create variables out of each element in the 2 element list
                [xstart,ystart], [xgoal,ygoal] = next(mapFile).split(), next(mapFile).split()
                #ignore the first two rows, then store the rest in a 2d array
                numMap = np.genfromtxt(File,dtype='str', skip_header=2)
                #set the start tile
                numMap[int(xstart), int(ystart)] = '3'
                #set the goal tile
                numMap[int(xgoal), int(ygoal)] = '4'
            return numMap

        else:#not a txt file
            continue
def main():
    newMap = mapMaker()
    root = tk.Tk()
    root.title("gridmap")
    my_gui = CellGrid(root, len(newMap), len(newMap[0]), 40, newMap)


    root.mainloop()

class CellGrid(tk.Canvas):
    def __init__(self, master, rowNum, colNum, cellSize, numMap):
        tk.Canvas.__init__(self, master, width=cellSize * colNum, height=cellSize * rowNum)
        self.config(scrollregion=self.bbox("all"))
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.cellSize = cellSize

        scr = tk.Scrollbar(self)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        scr2 = tk.Scrollbar(self)
        scr2.pack(side=tk.BOTTOM, fill=tk.X)
        self.config(yscrollcommand=scr.set)
        scr.config(command=self.yview)
        self.config(xscrollcommand=scr2.set)
        scr2.config(command=self.xview)

        self.configure(scrollregion=self.bbox("all"))
        # 2 dimensional array creation(a list of lists)
        self.grid = []
        for row in range(rowNum):
            line = [] #dd an empty array that will hold each cell in this row
            for column in range(colNum):
                line.append(Cell(self, column, row, cellSize, numMap[row][column]))
            self.grid.append(line)  # append a cell

        print(self.grid[0][0].value)
        self.draw()

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()

#Creation of our cell class,
class Cell():
    def __init__(self, master, x, y, size, value):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = 'white'
        self.value = value

    def setValue(self, value):
        self.value = value

    def draw(self):
        #mycolors dictionary - value of Cell determines color of cell.
        mycolors = {
            '0': 'black',  #a blocked cell
            '1': 'white',  #a regular unblocked cell
            '2': 'gray',  #hard to traverse cell
            '3': 'red',    #start block(based on coordinates)
            '4': 'green',  #finish block(based on coordinates)
            'a': 'cyan', #regular unblocked cell with a highway
            'b': 'blue', #hard to traverse cell with a highway
            'p': 'purple' #A* path
        }

        if self.master != None:
            #create our rectangle
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=mycolors[self.value], outline="black")


main()
