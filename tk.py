from tkinter import *
from tkinter import ttk
import function
from queue import PriorityQueue
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# # ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# box1 = "11"
# def nextPuzzle():
#     global box1 = "1000"
# ttk.Button(frm, text=box1, command=root.destroy).grid(column=1, row=0)
# ttk.Button(frm, text="1", command=root.destroy).grid(column=1, row=1)
# ttk.Button(frm, text="2", command=root.destroy).grid(column=0, row=1)
# ttk.Button(frm, text="3", command=root.destroy).grid(column=0, row=0)
# ttk.Button(frm, text="next", command=nextPuzzle()).grid(column=0, row=2)
# root.mainloop()

#KAMUS GLOBAL
gameState = "generate" # generate, solve, show, done. tepatnya kek 'after this, generate'
root = [[0 for i in range (function.puzzleSize)] for j in range(function.puzzleSize)]
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



rootWindow = Tk()
statusLabel = Label(rootWindow, text="status")
statusLabel.grid(column = function.puzzleSize + 1, row = 0)

actionButton = Button(rootWindow,text="action")


actionButton.grid(column = function.puzzleSize + 1, row = 1)


#create 2d array of button
puzzleButton = [[ Button(rootWindow, text = "   ") for i in range(function.puzzleSize)] for i in range(function.puzzleSize)]

for i in range (function.puzzleSize):
    for j in range (function.puzzleSize):
        puzzleButton[i][j].grid(column = j, row = i)


# function
def solving():
    global root
    global memo
    global jumlahDibangkitkan
    global pq
    global totalStep
    #buat priority queue

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
    if(gameState == "generate"):
        # root = function.generatePuzzle()
        root = function.txtToPuzzle("puzzle.txt")
        currentDisplayedPuzzle = root
        updateWindowPuzzle()
        hasil = function.kurang(root)
        if (hasil % 2 != 0):
            statusLabel.configure(text = "tidak ada solusi")
            gameState = "done"
        else:
            statusLabel.configure(text = "ada solusi")
            gameState = "solve"
    elif(gameState == "solve"):
            statusLabel.configure(text = "solving...")
            solving()
            configureMemoReversed()
            statusLabel.configure(text = "done!")
            gameState = "show"
            print("memoReversed")
            print(memoReversed)
            
           

    elif(gameState == "show"):
        if(currentStep > totalStep):
            statusLabel.configure(text = "done!")
            gameState = "done"
        else:
            statusLabel.configure(text = "show step " + str(currentStep) + " of " + str(totalStep))
            currentDisplayedPuzzle = function.stringToPuzzle(memoReversed[function.puzzleToString(currentDisplayedPuzzle)])
            updateWindowPuzzle()
            currentStep += 1
    elif (gameState == "done"):
        rootWindow.destroy()

# bind to button
actionButton.configure(command = actionButtonClicked)



# start the window
rootWindow.mainloop()


# IMPORT
# PROGRAM UTAMA
# root = function.generatePuzzle()
# function.printPuzzle(root)
# hasil = function.kurang(root)
# if (hasil % 2 != 0):
#     print("solusi tidak ada")
# else:
#     print("solusi ada")



# function.printLangkah(memo)

    
    

    