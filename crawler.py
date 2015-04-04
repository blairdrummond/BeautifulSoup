from bs4 import BeautifulSoup
import urllib.parse, urllib.request, re, time, random, math, sys, traceback

# NOTE THAT

# In order to supplement the missing data, we have added data/ manipulated data to fill everything

# The store manager is always 'Bill Clinton'
# The store was first opened on Bill Clinton's birthday
# Critics have the join date May 9, 1995
# The rating from urban spoon is randomly turned into a split of 4 traits with that average
# everyone has the password 'password'
# there are no real email addresses in the system
# critcs automatically have a rating of 5

# Cache values in these lists then flush them once everything is done.
restSet      = []
locaSet      = []
featSet      = []
cuisSet      = []
menuSet      = []
reviewerSet  = []
ratingSet    = []

restKeys     = []
criticData   = set([])
reviewerData = set([])

# Extract data from the hours tag on a restaurant
week   = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] 

months = { 
    'January'   : '01', 
    'February'  : '02',
    'March'     : '03',
    'April'     : '04',
    'May'       : '05',
    'June'      : '06',
    'July'      : '07',
    'August'    : '08',
    'September' : '09',
    'October'   : '10',
    'November'  : '11',
    'December'  : '12'
}

numParse = re.compile('(?<=/r/\d\d\d/)\d+')
urlParse = re.compile('(?<=http://).*?(?=/)')


#############################################################################################
#############################################################################################


def parseHours(hourstag):
    
    if hourstag.table == None:
        # reformat text like 'Monday - Friday' to 'Monday'
        days    = [ x.text.split()[0] for x in hourstag.find_all('h4')]
        hours   = [ x.text            for x in hourstag.find_all('p')]
        pairs = list(zip(days, hours))
        
        # For every day of the week except Monday...
        for i in range(1,7):
            # if a day is missing
            if len(pairs) <= i or pairs[i][0] != week[i]:
                # insert that day based on the previous day's hours
                pairs.insert( i,  (week[i], pairs[i-1][1])  )    
                
        return pairs

    else:
       weekl = [[ True if 'class' in y.attrs else False for y in x.find_all('td')[1:]] for x in hourstag.find('table').find_all('tr')[1:]]
       pairs = [ parseSchedule(day) for day in zip(*weekl) ]

       return list(zip(week, pairs))

#############################################################################################
#############################################################################################

def parseSchedule(x):
    table = ', '.join([y[1] for y in filter( (lambda z: z[0] ),  zip(x, ['Breakfast', 'Lunch', 'Dinner', 'Late']))])
    if table == '':
        return 'CLOSED'
    else:
        return table

#############################################################################################
#############################################################################################

# Extract data from he address tag on a restaurant
def parseAddress(addrtag):
    # Switch-Block for assigning the relevant variables
    for x in addrtag.find_all('span'):
        if 'class' in x.attrs:
            if   'street-address' in x['class']:
                address  = x.text.strip()
            elif 'locality' in x['class']:
                cityProv   = x.text.replace('\n',' ').replace(',','').split()
                city, prov = cityProv[0], cityProv[1]
            elif 'visible-xs-inline' in x['class']:
                postal   = x.text.strip()

    return address, city, prov, postal

#############################################################################################
#############################################################################################

def parseMenu(index, url):
    if url == '':
        return []

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)
    return [ (index, x.img['src'], x.h3.a.text) for x in soup.find_all('li', {'data-class' : 'Dish'})] 

#############################################################################################
#############################################################################################

def genRatings(average):
    ratings = []
    for i in range(0,4):
        x = max( 0, min( 100, round(random.gauss( average, 10 ))))  # Normal variable between 0 and 100
        ratings.insert( 0,  x )

    return ratings[0], ratings[1], ratings[2], ratings[3]


#############################################################################################
#############################################################################################

