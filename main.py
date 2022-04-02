# IMPORT
import random
from queue import PriorityQueue
import copy

# CONST 
puzzleSize = 4


#FUNGSI
def txtToPuzzle(path):
    #mengembalikan puzzle dari file txt
    puzzle = [[0 for i in range (puzzleSize)] for i in range(puzzleSize)]
    with open(path, "r") as file:
        lines = file.readlines()
        # print(lines)
        for i in range(puzzleSize):
            # print("line")
            # print(lines[i])
            # hilangkan \n
            eachline = lines[i].split("\n")[0]
            # split line dengan spasi
            eachnumber = eachline.split(" ")
            # print("line splitted")
            # print(eachnumber)
            for j in range(puzzleSize):
                puzzle[i][j] = int(eachnumber[j])
    return puzzle
    
def kurang(puzzle):
    
    print(puzzle)
    sum = 0
    flatten_list = []
    for i in puzzle:
        for j in i:
            flatten_list.append(j)
    # flatten_list = sum(puzzle, [])
    for i in range(puzzleSize*puzzleSize):
        temp = 0
        if(flatten_list[i] == 0):
            temp += puzzleSize*puzzleSize - i - 1
        for j in range(i, puzzleSize * puzzleSize):
            if (flatten_list[j] < flatten_list[i] and flatten_list[j] != 0):
                temp += 1
        print("temp = ", temp)
        sum += temp

    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if(puzzle[i][j] == 0):  
                if ((i + j) % 2 == 1):
                    sum += 1
    print("hasil algoritma kurang(i) + X:", sum)
    return sum

def printPuzzle(puzzle):
    #mencetak puzzle
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if(puzzle[i][j] < 10):
                print(puzzle[i][j], end="  ")
            else:
                print(puzzle[i][j], end=" ")
        print()

def generatePuzzle():
    puzzle = [[0 for i in range (puzzleSize)] for i in range(puzzleSize)]
    #mengembalikan sebuah array 2 dimensi berukuran puzzleSize x puzzleSize, yang berisi angka dari 1 hingga puzzleSize^2 dalam posisi acak dan setiap sel memiliki angka yang berbeda, dengan satu buah sel yang dibiarkan kosong
    for i in range(0, puzzleSize*puzzleSize):

        #selama belum terisi
        while True:
            #random baris dan kolom dari 0 sampai puzzleSize-1
            row = random.randint(0,puzzleSize-1)
            col = random.randint(0,puzzleSize-1)
            #jika selnya kosong, maka akan diisi dengan angka i
            if puzzle[row][col] == 0:
                puzzle[row][col] = i
                break

    return puzzle

def isGoal(puzzle):
    #mengecek apakah puzzle sudah selesai
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if(i*puzzleSize + j +1 != puzzleSize*puzzleSize):
                    # print("salah di ", i, j)
                    return False
            elif puzzle[i][j] != (i*puzzleSize + j + 1):
                # print("salah di ", i, j)
                return False
    return True

def isEmptyAbleMoveUp(puzzle):
    #mengecek apakah puzzle bisa bergerak ke atas
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if i == 0:
                    return False
                else:
                    return True

def moveEmptyUp(puzzle):

    #mengembalikan puzzle yang sudah bergerak
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                puzzle[i][j] = puzzle[i-1][j]
                puzzle[i-1][j] = 0
                return puzzle

def isEmptyAbleMoveDown(puzzle):
    #mengecek apakah puzzle bisa bergerak ke bawah
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if i == puzzleSize-1:
                    return False
                else:
                    return True

def moveEmptyDown(puzzle):
    #mengembalikan puzzle yang sudah bergerak
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                puzzle[i][j] = puzzle[i+1][j]
                puzzle[i+1][j] = 0
                return puzzle

def isEmptyAbleMoveLeft(puzzle):
    #mengecek apakah puzzle bisa bergerak ke kiri
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if j == 0:
                    return False
                else:
                    return True

def moveEmptyLeft(puzzle):
    #mengembalikan puzzle yang sudah bergerak
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                puzzle[i][j] = puzzle[i][j-1]
                puzzle[i][j-1] = 0
                return puzzle

def isEmptyAbleMoveRight(puzzle):
    #mengecek apakah puzzle bisa bergerak ke kanan
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if j == puzzleSize-1:
                    return False
                else:
                    return True

def moveEmptyRight(puzzle):
    #mengembalikan puzzle yang sudah bergerak
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                puzzle[i][j] = puzzle[i][j+1]
                puzzle[i][j+1] = 0
                return puzzle


def calculateCost(puzzle, depth):
    # hitung banyak sel yang salah tempat ditambah kedalamannya dari root
    cost = 0
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0 and (i*puzzleSize + j + 1) != puzzleSize*puzzleSize:
                    cost += 1

            elif puzzle[i][j] != (i*puzzleSize + j + 1):
                cost += 1
    cost += depth
    return cost
