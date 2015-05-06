import re


#Restaurant.sql is wrong

nums  = set([]) 
rests = []

num = re.compile('\d+')

with open('restaurants.sql','r') as f:
    rfile = f.readlines()


for line in rfile:

    if line.strip() == '':
        continue

    
    rid = int(num.search(line).group(0))

    if rid in nums:
        continue
    else:
        nums.add(rid)
        rests.insert(0, str(line.strip().encode('ascii','replace')) )



with open('restaurants1.sql','w') as f:
    f.write( '\n'.join(rests) )
    

