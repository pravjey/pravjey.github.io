from bottle import default_app, route, template, request
import wikipedia as wk
import tweepy
from textblob import TextBlob
import requests
import math
import time



# Global variables

HOST = "drpjeya.pythonanywhere.com"
responsive = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"

tweepy_consumer_key = "nP7BhUjbVGfMwZmG65kes8WNm"
tweepy_consumer_secret = "c3tYVD4ZUFN8ZkeIdMUktmBksqdpfqSLRsTbjNgJ2fXAPoB5jw"
tweepy_access_token = "897909419996041218-9w0Co5vu740brxciIOCsTm2clMPpHTl"
tweepy_access_token_secret = "6h3y5oZSIsNYpUXcEM5oTwOtR1wJJ70ffPR2lgMUlYNvf"
auth = tweepy.OAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
auth.set_access_token(tweepy_access_token, tweepy_access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit_notify=True)

google_api_key = "AIzaSyB0j0VPHo-wNWWP552bn_tYL9Fo9dReLZU"
google_client_id = "150298367843-rodkf208a95a29hsfsg3dngjihpaq1hj.apps.googleusercontent.com"
google_client_secret = "VrN1TIpgdAz5MMoa95rKGQGw"

@route('/')
def home():
    output = template("home.tpl")
    return output

def checkEmptyList(a):
    if len(a) == 0:
        a = "No tweets currently"
    return a

def meanSentiment(a):
    if len(a) == 0:
        return 0
    else:
        return sum(a) / len(a)

def summaryPage(keyword,objTweet,subjTweet,AvePol,AveSubj,sentiPol,sentiSubj,summary):
    title = "<title>Minipedia - about " + keyword + "</title>" + responsive
    link = "<p><a href=\"" + wk.page(keyword).url + "\">full Wikipedia article</a>"
    backlink = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    strPol, strSubj = sentiText(AvePol, AveSubj)
    strPol = strPol + "\t(Positive = >0.1, Negative = <-0.1)"
    strSubj = strSubj + "\t(Very Subjective = >0.5, Somewhat Subjective = >0.1)"
    sentiCat = "<p>More or less objective tweets: " + str(len(sentiPol)) + "<p>Subjective tweets: " + str(len(sentiSubj))
    sentiment = "<h3>Overall current sentiment on Twitter:</h3>" + "<br>Polarity: " + strPol + "<br>Subjectivity: " + strSubj + sentiCat + "<hr>"
    objTweet = '<h3>' + 'Mostly objective information about \"' +  keyword + '\"' + ' on Twitter' + '</h3><p>' + objTweet + "<hr>"
    subjTweet = '<h3>' + 'Comments about \"' +  keyword + '\"' + ' on Twitter: ' + '</h3><p>' + subjTweet + "<hr>"
    output = title + '<h1>' + keyword + '</h1><p>' + summary + link + backlink + "<hr>" + sentiment + '<p>' + objTweet + subjTweet
    return output

def summaryDropPage(keyword,objTweet,subjTweet,AvePol,AveSubj,sentiPol,sentiSubj,summary):
    title = "<title>Minipedia - about " + keyword + "</title>" + responsive
    link = "<p><a href=\"" + wk.page(keyword).url + "\">full Wikipedia article</a>"
    backlink1 = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    backlink2 = '<p><a href=\"javascript:history.back()\">Back to Suggestions</a>'
    strPol, strSubj = sentiText(AvePol, AveSubj)
    strPol = strPol + "\t(Positive = >0.1, Negative = <-0.1)"
    strSubj = strSubj + "\t(Very Subjective = >0.5, Somewhat Subjective = >0.1)"
    sentiCat = "<p>More or less objective tweets: " + str(len(sentiPol)) + "<p>Subjective tweets: " + str(len(sentiSubj))
    sentiment = "<h3>Overall current sentiment on Twitter:</h3>" + "<br>Polarity: " + strPol + "<br>Subjectivity: " + strSubj + sentiCat + "<hr>"
    objTweet = '<h3>' + 'Mostly objective information about \"' +  keyword + '\"' + ' on Twitter' + '</h3><p>' + objTweet + "<hr>"
    subjTweet = '<h3>' + 'Comments about \"' +  keyword + '\"' + ' on Twitter: ' + '</h3><p>' + subjTweet + "<hr>"
    output = title + '<h1>' + keyword + '</h1><p>' + summary + link + backlink1 + backlink2 + "<hr>" + sentiment + '<p>' + objTweet + subjTweet
    return output

# Display page containing summary of the Wikipedia page satisfying the search criteria input on the home page, after checking whether the page exist or whether
# the search criteria is too ambiguous to refer to a single page. The latter is done by getPage() function.
@route('/summary', method="POST")
def getSummary():
    keyword = request.forms["keyword"]
    length = request.forms["length"]
    setLang(request.forms["lang"])
    page = getPage(keyword, length)
    objTweet, subjTweet, tweetdatetime, sentiPol, sentiSubj = getTwitter(keyword)
    objTweet = checkEmptyList(objTweet)
    subjTweet = checkEmptyList(subjTweet)
    AvePol = meanSentiment(sentiPol)
    AveSubj = meanSentiment(sentiSubj)
    try:
        summary = wk.summary(keyword, sentences=length)
    except wk.DisambiguationError:
        return page
    except wk.exceptions.PageError:
        return "No page exists" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    else:
        output = summaryPage(keyword,objTweet,subjTweet,AvePol,AveSubj,sentiPol,sentiSubj,summary)
        return output