def grabPage(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)

    
    # Grab a Whole bunch of stuff
    name          = soup.find('meta', { "property"       : "og:title"                })['content']
    index         = soup.body['data-restaurant-id']
    imageURL      = soup.find('meta', { "property"       : "og:image"                })['content']
    neighbourhood = soup.find('meta', { "property"       : "urbanspoon:neighborhood" })['content']
    ratingPerc    = float(soup.find('meta', { "property"       : "urbanspoon:like_percent" })['content'])
    
    try:
        website   = soup.find('div',  { "data-ga-action" : "resto-website"           }).a['href']
    except:
        website   = 'NULL'
        
    try:
        menusite  = soup.find('a',    { "data-ga-action" : "menu-urbanspoon"         })['href']
    except:
        menusite  = '' 
        
    cuisines      = [ tag['content'] for tag in soup.find_all('meta', { "property"       : "urbanspoon:cuisine" }) ]
    features      = [ tag.text       for tag in soup.find_all('a',    { "data-ga-action" : "resto-feature"      }) ]
    phone         = soup.find('a', 'phone tel').text.strip()
    cost          = len(  soup.find('span', { "class" : "price" }).text )

    try:
        weeklyhours   = parseHours( soup.find('div', { "data-in-base-append" : "#hours-base" }) )
    except:
        weeklyhours   = list(zip( ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
                                  ['NULL'  ,'NULL'   ,'NULL'     ,'NULL'    ,'NULL'  ,'NULL'    ,'NULL'  ]))

    address, city, prov, postal = parseAddress(soup.find('div', id='address'))
    

    # Create Rows
    foodra, pricra, moodra, stafra = genRatings(ratingPerc)
    
    restSet.insert(0, (index, name, cost, foodra, pricra, moodra, stafra, website))
    
    # Useful for keeping track of something else later.
    restKeys.insert(0,index)
        
    locationindex = len([ x for x in locaSet if x[-1] == index ])
    locaSet.insert( 0, 
                    (  
                        locationindex, 
                        'NULL', 
                        '1948-08-19',
                        'Bill Clinton',
                        phone, 
                        address, 
                        imageURL,
                        weeklyhours[0][1], 
                        weeklyhours[1][1], 
                        weeklyhours[2][1], 
                        weeklyhours[3][1], 
                        weeklyhours[4][1], 
                        weeklyhours[5][1], 
                        weeklyhours[6][1], 
                        index           
                    ))
        
    for cuisine in cuisines:
        cuisSet.insert(0, (cuisine, index))
        
    for feature in features:
        featSet.insert(0, (feature, index))
        
    menulist = parseMenu( index, 'http://www.urbanspoon.com' + menusite  )
    for menuitem in menulist:
        menuSet.insert(0, menuitem)
            


        
    # AFTER all restaraunts are loaded, find all the critics/reviewers.
    # The urls are found here so that they can be referenced later.
    # Critics prone to repeats
    reviewers = [ x['href'] for x in soup.find_all('a', {'itemprop' : 'reviewer'})]
    critics   = set([ ( x['href'], x.img['src']  ) for x in soup.find_all('a', {'data-ga-action' : 'critic-page'})])
    
    for e in reviewers:
        reviewerData.add(e)
    for e in critics:
        criticData.add(e)
    # DONE

    
#############################################################################################
#############################################################################################


def grabReviewer():
    index = len(ratingSet)

    totalsize = len(reviewerData)
    progress  = 0 

    for e in reviewerData:

        sys.stdout.write("\rWorkng... " + str(int(round((progress*100)/float(totalsize)))) + "%")
        sys.stdout.flush()
        progress+=1


        page  = urllib.request.urlopen( 'http://www.urbanspoon.com' + e )
        soup  = BeautifulSoup(page)
        temp  = soup.find('header', {'class' : 'page-header'}).text.replace('\n',' ').split()
        name  = temp[0]
        month = months[temp[3]]
        day   = (lambda x: [0]+x if (len(x) == 1) else x )(temp[4].replace(',',''))
        year  = temp[5]
        joind = year +'-'+ month +'-'+ day 
        city  = temp[-1]

        image = [ x.img['src'] for x in soup.find_all('a', { 'data-ga-action' : 'user-profile-page' }) if x.img != None][0]

        numreviews = int(re.search('\d+',  [li.text.replace('\n','') for li in soup.find_all('li') if li.a != None and li.a.text == 'Reviews' ][0]  ).group(0))

        calcdrating = min( 5, max(1 , math.floor(math.log( max(numreviews, 1), 2) - 1)))
        
        reviewerSet.insert(0,    (index, name+'@foodie.ca', 'password', name, joind, 'reviewer', calcdrating ))

        addComments(index,  'http://www.urbanspoon.com' + e + '/comments' )
        index+=1

