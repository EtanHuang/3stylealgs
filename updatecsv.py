import csv 
import pandas as pd 

numberToLetterMap = { 0: "A", 1: "B", 2: "D", 3: "E", 4: "F", 5: "G", 6: "H", 7: "I", 8: "K", 9: "L", 10: "N",
                      11: "O", 12: "P", 13: "Q", 14: "R", 15: "S", 16: "T", 17: "U", 18: "V", 19: "W", 20: "X" }
letterToNumberMap = {v: k for k, v in numberToLetterMap.items()}

df = pd.read_csv('3BLD  - UFR Comms.csv')
f = input("Enter first letter").upper()
s = input("Enter second letter").upper()
first = letterToNumberMap[f] 
second = letterToNumberMap[s] 

print(df.columns)

print(first, second)
print(numberToLetterMap[second], numberToLetterMap[first])
value = df.iloc[second][first + 1]
print(value)
alg = input("Enter new alg")
col_name = df.columns[first + 1]  # +1 because column 0 is the empty label ("First ---->")
df.at[second, col_name] = alg
df.to_csv('3BLD  - UFR Comms.csv', index = False)
value = df.iloc[second][first + 1]

print(value)
# comms = []
# with open('3BLD  - UFR Comms.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)
#     data = list(csv_reader)
#     for i in range(1, len(data[0])):
#         line = []
#         for j in range(len(data)):
#             line.append(data[j][i])
#         comms.append(line)



# # new_row = comms[first]

# # with open('3BLD  - UFR Comms.csv', mode = 'w') as file:
# #     writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

# #     writer.writerow


