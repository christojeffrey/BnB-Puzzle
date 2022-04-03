from tkinter import *
from queue import PriorityQueue
import time

import function

#KAMUS GLOBAL
path = "../test/puzzle.txt"
gameState = "" # check, solve, show, done. tepatnya kek 'after this, check'
root = [[0 in range (function.puzzleSize)] in range(function.puzzleSize)]
hasil = 0
memo = {}
jumlahDibangkitkan = 0  
pq = PriorityQueue()
currentStep = 1
totalStep = 1
memoReversed = {}
goalNode = [[((i*function.puzzleSize) + j + 1) for j in range(function.puzzleSize)] for i in range(function.puzzleSize)]
goalNode[function.puzzleSize-1][function.puzzleSize-1] = 0
currentDisplayedPuzzle = [[(i*function.puzzleSize) + j + 1 for i in range (function.puzzleSize)] for j in range(function.puzzleSize)]
timeTaken = 0

#BUAT GUI
rootWindow = Tk()
rootWindow.geometry("500x300")
statusLabel = Label(rootWindow, text="waiting puzzle option")
statusLabel.grid(columnspan= function.puzzleSize, row=function.puzzleSize )

detailLabel = Label(rootWindow, text="")
detailLabel.grid(rowspan= function.puzzleSize + 3, column=function.puzzleSize + 1,  row = 0)

actionButton = Button(rootWindow,text="action", command = lambda : actionButtonClicked())
actionButton.grid(columnspan=function.puzzleSize + 1, row=function.puzzleSize + 1)

puzzleFromFileButton = Button(rootWindow, text="puzzle from file", command = lambda : puzzleSourceButtonClicked("file"))
puzzleFromFileButton.grid(column = function.puzzleSize + 1, row = 2)

puzzleGenerateRandomButton = Button(rootWindow, text="generate random", command = lambda : puzzleSourceButtonClicked("generate"))
puzzleGenerateRandomButton.grid(column = function.puzzleSize + 1, row = 3)

#create 2d array of button
puzzleButton = [[ Button(rootWindow, text = "   ") for i in range(function.puzzleSize)] for i in range(function.puzzleSize)]
for i in range (function.puzzleSize):
    for j in range (function.puzzleSize):
        puzzleButton[i][j].grid(column = j, row = i, padx= 10, pady= 10)



# FUNCTION
def puzzleSourceButtonClicked(optionSelected):

    global gameState
    global currentDisplayedPuzzle
    global root
    global path
    gameState = "check"
    puzzleFromFileButton.destroy()
    puzzleGenerateRandomButton.destroy()
    if(optionSelected == "generate"):
        root = function.generatePuzzle()
    else:
        root = function.txtToPuzzle(path)
    currentDisplayedPuzzle = root
    updateWindowPuzzle()
    statusLabel.config(text="click action check whether solution exist")


def solvePuzzle():
    global timeTaken
    global root
    global memo
    global jumlahDibangkitkan
    global pq
    global totalStep
    
    #mulai timer
    startTime = time.time()
    #dictionary memo terdiri atas key puzzle, dan value puzzle parent. kecuali root, yang valuenya "root"
    memo[function.puzzleToString(root)] = "root"
    pq.put((function.calculateCost(root, 0), root, "", 0))

    # selama priority queue masih ada
    while not pq.empty():
        currentNode = pq.get()
        # jika node ini sudah selesai
        if function.isGoal(currentNode[1]):
            totalStep = currentNode[3]
            break
        # jika node ini belum selesai
        else:
            # bangkitkan node baru dari node utama, gerakkan sel 0 ke kiri kanan atas bawah, kecuali ke last move
            for direction in ["up", "down", "left", "right"]:
                if function.isEmptyAbleMove(direction, currentNode[1]) and currentNode[2] != function.directionCounter(direction):
                    newNode = function.moveEmpty(direction, currentNode[1])
                    if function.puzzleToString(newNode) not in memo:
                        jumlahDibangkitkan += 1
                        newNodeDepth = currentNode[3] + 1
                        pq.put((function.calculateCost(newNode,newNodeDepth), newNode, direction, newNodeDepth))
                        memo[function.puzzleToString(newNode)] = function.puzzleToString(currentNode[1])
    # stop timer
    endTime = time.time()
    timeTaken = endTime - startTime

def updateWindowPuzzle():
    # update window sesuai current diplayed puzzle variable
    global puzzleButton
    global currentDisplayedPuzzle
    for i in range (function.puzzleSize):
        for j in range (function.puzzleSize):
            puzzleButton[i][j].config(text = str(currentDisplayedPuzzle[i][j]))

def configureMemoReversed():
    # siapkan memo
    global memo
    global memoReversed
    global goalNode
    
    stringNode = function.puzzleToString(goalNode)

    while (stringNode != "root"):
        memoReversed[memo[stringNode]] = stringNode
        stringNode = memo[stringNode]

def actionButtonClicked():
    global root
    global gameState
    global hasil
    global currentDisplayedPuzzle
    global currentStep
    global totalStep
    global puzzleSourceOption
    if (gameState == "check"):
        hasil, detail = function.kurang(currentDisplayedPuzzle)
        detailLabel.config(text = detail)
        if (hasil % 2 != 0):
            statusLabel.configure(text = "tidak ada solusi\nclick action to quit")
            gameState = "done"
        else:
            statusLabel.configure(text = "ada solusi\nclick action to solve")
            gameState = "solve"
    elif(gameState == "solve"):
            statusLabel.configure(text = "solving...")
            solvePuzzle()
            configureMemoReversed()
            statusLabel.configure(text = "show step 0 of " + str(totalStep))
            gameState = "show"
            detailLabel.configure(text = "solved!\n" + str(timeTaken)+ " seconds\n" + str(jumlahDibangkitkan) + " nodes generated")
            
    elif(gameState == "show"):
        statusLabel.configure(text = "show step " + str(currentStep) + " of " + str(totalStep))
        if(currentStep <= totalStep):
            currentDisplayedPuzzle = function.stringToPuzzle(memoReversed[function.puzzleToString(currentDisplayedPuzzle)])
            updateWindowPuzzle()
            currentStep += 1
        else:
            statusLabel.configure(text = "done!\nclick action to quit")
            gameState = "done"
        
        
    elif (gameState == "done"):
        rootWindow.destroy()



# start the window
rootWindow.mainloop()