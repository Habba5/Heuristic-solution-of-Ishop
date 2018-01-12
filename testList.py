class Foo(object):
    def __init__(self, name):
        self.name = name

aList = [["blubb1",[4, 3]], ["blubb2", 5]]
bList = [None, None]
a = Foo("erster")
a.price = 7.3
b = Foo("zweiter")
b.price = 5.2
c = Foo("dritter")
c.price = 9
otherList = []
sortList = [a,b,c]
#i = 0
#while i < 10:
#    aList.append(None)
#    i += 1
#aList.insert(7, 5)
#print(aList[0].index("blubb2"))
print(aList[0][1][0])
print(aList)
print(4 - 5)
for a in sortList:
    a.nutte = 4
print(sortList[0].nutte)
if otherList.__len__() == 0:
    print("Jo, is leer")
if bList is None:
    print("Hallo")
if bList == [None] * len(bList):
    print("Hallo")
print(sortList)
for a in sortList:
    print(a.name + " " + str(a.price))
sortList.sort(key=lambda x: x.price, reverse=False)
print(sortList)
print(sortList.__len__())
for a in sortList:
    print(a.name + " " + str(a.price))
print(any(x.name == "zweiter" for x in sortList))
newsortlist = [x for x in sortList if x.name == "erster" or x.name == "zweiter"]
print(newsortlist)
#sortList.remove(b)
#sortList.remove(a)
#print(sortList)
y = "5,3"
y = y.replace(",", ".")
print(float(y))

for a in sortList:
    print("Bin in liste a")
    for b in newsortlist:
        if b.name == "zweiter":
            break
        print("Treffer")