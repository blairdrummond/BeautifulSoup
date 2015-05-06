import re

number = re.compile('\d+')



with open('restaurants.txt','r') as f:
    lines = f.readlines()


def compare(l1, l2):
    n1 = int(number.search(l1).group(0))
    n2 = int(number.search(l2).group(0))


    if n1 < n2:
        return -1
    elif n1 > n2:
        return 1
    else:
        return 0

def value(l1):
    return int(number.search(l1).group(0))


newlist = sorted(lines, key=value)


for i in range(0,len(newlist)-1):
    if value(newlist[i]) == value(newlist[i+1]):
        print(newlist[i])


with open('restaurants2.txt','w') as f:
    f.write(''.join(newlist))