@route('/summarydrop', method="POST")
def getSummaryDrop():
    keyword = request.forms.get('dropdown')
    length = request.forms["lengthPassed"]
    #lang = request.forms["langPassed"]
    page = getPage(keyword, length)
    objTweet, subjTweet, tweetdatetime, sentiPol, sentiSubj = getTwitter(keyword)
    objTweet = checkEmptyList(objTweet)
    subjTweet = checkEmptyList(subjTweet)
    AvePol = meanSentiment(sentiPol)
    AveSubj = meanSentiment(sentiSubj)
    try:
        summary = wk.summary(keyword, sentences=length)
    except wk.DisambiguationError as e:
        backlink = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
        return page + backlink
    except wk.exceptions.PageError:
        return "No page exists for" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    else:
        output = summaryDropPage(keyword,objTweet,subjTweet,AvePol,AveSubj,sentiPol,sentiSubj,summary)
        return output

def suggestPage(keyword,menu,length):
    title = "<title>Minipedia - Suggestions for search \" " + keyword + "\"</title>" + responsive
    heading = "<h1>Suggestions for " + '\"' + keyword + '\"' + "</h1>"
    suggestions = '<p><select name="dropdown">'
    for i in range(len(menu)):
        suggestions = suggestions + "<option value ='" + menu[i] + "'>" + menu[i] + "</options>"
    suggestions += "</select>"
    lengthPassed = '<p>Selected Length: <select name="lengthPassed">' + '<option value="' + length + '" selected>' + length + '</option></select>'
    form = '<form action="/summarydrop" method="POST">' + suggestions + lengthPassed + '<p><input type="submit" value="Submit"></form>'
    output = title + heading + form
    return output

@route('/suggest', method="POST")
def getPage(keyword, length):
    search = wk.search(keyword)
    page_exists = False
    for i in search:
        if i.lower() == keyword.lower():
            page_exists = True
            break
    if page_exists:
        try:
            page = wk.page(keyword)
        except wk.DisambiguationError as e:
            output = suggestPage(keyword,e.options,length)
            return output
        except wk.exceptions.PageError:
            return "No page exists for" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>" + str(search)
        else:
            return page
    else:
        output = suggestPage(keyword,search,length)
        return output

def setLang(language):
    return wk.set_lang(language)

def sentiText(AvePol, AveSubj):
    if AvePol > 0.1:
        strPol = "Positive (" + str(AvePol) + ")"
    elif AvePol < -0.1:
        strPol = "Negative (" + str(AvePol) + ")"
    else:
        strPol = "More or less neutral (" + str(AvePol) + ")"
    if AveSubj > 0.5:
        strSubj = "Very subjective (" + str(AveSubj) + ")"
    elif AveSubj <= 0.5 and AveSubj > 0.1:
        strSubj = "Somewhat subjective (" + str(AveSubj) + ")"
    else:
        strSubj = "More or less objective (" + str(AveSubj) + ")"
    return strPol, strSubj

def getSentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity =  blob.sentiment.subjectivity
    return polarity, subjectivity

def getTwitter(keyword):
    query = keyword
    results = api.search(q=query, count=5000, tweet_mode="extended")
    objTweet = ""
    subjTweet = ""
    tweetdatetime = []
    sentiPol = []
    sentiSubj = []
    for tweet in results:
        if keyword in tweet.full_text:
            url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str
            a_url = '<a href=\"' + url + '\">' + url + '</a>'
            tweetdatetime.append(tweet.created_at)
            datetimeString = str(tweet.created_at)
            polarity, subjectivity = getSentiment(tweet.full_text)
            sentiPol.append(polarity)
            sentiSubj.append(subjectivity)
            sentiment = "<b><br>Polarity = " + str(polarity) + " Subjectivity = " + str(subjectivity) + "</b>"
            if subjectivity < 0.1:
                objTweet = objTweet + "<p>" + tweet.user.screen_name + "</b>" + " Tweeted: " + tweet.full_text + "<br>" + datetimeString + "<br>" + a_url + "<br>" + sentiment + "\n"
            else:
                subjTweet = subjTweet + "<p>" + tweet.user.screen_name + "</b>" + " Tweeted: " + tweet.full_text + "<br>" + datetimeString + "<br>" + a_url + "<br>" + sentiment + "\n"
    return objTweet, subjTweet, tweetdatetime, sentiPol, sentiSubj


def getData(api):
    request = requests.get(api)
    request_json = request.json()
    return request_json

