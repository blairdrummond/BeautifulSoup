def cleanline(line):

    if line.strip() == '':
        return ''

    # beginning of strings 
    begin = 0
    for i in range(0,6):
        begin = line.index(',', begin+1)
        
    begin+=1


    # end of strings
    end = [i for i, ltr in enumerate(line) if ltr == ','][-1] 
        

    text  = line[begin:end]
    
    split = text.index("',") 
    
    title   = text[:split+1].strip("' ").replace("'","''")
    comment = text[split+2:].strip("' ").replace("'","''")
    
    return line[:begin+1] + " '" + title + "', '" + comment + "'" + line[end:] 

    

with open('ratings.txt','r') as f:
    lines = f.readlines()


with open('ratings1.txt','w') as f:
    f.write(  ''.join(   [ cleanline(line) for line in lines]     )    )
