import csv
from collections import deque
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

comms = []
with open('UFR Comms.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    data = list(csv_reader)
    for i in range(1, len(data[0])):
        line = []
        for j in range(len(data)):
            line.append(data[j][i])
        comms.append(line)


piecesMap = { 0: "UBL", 1: "UBR", 2: "UFL", 3: "LBU", 4: "LFU", 5: "LDF", 6: "LDB", 7: "FUL", 8: "FDR", 9: "FDL", 10: "RUB",
              11: "RDB", 12: "RDF", 13: "BUR", 14: "BUL", 15: "BDL", 16: "BDR", 17: "DFL", 18: "DFR", 19: "DBR", 20: "DBL" }

numberToLetterMap = { 0: "A", 1: "B", 2: "D", 3: "E", 4: "F", 5: "G", 6: "H", 7: "I", 8: "K", 9: "L", 10: "N",
                      11: "O", 12: "P", 13: "Q", 14: "R", 15: "S", 16: "T", 17: "U", 18: "V", 19: "W", 20: "X" }
letterToNumberMap = {v: k for k, v in numberToLetterMap.items()}
notationToNumberMap = {v: k for k, v in piecesMap.items()}
# for i in range(len(comms)):
#     for j in range(len(comms[0])):
#         comm = comms[i][j]
#         if comm == '':
#             print("UFR-" + piecesMap[i] + "-" + piecesMap[j] + "\t" + numberToLetterMap[i] + numberToLetterMap[j] + "\t" + "Same piece")
#         else:
#             print("UFR-" + piecesMap[i] + "-" + piecesMap[j] + "\t" + numberToLetterMap[i] + numberToLetterMap[j] + "\t" + comm)

def reverse_moves(moves):
    ret = [""] * len(moves)
    for k in range(len(moves) - 1, -1, -1):
        if "2" in moves[k]:
            ret[len(moves) - k - 1] = moves[k]
        elif moves[k][-1] != "'" and "2" not in moves[k]:
            ret[len(moves) - k - 1] = moves[k] + "'"
        elif moves[k][-1] == "'":
            ret[len(moves) - k - 1] = moves[k][0:-1]
    return ret

def cancel_moves(moves):
    stack = []
    moves = deque(moves.split(" "))
    while len(moves) != 0:
        top = moves[0]
        moves.popleft()
        if len(stack) == 0:
            stack.append(top)
        #X'+X', X+X, X2+X2
        elif stack and top == stack[-1]:
            #X2+X2
            if top[-1] == "2":
                stack.pop()
            #X'+X', X+X
            else:
                stack.pop()
                stack.append(top[0] + "2")
        #X’+X2, X+X2
        elif stack and top != stack[-1] and stack[-1][0] == top[0]:
            if (stack[-1][-1] == "'" and top[-1] == "2") or (stack[-1][-1] == "2" and top[-1] == "'"):
                stack.pop()
                stack.append(top[0][0])
            elif (len(stack[-1]) == 1 and top[-1] == "2") or (len(top) == 1 and stack[-1][-1] == "2"):
                stack.pop()
                stack.append(top[0] + "'")
        else:
            stack.append(top)
    return stack

moves = [[] for _ in range(len(data))]
for i in range(len(comms)):
    row = []
    for j in range(len(comms[0])):
        comm = comms[i][j]
        move = ""
        if comm == '':
            moves[i].append(move)
        # No setup moves (pure comms)
        if ":" not in comm and comm != '':
            comm = comm[1:-1]
            comm = comm.split(",")
            comm = [part.strip() for part in comm]
            move += (comm[0] + " ")
            move += (comm[1] + " ")
            first_moves = comm[0].split(" ")
            first_moves_new = reverse_moves(first_moves)
            move += (" ".join(first_moves_new) + " ")
            second_moves = comm[1].split(" ")
            second_moves_new = reverse_moves(second_moves)
            move += " ".join(second_moves_new)
            moves[i].append(move)
        # setup, comm, undo setup
        if ":" in comm and comm != '':
            comm = comm[1:-1]
            setup, comm = comm.split(":")
            comm = comm.strip()
            setup = setup.strip()
            move += setup + " "
            setup = (setup.strip()).split(" ")
            comm = comm[1:-1]
            comm = comm.split(",")
            comm = [part.strip() for part in comm]
            move += (comm[0] + " ")
            move += (comm[1] + " ")
            first_moves = comm[0].split(" ")
            first_moves_new = reverse_moves(first_moves)
            move += (" ".join(first_moves_new) + " ")
            second_moves = comm[1].split(" ")
            second_moves_new = reverse_moves(second_moves)
            move += " ".join(second_moves_new) + " "
            move += " ".join(reverse_moves(setup))
            move = " ".join(cancel_moves(move))
            moves[i].append(move)

@app.route('/get_algorithm', methods=['GET'])
@cross_origin(origins=['http://localhost:5173','null'])
def get_algorithm():
    print("Request received")
    
    # Get query parameters
    first_piece = request.args.get('firstPiece')
    second_piece = request.args.get('secondPiece')
    print(first_piece, second_piece)
    if not first_piece or not second_piece:
        return jsonify({"error": "Invalid request. Missing query parameters."}), 400

    try:
        first = int(first_piece)
        second = int(second_piece)
    except ValueError:
        return jsonify({"error": "Invalid piece values. Must be integers."}), 400

    comm = comms[first][second]
    move = moves[first][second]
    print(comm, move)
    response = jsonify({"comm": comm, "moves": move})
    print(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)

alg = input("Enter letter pair").upper()
first = alg[0].upper()
second = alg[1].upper()
move = moves[letterToNumberMap[first]][letterToNumberMap[second]]
if move == '':
    print("Same piece")
else:
    print(comms[letterToNumberMap[first]][letterToNumberMap[second]])
    print(moves[letterToNumberMap[first]][letterToNumberMap[second]])

