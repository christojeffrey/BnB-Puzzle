# IMPORT
import random

# CONST 
puzzleSize = 4

#FUNGSI
def txtToPuzzle(path):
    #mengembalikan puzzle dari file txt
    puzzle = [[0 for i in range (puzzleSize)] for i in range(puzzleSize)]
    with open(path, "r") as file:
        lines = file.readlines()
        for i in range(puzzleSize):
            eachline = lines[i].split("\n")[0]
            # split line dengan spasi
            eachnumber = eachline.split(" ")
            for j in range(puzzleSize):
                puzzle[i][j] = int(eachnumber[j])
    return puzzle
    
def kurang(puzzle):
    detail = ""
    sum = 0
    flatten_list = []
    for i in puzzle:
        for j in i:
            flatten_list.append(j)
    for i in range(puzzleSize*puzzleSize    ):
        temp = 0
        if(flatten_list[i] == 0):
            temp += puzzleSize*puzzleSize - i - 1
        for j in range(i, puzzleSize * puzzleSize):
            if (flatten_list[j] < flatten_list[i] and flatten_list[j] != 0):
                # angka setelah(j) angka yg sedah di cek(i) harus lebih besar. jadi kalo lebih kecil, dijumlahkan ke temp
                # kecuali kalo j = 0 (karena aslinya 0 itu holder buat angka terbesar di puzzle, jadi gamungkin lebih kecil dari i)
                temp += 1
        detail += "nilai kurang di baris "+ str( (i // puzzleSize) + 1) +  " kolom " + str((i % puzzleSize) + 1 ) +  ": "+ str(temp)+ "\n"
        sum += temp

    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if(puzzle[i][j] == 0):  
                if ((i + j) % 2 == 1):
                    sum += 1
                    detail += "ditambah X = 1\n"
                else:
                    detail += "ditambah X = 0\n"
    detail += "hasil algoritma kurang(i) + X:"+ str(sum)
    return sum, detail



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
                # lokasi 0 harus berapa di baris dan kolom terakhir
                if(i != puzzleSize-1 or j != puzzleSize-1):
                    return False
            elif puzzle[i][j] != (i*puzzleSize + j + 1):
                return False
    return True

def isEmptyAbleMove(direction, puzzle):
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if direction == "up":
                    if i == 0:
                        return False
                elif direction == "down":
                    if i == puzzleSize-1:
                        return False
                elif direction == "left":
                    if j == 0:
                        return False
                elif direction == "right":
                    if j == puzzleSize-1:
                        return False
                return True

def calculateCost(puzzle, depth):
    # hitung banyak sel yang salah tempat ditambah kedalamannya dari root
    cost = 0
    for i in range(puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if(puzzleSize * puzzleSize != (i*puzzleSize + j + 1)):
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
            string += "_"
    return string

def stringToPuzzle(string):
    #mengembalikan puzzle dari string
    array = string.split("_")
    puzzle = [[0 for i in range (puzzleSize)] for i in range(puzzleSize)]
    for i in range(0, puzzleSize):
        for j in range(0, puzzleSize):
            puzzle[i][j] = int(array[i*puzzleSize + j])
    return puzzle


def directionCounter(direction):
    # mengembalikan arah yang berlawanan
    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "left":
        return "right"
    elif direction == "right":
        return "left"
    else:
        return ""

def moveEmpty(direction, puzzle):
    # mengganti puzzle dengan puzzle yang sudah di update, menggerakan sel 0 ke arah direction
    # dipastikan sel kosong bisa bergerak ke arah tersebut
    newPuzzle = list(map(list, puzzle))
    for i in range (puzzleSize):
        for j in range(puzzleSize):
            if puzzle[i][j] == 0:
                if direction == "up":
                    newPuzzle[i][j] = puzzle[i-1][j]
                    newPuzzle[i-1][j] = 0
                elif direction == "down":
                    newPuzzle[i][j] = puzzle[i+1][j]
                    newPuzzle[i+1][j] = 0
                elif direction == "left":
                    newPuzzle[i][j] = puzzle[i][j-1]
                    newPuzzle[i][j-1] = 0
                elif direction == "right":
                    newPuzzle[i][j] = puzzle[i][j+1]
                    newPuzzle[i][j+1] = 0
                return newPuzzle