
import re
import urllib.request
from bs4 import BeautifulSoup as BeautifulSoup



numParse = re.compile('\d+(?=/restaurant)')

table = []


def pleaseSir(url):

    i    = 0

    done = False

    while i < 10000 and not done:


        try:
            page  = urllib.request.urlopen( url )
            soup  = BeautifulSoup(page)
            done  = True # If it reaches here
        except:
            i += 1
            print('might be stuck? ' + str(i),end='\n')



    if not done:
        with open('errors.txt','a') as f:
            f.write(url)
        soup = None

    return soup






with open('sites.txt','r') as f:

    sites = f.readlines()

total = len(sites)

index = 0
for url in sites:

    print(index, total)

    soup = pleaseSir("http://www.urbanspoon.com/" + url)
    
    try:
        neighbourhood  =  soup.find('meta', { "property" : "urbanspoon:neighborhood" })['content']
    except:
        neighbourhood  = 'NULL' 

    num                = numParse.search(url).group(0)

    table.insert(0, (int(num), neighbourhood)  )

    index += 1


with open('neighborhoods.txt','w') as f:
    f.write( '\n'.join( [ str(x) for x in  table]) )