#############################################################################################
#############################################################################################

def revRating(index, url):
    page  = urllib.request.urlopen( url )
    soup  = BeautifulSoup(page)

    for x in [ x for x in soup.find_all('li', { 'class' : 'comment review'}) ]:
        restNum  = int(numParse.search( x.a['href']).group(0))

        # If it isn't referring to a known restaraunt, don't add it
        if restNum not in restKeys:
            continue

        rating   = x['data-positive'] # 0 < x < 10, x in R
        date     = soup.find('time')['datetime'][:10]
        revTitle = x.find('div', { 'class' : 'subtitle' }).text
        comment  = x.find('div', { 'class' : 'body'     }).text.strip()
        foodra, pricra, moodra, stafra = genRatings(rating)        
        ratingSet.insert(0,    (index, date,  foodra, pricra, moodra, stafra, revTitle, comment, restNum)       )


#############################################################################################
#############################################################################################


def grabCritic():

    index = len(ratingSet)
    for critic in criticData:
        page  = urllib.request.urlopen( 'http://www.urbanspoon.com' + critic[0] )
        soup  = BeautifulSoup(page)

        name  = soup.html.title.text.strip()
        image = critic[1]

        email = 'foodcritic@' + urlParse.search( soup.find('div', {'itemprop' : 'reviewer'}).a['href'] ).group(0)

        reviewerSet.insert(0,  (index, email, 'password', name, '1995-05-09', 'critic', 5 )       )

        for review in soup.find_all('li', { 'class' : 'review' }):
            tempTag  = review.find('a',{ 'data-ga-action' : 'resto-page'})
            restNum  = int(numParse.search( tempTag['href'] ).group(0))

            # If it isn't referring to a known restaraunt, don't add it
            if restNum not in restKeys:
                continue

            revTitle = tempTag.text
            date     = review.time['datetime']
            tempTag  = review.find('div', {'class' : 'body'})
            comment  = tempTag.text + '  ' + tempTag.a['href'] 
            ratingSet.insert(0,    (index, date, 'NULL', 'NULL', 'NULL', 'NULL', revTitle, comment, restNum)       )

        index+=1


#############################################################################################
#############################################################################################





####################################### SCRIPT ##############################################

#FIND THE URLS TO THE RESTAURANTS
#output = open('sites.txt','w')
#
#for i in range(1, 182): 
#    url='http://www.urbanspoon.com/lb/250/best-restaurants-Ottawa?page='+str(i)  #input('URL:')
#    print (i)
#    page = urllib.request.urlopen(url)
#    soup = BeautifulSoup(page)
#    
#    links1 =  soup.find_all('a','resto_name')
#    links2 =  [ tag['href'] for tag in links1 ]
#
#    for link in links2:
#        output.write(link + '\n')
#
#output.close()


with open('sites.txt','r') as f:
    sites = f.readlines()

progress = 0
total    = len(sites)
for url in sites:

    sys.stdout.write("\rWorkng... " + str((progress*100)/total) + "%")
    sys.stdout.flush()
    progress+=1

    grabPage('http://www.urbanspoon.com' + url )

print('reviewers')
grabReviewers()

print('critics')
grabCritics()


for pair in zip( 
   ['restaurants.txt', 'locations.txt', 'features.txt', 'cuisines.txt', 'menuitems.txt', 'raters.txt', 'ratings.txt' ],
   [ restSet         ,  locaSet       ,  featSet      ,  cuisSet      ,  menuSet       ,  reviewerSet,  ratingSet    ]):
    with open(pair[0],'w') as f:
        f.write("\n".join(pair[1]))

