from bs4 import BeautifulSoup
import urllib.parse, urllib.request, re, time, random, math, sys, traceback

# NOTE THAT

NULL = 'NULL'

# In order to supplement the missing data, we have added data/ manipulated data to fill everything


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

numParse = re.compile('\d+(?=/restaurant)')
urlParse = re.compile('(?<=http://).*?(?=/)')


#############################################################################################
#############################################################################################

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

#############################################################################################
#############################################################################################


def parseHours(hourstag):
    
    if hourstag.table == None:
        # reformat text like 'Monday - Friday' to 'Monday'
        days    = [ x.text.split()[0] for x in hourstag.find_all('h4')]
        hours   = [ x.text            for x in hourstag.find_all('p')]
        pairs   = list(zip(days, hours))
        
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
    if table: return table
    else:     return 'CLOSED'

#############################################################################################
#############################################################################################

# Extract data from he address tag on a restaurant
def parseAddress(addrtag):
    # Switch-Block for assigning the relevant variables
    address = city = prov = postal = NULL

    for x in addrtag.find_all('span'):
        if 'class' in x.attrs:
            if   'street-address' in x['class']:
                address = x.text.strip()

            elif 'locality' in x['class']:
                cityProv   = x.text.replace('\n',' ').replace(',','').split()
                city, prov = cityProv[0], cityProv[1]

            elif 'visible-xs-inline' in x['class']:
                postal = x.text.strip()

    return address, city, prov, postal

#############################################################################################
#############################################################################################

