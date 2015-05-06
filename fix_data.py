import re


locationsmatch = re.compile('\d+(?=\);)')
results = []

def parseNeighbourhood(line):
    thinger = line.strip("( )").replace("'",'').partition(',')
    num   = int(thinger[0])
    place = thinger[2].strip("' ")
    
    return (num, place)


def findmatch(number):
    size = len(towns)
    for i in range(0,size):
        if int(locationsmatch.search(towns[i]).group(0)) == number:
            return i


with open('neighborhoods.txt','r') as f:
    hoods = [parseNeighbourhood(x.strip()) for x in f.readlines()]

with open('locations.txt','r') as f:
    towns = f.readlines()


for x in hoods:
    toremove = findmatch(x[0])
    results.insert(0,   towns[toremove].replace( ');',    ', \''+x[1]+'\');'  ))
    towns.remove(towns[toremove])

with open('newlocations.txt','w') as f:
    f.write('\n'.join(results))
