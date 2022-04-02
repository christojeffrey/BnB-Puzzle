# IMPORT
import function
from queue import PriorityQueue
# PROGRAM UTAMA
root = function.generatePuzzle()
# root = function.txtToPuzzle("puzzle.txt")
function.printPuzzle(root)
hasil = function.kurang(root)
if (hasil % 2 != 0):
    print("solusi tidak ada")
else:
    print("solusi ada")
jumlahDibangkitkan = 0  
solusi = 0
#buat priority queue
pq = PriorityQueue()


#dictionary memo terdiri atas key puzzle, dan value puzzle parent. kecuali root, yang valuenya "root"
memo = {}
memo[function.puzzleToString(root)] = "root"

# buat node utama
# masukkan node utama ke priority queue
# tuple of node terdiri dari cost, puzzle, prev move, depth
pq.put((function.calculateCost(root, 0), root, "", 0))

# selama priority queue masih ada
while not pq.empty():
    currentNode = pq.get()
    if(jumlahDibangkitkan % 50000 == 0):
        print("Jumlah node di queue: ", pq.qsize())
        print("current node")
        print(currentNode)
        print("jumlahDibangkitkan")
        print(jumlahDibangkitkan)
    # jika node ini sudah selesai
    if function.isGoal(currentNode[1]):
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

# print solusi
print("solusi")
print(currentNode)
print("jumlahDibangkitkan")
print(jumlahDibangkitkan)
# print("memo")
# for i in memo:
#     print(i, ": ", memo[i])


function.printLangkah(memo)

    
    

    