def parseMenu(index, url):
    if url == '' or 'NULL' in url:  
        return []
        
    soup = pleaseSir(url) 
    
    if soup == None:
        return []
    
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
    soup = pleaseSir(url)
    if soup == None:
        return
    
    # Grab a Whole bunch of stuff
    index          =   int(soup.body['data-restaurant-id'])

    name           =       soup.find('meta', { "property" : "og:title"                })['content']
    imageURL       =       soup.find('meta', { "property" : "og:image"                })['content']
    neighbourhood  =       soup.find('meta', { "property" : "urbanspoon:neighborhood" })['content']
    ratingPerc     = float(soup.find('meta', { "property" : "urbanspoon:like_percent" })['content'])

    # Sometimes missing

    try:    cost     = len(soup.find('span', { "class" : "price" }).text )
    except: cost     = NULL 

    try:    website  = soup.find('div',  { "data-ga-action" : "resto-website"           }).a['href']
    except: website  = NULL
        
    try:    menusite = soup.find('a',    { "data-ga-action" : "menu-urbanspoon"         })['href']
    except: menusite = NULL 

    try:    phone    = soup.find('a', 'phone tel').text.strip()
    except: phone    = NULL
     
    try:    menulist = parseMenu( index, 'http://www.urbanspoon.com' + menusite  )
    except: menulist = []

    try:    weeklyhours = parseHours( soup.find('div', { "data-in-base-append" : "#hours-base" }) )
    except: weeklyhours = list(zip( ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
                                    [ NULL   , NULL    , NULL      , NULL     , NULL   , NULL     , NULL   ]))

    try:    address,  city,   prov,   postal = parseAddress(soup.find('div', id='address'))
    except: address = city =  prov =  postal = NULL


    cuisines      = [ tag['content'] for tag in soup.find_all('meta', { "property"       : "urbanspoon:cuisine" }) ]
    features      = [ tag.text       for tag in soup.find_all('a',    { "data-ga-action" : "resto-feature"      }) ]



    foodra,  pricra, moodra, stafra = genRatings(ratingPerc)
    

    


    restSet.insert(0, (index, name, cost, foodra, pricra, moodra, stafra, website))    

    # Useful for keeping track of something else later.
    restKeys.insert(0,index)
        
    locationindex = len([ x for x in locaSet if x[-1] == index ])
    locaSet.insert( 0, 
                    (  
                        locationindex, 
                        NULL, 
                        NULL,
                        NULL,
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
        
    for menuitem in menulist:      menuSet.insert(0,     menuitem      )
    for cuisine  in cuisines:      cuisSet.insert(0, (cuisine, index)  )
    for feature  in features:      featSet.insert(0, (feature, index)  )

    
        
    # AFTER all restaraunts are loaded, find all the critics/reviewers.
    # The urls are found here so that they can be referenced later.
    # Critics prone to repeats
    reviewers = [ x['href'] for x in soup.find_all('a', {'itemprop' : 'reviewer'})]
    critics   = set(   [    ( x['href'], x.img['src']  ) for x in soup.find_all('a', {'data-ga-action' : 'critic-page'})     ]     )
    
    for e in reviewers:    reviewerData.add(e)
    for e in critics:        criticData.add(e)
    # DONE

    
#############################################################################################
#############################################################################################


def grabReviewers():
    index = len(ratingSet)

    totalsize = len(reviewerData)
    progress  = 0 

    for e in reviewerData:

        sys.stdout.write("\rWorkng... " + str(int(round((progress*100)/float(totalsize)))) + "%")
        sys.stdout.flush()
        progress+=1

        soup  = pleaseSir('http://www.urbanspoon.com' + e )
        temp  = soup.find('header', {'class' : 'page-header'}).text.replace('\n',' ').partition('Joined on')
        name  = temp[0].strip()
        temp  = temp[2].split()
        month = months[temp[0]]
        day   = (lambda x: '0'+x if (len(x) == 1) else x )(temp[1].replace(',',''))
        year  = temp[2]
        joind = year +'-'+ month +'-'+ day 
        city  = temp[-1]

        image = [ x.img['src'] for x in soup.find_all('a', { 'data-ga-action' : 'user-profile-page' }) if x.img != None][0]

        numreviews  = int(re.search('\d+',  [li.text.replace('\n','') for li in soup.find_all('li') if li.a != None and li.a.text == 'Reviews' ][0]  ).group(0))

        calcdrating = min( 5, max(1 , math.floor(math.log( max(numreviews, 1), 2) - 1)))
        
        reviewerSet.insert(0,    (index, name.replace(' ','_')+'@foodie.ca', 'password', name, joind, 'reviewer', calcdrating ))

        revRating(index,  'http://www.urbanspoon.com' + e + '/comments' )
        index+=1

#############################################################################################
#############################################################################################

def revRating(index, url):

    soup = pleaseSir(url)
    if soup == None:
        return 

    for x in [ x for x in soup.find_all('li', { 'class' : 'comment review'}) ]:
        try:
            restNum  = int(numParse.search( [y for y in x.find_all('a', { 'data-ga-action' : 'resto-page' }) if 'href' in y.attrs][0]['href'] ).group(0))
        except:
            print(x)
            print(url)
            print( [y for y in x.find_all('a', { 'data-ga-action' : 'resto-page' }) if 'href' in y.attrs] )
            raise
        # If it isn't referring to a known restaraunt, don't add it
        if restNum not in restKeys:
            continue

        rating   = float(x['data-positive']) # 0 < x < 10, x in R
        date     = soup.find('time')['datetime'][:10]
        revTitle = x.find('div', { 'class' : 'subtitle' }).text
        comment  = x.find('div', { 'class' : 'body'     }).text.strip()
        foodra, pricra, moodra, stafra = genRatings(rating)        
        ratingSet.insert(0,    (index, date,  foodra, pricra, moodra, stafra, revTitle, comment, restNum)       )


#############################################################################################
#############################################################################################


def grabCritics():

    index = len(ratingSet)
    for critic in criticData:
        
        soup  = pleaseSir('http://www.urbanspoon.com' + critic[0] )
        if soup == None:
            continue

        name  = soup.html.title.text.strip()
        image = critic[1]

        email = 'foodcritic@' + urlParse.search( soup.find('div', {'itemprop' : 'reviewer'}).a['href'] ).group(0)

        reviewerSet.insert(0,  (index, email, 'password', name, NULL, 'critic', 5 )       )

        for review in soup.find_all('li', { 'class' : 'review' }):
            tempTag  = review.find('a',{ 'data-ga-action' : 'resto-page'})
            restNum  = int(numParse.search( tempTag['href'] ).group(0))

            # If it isn't referring to a known restaraunt, don't add it
            if restNum not in restKeys:
                continue

            revTitle = tempTag.text
            date     = review.time['datetime']
            tempTag  = review.find('div', {'class' : 'body'})

            try:
                link = [ x for x in tempTag.find_all('a') if 'href' in x.attrs][0]['href']
            except:
                link = ''

            try:
                commenttext = tempTag.text
                ratingSet.insert(0,    (index, date, NULL, NULL, NULL, NULL, revTitle, commenttext, restNum)       )
            except:
                print( critic[0] + '\n' + revTitle + '\n' + str(tempTag) + '\n\n')

        index+=1


#############################################################################################
#############################################################################################


#FIND THE URLS TO THE RESTAURANTS
def initial():
    output = open('sites.txt','w')

    for i in range(1, 182): 
        url='http://www.urbanspoon.com/lb/250/best-restaurants-Ottawa?page='+str(i)  #input('URL:')
        print (i)
        soup = pleaseSir(url)
        links = [ tag['href'] for tag in soup.find_all('a','resto_name') ]
        
        for link in links:
            output.write(link + '\n')

    output.close()


#############################################################################################
#############################################################################################


def run():
    with open('sites.txt','r') as f:
        sites = f.readlines()

    progress = 0
    total    = len(sites)
    for url in sites:
        
        sys.stdout.write("\rWorking... " + str((progress*100)/total) + "%")
        sys.stdout.flush()
        progress+=1

        grabPage('http://www.urbanspoon.com' + url )

    with open('restaurants.txt','w') as f:
        f.write("\n".join([ str(x) for x in restSet]))
        

    print('reviewers')
    grabReviewers()

    print('critics')
    grabCritics()


    for pair in zip( 
            ['locations.txt', 'features.txt', 'cuisines.txt', 'menuitems.txt', 'raters.txt', 'ratings.txt' ],
            [ locaSet       ,  featSet      ,  cuisSet      ,  menuSet       ,  reviewerSet,  ratingSet    ]):
        with open(pair[0],'w') as f:
            f.write("\n".join([ str(x) for x in pair[1]]))


####################################### SCRIPT ##############################################


#initial()
run()