def haversine(a1,a2,b1,b2):
    radius = 6371
    phi1 = a1*math.pi/180
    phi2 = a2*math.pi/180
    lambda1 = b1*math.pi/180
    lambda2 = b2*math.pi/180
    phi_delta = phi2 - phi1
    lambda_delta = lambda2 - lambda1
    a = (math.sin(phi_delta/2))**2 + math.cos(phi1)*math.cos(phi2)*(math.cos(lambda_delta/2))**2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = (radius * c)/1000
    return d

def getDistance(latitude, longitude):
    distance = 0
    for i in range(0,len(latitude)-1,2):
        distance = distance + haversine(latitude[i], latitude[i+1],longitude[i],longitude[i+1])
    return distance

def getMap(previousLat2,previousLong2,startLat,startLong):
    marker1 = "markers=size:small%color:red%7Clabel:S%7C" + str(startLat)+","+str(startLong)
    marker2 = "markers=size:small%color:red%7Clabel:C%7C" + str(previousLat2)+","+str(previousLong2)
    staticmap = "https://maps.googleapis.com/maps/api/staticmap?center="+str(previousLat2)+","+str(previousLong2)+"&zoom=6&size=600x600&maptype=roadmap&" + marker1 + "&" + marker2 + "&key="+google_api_key
    embedmap = "https://www.google.com/maps/embed/v1/directions?key="+google_api_key+"&origin="+str(startLat)+","+str(startLong)+"&destination="+str(previousLat2)+","+str(previousLong2)
    image1 = "<img src=\"" + str(staticmap) + "\"</img>"
    image2 = "<iframe width=\"600\" height=\"600\" frameborder=\"10px\" style=\"border:1px solid black;\" src=\"" + embedmap + "\" allowfullscreen></iframe>"
    return image1, image2

def getLocation(latitude,longitude):
    location_dict = getData("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+str(latitude)+"% "+str(longitude)+"&inputtype=textquery&key="+google_api_key)
    if (len(location_dict["candidates"]) == 0) & ("formatted_address" in location_dict["candidates"][0].keys()):
        location = "\t" + location_dict["candidates"][0]["formatted_address"]
    else:
        #placeid = str(location_dict["candidates"][0]["place_id"])
        #placedetails = getData("https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeid+"&key="+google_api_key)
        #if placedetails["result"]["formatted_address"] == placedetails["result"]["name"]:
        n = 1000
        nearby =  getData("https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + str(latitude)+","+str(longitude)+"&radius=" + str(n) + "&key="+google_api_key)
        if nearby["results"]:
            latitude = nearby["results"][0]["geometry"]["location"]["lat"]
            longitude = nearby["results"][0]["geometry"]["location"]["lng"]
            location = "\t " + str(n) + " metres near " + str(getLocation(latitude,longitude))
        else:
            n += 1000
            location = "\t" + str(getData("https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + str(latitude)+","+str(longitude)+"&radius=" + str(n) + "&key="+google_api_key))
    return location

def issPage(previousLat2,previousLong2,distance,clock,startLat,startLong):
    title = "<title>As far as the International Space Station flies</title>" + responsive
    heading = "<h1>" + "How fast does ths International Space Station go?" + "</h1>"
    backlink = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    startPos = "Starting position of ISS \t Latitude: " + str(startLat) + "\tLongitude: " + str(startLong) + "\t" + str(getLocation(startLat,startLong))
    closePos = "<p>Closing position of ISS \t Latitude: " + str(previousLat2) + "\tLongitude: " + str(previousLong2) + "\t" + str(getLocation(previousLat2,previousLong2))
    distanceText = "<p>Distance travelled so far: " + str(distance) + " km in " + str(clock) + " seconds."
    speed = distance / clock
    speedText = "<p>Average speed: " + str(speed) + " km//s."
    mapImage1, mapImage2 = getMap(previousLat2,previousLong2,startLat,startLong)
    mapImage1 = "<h2>Static map showing ISS position</h2>" + mapImage1
    mapImage2 = "<h2>Dynamic map showing ISS position (Zoom in/out)</h2>" + mapImage2
    return title + heading + startPos + closePos + distanceText + speedText + "<p>" + mapImage1 + mapImage2 + backlink

@route('/iss', method="POST")
def getIss():
    timeTotal = int(request.forms["timeTotal"])
    timeInterval = int(request.forms["timeInterval"])
    issLocation = getData('http://api.open-notify.org/iss-now.json')
    startLat = previousLat1 = float(issLocation["iss_position"]["latitude"])
    startLong = previousLong1 = float(issLocation["iss_position"]["longitude"])
    latitude = [previousLat1]
    longitude = [previousLong1]
    clock = 0
    while clock < timeTotal:
        start = time.time()
        end = time.time()
        while (end-start) < timeInterval:
            issLocation = getData('http://api.open-notify.org/iss-now.json')
            previousLat2 = float(issLocation["iss_position"]["latitude"])
            previousLong2 = float(issLocation["iss_position"]["longitude"])
            end = time.time()
        latitude.append(previousLat2)
        longitude.append(previousLong2)
        clock = clock + (end - start)
        previousLat1 = previousLat2
        previousLong1 = previousLong2
    distance = getDistance(latitude,longitude)
    output = issPage(previousLat2,previousLong2,distance,clock,startLat,startLong)
    return output



application = default_app()