def puzzleToString(puzzle):
    #mengembalikan string dari puzzle
    string = ""
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            string += str(puzzle[i][j])
            string += " "
    return string
def stringToPuzzle(string):
    #mengembalikan puzzle dari string
    array = string.split(" ")
    puzzle = [[0 for i in range (puzzleSize)] for i in range(puzzleSize)]
    for i in range(0, puzzleSize):
        for j in range(0, puzzleSize):
            puzzle[i][j] = int(array[i*puzzleSize + j])
    return puzzle
# PROGRAM UTAMA
root = generatePuzzle()
# root = txtToPuzzle("puzzle.txt")
printPuzzle(root)
hasil = kurang(root)
if (hasil % 2 != 0):
    print("solusi tidak ada")
else:
    print("solusi ada")
    jumlahDibangkitkan = 0  
    solusi = 0
    #buat priority queue
    pq = PriorityQueue()

    # tuple of node terdiri dari cost, puzzle, prev move, depth

    #dictionary memo terdiri atas key puzzle, dan value puzzle parent. kecuali root, yang valuenya "root"
    memo = {}
    memo[puzzleToString(root)] = "root"
    # buat node utama
    # masukkan node utama ke priority queue
    pq.put((calculateCost(root, 0), root, "", 0))

    # selama priority queue masih ada
    while not pq.empty():
        # a = input("berhenti bentar")
        # ambil node dengan cost terkecil
        currentNode = pq.get()
        # memo[puzzleToString(currentNode[1])] = "tes"
        # print jumlah node di priority queue
        # print("Jumlah node di queue: ", pq.qsize())
        # print("current node")
        # print(currentNode)
        # print("jumlahDibangkitkan")
        # print(jumlahDibangkitkan)
        if(jumlahDibangkitkan % 50000 == 0):
            print("Jumlah node di queue: ", pq.qsize())
            print("current node")
            print(currentNode)
            print("jumlahDibangkitkan")
            print(jumlahDibangkitkan)
        # jika node ini sudah selesai
        if isGoal(currentNode[1]):
            
            break
        # jika node ini belum selesai
        else:
            
        # bangkitkan node baru dari node utama, gerakkan sel 0 ke kiri kanan atas bawah, kecuali ke last move
            if isEmptyAbleMoveUp(currentNode[1]) and currentNode[2] != "down":
                # print("move up")
                newNode = moveEmptyUp(copy.deepcopy(currentNode[1]))
                # print(newNode)
                # print(currentNode[1])
                if puzzleToString(newNode) not in memo:
                    # print("bisa move up")
                    jumlahDibangkitkan += 1
                    newNodeDepth = currentNode[3] + 1
                    pq.put((calculateCost(newNode,newNodeDepth), newNode, "up", newNodeDepth))
                    memo[puzzleToString(newNode)] = puzzleToString(currentNode[1])
                # else:
                    # print("catch")

            if isEmptyAbleMoveDown(currentNode[1]) and currentNode[2] != "up":
                # print("move down")
                newNode = moveEmptyDown(copy.deepcopy(currentNode[1]))
                # print(newNode)

                if puzzleToString(newNode) not in memo:
                    # print("bisa move down")
                    jumlahDibangkitkan += 1
                    newNodeDepth = currentNode[3] + 1
                    pq.put((calculateCost(newNode, newNodeDepth), newNode, "down",newNodeDepth))
                    memo[puzzleToString(newNode)] = puzzleToString(currentNode[1])
                # else:
                    # print("catch")

            if isEmptyAbleMoveLeft(currentNode[1]) and currentNode[2] != "right":
                # print("move left")
                newNode = moveEmptyLeft(copy.deepcopy(currentNode[1]))
                # print(newNode)

                if puzzleToString(newNode) not in memo:
                    # print("bisa move left")
                    jumlahDibangkitkan += 1
                    newNodeDepth = currentNode[3] + 1
                    pq.put((calculateCost(newNode, newNodeDepth), newNode, "left", newNodeDepth))
                    memo[puzzleToString(newNode)] = puzzleToString(currentNode[1])
                # else:
                    # print("catch")

            if isEmptyAbleMoveRight(currentNode[1]) and currentNode[2] != "left":
                # print("move right")
                newNode = moveEmptyRight(copy.deepcopy(currentNode[1]))
                # print(newNode)

                if puzzleToString(newNode) not in memo:
                    # print("bisa move right")
                    jumlahDibangkitkan += 1
                    newNodeDepth = currentNode[3] + 1
                    pq.put((calculateCost(newNode, newNodeDepth), newNode, "right", newNodeDepth))
                    memo[puzzleToString(newNode)] = puzzleToString(currentNode[1])
                # else:
                    # print("catch")
    # print solusi
    print("solusi")
    print(currentNode)
    print("jumlahDibangkitkan")
    print(jumlahDibangkitkan)
    # print langkahnya
    string = puzzleToString(currentNode[1])
    
    while (string != "root"):
        printPuzzle(stringToPuzzle(string))
        string = memo[string]
        
        

        