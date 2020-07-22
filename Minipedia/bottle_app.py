# Libraries
from bottle import default_app, route, run, template, request, get, post
import wikipedia as wk
import tweepy
from textblob import TextBlob

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


@route('/')
def home():
    output = template("home.tpl")
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
    if len(objTweet) == 0:
        objTweet = "No objective tweets currently"
    if len(subjTweet) == 0:
        subjTweet = "No subjective tweets currently"
    if len(sentiPol) == 0:
        AvePol = 0
    else:
        AvePol = sum(sentiPol) / len(sentiPol)
    if len(sentiSubj) == 0:
        AveSubj = 0
    else:
        AveSubj = sum(sentiSubj) / len(sentiSubj)
    try:
        summary = wk.summary(keyword, sentences=length)
    except wk.DisambiguationError:
        return page
    except wk.exceptions.PageError:
        return "No page exists" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    else:
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
        style = '<style> table, th, td {border: 1px solid black; border-collapse: collapse; padding: 10px;} </style>'
        return style + title + '<h1>' + keyword + '</h1><p>' + summary + link + backlink + "<hr>" + sentiment + '<p>' + '<table><tr><td valign=\"top\">' + objTweet + '</td><td valign=\"top\">' + subjTweet + '</td>' + '</tr></table>'

@route('/summarydrop', method="POST")
def getSummaryDrop():
    keyword = request.forms.get('dropdown')
    length = request.forms["lengthPassed"]
    #lang = request.forms["langPassed"]
    page = getPage(keyword, length)
    objTweet, subjTweet, tweetdatetime, sentiPol, sentiSubj = getTwitter(keyword)
    if len(objTweet) == 0:
        objTweet = "No objective tweets currently"
    if len(subjTweet) == 0:
        subjTweet = "No subjective tweets currently"
    if len(sentiPol) == 0:
        AvePol = 0
    else:
        AvePol = sum(sentiPol) / len(sentiPol)
    if len(sentiSubj) == 0:
        AveSubj = 0
    else:
        AveSubj = sum(sentiSubj) / len(sentiSubj)
    try:
        summary = wk.summary(keyword, sentences=length)
    except wk.DisambiguationError as e:
        backlink = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
        return page + backlink
    except wk.exceptions.PageError:
        return "No page exists for" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
    else:
        title = "<title>Minipedia - about " + keyword + "</title>" + responsive
        link = "<p><a href=\"" + page.url + "\">full Wikipedia article</a>"
        backlink1 = "<p><a href=\"\/" + HOST + "\">Back to home page</a>"
        backlink2 = '<p><a href=\"javascript:history.back()\">Back to Suggestions</a>'
        strPol, strSubj = sentiText(AvePol, AveSubj)
        strPol = strPol + "\t(Positive = >0.1, Negative = <-0.1)"
        strSubj = strSubj + "\t(Very Subjective = >0.5, Somewhat Subjective = >0.1)"
        sentiCat = "<p>More or less objective tweets: " + str(len(sentiPol)) + "<p>Subjective tweets: " + str(len(sentiSubj))
        sentiment = "<h3>Overall current sentiment on Twitter:</h3>" + "<br>Polarity: " + strPol + "<br>Subjectivity: " + strSubj + sentiCat + "<hr>"
        objTweet = '<h3>' + 'Mostly objective information about \"' +  keyword + '\"' + ' on Twitter' + '</h3><p>' + objTweet + "<hr>"
        subjTweet = '<h3>' + 'Comments about \"' +  keyword + '\"' + ' on Twitter: ' + '</h3><p>' + subjTweet + "<hr>"
        style = '<style> table, th, td {border: 1px solid black; border-collapse: collapse; padding: 10px;} </style>'
        return style + title + '<h1>' + keyword + '</h1><p>' + summary + link + backlink1 + backlink2 + "<hr>" + sentiment + '<p>' + '<table><tr><td valign=\"top\">' + objTweet + '</td><td valign=\"top\">' + subjTweet + '</td>' + '</tr></table>'

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
            title = "<title>Minipedia - Suggestions for search \" " + keyword + "\"</title>" + responsive
            heading = "<h1>Suggestions for " + '\"' + keyword + '\"' + "</h1>"
            suggestions = '<p><select name="dropdown">'
            for i in range(len(e.options)):
                suggestions = suggestions + "<option value ='" + e.options[i] + "'>" + e.options[i] + "</options>"
            suggestions += "</select>"
            lengthPassed = '<p>Selected Length: <select name="lengthPassed">' + '<option value="' + length + '" selected>' + length + '</option></select>'
            #langPassed = '<p>Selected Language: <select name=\"langPassed\">' + '<option value=\"' + lang + '\" selected>' + lang + '<\/option><\/select>'
            form = '<form action="/summarydrop" method="POST">' + suggestions + lengthPassed + '<p><input type="submit" value="Submit"></form>'
            output = title + heading + form
            return output
        except wk.exceptions.PageError:
            return "No page exists for" + "<p><a href=\"\/" + HOST + "\">Back to home page</a>" + str(search)
        else:
            return page
    else:
        title = "<title>Minipedia - Suggestions for search \" " + keyword + "\"</title>" + responsive
        heading = "<h1>Suggestions for " + '\"' + keyword + '\"' + "</h1>"
        suggestions = '<p><select name="dropdown">'
        for i in range(len(search)):
            suggestions = suggestions + "<option value ='" + search[i] + "'>" + search[i] + "</options>"
        suggestions += "</select>"
        lengthPassed = '<p>Selected Length: <select name="lengthPassed">' + '<option value="' + length + '" selected>' + length + '</option></select>'
        #langPassed = '<p>Selected Language: <select name="langPassed">' + '<option value="' + str(lang) + '" selected>' + str(lang) + '</option></select>'
        form = '<form action="/summarydrop" method="POST">' + suggestions + lengthPassed + '<p><input type="submit" value="Submit"></form>'
        page = title + heading + form
        return page

def setLang(language):
    return wk.set_lang(language)

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

def getSentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity =  blob.sentiment.subjectivity
    return polarity, subjectivity

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


application = default_app()