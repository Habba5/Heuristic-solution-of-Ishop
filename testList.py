aList = [["blubb1",[4, 3]], ["blubb2", 5]]
bList = [None, None, None]
#i = 0
#while i < 10:
#    aList.append(None)
#    i += 1
#aList.insert(7, 5)
#print(aList[0].index("blubb2"))
print(aList[0][1][0])
print(aList)
print(4 - 5)
if bList is None:
    print("Hallo")
#bList[0][0] = "1"
i = 0
for blisti, b in enumerate(bList):
    bList[blisti] = []
    for a in aList:
        bList[blisti].append(None)
    print(b)
    i+=1
print(bList)
if bList == [None] * len(bList):
    print("Hallo")