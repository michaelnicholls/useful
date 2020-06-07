from google.appengine.api import mail 
from google.appengine.api import urlfetch
import cgi
import time
import datetime
import math
import random
import csv
import base64 

from datetime import datetime, date
from datetime import timedelta

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
class ScheduleLocation(db.Model):
  location = db.StringProperty();
  
class QuizMail(db.Model):
  xxx = db.StringProperty()
  lastSent = db.DateTimeProperty()

class EventHistory(db.Model):
  event = db.StringProperty()
  runat = db.StringProperty()

class Event(db.Model):
  course = db.StringProperty()
  event = db.StringProperty()
  instructor = db.StringProperty()
  country = db.StringProperty()
  location = db.StringProperty()
  lastday = db.StringProperty()
  groups = db.StringProperty()
  abappwd = db.StringProperty()
  ospwd = db.StringProperty()
  language = db.StringProperty()
  decfmt = db.StringProperty()
  datefmt = db.StringProperty()
  clones = db.StringProperty()

class Alias(db.Model):
  alias = db.StringProperty()
  ccode = db.StringProperty()
  location = db.StringProperty()


class Country(db.Model):
  ccode = db.StringProperty()
  weeks = db.IntegerProperty()
#  a = db.StringProperty()
#  date = db.StringProperty()

class CI(db.Model):
   host = db.StringProperty()
   instructions = db.TextProperty()

class CITemplates(db.Model):
   name = db.StringProperty()
   lang = db.StringProperty()
   text = db.TextProperty()

class CIHistory(db.Model):
   created = db.DateTimeProperty()
   course = db.StringProperty()
   host = db.StringProperty()
   username = db.StringProperty()
   password = db.StringProperty()

class Course(db.Model):
  ccode = db.StringProperty()
  location = db.StringProperty();
  ccourse = db.StringProperty();
  weeks = db.IntegerProperty()

class LocWeeks(db.Model):
  ccode = db.StringProperty();
  location = db.StringProperty();
  weeks = db.IntegerProperty()

class Location(db.Model):
  location = db.StringProperty();
  coords = db.StringProperty()

class History(db.Model):
  ccode = db.StringProperty();
  weeks = db.IntegerProperty();
  ccourse = db.StringProperty();

class getEvent(webapp.RequestHandler):
  def get(self):
     now = date.today()
     today = now.strftime("%Y%m%d")
     e = self.request.get('event','')
     f = self.request.get('format')
     all = self.request.get('all')
     if len(f) == 0:
         f="text"
     found = 0
     if all != "":
       events = db.GqlQuery("SELECT * from Event order by event")
       if f == "json" or f == "ui5json":
           self.response.out.write('{"Events":[')
#       f = "text"
     else:
       events = db.GqlQuery("SELECT * from Event where event = :1", e)
     counter = 0
     for event in events:
#       found = 1
       valid = False
       if event.lastday >= today:
           valid = True
           found = 1
           counter = counter + 1
       else:
           event.delete()
           histories = db.GqlQuery("SELECT * from EventHistory where event = :1", event.event)
           for history in histories:
                history.delete()
       histories = db.GqlQuery("SELECT * from EventHistory where event = :1", event.event)
       firstrun = ""
       lastrun = ""
       histcounter = 0
       for history in histories:
          lastrun = history.runat[:16]
          if histcounter == 0:
	    firstrun = history.runat[:16]
          histcounter = histcounter + 1
       if f=="ui5":
             self.response.out.write("<script>")
	     url = "https://event-p2000183813trial.dispatcher.hanatrial.ondemand.com/#/Details/"+event.event
             self.response.out.write(' window.location.href="'+url+'";')
	     self.response.out.write("</script>")
       numclones = 0
       if '[' in event.clones:
           numclones = event.clones.count(",") + 1
       ut = "4.x"
       ut41 = "ut41" in event.clones.lower()
       ut42 = "ut42" in event.clones.lower()
       ut43 = "ut43" in event.clones.lower()
       if ut41 and (not ut42) and (not ut43):
           ut = "4.1"
       if ut42 and (not ut41) and (not ut43):
           ut = "4.2"
       if ut43 and (not ut41) and (not ut42):
           ut = "4.3"
       if f=="text":
         self.response.out.write("event:"+event.event+"\n")
         self.response.out.write("course:"+event.course+"\n")
         self.response.out.write("instructor:"+event.instructor+"\n")
         self.response.out.write("country:"+event.country+"\n")
         self.response.out.write("location:"+event.location+"\n")
         self.response.out.write("lastday:"+event.lastday+"\n")
         self.response.out.write("groups:"+event.groups+"\n")
         self.response.out.write("abappwd:"+event.abappwd+"\n")
         self.response.out.write("ospwd:"+event.ospwd+"\n")
         self.response.out.write("language:"+event.language+"\n")
         self.response.out.write("decfmt:"+event.decfmt+"\n")
         self.response.out.write("datefmt:"+event.datefmt+"\n")
         self.response.out.write("clones:"+event.clones+"\n")
#         self.response.out.write("firstrun:"+firstrun+"\n")
         self.response.out.write("==============\n")
       if f=="xml":
         self.response.out.write("<Event><event>"+event.event+"</event>\n")
         self.response.out.write("<course>"+event.course+"</course>\n")
         self.response.out.write("<instructor>"+event.instructor+"</instructor>\n")
         self.response.out.write("<country>"+event.country+"</country>\n")
         self.response.out.write("<location>"+event.location+"</location>\n")
         self.response.out.write("<lastday>"+event.lastday+"</lastday>\n")
         self.response.out.write("<groups>"+event.groups+"</groups>\n")
         self.response.out.write("<abappwd>"+event.abappwd+"</abappwd>\n")
         self.response.out.write("<ospwd>"+event.ospwd+"</ospwd>\n")
         self.response.out.write("<language>"+event.language+"</language>\n")
         self.response.out.write("<decfmt>"+event.decfmt+"</decfmt>\n")
         self.response.out.write("<datefmt>"+event.datefmt+"</datefmt>\n")
         self.response.out.write("<clones>"+event.clones+"</clones></Event>\n")
       if f=="json" and valid:
         if counter > 1:
            self.response.out.write(",")
	 self.response.out.write('{"Event":{"event":"'+event.event+'",')
         self.response.out.write('"course":"'+event.course+'",')
         self.response.out.write('"instructor":"'+event.instructor+'",')
         self.response.out.write('"country":"'+event.country+'",')
         self.response.out.write('"location":"'+event.location+'",')
         self.response.out.write('"lastday":"'+event.lastday+'",')
         self.response.out.write('"groups":"'+event.groups+'",')
         self.response.out.write('"abappwd":"'+event.abappwd+'",')
         self.response.out.write('"ospwd":"'+event.ospwd+'",')
         self.response.out.write('"language":"'+event.language+'",')
         self.response.out.write('"decfmt":"'+event.decfmt+'",')
         self.response.out.write('"datefmt":"'+event.datefmt+'",')
         self.response.out.write('"clones":"'+event.clones+'",')
         self.response.out.write('"messageText":"",')
         self.response.out.write('"messageExists":false,')
         self.response.out.write('"eventFound":true}}')
       if f=="ui5json" and valid:
         if counter > 1:
            self.response.out.write(",")
         if event.instructor=="":
               event.instructor="unspecified"
         if event.lastday=="" or len(event.lastday) != 8:
               event.lastday="unspecified"
	 else:
               event.lastday=event.lastday[0:4]+"."+event.lastday[4:6]+"."+event.lastday[6:]
         if event.groups=="":
               event.groups="unspecified"
         if event.abappwd=="":
               event.abappwd="unspecified"
         if event.ospwd=="":
               event.ospwd="unspecified"
         if event.language=="":
               event.language="unspecified"
         if event.clones=="":
               event.clones="unspecified"
         if event.instructor=="":
               event.instructor="unspecified"
         if event.decfmt=="" or event.decfmt == "1":
               event.decfmt="1.234.567,89"
         if event.decfmt=="X":
               event.decfmt="1,234,567.89"
         if event.decfmt=="Y":
               event.decfmt="1 234 567,89"
         if event.datefmt=="1":
               event.datefmt="DD.MM.YYYY"
         if event.datefmt=="2":
               event.datefmt="MM/DD/YYYY"
         if event.datefmt=="3":
               event.datefmt="MM-DD-YYYY"
         if event.datefmt=="1":
               event.datefmt="DD.MM.YYYY"
         if event.datefmt=="4":
               event.datefmt="YYYY.MM.DD"
         if event.datefmt=="5":
               event.datefmt="YYYY/MM/DD"
         if event.datefmt=="6":
               event.datefmt="YYYY-MM-DD"
         if event.datefmt=="7":
               event.datefmt="GYY.MM.DD (Japanese)"
         if event.datefmt=="8":
               event.datefmt="GYY/MM/DD (Japanese)"
         if event.datefmt=="9":
               event.datefmt="GYY-MM-DD (Japanese)"
         if event.datefmt=="A":
               event.datefmt="YYYY/MM/DD (Islamic 1)"
         if event.datefmt=="B":
               event.datefmt="YYYY/MM/DD (Islamic 2)"
         if event.datefmt=="C":
               event.datefmt="YYYY/MM/DD (Iranian)"
         if event.datefmt=="":
               event.datefmt="unspecified"
         self.response.out.write('{"Event":{"event":"'+event.event+'",')
         self.response.out.write('"course":"'+event.course+'",')
         self.response.out.write('"instructor":"'+event.instructor+'",')
         self.response.out.write('"country":"'+event.country+'",')
         self.response.out.write('"location":"'+event.location+'",')
         self.response.out.write('"lastday":"'+event.lastday+'",')
         self.response.out.write('"groups":"'+event.groups+'",')
         self.response.out.write('"abappwd":"'+event.abappwd+'",')
         self.response.out.write('"ospwd":"'+event.ospwd+'",')
         self.response.out.write('"language":"'+event.language+'",')
         self.response.out.write('"decfmt":"'+event.decfmt+'",')
         self.response.out.write('"datefmt":"'+event.datefmt+'",')
         self.response.out.write('"clones":"'+event.clones+'",')
         self.response.out.write('"numclones":"'+str(numclones)+'",')
         self.response.out.write('"firstrun":"'+firstrun+'",')
         self.response.out.write('"lastrun":"'+lastrun+'",')
         self.response.out.write('"ut":"'+ut+'",')
         self.response.out.write('"messageText":"",')
         self.response.out.write('"messageExists":false,')
         self.response.out.write('"eventFound":true}}')
       if f=="html":
         self.response.out.write('<form action="/add"><table><tr><td>')
         self.response.out.write('event     </td><td><input name="event" readonly value="'+event.event+'"></td></tr><tr><td>')
         self.response.out.write('course    </td><td><input name="course" value="'+event.course+'"></td></tr><tr><td>')
         self.response.out.write('instructor</td><td><input name="instructor" value="'+event.instructor+'"></td></tr><tr><td>')
         self.response.out.write('country   </td><td><input name="country" value="'+event.country+'"></td></tr><tr><td>')
         self.response.out.write('location  </td><td><input name="location" value="'+event.location+'"></td></tr><tr><td>')
         self.response.out.write('lastday   </td><td><input name="lastday" value="'+event.lastday+'"></td></tr><tr><td>')
         self.response.out.write('groups    </td><td><input name="groups" value="'+event.groups+'"></td></tr><tr><td>')
         self.response.out.write('abappwd   </td><td><input name="abappwd" value="'+event.abappwd+'"></td></tr><tr><td>')
         self.response.out.write('ospwd     </td><td><input name="ospwd" value="'+event.ospwd+'"></td></tr><tr><td>')
         self.response.out.write('language  </td><td><input name="language" value="'+event.language+'"></td></tr><tr><td>')
         self.response.out.write('decfmt    </td><td><input name="decfmt" value="'+event.decfmt+'"></td></tr><tr><td>')
         self.response.out.write('datefmt   </td><td><input name="datefmt" value="'+event.datefmt+'"></td></tr><tr><td>')
         self.response.out.write('clones    </td><td><input name="clones" value="'+event.clones+'"></td></tr><tr><td>')
         self.response.out.write('<input type="submit" value="Submit"></tr></table></form>')
     if all != "":
         if f == "json" or f == "ui5json":
            self.response.out.write("]}")
     if found == 0:
         if f != "json" and f != "ui5json":
            self.response.out.write("Invalid event")
         if all == "" and (f == "json" or f == "ui5json"):
           self.response.out.write('{"Event":{"event":"",')
           self.response.out.write('"course":"",')
           self.response.out.write('"instructor":"",')
           self.response.out.write('"country":"",')
           self.response.out.write('"location":"",')
           self.response.out.write('"lastday":"",')
           self.response.out.write('"groups":"",')
           self.response.out.write('"abappwd":"",')
           self.response.out.write('"ospwd":"",')
           self.response.out.write('"language":"",')
           self.response.out.write('"decfmt":"",')
           self.response.out.write('"decfmt":"",')
           self.response.out.write('"clones":"",')
           self.response.out.write('"messageText":"No ZSYSTEMSETUP found for event '+e+'",')
           self.response.out.write('"messageExists":true,')
           self.response.out.write('"eventFound":false}}')
            


class launchYahoo(webapp.RequestHandler):
  def post(self):
    username = self.request.get('login','no username')
    password = self.request.get('passwd', 'no password')

    self.response.out.write("""
<script>
function go() {
var mapForm = document.createElement("form");
mapForm.target = "_blank";    
mapForm.method = "POST";
mapForm.action = "https://login.yahoo.com/config/login";

// Create an input
var mapLogin = document.createElement("input");
mapLogin.type = "text";
mapLogin.name = "login";
var mapPasswd = document.createElement("input");
mapPasswd.type = "password";
mapPasswd.name = "passwd";
""")
    self.response.out.write('mapLogin.value = "'+username+'";\n')
    self.response.out.write('mapPasswd.value = "'+password+'";')
    self.response.out.write("""


// Add the input to the form
mapForm.appendChild(mapLogin);
mapForm.appendChild(mapPasswd);

// Add the form to dom
document.body.appendChild(mapForm);

// Just submit
mapForm.submit();

}

</script>
<body onLoad="go()"></body>
""")

def getTemplate(string,lang):
#   result = urlfetch.fetch("http://sap-netweaver-training.appspot.com/handouts/"+lang+"/"+string+".template")
#   return result.content
    texts = db.GqlQuery("SELECT * from CITemplates where name = :1 and lang = :2", string+".template", lang)
    for t in texts:    
       s = t.text
    return s

def StoreTemplate(string,lang):
   result = urlfetch.fetch("http://sap-netweaver-training.appspot.com/handouts/"+lang+"/"+string)
   citemp = CITemplates( key_name = lang+string, name = string, lang = lang, text = db.Text(result.content))
   citemp.put()
   return "<br>"+lang+"/"+string+" stored"   

def fixXML(string):
   result = ""
   for ss in string:
      if ss=="&":
         result = result+"&amp;"
      elif ss=="<":
         result = result+"&lt;"
      elif ss==">":
         result = result+"&gt;"
      else:
         result = result+ss
#   return string
   return result

class StoreTemplates(webapp.RequestHandler):
  def get(self):
    self.response.out.write(StoreTemplate("BI.template","en"))     
    self.response.out.write(StoreTemplate("Cloud.template","en"))     
    self.response.out.write(StoreTemplate("Desktop.template","en"))     
    self.response.out.write(StoreTemplate("Finally.template","en"))     
    self.response.out.write(StoreTemplate("HANA.template","en"))     
    self.response.out.write(StoreTemplate("Initcourse.template","en"))     
    self.response.out.write(StoreTemplate("Newaccess.template","en"))     
    self.response.out.write(StoreTemplate("OES.template","en"))     
    self.response.out.write(StoreTemplate("System.template","en"))     
    self.response.out.write(StoreTemplate("VDI.template","en"))     

class KnownLocations(webapp.RequestHandler):  
  def get(self):
     simple = self.request.get('simple')
     c = self.request.get('c')
     if simple == "":
       self.response.out.write('<h2>Known locations for training</h2>')
       self.response.out.write('<h3>Other locations may be used, but may not be visible immediately on the map</h3>')
       if c == "":
         self.response.out.write('<form action="/knownLocations"><select name="c">')
       else:
         self.response.out.write('<table><tr><td valign="top"><table border="1"><tr><td>Country</td><td>Location</td></th>')
     locations = db.GqlQuery("SELECT * from Location order by location")
     lastloc = ""
     loclist = []
     for location in locations:
#          if location.location[0:2] == lastloc:
#            self.response.out.write('<tr><td></td><td>'+location.location[2:]+'</td></tr>' )
#          else:
            lastloc = location.location[0:2]
	    disploc = lastloc
            if lastloc == "AF":
                 disploc = "Afghanistan"
            if lastloc == "AX":
                 disploc = "Åland Islands"
            if lastloc == "AL": 
                disploc = "Albania"
            if lastloc == "DZ": 
                disploc = "Algeria"
            if lastloc == "AS": 
                disploc = "American Samoa"
            if lastloc == "AD": 
                disploc = "Andorra"
            if lastloc == "AO":
                disploc = "Angola"
            if lastloc == "AI": 
                disploc = "Anguilla"
            if lastloc == "AQ": 
                disploc = "Antarctica"
            if lastloc == "AG": 
                disploc = "Antigua and Barbuda"
            if lastloc == "AR": 
                disploc = "Argentina"
            if lastloc == "AM": 
                disploc = "Armenia"
            if lastloc == "AW": 
                disploc = "Aruba"
            if lastloc == "AU": 
                disploc = "Australia"
            if lastloc == "AT": 
                disploc = "Austria"
            if lastloc == "AZ": 
                disploc = "Azerbaijan"
            if lastloc == "BS": 
                disploc = "Bahamas"
            if lastloc == "BH": 
                disploc = "Bahrain"
            if lastloc == "BD": 
                disploc = "Bangladesh"
            if lastloc == "BB": 
                disploc = "Barbados"
            if lastloc == "BY": 
                disploc = "Belarus"
            if lastloc == "BE": 
                disploc = "Belgium"
            if lastloc == "BZ": 
                disploc = "Belize"
            if lastloc == "BJ": 
                disploc = "Benin"
            if lastloc == "BM": 
                disploc = "Bermuda"
            if lastloc == "BT": 
                disploc = "Bhutan"
            if lastloc == "BO": 
                disploc = "Bolivia"
            if lastloc == "BA": 
                disploc = "Bosnia and Herzegovina"
            if lastloc == "BW": 
                disploc = "Botswana"
            if lastloc == "BV": 
                disploc = "Bouvet Island"
            if lastloc == "BR": 
                disploc = "Brazil"
            if lastloc == "IO": 
                disploc = "British Indian Ocean Territory"
            if lastloc == "BN": 
                disploc = "Brunei Darussalam"
            if lastloc == "BG": 
                disploc = "Bulgaria"
            if lastloc == "BF": 
                disploc = "Burkina Faso"
            if lastloc == "BI": 
                disploc = "Burundi"
            if lastloc == "KH": 
                disploc = "Cambodia"
            if lastloc == "CM": 
                disploc = "Cameroon"
            if lastloc == "CA": 
                disploc = "Canada"
            if lastloc == "CV": 
                disploc = "Cape Verde"
            if lastloc == "KY": 
                disploc = "Cayman Islands"
            if lastloc == "CF": 
                disploc = "Central African Republic"
            if lastloc == "TD": 
                disploc = "Chad"
            if lastloc == "CL": 
                disploc = "Chile"
            if lastloc == "CN": 
                disploc = "China"
            if lastloc == "CX": 
                disploc = "Christmas Island"
            if lastloc == "CC": 
                disploc = "Cocos (Keeling) Islands"
            if lastloc == "CO": 
                disploc = "Colombia"
            if lastloc == "KM": 
                disploc = "Comoros"
            if lastloc == "CG": 
                disploc = "Congo"
            if lastloc == "CD": 
                disploc = "Congo, The Democratic Republic of the"
            if lastloc == "CK": 
                disploc = "Cook Islands"
            if lastloc == "CR": 
                disploc = "Costa Rica"
            if lastloc == "CI": 
                disploc = "Côte d'Ivoire"
            if lastloc == "HR": 
                disploc = "Croatia"
            if lastloc == "CU": 
                disploc = "Cuba"
            if lastloc == "CY": 
                disploc = "Cyprus"
            if lastloc == "CZ": 
                disploc = "Czech Republic"
            if lastloc == "DK": 
                disploc = "Denmark"
            if lastloc == "DJ": 
                disploc = "Djibouti"
            if lastloc == "DM": 
                disploc = "Dominica"
            if lastloc == "DO": 
                disploc = "Dominican Republic"
            if lastloc == "EC": 
                disploc = "Ecuador"
            if lastloc == "EG": 
                disploc = "Egypt"
            if lastloc == "SV": 
                disploc = "El Salvador"
            if lastloc == "GQ": 
                disploc = "Equatorial Guinea"
            if lastloc == "ER": 
                disploc = "Eritrea"
            if lastloc == "EE": 
                disploc = "Estonia"
            if lastloc == "ET": 
                disploc = "Ethiopia"
            if lastloc == "FK": 
                disploc = "Falkland Islands (Malvinas)"
            if lastloc == "FO": 
                disploc = "Faroe Islands"
            if lastloc == "FJ": 
                disploc = "Fiji"
            if lastloc == "FI": 
                disploc = "Finland"
            if lastloc == "FR": 
                disploc = "France"
            if lastloc == "GF": 
                disploc = "French Guiana"
            if lastloc == "PF": 
                disploc = "French Polynesia"
            if lastloc == "TF": 
                disploc = "French Southern Territories"
            if lastloc == "GA": 
                disploc = "Gabon"
            if lastloc == "GM": 
                disploc = "Gambia"
            if lastloc == "GE": 
                disploc = "Georgia"
            if lastloc == "DE": 
                disploc = "Germany"
            if lastloc == "GH": 
                disploc = "Ghana"
            if lastloc == "GI": 
                disploc = "Gibraltar"
            if lastloc == "GR": 
                disploc = "Greece"
            if lastloc == "GL": 
                disploc = "Greenland"
            if lastloc == "GD": 
                disploc = "Grenada"
            if lastloc == "GP": 
                disploc = "Guadeloupe"
            if lastloc == "GU": 
                disploc = "Guam"
            if lastloc == "GT": 
                disploc = "Guatemala"
            if lastloc == "GG": 
                disploc = "Guernsey"
            if lastloc == "GN": 
                disploc = "Guinea"
            if lastloc == "GW": 
                disploc = "Guinea-Bissau"
            if lastloc == "GY": 
                disploc = "Guyana"
            if lastloc == "HT": 
                disploc = "Haiti"
            if lastloc == "HM": 
                disploc = "Heard Island and McDonald Islands"
            if lastloc == "VA": 
                disploc = "Holy See (Vatican City State)"
            if lastloc == "HN": 
                disploc = "Honduras"
            if lastloc == "HK": 
                disploc = "Hong Kong"
            if lastloc == "HU": 
                disploc = "Hungary"
            if lastloc == "IS": 
                disploc = "Iceland"
            if lastloc == "IN": 
                disploc = "India"
            if lastloc == "ID": 
                disploc = "Indonesia"
            if lastloc == "IR": 
                disploc = "Iran, Islamic Republic of"
            if lastloc == "IQ": 
                disploc = "Iraq"
            if lastloc == "IE": 
                disploc = "Ireland"
            if lastloc == "IM": 
                disploc = "Isle of Man"
            if lastloc == "IL": 
                disploc = "Israel"
            if lastloc == "IT": 
                disploc = "Italy"
            if lastloc == "JM": 
                disploc = "Jamaica"
            if lastloc == "JP": 
                disploc = "Japan"
            if lastloc == "JE": 
                disploc = "Jersey"
            if lastloc == "JO": 
                disploc = "Jordan"
            if lastloc == "KZ": 
                disploc = "Kazakhstan"
            if lastloc == "KE": 
                disploc = "Kenya"
            if lastloc == "KI": 
                disploc = "Kiribati"
            if lastloc == "KP": 
                disploc = "Korea, Democratic People's Republic of"
            if lastloc == "KR": 
                disploc = "Korea, Republic of"
            if lastloc == "KW": 
                disploc = "Kuwait"
            if lastloc == "KG": 
                disploc = "Kyrgyzstan"
            if lastloc == "LA": 
                disploc = "Lao People's Democratic Republic"
            if lastloc == "LV": 
                disploc = "Latvia"
            if lastloc == "LB": 
                disploc = "Lebanon"
            if lastloc == "LS": 
                disploc = "Lesotho"
            if lastloc == "LR": 
                disploc = "Liberia"
            if lastloc == "LY": 
                disploc = "Libyan Arab Jamahiriya"
            if lastloc == "LI": 
                disploc = "Liechtenstein"
            if lastloc == "LT": 
                disploc = "Lithuania"
            if lastloc == "LU": 
                disploc = "Luxembourg"
            if lastloc == "MO": 
                disploc = "Macao"
            if lastloc == "MK": 
                disploc = "Macedonia, The Former Yugoslav Republic of"
            if lastloc == "MG": 
                disploc = "Madagascar"
            if lastloc == "MW": 
                disploc = "Malawi"
            if lastloc == "MY": 
                disploc = "Malaysia"
            if lastloc == "MV": 
                disploc = "Maldives"
            if lastloc == "ML": 
                disploc = "Mali"
            if lastloc == "MT": 
                disploc = "Malta"
            if lastloc == "MH": 
                disploc = "Marshall Islands"
            if lastloc == "MQ": 
                disploc = "Martinique"
            if lastloc == "MR": 
                disploc = "Mauritania"
            if lastloc == "MU": 
                disploc = "Mauritius"
            if lastloc == "YT": 
                disploc = "Mayotte"
            if lastloc == "MX": 
                disploc = "Mexico"
            if lastloc == "FM": 
                disploc = "Micronesia, Federated States of"
            if lastloc == "MD": 
                disploc = "Moldova"
            if lastloc == "MC": 
                disploc = "Monaco"
            if lastloc == "MN": 
                disploc = "Mongolia"
            if lastloc == "ME": 
                disploc = "Montenegro"
            if lastloc == "MS": 
                disploc = "Montserrat"
            if lastloc == "MA": 
                disploc = "Morocco"
            if lastloc == "MZ": 
                disploc = "Mozambique"
            if lastloc == "MM": 
                disploc = "Myanmar"
            if lastloc == "NA": 
                disploc = "Namibia"
            if lastloc == "NR": 
                disploc = "Nauru"
            if lastloc == "NP": 
                disploc = "Nepal"
            if lastloc == "NL": 
                disploc = "Netherlands"
            if lastloc == "AN": 
                disploc = "Netherlands Antilles"
            if lastloc == "NC": 
                disploc = "New Caledonia"
            if lastloc == "NZ": 
                disploc = "New Zealand"
            if lastloc == "NI": 
                disploc = "Nicaragua"
            if lastloc == "NE": 
                disploc = "Niger"
            if lastloc == "NG": 
                disploc = "Nigeria"
            if lastloc == "NU": 
                disploc = "Niue"
            if lastloc == "NF": 
                disploc = "Norfolk Island"
            if lastloc == "MP": 
                disploc = "Northern Mariana Islands"
            if lastloc == "NO": 
                disploc = "Norway"
            if lastloc == "OM": 
                disploc = "Oman"
            if lastloc == "PK": 
                disploc = "Pakistan"
            if lastloc == "PW": 
                disploc = "Palau"
            if lastloc == "PS": 
                disploc = "Palestinian Territory, Occupied"
            if lastloc == "PA": 
                disploc = "Panama"
            if lastloc == "PG": 
                disploc = "Papua New Guinea"
            if lastloc == "PY": 
                disploc = "Paraguay"
            if lastloc == "PE": 
                disploc = "Peru"
            if lastloc == "PH": 
                disploc = "Philippines"
            if lastloc == "PN": 
                disploc = "Pitcairn"
            if lastloc == "PL": 
                disploc = "Poland"
            if lastloc == "PT": 
                disploc = "Portugal"
            if lastloc == "PR": 
                disploc = "Puerto Rico"
            if lastloc == "QA": 
                disploc = "Qatar"
            if lastloc == "RE": 
                disploc = "Réunion"
            if lastloc == "RO": 
                disploc = "Romania"
            if lastloc == "RU": 
                disploc = "Russian Federation"
            if lastloc == "RW": 
                disploc = "Rwanda"
            if lastloc == "BL": 
                disploc = "Saint Barthélemy"
            if lastloc == "SH": 
                disploc = "Saint Helena"
            if lastloc == "KN": 
                disploc = "Saint Kitts and Nevis"
            if lastloc == "LC": 
                disploc = "Saint Lucia"
            if lastloc == "MF": 
                disploc = "Saint Martin"
            if lastloc == "PM": 
                disploc = "Saint Pierre and Miquelon"
            if lastloc == "VC": 
                disploc = "Saint Vincent and the Grenadines"
            if lastloc == "WS": 
                disploc = "Samoa"
            if lastloc == "SM": 
                disploc = "San Marino"
            if lastloc == "ST": 
                disploc = "Sao Tome and Principe"
            if lastloc == "SA": 
                disploc = "Saudi Arabia"
            if lastloc == "SN": 
                disploc = "Senegal"
            if lastloc == "RS": 
                disploc = "Serbia"
            if lastloc == "SC": 
                disploc = "Seychelles"
            if lastloc == "SL": 
                disploc = "Sierra Leone"
            if lastloc == "SG": 
                disploc = "Singapore"
            if lastloc == "SK": 
                disploc = "Slovakia"
            if lastloc == "SI": 
                disploc = "Slovenia"
            if lastloc == "SB": 
                disploc = "Solomon Islands"
            if lastloc == "SO": 
                disploc = "Somalia"
            if lastloc == "ZA": 
                disploc = "South Africa"
            if lastloc == "GS": 
                disploc = "South Georgia and the South Sandwich Islands"
            if lastloc == "ES": 
                disploc = "Spain"
            if lastloc == "LK": 
                disploc = "Sri Lanka"
            if lastloc == "SD": 
                disploc = "Sudan"
            if lastloc == "SR": 
                disploc = "Suriname"
            if lastloc == "SJ": 
                disploc = "Svalbard and Jan Mayen"
            if lastloc == "SZ": 
                disploc = "Swaziland"
            if lastloc == "SE": 
                disploc = "Sweden"
            if lastloc == "CH": 
                disploc = "Switzerland"
            if lastloc == "SY": 
                disploc = "Syrian Arab Republic"
            if lastloc == "TW": 
                disploc = "Taiwan, Province of China"
            if lastloc == "TJ": 
                disploc = "Tajikistan"
            if lastloc == "TZ": 
                disploc = "Tanzania, United Republic of"
            if lastloc == "TH": 
                disploc = "Thailand"
            if lastloc == "TL": 
                disploc = "Timor-Leste"
            if lastloc == "TG": 
                disploc = "Togo"
            if lastloc == "TK": 
                disploc = "Tokelau"
            if lastloc == "TO": 
                disploc = "Tonga"
            if lastloc == "TT": 
                disploc = "Trinidad and Tobago"
            if lastloc == "TN": 
                disploc = "Tunisia"
            if lastloc == "TR": 
                disploc = "Turkey"
            if lastloc == "TM": 
                disploc = "Turkmenistan"
            if lastloc == "TC": 
                disploc = "Turks and Caicos Islands"
            if lastloc == "TV": 
                disploc = "Tuvalu"
            if lastloc == "UG": 
                disploc = "Uganda"
            if lastloc == "UA": 
                disploc = "Ukraine"
            if lastloc == "AE": 
                disploc = "United Arab Emirates"
            if lastloc == "GB": 
                disploc = "United Kingdom"
            if lastloc == "US": 
                disploc = "United States"
            if lastloc == "UM": 
                disploc = "United States Minor Outlying Islands"
            if lastloc == "UY": 
                disploc = "Uruguay"
            if lastloc == "UZ": 
                disploc = "Uzbekistan"
            if lastloc == "VU": 
                disploc = "Vanuatu"
            if lastloc == "VE": 
                disploc = "Venezuela"
            if lastloc == "VN": 
                disploc = "Viet Nam"
            if lastloc == "VG": 
                disploc = "Virgin Islands, British"
            if lastloc == "VI": 
                disploc = "Virgin Islands, U.S."
            if lastloc == "WF": 
                disploc = "Wallis and Futuna"
            if lastloc == "EH": 
                disploc = "Western Sahara"
            if lastloc == "YE": 
                disploc = "Yemen"
            if lastloc == "ZM": 
                disploc = "Zambia"
            if lastloc == "ZW": 
                disploc = "Zimbabwe"
#            self.response.out.write('<tr><td>'+disploc+'</td><td>'+location.location[2:]+'</td></tr>' )
            try:
               loclist.append(disploc+":"+location.location[0:2]+location.location[2:].title().replace('Sap ','SAP '))
            except:
             a = 10
            finally:
             a = 20
#            loclist.append(disploc+":"+location.location[0:2]+location.location[2:])
#            self.response.out.write("added "+disploc) 
#            self.response.out.write('<tr><td>'+disploc+'</td><td>'+location.location[2:]+'</td></tr>' )
     loclist.sort()
     lastloc = ""
     for l in loclist:
        locparts = l.split(":")
        if (locparts[0] == lastloc):
          if simple == "":  
             if c != "":
               if c == locparts[1][0:2]:
                 self.response.out.write('<tr><td></td><td>'+locparts[1][2:]+'</td></tr>' )
          else:
              self.response.out.write(l +"""
""")
        else:
            lastloc = locparts[0]
            if simple == "":
              if c == "":
                self.response.out.write('<option value="'+locparts[1][0:2]+'">'+lastloc+'</option>')
              else:
                if c == locparts[1][0:2]:
                  self.response.out.write('<tr><td>'+lastloc+'</td><td>'+locparts[1][2:]+'</td></tr>' )
            else:
              self.response.out.write(l +"""
""")
     if simple == "":  
         if c == "":
           self.response.out.write('</select><br><input type="submit" value="Show locations in country"></form>')
         else:  
           self.response.out.write('</table></td><td valign="top"><iframe src="/coordsin?c='+c+'" width="300" height="300"></iframe>')
           self.response.out.write('<br><a href="/knownLocations">Country list</a></td></tr></table>')
     
class Missing(webapp.RequestHandler):  
  def get(self):    
#     self.response.headers['Content-Type'] = 'text/plain'
     days = int(math.floor(time.time()/(60*60*24)))
     days = days - 3
     weeks = int(math.floor(days / 7))
     totalmissing = 0
     courses = db.GqlQuery("SELECT * from LocWeeks where weeks = :1", weeks)
     for course in courses:
        courselist = ""
        lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
        for lc in lcs:
            if courselist <> "":
                courselist = courselist + ","
            courselist = courselist + lc.ccourse
        locations = db.GqlQuery("SELECT * from Location where location = :1", lc.ccode + lc.location)
        
        matching = 0
        for location in locations:
           matching = matching + 1
        if matching == 0:
          totalmissing = totalmissing + 1
#          courselist = ""
#          lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
#          for lc in lcs:
#            if courselist <> "":
#                courselist = courselist + ","
#            courselist = courselist + lc.ccourse
          self.response.out.write('<br><a href="/modLocation?c=%s' % lc.ccode )
          self.response.out.write('&l=%s' % lc.location )
          self.response.out.write('">Setup coordinates for %s ' % lc.ccode)
          self.response.out.write('%s</a>' % lc.location)
          self.response.out.write(' Course(s): %s' % courselist)
          self.response.out.write('<br><a href="/modLocation?c=%s' % lc.ccode )
          self.response.out.write('&l=External/virtual' )
          self.response.out.write('">Setup coordinates for %s ' % lc.ccode)
          self.response.out.write('External/virtual</a>' )
#          self.response.out.write("."+courselist)
     if totalmissing == 0:
        self.response.out.write('All locations have coordinates maintained')
     self.response.out.write('<br><a href="/">Home</a>')

      
class MainPage(webapp.RequestHandler):  
  def get(self):    
#     self.response.headers['Content-Type'] = 'text/plain'
     self.response.out.write("""
<head><meta name="google-site-verification" content="DLD3mU8DTsrZ4urK3GbphVP4lDTEwm9C2ohZWX1VQvM" /></head>
<h2>SAP NetWeaver Training</h2>
<table border="1">
<tr>
<td><a target='_new' href='http://www.sap.com/services/education/catalog/netweaver/index.epx'>SAP NetWeaver training course directory</a></td>
</tr>
<tr>
<td><a href='/thisweekui5'>SAP NetWeaver training locations this week</a></td>
</tr>
<tr>
<td><a target='_new' href='/thisweekkml'>SAP NetWeaver training locations this week using the Google Earth plug-in.</a>
The plug-in is available <a target='_new' href='http://www.google.com/earth/explore/products/plugin.html'>here<a>.</td>
</tr>
<tr>
<td><a href='/downloads'>Downloads</a></td>
</tr>
<tr>
<td><a href='/launchpad'>URLs to start SAP NetWeaver applications</a></td>
</tr>
<tr>
<td><a target='_new' href="https://portal.wdf.sap.corp/irj/portal?

NavigationTarget=navurl://67255e30dc3f398a35f6e7f941a66df6">Instructor forum (Only available inside the SAP Corporate network)</a></td>
</tr>
<tr>
<td><a href='/capture'>Sample site for capture exercise in SAPEP</a></td>
</tr>
<tr>
<td><a href='/showtime'>Show time for a particular timezone</a></td>
</tr>

</table>      
      
      
        
     """)
     
class sitemap(webapp.RequestHandler):
  def get(self):    
#     self.response.headers['Content-Type'] = 'text/plain'
     self.response.out.write("""
<?xml version="1.0" encoding="UTF-8"?>
  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
	  xmlns:geo="http://www.google.com/geo/schemas/sitemap/1.0">
    <url>      
      <loc>http://sap-netweaver-training.appspot.com/thisweekkml</loc>
      <geo:geo>
        <geo:format>kml</geo:format>
      </geo:geo>
    </url> 
  </urlset>
    """)

class ModLocation(webapp.RequestHandler):
  def get(self):
    c = self.request.get('c')
    l = self.request.get('l')
    ca = self.request.get('ca')
    cl = self.request.get('cl')
    l = l.upper()
    c = c.upper()
    coords = self.request.get('coords')
    if len(c) > 0 and len(l) > 0 and len(ca)  and len(cl) > 0:
       alias = Alias(key_name = c + l,
                      alias = c + l,
                      ccode = ca,
                      location = cl)
       alias.put()
       self.response.out.write('<br><a href="/missingLocations">Missing location list</a>')
    elif len(c) > 0 and len(l) > 0 and len(coords) > 0:
       loc = Location(key_name = c + l,
                      location = c + l,
                      coords = coords)
       loc.put()
       self.response.out.write('<br><a href="/missingLocations">Missing location list</a>')
    else:  
      self.response.out.write("""
<h2>Set up the coordinates of a training location</h2>
<form action="/modLocation">
<table>
<tr><td>Country:</td><td><input name="c" readonly="readonly" class="box300" type="text" 
  """);
      self.response.out.write('value="' + c +'"/><br>')
      self.response.out.write("""</td><td>Alias for country:</td><td><input name="ca" type="text" class="box300"><td></tr>

<tr><td>Location:</td><td><input name="l" readonly="readonly" class="box300" type="text" 
  """);
      self.response.out.write('value="' + l + '"/><br>');
      self.response.out.write("""</td><td>Alias for location:</td><td><input name="cl" type="text" class="box300"><td></tr>

<tr><td>Coords:</td><td><input id="coords" name="coords" readonly="readonly"  class="box300" type="text" 
    """)
      self.response.out.write('value="' + coords + '"/><br>')
      self.response.out.write("""</td></tr>
</table>
<input type="submit" value="Submit">
<endform>
    <div id="map" style="width: 600px; height: 400px"></div>
  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAA_S1Hl34gSiyKpeqgnrugzhR9vd8S41iklsgskBU3cAd33nzXNhTIzzMOyagAm_eMutrMaeHshoM8kw"
      type="text/javascript"></script>
    <script type="text/javascript">
    //<![CDATA[
//    function load(pcount) {
      if (GBrowserIsCompatible()) {
        var map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
	var thisone = "EE";
	var lat = 0;
	var lng = 0;
	map.setCenter(new GLatLng(lat,lng),1);
	GEvent.addListener(map, "click", function(overlay,point) {
	if (point) document.getElementById('coords').value=point;
	});
//	   var point = new GLatLng(lat,lng);
//	   markerOptions = { title:thisone };
//	   var marker = new GMarker(point, markerOptions);
//	   map.addOverlay(marker);
//	}	
//       }
//     }
    }
    //]]>
    </script>
     <br><a href="/missingLocations">Missing location list</a>
  
      """);

class CoordsIn(webapp.RequestHandler):
  def get(self):
     country = self.request.get('c')
     if country == "":
 	country = 'US'

     kml = self.request.get('kml')
     if kml <> "":
        self.response.headers['Content-Type'] = 'application/vnd.google-earth.kml+xml'
        self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  <name>Coords in country</name>
      """)
        locations = db.GqlQuery("SELECT * from Location order by location")
        for location in locations:
	   if location.location[0:2]==country:
              disploc = location.location[2:].title().replace('Sap ','SAP ')
	      coords = location.coords[1:len(location.coords)-1].replace(" ","").split(",")
              self.response.out.write("<Placemark><name>"+disploc+"</name><description>"+disploc)
              self.response.out.write("</description><LookAt><longitude>"+coords[1]+"</longitude>")
	      self.response.out.write("<latitude>"+coords[0]+"</latitude><altitude>2000000</altitude>")
	      self.response.out.write("<altitudeMode>absolute</altitudeMode></LookAt><Point><coordinates>")
	      self.response.out.write(coords[1]+","+coords[0]+",0</coordinates></Point></Placemark>")

        self.response.out.write("""
</Document>
</kml>
      """);
     else:
       url =   'http://sap-netweaver-training.appspot.com/coordsin?kml=true&c='+country+'&xxx='+str(time.time())
       locations = db.GqlQuery("SELECT * from Location order by location")
       num = 0
       for location in locations:
	   if location.location[0:2]==country:
              disploc = location.location[2:].title().replace('Sap ','SAP ')
              num = num+1
	      coords = location.coords[1:len(location.coords)-1].replace(" ","").split(",")
       self.response.out.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<style type="text/css">   
html { height: 100% }   
body { height: 100%; margin: 0px; padding: 0px }   
#map_canvas { height: 100% } 
</style>

<title>SAP NetWeaver training locations</title>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
function initialize() {
  """)
       self.response.out.write('var zero = new google.maps.LatLng('+coords[0]+','+coords[1]+');')
       self.response.out.write("""
  var myOptions = {
    zoom: 5,
    center: zero,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  """)
       if (num == 1):
          self.response.out.write('var ctaLayer = new google.maps.KmlLayer("'+url+'",{ preserveViewport : true });')
       else:
          self.response.out.write('var ctaLayer = new google.maps.KmlLayer("'+url+'");')
       self.response.out.write("""
  ctaLayer.setMap(map);
}
</script>
</head>
<body onload="initialize()">
  <div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
    """);

class ThisWeekKml(webapp.RequestHandler):
  def get(self): 
     days = int(math.floor(time.time()/(60*60*24)))
     days = days - 3
     weeks = int(math.floor(days / 7))
     self.response.headers['Content-Type'] = 'application/vnd.google-earth.kml+xml'
     self.response.out.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
  <name>SAP NetWeaver Training Courses this week</name>
      """)
     oldcourses = db.GqlQuery("SELECT * from LocWeeks where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Course where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Country where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
         
     courses = db.GqlQuery("SELECT * from LocWeeks where weeks = :1", weeks)
     for course in courses:
        courselist = ""
        lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
        for lc in lcs:
            if courselist <> "":
                courselist = courselist + ","
            courselist = courselist + lc.ccourse
        locations = db.GqlQuery("SELECT * from Location where location = :1", lc.ccode + lc.location)
        matching = 0
        for location in locations:
           disploc = lc.location.title().replace('Sap ','SAP ')
#	   disploc = disploc.replace("\'","\\'")
           matching = matching + 1
        if matching > 0:
	   coords = location.coords[1:len(location.coords)-1].replace(" ","").split(",")
           self.response.out.write("<Placemark><name>"+disploc+"</name><description>Courses: "+courselist)
           self.response.out.write("</description><LookAt><longitude>"+coords[1]+"</longitude>")
	   self.response.out.write("<latitude>"+coords[0]+"</latitude><altitude>2000000</altitude>")
	   self.response.out.write("<altitudeMode>absolute</altitudeMode></LookAt><Point><coordinates>")
	   self.response.out.write(coords[1]+","+coords[0]+",0</coordinates></Point></Placemark>")


     self.response.out.write("""
</Document>
</kml>
      """);

class thisweekui5(webapp.RequestHandler):
  def get(self):
	self.response.out.write("""
	<script>
	window.location.href="https://thisweek-p2000183813trial.dispatcher.hanatrial.ondemand.com/index.html";
	</script>
	""")

class thisweekui5x(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<!DOCTYPE HTML>
<html>

	<head>
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta charset="UTF-8">
		<!--Author michael.nicholls@orange.fr -->
		<title>SAP courses running this week</title>

		<script id="sap-ui-bootstrap"
			src="https://storage.googleapis.com/sap-netweaver-training-hrd.appspot.com/ui5/sap-ui-core.js"
			data-sap-ui-libs="sap.m"
			data-sap-ui-theme="sap_bluecrystal"
			data-sap-ui-compatVersion="edge"
			data-sap-ui-resourceroots='{"Map": "/ui5"}'>
		</script>

		<link rel="stylesheet" type="text/css" href="css/style.css">

		<script>

			
			sap.ui.getCore().attachInit(function() {
				new sap.m.Shell({
					app: new sap.ui.core.ComponentContainer({
						height : "100%",
						name : "Map"
					})
				}).placeAt("content");
			});
		</script>
	</head>

	<body class="sapUiBody" id="content">
	</body>

</html>
    """)

class ci2(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<script>
		window.location.href="https://ci-p2000183813trial.dispatcher.hanatrial.ondemand.com/index.html";

</script>
    """)

class ci2x(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<!DOCTYPE HTML>
<html>

	<head>
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />
		<meta charset="UTF-8">
		<!--Author michael.nicholls@orange.fr -->
		<title>Generate access.sap.com connection instructions</title>

		<script id="sap-ui-bootstrap"
			src="https://storage.googleapis.com/sap-netweaver-training-hrd.appspot.com/ui5/sap-ui-core.js"
			data-sap-ui-libs="sap.m"
			data-sap-ui-theme="sap_bluecrystal"
			data-sap-ui-compatVersion="edge"
			data-sap-ui-resourceroots='{"CI": "/ci"}'>
		</script>

		<link rel="stylesheet" type="text/css" href="css/style.css">

		<script>

			
			sap.ui.getCore().attachInit(function() {
				new sap.m.Shell({
					app: new sap.ui.core.ComponentContainer({
						height : "100%",
						name : "CI"
					})
				}).placeAt("content");
			});
		</script>
	</head>

	<body class="sapUiBody" id="content">
	</body>

</html>
    """)
 
class ThisWeekJs(webapp.RequestHandler):
  def get(self): 
     days = int(math.floor(time.time()/(60*60*24)))
     days = days - 3
     weeks = int(math.floor(days / 7))
     self.response.out.write("""
<html>
<head>	
<title>SAP courses running this week</title>
	<meta charset="utf-8" />

	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
</head>
<body onresize="resize()">	<div id="select" style="width: 70px; height: 100%;float:left;"></div>
<div id="map" style="width: 1200px; height: 100%;float:left;"></div>
 <div id="counters" style="pointer-events: none; position: absolute; top: 20px; left: 150px">No courses currently running
</div>
	<script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
	<script src="/download_files/locations.js"></script>
	<script>
	var width = screen.availWidth - 120;
//	var width = window.outerWidth - 90;
//	alert(width);
//	document.getElementById('select').setAttribute("style","width:70px;height:100%;float:left;");
	var e1=document.getElementById('map');
	e1.style.width = width+"px";
//setAttribute("style","width:"+width+"px;height:100%;float:left;");
	var map = L.map('map').setView([0,0],2);
//		L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
                L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
				'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery  <a href="http://mapbox.com">Mapbox</a>',
			accessToken: 'pk.eyJ1IjoiaTAxNjQxNiIsImEiOiJmMWUxNGI5YmE1YzBmMTRkZDZjYmRkYTk4MmU0MzdlNSJ9.4VV4xXRJQzgVGuShkVFwpA',
			id: 'i016416.2cecf1f9'
		}).addTo(map);

        var MyIcon = L.Icon.Default.extend({
            options: { iconSize:     [10, 20], shadowSize:   [10,20], iconAnchor:   [10,10],  shadowAnchor: [10,20],   popupAnchor:  [-3, -6]  }});
         var myIcon = new MyIcon();
        var MyCloudIcon = L.Icon.Default.extend({
            options: { 
		iconUrl : '/download_files/cloud.png',
		shadowUrl : '/download_files/cloud.png',
		iconSize:     [20, 10], shadowSize:   [20,10], iconAnchor:   [10,10],  shadowAnchor: [10,10],   popupAnchor:  [-3, -6]  }});
         var myCloudIcon = new MyCloudIcon();
   	 var courses = [  

	

     """)
     oldcourses = db.GqlQuery("SELECT * from LocWeeks where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Course where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Country where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
         
     courses = db.GqlQuery("SELECT * from LocWeeks where weeks = :1", weeks)
     loccount = 0
     totalcourses = 0
     for course in courses:
        courselist = ""
        lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
        coursecount = 0
	locationcount = 0
	countrycount = 0
        coursetext = "Course:"
        for lc in lcs:
            totalcourses = totalcourses + 1
            coursecount = coursecount + 1
            if courselist <> "":
                coursetext = "Courses:"
                courselist = courselist + ","
                if (coursecount % 5) == 0:
                     courselist = courselist+"<br>"
            courselist = courselist + lc.ccourse
        locations = db.GqlQuery("SELECT * from Location where location = :1", lc.ccode + lc.location)
        matching = 0
        for location in locations:
           disploc = lc.location.title().replace('Sap ','SAP ')
	   disploc = disploc.replace("\'","&rsquo;")
           matching = matching + 1
        if matching > 0:
	   coords = location.coords[1:len(location.coords)-1].replace(" ","").split(",")
	   if disploc == "SAP Live Access Cloud":
                random.seed()
                coords[0] = str(random.randint(-80,80))
                coords[1] = str(random.randint(-170,170))
#                coords = (randlong+","+randlat).split(",")
           if loccount > 0:
               self.response.out.write(",")
           self.response.out.write(" {country: '"+course.ccode+"', pos: ["+coords[0]+","+coords[1]+"], t1: '<b>"+disploc+"</b>', t2: '"+coursetext+courselist+"' }")
           loccount = loccount + 1
#           self.response.out.write("<Placemark><name>"+disploc+"</name><description>Courses: "+courselist)
#           self.response.out.write("</description><LookAt><longitude>"+coords[1]+"</longitude>")
#	   self.response.out.write("<latitude>"+coords[0]+"</latitude><altitude>2000000</altitude>")
#	   self.response.out.write("<altitudeMode>absolute</altitudeMode></LookAt><Point><coordinates>")
#	   self.response.out.write(coords[1]+","+coords[0]+",0</coordinates></Point></Placemark>")


     self.response.out.write("];\r\ntotalcourses ="+str(totalcourses)+";")
     self.response.out.write("""
//		];
		for (i=0; i< courses.length;i++) {
//		if (courses[i].t1.includes('SAP Live Access Cloud')) {
	        if (courses[i].t1.search('SAP Live Access Cloud')>0) {
			L.marker(courses[i].pos, {icon: myCloudIcon}).addTo(map).bindPopup(courses[i].t1+"<br />"+courses[i].t2);
		} else {
			L.marker(courses[i].pos, {icon: myIcon}).addTo(map).bindPopup(courses[i].t1+"<br />"+courses[i].t2);
		}};
var mydiv = document.getElementById("select");
var counterdiv = document.getElementById("counters");


var aTag = document.createElement('button');
	aTag.style.width="50px";
	aTag.style.margin="3px";

	aTag.href = "#";
	aTag.onclick = function(){map.setView([0,0],2)};
	aTag.innerHTML = "Global";
	mydiv.appendChild(aTag);
//	mydiv.appendChild(document.createElement('br'));
        var prev = "";
	var countryCount = 0;
      for (i=0; i < courses.length;i++) {
        if (courses[i].country != prev && courses[i].country != 'XX') {
	if (L.CountrySelect.countries[courses[i].country]!=null) 
			map.addLayer(L.geoJson(L.CountrySelect.countries[courses[i].country].geometry))	
	var aTag = document.createElement('button');
	aTag.style.width="50px";
	aTag.style.margin="3px";
	aTag.href = "#";
	aTag.setAttribute("title","Zoom to "+courses[i].country);
	aTag.onclick = (function(opt) {
		 return function() {
			setview(opt);
		};
	})(i);
	countryCount++;
	var coursesText = (totalcourses == 1) ? " course at " : " courses at ";
	var locationsText = ( courses.length == 1) ? " location in " : " locations in ";
	var countriesText = ( countryCount == 1) ? " country" : " countries";
 
	if (totalcourses > 0 ) {
		counterdiv.innerHTML = totalcourses +  coursesText + courses.length + locationsText + countryCount + countriesText;
	};
	aTag.innerHTML = courses[i].country;
	var aBr = document.createElement('br');
	mydiv.appendChild(aBr);
	mydiv.appendChild(aTag);
//	mydiv.appendChild(document.createElement('br'));
        };
        prev = courses[i].country;
	};
	function resize() {
//		alert('resize');
		width = window.outerWidth - 120;
		var e1 = document.getElementById('map');
		e1.style.width = width+'px';
//		document.getElementById('select').setAttribute("style","width:70px;height:100%;float:left;");
//		document.getElementById('map').setAttribute("style","width:"+width+"px;height:100%;float:left;");
	
	};
	function setview(p1) {
	
	map.setView(courses[p1].pos,5);
};
	</script></body></html>     """);

 
class ThisWeeki(webapp.RequestHandler):  
  def get(self):  
     url =   'http://sap-netweaver-training.appspot.com/thisweekkml?'+str(time.time())
     now = datetime.now()
     self.response.out.write("""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">   
html { height: 100% }   
body { height: 100%; margin: 0px; padding: 0px }   
#map_canvas { height: 100% } 
</style>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<title>SAP NetWeaver courses running this week</title>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript">
function initialize() {
  var zero = new google.maps.LatLng(0,0);
  var myOptions = {
    zoom: 2,
    center: zero,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
  """)
     self.response.out.write('var ctaLayer = new google.maps.KmlLayer("'+url+'",{ preserveViewport : true });')
     self.response.out.write("""
  ctaLayer.setMap(map);
}
</script>
</head>
<body onload="initialize()">
    """);
     self.response.out.write("<br>Details as at: "+now.strftime("%a %d %b %Y %H:%M:%S")+" GMT/UTC. Course details reset early on Sunday morning GMT/UTC. ")
     self.response.out.write(" Can't find your course location? Please try <a target='_new' href='/download_files/Instructor_hints.pdf'>this document</a>.</br>")
     self.response.out.write("""
  <div id="map_canvas" style="width:100%; height:90%"></div>
</body>
</html>
    """);

  
class ThisWeekOld(webapp.RequestHandler):  
  def get(self):    
#     self.response.headers['Content-Type'] = 'text/plain'    
#     self.response.out.write("<html><body>")
     brief = self.request.get('brief')
     days = int(math.floor(time.time()/(60*60*24)))
     days = days - 3
     weeks = int(math.floor(days / 7))
     self.response.out.write("""
    <html><head>
  <title>SAP NetWeaver training courses running this week</title>
  <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAA_S1Hl34gSiyKpeqgnrugzhR9vd8S41iklsgskBU3cAd33nzXNhTIzzMOyagAm_eMutrMaeHshoM8kw"
      type="text/javascript"></script>
    <script type="text/javascript">
    //<![CDATA[
    function load(pcount) {
      if (GBrowserIsCompatible() && pcount != "") {
        var map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
	var thisone;
	var lat;
	var lng;
    """);

     oldcourses = db.GqlQuery("SELECT * from LocWeeks where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Course where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Country where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
         
     courses = db.GqlQuery("SELECT * from LocWeeks where weeks = :1", weeks)
     for course in courses:
        courselist = ""
        lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
        for lc in lcs:
            if courselist <> "":
                courselist = courselist + ","
            courselist = courselist + lc.ccourse
        locations = db.GqlQuery("SELECT * from Location where location = :1", lc.ccode + lc.location)
        matching = 0
        for location in locations:
           disploc = lc.location
	   disploc = disploc.replace("\'","\\'")
           matching = matching + 1
        if matching > 0:
           self.response.out.write("	map.setCenter(new GLatLng"+location.coords+",1);")
           self.response.out.write("var point = new GLatLng"+location.coords+";")
	   self.response.out.write("markerOptions = { title:'"+disploc+" - courses: "+courselist+"' };")
	   self.response.out.write("var marker = new GMarker(point, markerOptions);")
	   self.response.out.write("map.addOverlay(marker);")

     self.response.out.write("""
	for (var i=0; i < pcount.length / 2; i++) {
	   thisone = pcount.substring(i*2,2*(i+1));
	   thisone = "";
	lat = 0; lng = 0;
	lat = 0; lng = 0;
if (thisone == 'AD') { lat = 42.5;lng = 1.5;}
if (thisone == 'AE') { lat = 24;lng = 54;}
if (thisone == 'AF') { lat = 33;lng = 65;}
if (thisone == 'AG') { lat = 17.05;lng = -61.8;}
if (thisone == 'AI') { lat = 18.25;lng = -63.1667;}
if (thisone == 'AL') { lat = 41;lng = 20;}
if (thisone == 'AM') { lat = 40;lng = 45;}
if (thisone == 'AN') { lat = 12.25;lng = -68.75;}
if (thisone == 'AO') { lat = -12.5;lng = 18.5;}
if (thisone == 'AP') { lat = 35;lng = 105;}
if (thisone == 'AQ') { lat = -90;lng = 0;}
if (thisone == 'AR') { lat = -34;lng = -64;}
if (thisone == 'AS') { lat = -14.3333;lng = -170;}
if (thisone == 'AT') { lat = 47.3333;lng = 13.3333;}
if (thisone == 'AU') { lat = -27;lng = 133;}
if (thisone == 'AW') { lat = 12.5;lng = -69.9667;}
if (thisone == 'AZ') { lat = 40.5;lng = 47.5;}
if (thisone == 'BA') { lat = 44;lng = 18;}
if (thisone == 'BB') { lat = 13.1667;lng = -59.5333;}
if (thisone == 'BD') { lat = 24;lng = 90;}
if (thisone == 'BE') { lat = 50.8333;lng = 4;}
if (thisone == 'BF') { lat = 13;lng = -2;}
if (thisone == 'BG') { lat = 43;lng = 25;}
if (thisone == 'BH') { lat = 26;lng = 50.55;}
if (thisone == 'BI') { lat = -3.5;lng = 30;}
if (thisone == 'BJ') { lat = 9.5;lng = 2.25;}
if (thisone == 'BM') { lat = 32.3333;lng = -64.75;}
if (thisone == 'BN') { lat = 4.5;lng = 114.6667;}
if (thisone == 'BO') { lat = -17;lng = -65;}
if (thisone == 'BR') { lat = -10;lng = -55;}
if (thisone == 'BS') { lat = 24.25;lng = -76;}
if (thisone == 'BT') { lat = 27.5;lng = 90.5;}
if (thisone == 'BV') { lat = -54.4333;lng = 3.4;}
if (thisone == 'BW') { lat = -22;lng = 24;}
if (thisone == 'BY') { lat = 53;lng = 28;}
if (thisone == 'BZ') { lat = 17.25;lng = -88.75;}
if (thisone == 'CA') { lat = 60;lng = -95;}
if (thisone == 'CC') { lat = -12.5;lng = 96.8333;}
if (thisone == 'CD') { lat = 0;lng = 25;}
if (thisone == 'CF') { lat = 7;lng = 21;}
if (thisone == 'CG') { lat = -1;lng = 15;}
if (thisone == 'CH') { lat = 47;lng = 8;}
if (thisone == 'CI') { lat = 8;lng = -5;}
if (thisone == 'CK') { lat = -21.2333;lng = -159.7667;}
if (thisone == 'CL') { lat = -30;lng = -71;}
if (thisone == 'CM') { lat = 6;lng = 12;}
if (thisone == 'CN') { lat = 35;lng = 105;}
if (thisone == 'CO') { lat = 4;lng = -72;}
if (thisone == 'CR') { lat = 10;lng = -84;}
if (thisone == 'CU') { lat = 21.5;lng = -80;}
if (thisone == 'CV') { lat = 16;lng = -24;}
if (thisone == 'CX') { lat = -10.5;lng = 105.6667;}
if (thisone == 'CY') { lat = 35;lng = 33;}
if (thisone == 'CZ') { lat = 49.75;lng = 15.5;}
if (thisone == 'DE') { lat = 51;lng = 9;}
if (thisone == 'DJ') { lat = 11.5;lng = 43;}
if (thisone == 'DK') { lat = 56;lng = 10;}
if (thisone == 'DM') { lat = 15.4167;lng = -61.3333;}
if (thisone == 'DO') { lat = 19;lng = -70.6667;}
if (thisone == 'DZ') { lat = 28;lng = 3;}
if (thisone == 'EC') { lat = -2;lng = -77.5;}
if (thisone == 'EE') { lat = 59;lng = 26;}
if (thisone == 'EG') { lat = 27;lng = 30;}
if (thisone == 'EH') { lat = 24.5;lng = -13;}
if (thisone == 'ER') { lat = 15;lng = 39;}
if (thisone == 'ES') { lat = 40;lng = -4;}
if (thisone == 'ET') { lat = 8;lng = 38;}
if (thisone == 'EU') { lat = 47;lng = 8;}
if (thisone == 'FI') { lat = 64;lng = 26;}
if (thisone == 'FJ') { lat = -18;lng = 175;}
if (thisone == 'FK') { lat = -51.75;lng = -59;}
if (thisone == 'FM') { lat = 6.9167;lng = 158.25;}
if (thisone == 'FO') { lat = 62;lng = -7;}
if (thisone == 'FR') { lat = 46;lng = 2;}
if (thisone == 'GA') { lat = -1;lng = 11.75;}
if (thisone == 'GB') { lat = 54;lng = -2;}
if (thisone == 'GD') { lat = 12.1167;lng = -61.6667;}
if (thisone == 'GE') { lat = 42;lng = 43.5;}
if (thisone == 'GF') { lat = 4;lng = -53;}
if (thisone == 'GH') { lat = 8;lng = -2;}
if (thisone == 'GI') { lat = 36.1833;lng = -5.3667;}
if (thisone == 'GL') { lat = 72;lng = -40;}
if (thisone == 'GM') { lat = 13.4667;lng = -16.5667;}
if (thisone == 'GN') { lat = 11;lng = -10;}
if (thisone == 'GP') { lat = 16.25;lng = -61.5833;}
if (thisone == 'GQ') { lat = 2;lng = 10;}
if (thisone == 'GR') { lat = 39;lng = 22;}
if (thisone == 'GS') { lat = -54.5;lng = -37;}
if (thisone == 'GT') { lat = 15.5;lng = -90.25;}
if (thisone == 'GU') { lat = 13.4667;lng = 144.7833;}
if (thisone == 'GW') { lat = 12;lng = -15;}
if (thisone == 'GY') { lat = 5;lng = -59;}
if (thisone == 'HK') { lat = 22.25;lng = 114.1667;}
if (thisone == 'HM') { lat = -53.1;lng = 72.5167;}
if (thisone == 'HN') { lat = 15;lng = -86.5;}
if (thisone == 'HR') { lat = 45.1667;lng = 15.5;}
if (thisone == 'HT') { lat = 19;lng = -72.4167;}
if (thisone == 'HU') { lat = 47;lng = 20;}
if (thisone == 'ID') { lat = -5;lng = 120;}
if (thisone == 'IE') { lat = 53;lng = -8;}
if (thisone == 'IL') { lat = 31.5;lng = 34.75;}
if (thisone == 'IN') { lat = 20;lng = 77;}
if (thisone == 'IO') { lat = -6;lng = 71.5;}
if (thisone == 'IQ') { lat = 33;lng = 44;}
if (thisone == 'IR') { lat = 32;lng = 53;}
if (thisone == 'IS') { lat = 65;lng = -18;}
if (thisone == 'IT') { lat = 42.8333;lng = 12.8333;}
if (thisone == 'JM') { lat = 18.25;lng = -77.5;}
if (thisone == 'JO') { lat = 31;lng = 36;}
if (thisone == 'JP') { lat = 36;lng = 138;}
if (thisone == 'KE') { lat = 1;lng = 38;}
if (thisone == 'KG') { lat = 41;lng = 75;}
if (thisone == 'KH') { lat = 13;lng = 105;}
if (thisone == 'KI') { lat = 1.4167;lng = 173;}
if (thisone == 'KM') { lat = -12.1667;lng = 44.25;}
if (thisone == 'KN') { lat = 17.3333;lng = -62.75;}
if (thisone == 'KP') { lat = 40;lng = 127;}
if (thisone == 'KR') { lat = 37;lng = 127.5;}
if (thisone == 'KW') { lat = 29.3375;lng = 47.6581;}
if (thisone == 'KY') { lat = 19.5;lng = -80.5;}
if (thisone == 'KZ') { lat = 48;lng = 68;}
if (thisone == 'LA') { lat = 18;lng = 105;}
if (thisone == 'LB') { lat = 33.8333;lng = 35.8333;}
if (thisone == 'LC') { lat = 13.8833;lng = -61.1333;}
if (thisone == 'LI') { lat = 47.1667;lng = 9.5333;}
if (thisone == 'LK') { lat = 7;lng = 81;}
if (thisone == 'LR') { lat = 6.5;lng = -9.5;}
if (thisone == 'LS') { lat = -29.5;lng = 28.5;}
if (thisone == 'LT') { lat = 56;lng = 24;}
if (thisone == 'LU') { lat = 49.75;lng = 6.1667;}
if (thisone == 'LV') { lat = 57;lng = 25;}
if (thisone == 'LY') { lat = 25;lng = 17;}
if (thisone == 'MA') { lat = 32;lng = -5;}
if (thisone == 'MC') { lat = 43.7333;lng = 7.4;}
if (thisone == 'MD') { lat = 47;lng = 29;}
if (thisone == 'ME') { lat = 42;lng = 19;}
if (thisone == 'MG') { lat = -20;lng = 47;}
if (thisone == 'MH') { lat = 9;lng = 168;}
if (thisone == 'MK') { lat = 41.8333;lng = 22;}
if (thisone == 'ML') { lat = 17;lng = -4;}
if (thisone == 'MM') { lat = 22;lng = 98;}
if (thisone == 'MN') { lat = 46;lng = 105;}
if (thisone == 'MO') { lat = 22.1667;lng = 113.55;}
if (thisone == 'MP') { lat = 15.2;lng = 145.75;}
if (thisone == 'MQ') { lat = 14.6667;lng = -61;}
if (thisone == 'MR') { lat = 20;lng = -12;}
if (thisone == 'MS') { lat = 16.75;lng = -62.2;}
if (thisone == 'MT') { lat = 35.8333;lng = 14.5833;}
if (thisone == 'MU') { lat = -20.2833;lng = 57.55;}
if (thisone == 'MV') { lat = 3.25;lng = 73;}
if (thisone == 'MW') { lat = -13.5;lng = 34;}
if (thisone == 'MX') { lat = 23;lng = -102;}
if (thisone == 'MY') { lat = 2.5;lng = 112.5;}
if (thisone == 'MZ') { lat = -18.25;lng = 35;}
if (thisone == 'NA') { lat = -22;lng = 17;}
if (thisone == 'NC') { lat = -21.5;lng = 165.5;}
if (thisone == 'NE') { lat = 16;lng = 8;}
if (thisone == 'NF') { lat = -29.0333;lng = 167.95;}
if (thisone == 'NG') { lat = 10;lng = 8;}
if (thisone == 'NI') { lat = 13;lng = -85;}
if (thisone == 'NL') { lat = 52.5;lng = 5.75;}
if (thisone == 'NO') { lat = 62;lng = 10;}
if (thisone == 'NP') { lat = 28;lng = 84;}
if (thisone == 'NR') { lat = -0.5333;lng = 166.9167;}
if (thisone == 'NU') { lat = -19.0333;lng = -169.8667;}
if (thisone == 'NZ') { lat = -41;lng = 174;}
if (thisone == 'OM') { lat = 21;lng = 57;}
if (thisone == 'PA') { lat = 9;lng = -80;}
if (thisone == 'PE') { lat = -10;lng = -76;}
if (thisone == 'PF') { lat = -15;lng = -140;}
if (thisone == 'PG') { lat = -6;lng = 147;}
if (thisone == 'PH') { lat = 13;lng = 122;}
if (thisone == 'PK') { lat = 30;lng = 70;}
if (thisone == 'PL') { lat = 52;lng = 20;}
if (thisone == 'PM') { lat = 46.8333;lng = -56.3333;}
if (thisone == 'PR') { lat = 18.25;lng = -66.5;}
if (thisone == 'PS') { lat = 32;lng = 35.25;}
if (thisone == 'PT') { lat = 39.5;lng = -8;}
if (thisone == 'PW') { lat = 7.5;lng = 134.5;}
if (thisone == 'PY') { lat = -23;lng = -58;}
if (thisone == 'QA') { lat = 25.5;lng = 51.25;}
if (thisone == 'RE') { lat = -21.1;lng = 55.6;}
if (thisone == 'RO') { lat = 46;lng = 25;}
if (thisone == 'RS') { lat = 44;lng = 21;}
if (thisone == 'RU') { lat = 60;lng = 100;}
if (thisone == 'RW') { lat = -2;lng = 30;}
if (thisone == 'SA') { lat = 25;lng = 45;}
if (thisone == 'SB') { lat = -8;lng = 159;}
if (thisone == 'SC') { lat = -4.5833;lng = 55.6667;}
if (thisone == 'SD') { lat = 15;lng = 30;}
if (thisone == 'SE') { lat = 62;lng = 15;}
if (thisone == 'SG') { lat = 1.3667;lng = 103.8;}
if (thisone == 'SH') { lat = -15.9333;lng = -5.7;}
if (thisone == 'SI') { lat = 46;lng = 15;}
if (thisone == 'SJ') { lat = 78;lng = 20;}
if (thisone == 'SK') { lat = 48.6667;lng = 19.5;}
if (thisone == 'SL') { lat = 8.5;lng = -11.5;}
if (thisone == 'SM') { lat = 43.7667;lng = 12.4167;}
if (thisone == 'SN') { lat = 14;lng = -14;}
if (thisone == 'SO') { lat = 10;lng = 49;}
if (thisone == 'SR') { lat = 4;lng = -56;}
if (thisone == 'ST') { lat = 1;lng = 7;}
if (thisone == 'SV') { lat = 13.8333;lng = -88.9167;}
if (thisone == 'SY') { lat = 35;lng = 38;}
if (thisone == 'SZ') { lat = -26.5;lng = 31.5;}
if (thisone == 'TC') { lat = 21.75;lng = -71.5833;}
if (thisone == 'TD') { lat = 15;lng = 19;}
if (thisone == 'TF') { lat = -43;lng = 67;}
if (thisone == 'TG') { lat = 8;lng = 1.1667;}
if (thisone == 'TH') { lat = 15;lng = 100;}
if (thisone == 'TJ') { lat = 39;lng = 71;}
if (thisone == 'TK') { lat = -9;lng = -172;}
if (thisone == 'TM') { lat = 40;lng = 60;}
if (thisone == 'TN') { lat = 34;lng = 9;}
if (thisone == 'TO') { lat = -20;lng = -175;}
if (thisone == 'TR') { lat = 39;lng = 35;}
if (thisone == 'TT') { lat = 11;lng = -61;}
if (thisone == 'TV') { lat = -8;lng = 178;}
if (thisone == 'TW') { lat = 23.5;lng = 121;}
if (thisone == 'TZ') { lat = -6;lng = 35;}
if (thisone == 'UA') { lat = 49;lng = 32;}
if (thisone == 'UG') { lat = 1;lng = 32;}
if (thisone == 'UM') { lat = 19.2833;lng = 166.6;}
if (thisone == 'US') { lat = 38;lng = -97;}
if (thisone == 'UY') { lat = -33;lng = -56;}
if (thisone == 'UZ') { lat = 41;lng = 64;}
if (thisone == 'VA') { lat = 41.9;lng = 12.45;}
if (thisone == 'VC') { lat = 13.25;lng = -61.2;}
if (thisone == 'VE') { lat = 8;lng = -66;}
if (thisone == 'VG') { lat = 18.5;lng = -64.5;}
if (thisone == 'VI') { lat = 18.3333;lng = -64.8333;}
if (thisone == 'VN') { lat = 16;lng = 106;}
if (thisone == 'VU') { lat = -16;lng = 167;}
if (thisone == 'WF') { lat = -13.3;lng = -176.2;}
if (thisone == 'WS') { lat = -13.5833;lng = -172.3333;}
if (thisone == 'YE') { lat = 15;lng = 48;}
if (thisone == 'YT') { lat = -12.8333;lng = 45.1667;}
if (thisone == 'ZA') { lat = -29;lng = 24;}
if (thisone == 'ZM') { lat = -15;lng = 30;}
if (thisone == 'ZW') { lat = -20;lng = 30;}
        
	if (lat != 0 && lng != 0) {
	map.setCenter(new GLatLng(lat,lng),1);
	   var point = new GLatLng(lat,lng);
	   markerOptions = { title:thisone };
	   var marker = new GMarker(point, markerOptions);
	   map.addOverlay(marker);
	}	
       }
     }
    }
    //]]>
    </script>
  </head>
      """);
     countries = db.GqlQuery("SELECT * from Country where weeks = :1", weeks)
     pcount = ""
     pcol = ""
     for country in countries:
#        self.response.out.write('<br>%s' % country.ccode )
#        self.response.out.write("@" + str(time.time()))
#        self.response.out.write(" = " + str(country.weeks))
#        self.response.out.write('%s' % country.a )
        pcount = pcount + country.ccode
        pcol = pcol+"A"

     self.response.out.write('<body onload="load(\'' + pcount +'\')" onunload="GUnload()">')
     self.response.out.write('<table><tr><td><div id="map" style="width: 600px; height: 400px"></div></td>')
     if len(brief) == 0:
	     self.response.out.write('<td valign="top"><img src="http://chart.apis.google.com/chart?cht=t&chs=440x220&chd=s:' + pcol+ '&chtm=world&chld=' + pcount+'&chco=ffffff,4df0d4,43390a&chf=bg,s,EAF7FE"/></td>')
     
     self.response.out.write('</tr></table>')
     if len(brief) == 0:
	 self.response.out.write('<a href="/">Home</a>')
      
     self.response.out.write("</body></html>")
      
class odata(webapp.RequestHandler):
  def get(self):
     self.response.write(self.request.path_qs)


class Launchpad(webapp.RequestHandler):
  def get(self):
     self.response.out.write("""
<form>
<h2>Launchpad for instructors</h2>
Enter your instructor hostname and select the type of system to be accessed.
<br>
Hostname:
<input id="t" class="box300" type="text" value="twdfxxxx"/><br>
<button onclick="window.open('http://'+document.getElementById('t').value+'.wdf.sap.corp:50000/irj');">SAP NetWeaver Portal (P7T)</button>
<button onclick="window.open('http://'+document.getElementById('t').value+'.wdf.sap.corp:50000/PoCoThreeCERun');">SAP NetWeaver CE 7.1 (CEM)</button>
<button onclick="window.open('http://'+document.getElementById('t').value+'.wdf.sap.corp:52000/webdynpro/dispatcher/local/SysCoToo/SystemSetup');">SAP NetWeaver Development Infrastructure (NDI)</button>
<br>
<button onclick="window.open('http://'+document.getElementById('t').value+'.wdf.sap.corp:50000/webdynpro/dispatcher/sap.com/grc~ccappcomp/ComplianceCalibrator');">Virsa Compliance Calibrator</button>

<endform>
     <br><a href="/">Home</a>

      """);

class Showtime(webapp.RequestHandler):
  def get(self):
    now = datetime.now()
    nowdst = 0
    tz = self.request.get('timezone').strip()
    tzu = tz.upper()
    format = "%a %d %b %Y %H:%M:%S"
    ok = True 
    if len(tzu) == 0:
     now = datetime.now()
#
#
    elif tzu == 'ACT':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'ACT'
     longname = "Central Standard Time (Northern Territory)"
    elif tzu == 'AET':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'AET'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AGT':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'AGT'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'ART':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'ART'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'AST':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'AST'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'AFRICA/ABIDJAN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Abidjan'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/ACCRA':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Accra'
     longname = "Ghana Mean Time"
    elif tzu == 'AFRICA/ADDIS_ABABA':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Addis_Ababa'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/ALGIERS':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Algiers'
     longname = "Central European Time"
    elif tzu == 'AFRICA/ASMARA':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Asmara'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/ASMERA':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Asmera'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/BAMAKO':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Bamako'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/BANGUI':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Bangui'
     longname = "Western African Time"
    elif tzu == 'AFRICA/BANJUL':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Banjul'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/BISSAU':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Bissau'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/BLANTYRE':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Blantyre'
     longname = "Central African Time"
    elif tzu == 'AFRICA/BRAZZAVILLE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Brazzaville'
     longname = "Western African Time"
    elif tzu == 'AFRICA/BUJUMBURA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Bujumbura'
     longname = "Central African Time"
    elif tzu == 'AFRICA/CAIRO':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Cairo'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'AFRICA/CASABLANCA':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Casablanca'
     longname = "Western European Time"
    elif tzu == 'AFRICA/CEUTA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Ceuta'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'AFRICA/CONAKRY':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Conakry'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/DAKAR':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Dakar'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/DAR_ES_SALAAM':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Dar_es_Salaam'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/DJIBOUTI':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Djibouti'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/DOUALA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Douala'
     longname = "Western African Time"
    elif tzu == 'AFRICA/EL_AAIUN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/El_Aaiun'
     longname = "Western European Time"
    elif tzu == 'AFRICA/FREETOWN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Freetown'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/GABORONE':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Gaborone'
     longname = "Central African Time"
    elif tzu == 'AFRICA/HARARE':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Harare'
     longname = "Central African Time"
    elif tzu == 'AFRICA/JOHANNESBURG':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Johannesburg'
     longname = "South Africa Standard Time"
    elif tzu == 'AFRICA/KAMPALA':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Kampala'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/KHARTOUM':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Khartoum'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/KIGALI':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Kigali'
     longname = "Central African Time"
    elif tzu == 'AFRICA/KINSHASA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Kinshasa'
     longname = "Western African Time"
    elif tzu == 'AFRICA/LAGOS':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Lagos'
     longname = "Western African Time"
    elif tzu == 'AFRICA/LIBREVILLE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Libreville'
     longname = "Western African Time"
    elif tzu == 'AFRICA/LOME':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Lome'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/LUANDA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Luanda'
     longname = "Western African Time"
    elif tzu == 'AFRICA/LUBUMBASHI':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Lubumbashi'
     longname = "Central African Time"
    elif tzu == 'AFRICA/LUSAKA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Lusaka'
     longname = "Central African Time"
    elif tzu == 'AFRICA/MALABO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Malabo'
     longname = "Western African Time"
    elif tzu == 'AFRICA/MAPUTO':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Maputo'
     longname = "Central African Time"
    elif tzu == 'AFRICA/MASERU':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Maseru'
     longname = "South Africa Standard Time"
    elif tzu == 'AFRICA/MBABANE':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Mbabane'
     longname = "South Africa Standard Time"
    elif tzu == 'AFRICA/MOGADISHU':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Mogadishu'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/MONROVIA':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Monrovia'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/NAIROBI':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Africa/Nairobi'
     longname = "Eastern African Time"
    elif tzu == 'AFRICA/NDJAMENA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Ndjamena'
     longname = "Western African Time"
    elif tzu == 'AFRICA/NIAMEY':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Niamey'
     longname = "Western African Time"
    elif tzu == 'AFRICA/NOUAKCHOTT':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Nouakchott'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/OUAGADOUGOU':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Ouagadougou'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/PORTO-NOVO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Porto-Novo'
     longname = "Western African Time"
    elif tzu == 'AFRICA/SAO_TOME':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Sao_Tome'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/TIMBUKTU':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Africa/Timbuktu'
     longname = "Greenwich Mean Time"
    elif tzu == 'AFRICA/TRIPOLI':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Africa/Tripoli'
     longname = "Eastern European Time"
    elif tzu == 'AFRICA/TUNIS':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Tunis'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'AFRICA/WINDHOEK':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Africa/Windhoek'
     longname = "Western African Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'AMERICA/ADAK':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'America/Adak'
     longname = "Hawaii-Aleutian Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -540)
    elif tzu == 'AMERICA/ANCHORAGE':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'America/Anchorage'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'AMERICA/ANGUILLA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Anguilla'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ANTIGUA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Antigua'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ARAGUAINA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Araguaina'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/ARGENTINA/BUENOS_AIRES':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Buenos_Aires'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/ARGENTINA/CATAMARCA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Catamarca'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/COMODRIVADAVIA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/ComodRivadavia'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/CORDOBA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Cordoba'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/ARGENTINA/JUJUY':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Jujuy'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/LA_RIOJA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/La_Rioja'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/MENDOZA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Mendoza'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/RIO_GALLEGOS':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Rio_Gallegos'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/SALTA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Salta'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/SAN_JUAN':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/San_Juan'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/SAN_LUIS':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/San_Luis'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARGENTINA/TUCUMAN':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Tucuman'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/ARGENTINA/USHUAIA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Argentina/Ushuaia'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/ARUBA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Aruba'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ASUNCION':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Asuncion'
     longname = "Paraguay Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/ATIKOKAN':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Atikokan'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/ATKA':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'America/Atka'
     longname = "Hawaii-Aleutian Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -540)
    elif tzu == 'AMERICA/BAHIA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Bahia'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/BARBADOS':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Barbados'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/BELEM':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Belem'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/BELIZE':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Belize'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/BLANC-SABLON':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Blanc-Sablon'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/BOA_VISTA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Boa_Vista'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/BOGOTA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Bogota'
     longname = "Colombia Time"
    elif tzu == 'AMERICA/BOISE':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Boise'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/BUENOS_AIRES':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Buenos_Aires'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/CAMBRIDGE_BAY':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Cambridge_Bay'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/CAMPO_GRANDE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Campo_Grande'
     longname = "Amazon Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/CANCUN':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Cancun'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/CARACAS':
     now = datetime.utcnow() + timedelta(minutes = -270)
     tzu = 'America/Caracas'
     longname = "Venezuela Time"
    elif tzu == 'AMERICA/CATAMARCA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Catamarca'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/CAYENNE':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Cayenne'
     longname = "French Guiana Time"
    elif tzu == 'AMERICA/CAYMAN':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Cayman'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/CHICAGO':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Chicago'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/CHIHUAHUA':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Chihuahua'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/CORAL_HARBOUR':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Coral_Harbour'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/CORDOBA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Cordoba'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/COSTA_RICA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Costa_Rica'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/CUIABA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Cuiaba'
     longname = "Amazon Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/CURACAO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Curacao'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/DANMARKSHAVN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'America/Danmarkshavn'
     longname = "Greenwich Mean Time"
    elif tzu == 'AMERICA/DAWSON':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Dawson'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/DAWSON_CREEK':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Dawson_Creek'
     longname = "Mountain Standard Time"
    elif tzu == 'AMERICA/DENVER':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Denver'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/DETROIT':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Detroit'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/DOMINICA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Dominica'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/EDMONTON':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Edmonton'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/EIRUNEPE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Eirunepe'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/EL_SALVADOR':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/El_Salvador'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/ENSENADA':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Ensenada'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/FORT_WAYNE':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Fort_Wayne'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/FORTALEZA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Fortaleza'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/GLACE_BAY':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Glace_Bay'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/GODTHAB':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Godthab'
     longname = "Western Greenland Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/GOOSE_BAY':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Goose_Bay'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/GRAND_TURK':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Grand_Turk'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/GRENADA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Grenada'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/GUADELOUPE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Guadeloupe'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/GUATEMALA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Guatemala'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/GUAYAQUIL':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Guayaquil'
     longname = "Ecuador Time"
    elif tzu == 'AMERICA/GUYANA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Guyana'
     longname = "Guyana Time"
    elif tzu == 'AMERICA/HALIFAX':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Halifax'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/HAVANA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Havana'
     longname = "Cuba Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/HERMOSILLO':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Hermosillo'
     longname = "Mountain Standard Time"
    elif tzu == 'AMERICA/INDIANA/INDIANAPOLIS':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Indianapolis'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANA/KNOX':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Indiana/Knox'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/INDIANA/MARENGO':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Marengo'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANA/PETERSBURG':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Petersburg'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANA/TELL_CITY':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Indiana/Tell_City'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/INDIANA/VEVAY':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Vevay'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANA/VINCENNES':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Vincennes'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANA/WINAMAC':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indiana/Winamac'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INDIANAPOLIS':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Indianapolis'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/INUVIK':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Inuvik'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/IQALUIT':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Iqaluit'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/JAMAICA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Jamaica'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/JUJUY':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Jujuy'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/JUNEAU':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'America/Juneau'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'AMERICA/KENTUCKY/LOUISVILLE':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Kentucky/Louisville'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/KENTUCKY/MONTICELLO':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Kentucky/Monticello'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/KNOX_IN':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Knox_IN'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/LA_PAZ':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/La_Paz'
     longname = "Bolivia Time"
    elif tzu == 'AMERICA/LIMA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Lima'
     longname = "Peru Time"
    elif tzu == 'AMERICA/LOS_ANGELES':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Los_Angeles'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/LOUISVILLE':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Louisville'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/MACEIO':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Maceio'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/MANAGUA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Managua'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/MANAUS':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Manaus'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/MARIGOT':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Marigot'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/MARTINIQUE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Martinique'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/MAZATLAN':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Mazatlan'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/MENDOZA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Mendoza'
     longname = "Argentine Time"
    elif tzu == 'AMERICA/MENOMINEE':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Menominee'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/MERIDA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Merida'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/MEXICO_CITY':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Mexico_City'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/MIQUELON':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Miquelon'
     longname = "Pierre & Miquelon Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/MONCTON':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Moncton'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/MONTERREY':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Monterrey'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/MONTEVIDEO':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Montevideo'
     longname = "Uruguay Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/MONTREAL':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Montreal'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/MONTSERRAT':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Montserrat'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/NASSAU':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Nassau'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/NEW_YORK':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/New_York'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/NIPIGON':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Nipigon'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/NOME':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'America/Nome'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'AMERICA/NORONHA':
     now = datetime.utcnow() + timedelta(minutes = -120)
     tzu = 'America/Noronha'
     longname = "Fernando de Noronha Time"
    elif tzu == 'AMERICA/NORTH_DAKOTA/CENTER':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/North_Dakota/Center'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/NORTH_DAKOTA/NEW_SALEM':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/North_Dakota/New_Salem'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/PANAMA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Panama'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/PANGNIRTUNG':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Pangnirtung'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/PARAMARIBO':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Paramaribo'
     longname = "Suriname Time"
    elif tzu == 'AMERICA/PHOENIX':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Phoenix'
     longname = "Mountain Standard Time"
    elif tzu == 'AMERICA/PORT-AU-PRINCE':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Port-au-Prince'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/PORT_OF_SPAIN':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Port_of_Spain'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/PORTO_ACRE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Porto_Acre'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/PORTO_VELHO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Porto_Velho'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/PUERTO_RICO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Puerto_Rico'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/RAINY_RIVER':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Rainy_River'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/RANKIN_INLET':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Rankin_Inlet'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/RECIFE':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Recife'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/REGINA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Regina'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/RESOLUTE':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Resolute'
     longname = "Eastern Standard Time"
    elif tzu == 'AMERICA/RIO_BRANCO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Rio_Branco'
     longname = "Amazon Time"
    elif tzu == 'AMERICA/ROSARIO':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Rosario'
     longname = "Argentine Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/SANTAREM':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Santarem'
     longname = "Brasilia Time"
    elif tzu == 'AMERICA/SANTIAGO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Santiago'
     longname = "Chile Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/SANTO_DOMINGO':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Santo_Domingo'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/SAO_PAULO':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'America/Sao_Paulo'
     longname = "Brasilia Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'AMERICA/SCORESBYSUND':
     now = datetime.utcnow() + timedelta(minutes = -60)
     tzu = 'America/Scoresbysund'
     longname = "Eastern Greenland Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 0)
    elif tzu == 'AMERICA/SHIPROCK':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Shiprock'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'AMERICA/ST_BARTHELEMY':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/St_Barthelemy'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ST_JOHNS':
     now = datetime.utcnow() + timedelta(minutes = -210)
     tzu = 'America/St_Johns'
     longname = "Newfoundland Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -150)
    elif tzu == 'AMERICA/ST_KITTS':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/St_Kitts'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ST_LUCIA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/St_Lucia'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ST_THOMAS':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/St_Thomas'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/ST_VINCENT':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/St_Vincent'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/SWIFT_CURRENT':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Swift_Current'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/TEGUCIGALPA':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Tegucigalpa'
     longname = "Central Standard Time"
    elif tzu == 'AMERICA/THULE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Thule'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AMERICA/THUNDER_BAY':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Thunder_Bay'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/TIJUANA':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Tijuana'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/TORONTO':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'America/Toronto'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'AMERICA/TORTOLA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Tortola'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/VANCOUVER':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Vancouver'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/VIRGIN':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'America/Virgin'
     longname = "Atlantic Standard Time"
    elif tzu == 'AMERICA/WHITEHORSE':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'America/Whitehorse'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'AMERICA/WINNIPEG':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'America/Winnipeg'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'AMERICA/YAKUTAT':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'America/Yakutat'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'AMERICA/YELLOWKNIFE':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'America/Yellowknife'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'ANTARCTICA/CASEY':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Antarctica/Casey'
     longname = "Western Standard Time (Australia)"
    elif tzu == 'ANTARCTICA/DAVIS':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Antarctica/Davis'
     longname = "Davis Time"
    elif tzu == 'ANTARCTICA/DUMONTDURVILLE':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Antarctica/DumontDUrville'
     longname = "Dumont-d'Urville Time"
    elif tzu == 'ANTARCTICA/MAWSON':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Antarctica/Mawson'
     longname = "Mawson Time"
    elif tzu == 'ANTARCTICA/MCMURDO':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Antarctica/McMurdo'
     longname = "New Zealand Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'ANTARCTICA/PALMER':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Antarctica/Palmer'
     longname = "Chile Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'ANTARCTICA/ROTHERA':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'Antarctica/Rothera'
     longname = "Rothera Time"
    elif tzu == 'ANTARCTICA/SOUTH_POLE':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Antarctica/South_Pole'
     longname = "New Zealand Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'ANTARCTICA/SYOWA':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Antarctica/Syowa'
     longname = "Syowa Time"
    elif tzu == 'ANTARCTICA/VOSTOK':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Antarctica/Vostok'
     longname = "Vostok Time"
    elif tzu == 'ARCTIC/LONGYEARBYEN':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Arctic/Longyearbyen'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'ASIA/ADEN':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Aden'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/ALMATY':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Almaty'
     longname = "Alma-Ata Time"
    elif tzu == 'ASIA/AMMAN':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Amman'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/ANADYR':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Asia/Anadyr'
     longname = "Anadyr Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'ASIA/AQTAU':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Aqtau'
     longname = "Aqtau Time"
    elif tzu == 'ASIA/AQTOBE':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Aqtobe'
     longname = "Aqtobe Time"
    elif tzu == 'ASIA/ASHGABAT':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Ashgabat'
     longname = "Turkmenistan Time"
    elif tzu == 'ASIA/ASHKHABAD':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Ashkhabad'
     longname = "Turkmenistan Time"
    elif tzu == 'ASIA/BAGHDAD':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Baghdad'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/BAHRAIN':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Bahrain'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/BAKU':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Asia/Baku'
     longname = "Azerbaijan Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 300)
    elif tzu == 'ASIA/BANGKOK':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Bangkok'
     longname = "Indochina Time"
    elif tzu == 'ASIA/BEIRUT':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Beirut'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/BISHKEK':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Bishkek'
     longname = "Kirgizstan Time"
    elif tzu == 'ASIA/BRUNEI':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Brunei'
     longname = "Brunei Time"
    elif tzu == 'ASIA/CALCUTTA':
     now = datetime.utcnow() + timedelta(minutes = 330)
     tzu = 'Asia/Calcutta'
     longname = "India Standard Time"
    elif tzu == 'ASIA/CHOIBALSAN':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Choibalsan'
     longname = "Choibalsan Time"
    elif tzu == 'ASIA/CHONGQING':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Chongqing'
     longname = "China Standard Time"
    elif tzu == 'ASIA/CHUNGKING':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Chungking'
     longname = "China Standard Time"
    elif tzu == 'ASIA/COLOMBO':
     now = datetime.utcnow() + timedelta(minutes = 330)
     tzu = 'Asia/Colombo'
     longname = "India Standard Time"
    elif tzu == 'ASIA/DACCA':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Dacca'
     longname = "Bangladesh Time"
    elif tzu == 'ASIA/DAMASCUS':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Damascus'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/DHAKA':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Dhaka'
     longname = "Bangladesh Time"
    elif tzu == 'ASIA/DILI':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Dili'
     longname = "Timor-Leste Time"
    elif tzu == 'ASIA/DUBAI':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Asia/Dubai'
     longname = "Gulf Standard Time"
    elif tzu == 'ASIA/DUSHANBE':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Dushanbe'
     longname = "Tajikistan Time"
    elif tzu == 'ASIA/GAZA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Gaza'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/HARBIN':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Harbin'
     longname = "China Standard Time"
    elif tzu == 'ASIA/HO_CHI_MINH':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Ho_Chi_Minh'
     longname = "Indochina Time"
    elif tzu == 'ASIA/HONG_KONG':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Hong_Kong'
     longname = "Hong Kong Time"
    elif tzu == 'ASIA/HOVD':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Hovd'
     longname = "Hovd Time"
    elif tzu == 'ASIA/IRKUTSK':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Irkutsk'
     longname = "Irkutsk Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 540)
    elif tzu == 'ASIA/ISTANBUL':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Istanbul'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/JAKARTA':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Jakarta'
     longname = "West Indonesia Time"
    elif tzu == 'ASIA/JAYAPURA':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Jayapura'
     longname = "East Indonesia Time"
    elif tzu == 'ASIA/JERUSALEM':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Jerusalem'
     longname = "Israel Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/KABUL':
     now = datetime.utcnow() + timedelta(minutes = 270)
     tzu = 'Asia/Kabul'
     longname = "Afghanistan Time"
    elif tzu == 'ASIA/KAMCHATKA':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Asia/Kamchatka'
     longname = "Petropavlovsk-Kamchatski Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'ASIA/KARACHI':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Karachi'
     longname = "Pakistan Time"
    elif tzu == 'ASIA/KASHGAR':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Kashgar'
     longname = "China Standard Time"
    elif tzu == 'ASIA/KATMANDU':
     now = datetime.utcnow() + timedelta(minutes = 345)
     tzu = 'Asia/Katmandu'
     longname = "Nepal Time"
    elif tzu == 'ASIA/KOLKATA':
     now = datetime.utcnow() + timedelta(minutes = 330)
     tzu = 'Asia/Kolkata'
     longname = "India Standard Time"
    elif tzu == 'ASIA/KRASNOYARSK':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Krasnoyarsk'
     longname = "Krasnoyarsk Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 480)
    elif tzu == 'ASIA/KUALA_LUMPUR':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Kuala_Lumpur'
     longname = "Malaysia Time"
    elif tzu == 'ASIA/KUCHING':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Kuching'
     longname = "Malaysia Time"
    elif tzu == 'ASIA/KUWAIT':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Kuwait'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/MACAO':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Macao'
     longname = "China Standard Time"
    elif tzu == 'ASIA/MACAU':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Macau'
     longname = "China Standard Time"
    elif tzu == 'ASIA/MAGADAN':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Asia/Magadan'
     longname = "Magadan Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 720)
    elif tzu == 'ASIA/MAKASSAR':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Makassar'
     longname = "Central Indonesia Time"
    elif tzu == 'ASIA/MANILA':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Manila'
     longname = "Philippines Time"
    elif tzu == 'ASIA/MUSCAT':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Asia/Muscat'
     longname = "Gulf Standard Time"
    elif tzu == 'ASIA/NICOSIA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Nicosia'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/NOVOSIBIRSK':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Novosibirsk'
     longname = "Novosibirsk Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 420)
    elif tzu == 'ASIA/OMSK':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Omsk'
     longname = "Omsk Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 420)
    elif tzu == 'ASIA/ORAL':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Oral'
     longname = "Oral Time"
    elif tzu == 'ASIA/PHNOM_PENH':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Phnom_Penh'
     longname = "Indochina Time"
    elif tzu == 'ASIA/PONTIANAK':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Pontianak'
     longname = "West Indonesia Time"
    elif tzu == 'ASIA/PYONGYANG':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Pyongyang'
     longname = "Korea Standard Time"
    elif tzu == 'ASIA/QATAR':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Qatar'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/QYZYLORDA':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Qyzylorda'
     longname = "Qyzylorda Time"
    elif tzu == 'ASIA/RANGOON':
     now = datetime.utcnow() + timedelta(minutes = 390)
     tzu = 'Asia/Rangoon'
     longname = "Myanmar Time"
    elif tzu == 'ASIA/RIYADH':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Asia/Riyadh'
     longname = "Arabia Standard Time"
    elif tzu == 'ASIA/RIYADH87':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Asia/Riyadh87'
     longname = "GMT+03:07"
    elif tzu == 'ASIA/RIYADH88':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Asia/Riyadh88'
     longname = "GMT+03:07"
    elif tzu == 'ASIA/RIYADH89':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Asia/Riyadh89'
     longname = "GMT+03:07"
    elif tzu == 'ASIA/SAIGON':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Saigon'
     longname = "Indochina Time"
    elif tzu == 'ASIA/SAKHALIN':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Asia/Sakhalin'
     longname = "Sakhalin Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'ASIA/SAMARKAND':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Samarkand'
     longname = "Uzbekistan Time"
    elif tzu == 'ASIA/SEOUL':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Seoul'
     longname = "Korea Standard Time"
    elif tzu == 'ASIA/SHANGHAI':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Shanghai'
     longname = "China Standard Time"
    elif tzu == 'ASIA/SINGAPORE':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Singapore'
     longname = "Singapore Time"
    elif tzu == 'ASIA/TAIPEI':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Taipei'
     longname = "China Standard Time"
    elif tzu == 'ASIA/TASHKENT':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Tashkent'
     longname = "Uzbekistan Time"
    elif tzu == 'ASIA/TBILISI':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Asia/Tbilisi'
     longname = "Georgia Time"
    elif tzu == 'ASIA/TEHRAN':
     now = datetime.utcnow() + timedelta(minutes = 210)
     tzu = 'Asia/Tehran'
     longname = "Iran Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 270)
    elif tzu == 'ASIA/TEL_AVIV':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Asia/Tel_Aviv'
     longname = "Israel Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'ASIA/THIMBU':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Thimbu'
     longname = "Bhutan Time"
    elif tzu == 'ASIA/THIMPHU':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Asia/Thimphu'
     longname = "Bhutan Time"
    elif tzu == 'ASIA/TOKYO':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Tokyo'
     longname = "Japan Standard Time"
    elif tzu == 'ASIA/UJUNG_PANDANG':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Ujung_Pandang'
     longname = "Central Indonesia Time"
    elif tzu == 'ASIA/ULAANBAATAR':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Ulaanbaatar'
     longname = "Ulaanbaatar Time"
    elif tzu == 'ASIA/ULAN_BATOR':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Ulan_Bator'
     longname = "Ulaanbaatar Time"
    elif tzu == 'ASIA/URUMQI':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Asia/Urumqi'
     longname = "China Standard Time"
    elif tzu == 'ASIA/VIENTIANE':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Asia/Vientiane'
     longname = "Indochina Time"
    elif tzu == 'ASIA/VLADIVOSTOK':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Asia/Vladivostok'
     longname = "Vladivostok Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'ASIA/YAKUTSK':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Asia/Yakutsk'
     longname = "Yakutsk Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 600)
    elif tzu == 'ASIA/YEKATERINBURG':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Asia/Yekaterinburg'
     longname = "Yekaterinburg Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 360)
    elif tzu == 'ASIA/YEREVAN':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Asia/Yerevan'
     longname = "Armenia Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 300)
    elif tzu == 'ATLANTIC/AZORES':
     now = datetime.utcnow() + timedelta(minutes = -60)
     tzu = 'Atlantic/Azores'
     longname = "Azores Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 0)
    elif tzu == 'ATLANTIC/BERMUDA':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Atlantic/Bermuda'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'ATLANTIC/CANARY':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/Canary'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ATLANTIC/CAPE_VERDE':
     now = datetime.utcnow() + timedelta(minutes = -60)
     tzu = 'Atlantic/Cape_Verde'
     longname = "Cape Verde Time"
    elif tzu == 'ATLANTIC/FAEROE':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/Faeroe'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ATLANTIC/FAROE':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/Faroe'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ATLANTIC/JAN_MAYEN':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Atlantic/Jan_Mayen'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'ATLANTIC/MADEIRA':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/Madeira'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ATLANTIC/REYKJAVIK':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/Reykjavik'
     longname = "Greenwich Mean Time"
    elif tzu == 'ATLANTIC/SOUTH_GEORGIA':
     now = datetime.utcnow() + timedelta(minutes = -120)
     tzu = 'Atlantic/South_Georgia'
     longname = "South Georgia Standard Time"
    elif tzu == 'ATLANTIC/ST_HELENA':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Atlantic/St_Helena'
     longname = "Greenwich Mean Time"
    elif tzu == 'ATLANTIC/STANLEY':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Atlantic/Stanley'
     longname = "Falkland Is. Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'AUSTRALIA/ACT':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/ACT'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/ADELAIDE':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/Adelaide'
     longname = "Central Standard Time (South Australia)"
     nowdst = datetime.utcnow() + timedelta(minutes = 630)
    elif tzu == 'AUSTRALIA/BRISBANE':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Brisbane'
     longname = "Eastern Standard Time (Queensland)"
    elif tzu == 'AUSTRALIA/BROKEN_HILL':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/Broken_Hill'
     longname = "Central Standard Time (South Australia/New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 630)
    elif tzu == 'AUSTRALIA/CANBERRA':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Canberra'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/CURRIE':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Currie'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/DARWIN':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/Darwin'
     longname = "Central Standard Time (Northern Territory)"
    elif tzu == 'AUSTRALIA/EUCLA':
     now = datetime.utcnow() + timedelta(minutes = 525)
     tzu = 'Australia/Eucla'
     longname = "Central Western Standard Time (Australia)"
    elif tzu == 'AUSTRALIA/HOBART':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Hobart'
     longname = "Eastern Standard Time (Tasmania)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/LHI':
     now = datetime.utcnow() + timedelta(minutes = 630)
     tzu = 'Australia/LHI'
     longname = "Lord Howe Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/LINDEMAN':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Lindeman'
     longname = "Eastern Standard Time (Queensland)"
    elif tzu == 'AUSTRALIA/LORD_HOWE':
     now = datetime.utcnow() + timedelta(minutes = 630)
     tzu = 'Australia/Lord_Howe'
     longname = "Lord Howe Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/MELBOURNE':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Melbourne'
     longname = "Eastern Standard Time (Victoria)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/NSW':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/NSW'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/NORTH':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/North'
     longname = "Central Standard Time (Northern Territory)"
    elif tzu == 'AUSTRALIA/PERTH':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Australia/Perth'
     longname = "Western Standard Time (Australia)"
    elif tzu == 'AUSTRALIA/QUEENSLAND':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Queensland'
     longname = "Eastern Standard Time (Queensland)"
    elif tzu == 'AUSTRALIA/SOUTH':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/South'
     longname = "Central Standard Time (South Australia)"
     nowdst = datetime.utcnow() + timedelta(minutes = 630)
    elif tzu == 'AUSTRALIA/SYDNEY':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Sydney'
     longname = "Eastern Standard Time (New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/TASMANIA':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Tasmania'
     longname = "Eastern Standard Time (Tasmania)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/VICTORIA':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Australia/Victoria'
     longname = "Eastern Standard Time (Victoria)"
     nowdst = datetime.utcnow() + timedelta(minutes = 660)
    elif tzu == 'AUSTRALIA/WEST':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Australia/West'
     longname = "Western Standard Time (Australia)"
    elif tzu == 'AUSTRALIA/YANCOWINNA':
     now = datetime.utcnow() + timedelta(minutes = 570)
     tzu = 'Australia/Yancowinna'
     longname = "Central Standard Time (South Australia/New South Wales)"
     nowdst = datetime.utcnow() + timedelta(minutes = 630)
    elif tzu == 'BET':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'BET'
     longname = "Brasilia Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'BST':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'BST'
     longname = "Bangladesh Time"
    elif tzu == 'BRAZIL/ACRE':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Brazil/Acre'
     longname = "Amazon Time"
    elif tzu == 'BRAZIL/DENORONHA':
     now = datetime.utcnow() + timedelta(minutes = -120)
     tzu = 'Brazil/DeNoronha'
     longname = "Fernando de Noronha Time"
    elif tzu == 'BRAZIL/EAST':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'Brazil/East'
     longname = "Brasilia Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -120)
    elif tzu == 'BRAZIL/WEST':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Brazil/West'
     longname = "Amazon Time"
    elif tzu == 'CAT':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'CAT'
     longname = "Central African Time"
    elif tzu == 'CET':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'CET'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'CNT':
     now = datetime.utcnow() + timedelta(minutes = -210)
     tzu = 'CNT'
     longname = "Newfoundland Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -150)
    elif tzu == 'CST':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'CST'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'CST6CDT':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'CST6CDT'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'CTT':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'CTT'
     longname = "China Standard Time"
    elif tzu == 'CANADA/ATLANTIC':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Canada/Atlantic'
     longname = "Atlantic Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'CANADA/CENTRAL':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Canada/Central'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'CANADA/EAST-SASKATCHEWAN':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Canada/East-Saskatchewan'
     longname = "Central Standard Time"
    elif tzu == 'CANADA/EASTERN':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'Canada/Eastern'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'CANADA/MOUNTAIN':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'Canada/Mountain'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'CANADA/NEWFOUNDLAND':
     now = datetime.utcnow() + timedelta(minutes = -210)
     tzu = 'Canada/Newfoundland'
     longname = "Newfoundland Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -150)
    elif tzu == 'CANADA/PACIFIC':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'Canada/Pacific'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'CANADA/SASKATCHEWAN':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Canada/Saskatchewan'
     longname = "Central Standard Time"
    elif tzu == 'CANADA/YUKON':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'Canada/Yukon'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'CHILE/CONTINENTAL':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Chile/Continental'
     longname = "Chile Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -180)
    elif tzu == 'CHILE/EASTERISLAND':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Chile/EasterIsland'
     longname = "Easter Is. Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'CUBA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'Cuba'
     longname = "Cuba Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'EAT':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'EAT'
     longname = "Eastern African Time"
    elif tzu == 'ECT':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'ECT'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EET':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'EET'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EST':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'EST'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'EST5EDT':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'EST5EDT'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'EGYPT':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Egypt'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EIRE':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Eire'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ETC/GMT':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/GMT'
     longname = "GMT+00:00"
    elif tzu == 'ETC/GMT+0':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/GMT+0'
     longname = "GMT+00:00"
    elif tzu == 'ETC/GMT+1':
     now = datetime.utcnow() + timedelta(minutes = -60)
     tzu = 'Etc/GMT+1'
     longname = "GMT-01:00"
    elif tzu == 'ETC/GMT+10':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Etc/GMT+10'
     longname = "GMT-10:00"
    elif tzu == 'ETC/GMT+11':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Etc/GMT+11'
     longname = "GMT-11:00"
    elif tzu == 'ETC/GMT+12':
     now = datetime.utcnow() + timedelta(minutes = -720)
     tzu = 'Etc/GMT+12'
     longname = "GMT-12:00"
    elif tzu == 'ETC/GMT+2':
     now = datetime.utcnow() + timedelta(minutes = -120)
     tzu = 'Etc/GMT+2'
     longname = "GMT-02:00"
    elif tzu == 'ETC/GMT+3':
     now = datetime.utcnow() + timedelta(minutes = -180)
     tzu = 'Etc/GMT+3'
     longname = "GMT-03:00"
    elif tzu == 'ETC/GMT+4':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'Etc/GMT+4'
     longname = "GMT-04:00"
    elif tzu == 'ETC/GMT+5':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'Etc/GMT+5'
     longname = "GMT-05:00"
    elif tzu == 'ETC/GMT+6':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Etc/GMT+6'
     longname = "GMT-06:00"
    elif tzu == 'ETC/GMT+7':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'Etc/GMT+7'
     longname = "GMT-07:00"
    elif tzu == 'ETC/GMT+8':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'Etc/GMT+8'
     longname = "GMT-08:00"
    elif tzu == 'ETC/GMT+9':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'Etc/GMT+9'
     longname = "GMT-09:00"
    elif tzu == 'ETC/GMT-0':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/GMT-0'
     longname = "GMT+00:00"
    elif tzu == 'ETC/GMT-1':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Etc/GMT-1'
     longname = "GMT+01:00"
    elif tzu == 'ETC/GMT-10':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Etc/GMT-10'
     longname = "GMT+10:00"
    elif tzu == 'ETC/GMT-11':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Etc/GMT-11'
     longname = "GMT+11:00"
    elif tzu == 'ETC/GMT-12':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Etc/GMT-12'
     longname = "GMT+12:00"
    elif tzu == 'ETC/GMT-13':
     now = datetime.utcnow() + timedelta(minutes = 780)
     tzu = 'Etc/GMT-13'
     longname = "GMT+13:00"
    elif tzu == 'ETC/GMT-14':
     now = datetime.utcnow() + timedelta(minutes = 840)
     tzu = 'Etc/GMT-14'
     longname = "GMT+14:00"
    elif tzu == 'ETC/GMT-2':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Etc/GMT-2'
     longname = "GMT+02:00"
    elif tzu == 'ETC/GMT-3':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Etc/GMT-3'
     longname = "GMT+03:00"
    elif tzu == 'ETC/GMT-4':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Etc/GMT-4'
     longname = "GMT+04:00"
    elif tzu == 'ETC/GMT-5':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Etc/GMT-5'
     longname = "GMT+05:00"
    elif tzu == 'ETC/GMT-6':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Etc/GMT-6'
     longname = "GMT+06:00"
    elif tzu == 'ETC/GMT-7':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Etc/GMT-7'
     longname = "GMT+07:00"
    elif tzu == 'ETC/GMT-8':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Etc/GMT-8'
     longname = "GMT+08:00"
    elif tzu == 'ETC/GMT-9':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Etc/GMT-9'
     longname = "GMT+09:00"
    elif tzu == 'ETC/GMT0':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/GMT0'
     longname = "GMT+00:00"
    elif tzu == 'ETC/GREENWICH':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/Greenwich'
     longname = "Greenwich Mean Time"
    elif tzu == 'ETC/UCT':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/UCT'
     longname = "Coordinated Universal Time"
    elif tzu == 'ETC/UTC':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/UTC'
     longname = "Coordinated Universal Time"
    elif tzu == 'ETC/UNIVERSAL':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/Universal'
     longname = "Coordinated Universal Time"
    elif tzu == 'ETC/ZULU':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Etc/Zulu'
     longname = "Coordinated Universal Time"
    elif tzu == 'EUROPE/AMSTERDAM':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Amsterdam'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/ANDORRA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Andorra'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/ATHENS':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Athens'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/BELFAST':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Belfast'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/BELGRADE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Belgrade'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/BERLIN':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Berlin'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/BRATISLAVA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Bratislava'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/BRUSSELS':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Brussels'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/BUCHAREST':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Bucharest'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/BUDAPEST':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Budapest'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/CHISINAU':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Chisinau'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/COPENHAGEN':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Copenhagen'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/DUBLIN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Dublin'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/GIBRALTAR':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Gibraltar'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/GUERNSEY':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Guernsey'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/HELSINKI':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Helsinki'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/ISLE_OF_MAN':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Isle_of_Man'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/ISTANBUL':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Istanbul'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/JERSEY':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Jersey'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/KALININGRAD':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Kaliningrad'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/KIEV':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Kiev'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/LISBON':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/Lisbon'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/LJUBLJANA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Ljubljana'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/LONDON':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Europe/London'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'EUROPE/LUXEMBOURG':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Luxembourg'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/MADRID':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Madrid'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/MALTA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Malta'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/MARIEHAMN':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Mariehamn'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/MINSK':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Minsk'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/MONACO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Monaco'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/MOSCOW':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Europe/Moscow'
     longname = "Moscow Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 240)
    elif tzu == 'EUROPE/NICOSIA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Nicosia'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/OSLO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Oslo'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/PARIS':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Paris'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/PODGORICA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Podgorica'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/PRAGUE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Prague'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/RIGA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Riga'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/ROME':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Rome'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/SAMARA':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Europe/Samara'
     longname = "Samara Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 300)
    elif tzu == 'EUROPE/SAN_MARINO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/San_Marino'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/SARAJEVO':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Sarajevo'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/SIMFEROPOL':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Simferopol'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/SKOPJE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Skopje'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/SOFIA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Sofia'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/STOCKHOLM':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Stockholm'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/TALLINN':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Tallinn'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/TIRANE':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Tirane'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/TIRASPOL':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Tiraspol'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/UZHGOROD':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Uzhgorod'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/VADUZ':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Vaduz'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/VATICAN':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Vatican'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/VIENNA':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Vienna'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/VILNIUS':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Vilnius'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/VOLGOGRAD':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Europe/Volgograd'
     longname = "Volgograd Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 240)
    elif tzu == 'EUROPE/WARSAW':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Warsaw'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/ZAGREB':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Zagreb'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'EUROPE/ZAPOROZHYE':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Europe/Zaporozhye'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'EUROPE/ZURICH':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Europe/Zurich'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'GB':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'GB'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'GB-EIRE':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'GB-Eire'
     longname = "Greenwich Mean Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'GMT':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'GMT'
     longname = "Greenwich Mean Time"
    elif tzu == 'GMT0':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'GMT0'
     longname = "GMT+00:00"
    elif tzu == 'GREENWICH':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Greenwich'
     longname = "Greenwich Mean Time"
    elif tzu == 'HST':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'HST'
     longname = "Hawaii Standard Time"
    elif tzu == 'HONGKONG':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Hongkong'
     longname = "Hong Kong Time"
    elif tzu == 'IET':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'IET'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'IST':
     now = datetime.utcnow() + timedelta(minutes = 330)
     tzu = 'IST'
     longname = "India Standard Time"
    elif tzu == 'ICELAND':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Iceland'
     longname = "Greenwich Mean Time"
    elif tzu == 'INDIAN/ANTANANARIVO':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Indian/Antananarivo'
     longname = "Eastern African Time"
    elif tzu == 'INDIAN/CHAGOS':
     now = datetime.utcnow() + timedelta(minutes = 360)
     tzu = 'Indian/Chagos'
     longname = "Indian Ocean Territory Time"
    elif tzu == 'INDIAN/CHRISTMAS':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'Indian/Christmas'
     longname = "Christmas Island Time"
    elif tzu == 'INDIAN/COCOS':
     now = datetime.utcnow() + timedelta(minutes = 390)
     tzu = 'Indian/Cocos'
     longname = "Cocos Islands Time"
    elif tzu == 'INDIAN/COMORO':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Indian/Comoro'
     longname = "Eastern African Time"
    elif tzu == 'INDIAN/KERGUELEN':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Indian/Kerguelen'
     longname = "French Southern & Antarctic Lands Time"
    elif tzu == 'INDIAN/MAHE':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Indian/Mahe'
     longname = "Seychelles Time"
    elif tzu == 'INDIAN/MALDIVES':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'Indian/Maldives'
     longname = "Maldives Time"
    elif tzu == 'INDIAN/MAURITIUS':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Indian/Mauritius'
     longname = "Mauritius Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 300)
    elif tzu == 'INDIAN/MAYOTTE':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'Indian/Mayotte'
     longname = "Eastern African Time"
    elif tzu == 'INDIAN/REUNION':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'Indian/Reunion'
     longname = "Reunion Time"
    elif tzu == 'IRAN':
     now = datetime.utcnow() + timedelta(minutes = 210)
     tzu = 'Iran'
     longname = "Iran Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 270)
    elif tzu == 'ISRAEL':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Israel'
     longname = "Israel Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'JST':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'JST'
     longname = "Japan Standard Time"
    elif tzu == 'JAMAICA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'Jamaica'
     longname = "Eastern Standard Time"
    elif tzu == 'JAPAN':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Japan'
     longname = "Japan Standard Time"
    elif tzu == 'KWAJALEIN':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Kwajalein'
     longname = "Marshall Islands Time"
    elif tzu == 'LIBYA':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Libya'
     longname = "Eastern European Time"
    elif tzu == 'MET':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'MET'
     longname = "Middle Europe Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'MIT':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'MIT'
     longname = "West Samoa Time"
    elif tzu == 'MST':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'MST'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'MST7MDT':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'MST7MDT'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'MEXICO/BAJANORTE':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'Mexico/BajaNorte'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'MEXICO/BAJASUR':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'Mexico/BajaSur'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'MEXICO/GENERAL':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Mexico/General'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'MIDEAST/RIYADH87':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Mideast/Riyadh87'
     longname = "GMT+03:07"
    elif tzu == 'MIDEAST/RIYADH88':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Mideast/Riyadh88'
     longname = "GMT+03:07"
    elif tzu == 'MIDEAST/RIYADH89':
     now = datetime.utcnow() + timedelta(minutes = 187)
     tzu = 'Mideast/Riyadh89'
     longname = "GMT+03:07"
    elif tzu == 'NET':
     now = datetime.utcnow() + timedelta(minutes = 240)
     tzu = 'NET'
     longname = "Armenia Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 300)
    elif tzu == 'NST':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'NST'
     longname = "New Zealand Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'NZ':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'NZ'
     longname = "New Zealand Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'NZ-CHAT':
     now = datetime.utcnow() + timedelta(minutes = 765)
     tzu = 'NZ-CHAT'
     longname = "Chatham Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 825)
    elif tzu == 'NAVAJO':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'Navajo'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'PLT':
     now = datetime.utcnow() + timedelta(minutes = 300)
     tzu = 'PLT'
     longname = "Pakistan Time"
    elif tzu == 'PNT':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'PNT'
     longname = "Mountain Standard Time"
    elif tzu == 'PRC':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'PRC'
     longname = "China Standard Time"
    elif tzu == 'PRT':
     now = datetime.utcnow() + timedelta(minutes = -240)
     tzu = 'PRT'
     longname = "Atlantic Standard Time"
    elif tzu == 'PST':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'PST'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'PST8PDT':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'PST8PDT'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'PACIFIC/APIA':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Pacific/Apia'
     longname = "West Samoa Time"
    elif tzu == 'PACIFIC/AUCKLAND':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Auckland'
     longname = "New Zealand Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 780)
    elif tzu == 'PACIFIC/CHATHAM':
     now = datetime.utcnow() + timedelta(minutes = 765)
     tzu = 'Pacific/Chatham'
     longname = "Chatham Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 825)
    elif tzu == 'PACIFIC/EASTER':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Pacific/Easter'
     longname = "Easter Is. Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'PACIFIC/EFATE':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Pacific/Efate'
     longname = "Vanuatu Time"
    elif tzu == 'PACIFIC/ENDERBURY':
     now = datetime.utcnow() + timedelta(minutes = 780)
     tzu = 'Pacific/Enderbury'
     longname = "Phoenix Is. Time"
    elif tzu == 'PACIFIC/FAKAOFO':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Pacific/Fakaofo'
     longname = "Tokelau Time"
    elif tzu == 'PACIFIC/FIJI':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Fiji'
     longname = "Fiji Time"
    elif tzu == 'PACIFIC/FUNAFUTI':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Funafuti'
     longname = "Tuvalu Time"
    elif tzu == 'PACIFIC/GALAPAGOS':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'Pacific/Galapagos'
     longname = "Galapagos Time"
    elif tzu == 'PACIFIC/GAMBIER':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'Pacific/Gambier'
     longname = "Gambier Time"
    elif tzu == 'PACIFIC/GUADALCANAL':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Pacific/Guadalcanal'
     longname = "Solomon Is. Time"
    elif tzu == 'PACIFIC/GUAM':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Pacific/Guam'
     longname = "Chamorro Standard Time"
    elif tzu == 'PACIFIC/HONOLULU':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Pacific/Honolulu'
     longname = "Hawaii Standard Time"
    elif tzu == 'PACIFIC/JOHNSTON':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Pacific/Johnston'
     longname = "Hawaii Standard Time"
    elif tzu == 'PACIFIC/KIRITIMATI':
     now = datetime.utcnow() + timedelta(minutes = 840)
     tzu = 'Pacific/Kiritimati'
     longname = "Line Is. Time"
    elif tzu == 'PACIFIC/KOSRAE':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Pacific/Kosrae'
     longname = "Kosrae Time"
    elif tzu == 'PACIFIC/KWAJALEIN':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Kwajalein'
     longname = "Marshall Islands Time"
    elif tzu == 'PACIFIC/MAJURO':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Majuro'
     longname = "Marshall Islands Time"
    elif tzu == 'PACIFIC/MARQUESAS':
     now = datetime.utcnow() + timedelta(minutes = -570)
     tzu = 'Pacific/Marquesas'
     longname = "Marquesas Time"
    elif tzu == 'PACIFIC/MIDWAY':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Pacific/Midway'
     longname = "Samoa Standard Time"
    elif tzu == 'PACIFIC/NAURU':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Nauru'
     longname = "Nauru Time"
    elif tzu == 'PACIFIC/NIUE':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Pacific/Niue'
     longname = "Niue Time"
    elif tzu == 'PACIFIC/NORFOLK':
     now = datetime.utcnow() + timedelta(minutes = 690)
     tzu = 'Pacific/Norfolk'
     longname = "Norfolk Time"
    elif tzu == 'PACIFIC/NOUMEA':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Pacific/Noumea'
     longname = "New Caledonia Time"
    elif tzu == 'PACIFIC/PAGO_PAGO':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Pacific/Pago_Pago'
     longname = "Samoa Standard Time"
    elif tzu == 'PACIFIC/PALAU':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'Pacific/Palau'
     longname = "Palau Time"
    elif tzu == 'PACIFIC/PITCAIRN':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'Pacific/Pitcairn'
     longname = "Pitcairn Standard Time"
    elif tzu == 'PACIFIC/PONAPE':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'Pacific/Ponape'
     longname = "Ponape Time"
    elif tzu == 'PACIFIC/PORT_MORESBY':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Pacific/Port_Moresby'
     longname = "Papua New Guinea Time"
    elif tzu == 'PACIFIC/RAROTONGA':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Pacific/Rarotonga'
     longname = "Cook Is. Time"
    elif tzu == 'PACIFIC/SAIPAN':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Pacific/Saipan'
     longname = "Chamorro Standard Time"
    elif tzu == 'PACIFIC/SAMOA':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'Pacific/Samoa'
     longname = "Samoa Standard Time"
    elif tzu == 'PACIFIC/TAHITI':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'Pacific/Tahiti'
     longname = "Tahiti Time"
    elif tzu == 'PACIFIC/TARAWA':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Tarawa'
     longname = "Gilbert Is. Time"
    elif tzu == 'PACIFIC/TONGATAPU':
     now = datetime.utcnow() + timedelta(minutes = 780)
     tzu = 'Pacific/Tongatapu'
     longname = "Tonga Time"
    elif tzu == 'PACIFIC/TRUK':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Pacific/Truk'
     longname = "Truk Time"
    elif tzu == 'PACIFIC/WAKE':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Wake'
     longname = "Wake Time"
    elif tzu == 'PACIFIC/WALLIS':
     now = datetime.utcnow() + timedelta(minutes = 720)
     tzu = 'Pacific/Wallis'
     longname = "Wallis & Futuna Time"
    elif tzu == 'PACIFIC/YAP':
     now = datetime.utcnow() + timedelta(minutes = 600)
     tzu = 'Pacific/Yap'
     longname = "Truk Time"
    elif tzu == 'POLAND':
     now = datetime.utcnow() + timedelta(minutes = 60)
     tzu = 'Poland'
     longname = "Central European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 120)
    elif tzu == 'PORTUGAL':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Portugal'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ROK':
     now = datetime.utcnow() + timedelta(minutes = 540)
     tzu = 'ROK'
     longname = "Korea Standard Time"
    elif tzu == 'SST':
     now = datetime.utcnow() + timedelta(minutes = 660)
     tzu = 'SST'
     longname = "Solomon Is. Time"
    elif tzu == 'SINGAPORE':
     now = datetime.utcnow() + timedelta(minutes = 480)
     tzu = 'Singapore'
     longname = "Singapore Time"
    elif tzu == 'TURKEY':
     now = datetime.utcnow() + timedelta(minutes = 120)
     tzu = 'Turkey'
     longname = "Eastern European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 180)
    elif tzu == 'UCT':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'UCT'
     longname = "Coordinated Universal Time"
    elif tzu == 'US/ALASKA':
     now = datetime.utcnow() + timedelta(minutes = -540)
     tzu = 'US/Alaska'
     longname = "Alaska Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -480)
    elif tzu == 'US/ALEUTIAN':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'US/Aleutian'
     longname = "Hawaii-Aleutian Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -540)
    elif tzu == 'US/ARIZONA':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'US/Arizona'
     longname = "Mountain Standard Time"
    elif tzu == 'US/CENTRAL':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'US/Central'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'US/EAST-INDIANA':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'US/East-Indiana'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'US/EASTERN':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'US/Eastern'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'US/HAWAII':
     now = datetime.utcnow() + timedelta(minutes = -600)
     tzu = 'US/Hawaii'
     longname = "Hawaii Standard Time"
    elif tzu == 'US/INDIANA-STARKE':
     now = datetime.utcnow() + timedelta(minutes = -360)
     tzu = 'US/Indiana-Starke'
     longname = "Central Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -300)
    elif tzu == 'US/MICHIGAN':
     now = datetime.utcnow() + timedelta(minutes = -300)
     tzu = 'US/Michigan'
     longname = "Eastern Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -240)
    elif tzu == 'US/MOUNTAIN':
     now = datetime.utcnow() + timedelta(minutes = -420)
     tzu = 'US/Mountain'
     longname = "Mountain Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -360)
    elif tzu == 'US/PACIFIC':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'US/Pacific'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'US/PACIFIC-NEW':
     now = datetime.utcnow() + timedelta(minutes = -480)
     tzu = 'US/Pacific-New'
     longname = "Pacific Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = -420)
    elif tzu == 'US/SAMOA':
     now = datetime.utcnow() + timedelta(minutes = -660)
     tzu = 'US/Samoa'
     longname = "Samoa Standard Time"
    elif tzu == 'UTC':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'UTC'
     longname = "Coordinated Universal Time"
    elif tzu == 'UNIVERSAL':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Universal'
     longname = "Coordinated Universal Time"
    elif tzu == 'VST':
     now = datetime.utcnow() + timedelta(minutes = 420)
     tzu = 'VST'
     longname = "Indochina Time"
    elif tzu == 'W-SU':
     now = datetime.utcnow() + timedelta(minutes = 180)
     tzu = 'W-SU'
     longname = "Moscow Standard Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 240)
    elif tzu == 'WET':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'WET'
     longname = "Western European Time"
     nowdst = datetime.utcnow() + timedelta(minutes = 60)
    elif tzu == 'ZULU':
     now = datetime.utcnow() + timedelta(minutes = 0)
     tzu = 'Zulu'
     longname = "Coordinated Universal Time"
#
#
#
    else:
     self.response.out.write('Bad timezone <b>'+tz+'</b> passed. <p>A list of timezones can be found <a href="http://en.wikipedia.org/wiki/List_of_tz_database_time_zones">here in Wikipedia</a>')
     ok = False
     
    if ok == True: 
	self.response.out.write('It is currently '+ now.strftime(format))
    	if len(tzu) == 0: 
  	   self.response.out.write(' (UTC/GMT)')
 	   self.response.out.write("""
	<br>You can see the time in a particular timezone by using http://sap-netweaver-training.appspot.com/showtime?timezone=&lt;required timezone&gt;, 
	<br>for example: <a href="http://sap-netweaver-training.appspot.com/showtime?timezone=Australia/Melbourne">
http://sap-netweaver-training.appspot.com/showtime?timezone=Australia/Melbourne</a> will show the current time in Melbourne, Australia
<p>A list of timezones can be found <a href="http://en.wikipedia.org/wiki/List_of_tz_database_time_zones">here in Wikipedia</a>
""")
    	else:
           self.response.out.write(' in timezone '+tzu+' - '+longname)
	   if nowdst <> 0:
               self.response.out.write('<br>  or '+nowdst.strftime(format)+' when daylight savings is in effect')

class Capture(webapp.RequestHandler):
  def get(self):
   random.seed()
   count = random.randint(5,35)

   self.response.out.write("""
This page contains a table that can be captured using the URL iView template<p>
After capturing the table, remember to set the <b>Look and Feel</b> option to <b>Apply full portal rendering</b>.
<p>
<table  border="1">
     """)
   for i in range(1, count+1):
      self.response.out.write("""
<tr><td>
      """)
      self.response.out.write(random.choice("JYAVZNMLOUYTRERTYGAVZNMOPITY"))
      self.response.out.write(random.choice("nythasnkfuatqjhnwmdsyjansnd"))
      self.response.out.write(random.choice("oinmlkhtrewanythasnkfuatqjhnwmdsyjansnd"))
      self.response.out.write("""
</td><td>
      """)
      self.response.out.write(random.choice("123456789"))
      self.response.out.write(random.choice("123405878546789"))
      self.response.out.write(random.choice("10986523456789"))
      self.response.out.write("""
</td></tr>
      """)
   self.response.out.write("""
</table>

      """)

class Addscheduleprompt(webapp.RequestHandler):
  def get(self):
   self.response.out.write("""
<form action="/addSchedule">
<p>Details about the scheduled course</p>
<table>
<tr><td>Course: </td><td><input name="course"></td></tr>
<td>Location: </td><td><select name="location">
""")
#   newloc = ScheduleLocation(location="Adelaide")
#   newloc.put()
   locations = db.GqlQuery("SELECT * from ScheduleLocation order by location")
   for location in locations:
     self.response.out.write("option value='"+location.location+"'>"+location.location+"</option>")
   self.response.out.write("""
#  <option value="Adelaide">Adelaide</option>
#  <option value="Auckland">Auckland</option>
#  <option value="Brisbane">Brisbane</option>
#  <option value="Canberra">Canberra</option>
#  <option value="Christchurch">Christchurch</option>
#  <option value="Melbourne">Melbourne</option>
#  <option value="Perth">Perth</option>
#  <option value="Sydney">Sydney</option>
#  <option value="Virtual">Virtual</option>
#  <option value="Wellington">Wellington</option>
</select></td></tr>
<tr><td>Starting date:</td><td><input name="date"></td></tr>
<tr><td>Status:</td><td><select name="status">
  <option value="planned">Planned</option>
  <option value="confirmed">Confirmed</option>
</select></td></tr>
</table>
<br><input type="submit" value="Submit">

</form>
     """)

     
class Addprompt(webapp.RequestHandler):
  def get(self):
   self.response.out.write("""
<form action="/add">
<p>Details about your course running this week</p>
<table>
<tr><td>Event: </td><td><input name="event" value="71234567"></td></tr>
<tr><td>Country: </td><td><select name="country">
  <option value="AF">Afghanistan</option>
  <option value="AX">Åland Islands</option>
  <option value="AL">Albania</option>
  <option value="DZ">Algeria</option>
  <option value="AS">American Samoa</option>
  <option value="AD">Andorra</option>
  <option value="AO">Angola</option>
  <option value="AI">Anguilla</option>
  <option value="AQ">Antarctica</option>
  <option value="AG">Antigua and Barbuda</option>
  <option value="AR">Argentina</option>
  <option value="AM">Armenia</option>
  <option value="AW">Aruba</option>
  <option value="AU">Australia</option>
  <option value="AT">Austria</option>
  <option value="AZ">Azerbaijan</option>
  <option value="BS">Bahamas</option>
  <option value="BH">Bahrain</option>
  <option value="BD">Bangladesh</option>
  <option value="BB">Barbados</option>
  <option value="BY">Belarus</option>
  <option value="BE">Belgium</option>
  <option value="BZ">Belize</option>
  <option value="BJ">Benin</option>
  <option value="BM">Bermuda</option>
  <option value="BT">Bhutan</option>
  <option value="BO">Bolivia</option>
  <option value="BA">Bosnia and Herzegovina</option>
  <option value="BW">Botswana</option>
  <option value="BV">Bouvet Island</option>
  <option value="BR">Brazil</option>
  <option value="IO">British Indian Ocean Territory</option>
  <option value="BN">Brunei Darussalam</option>
  <option value="BG">Bulgaria</option>
  <option value="BF">Burkina Faso</option>
  <option value="BI">Burundi</option>
  <option value="KH">Cambodia</option>
  <option value="CM">Cameroon</option>
  <option value="CA">Canada</option>
  <option value="CV">Cape Verde</option>
  <option value="KY">Cayman Islands</option>
  <option value="CF">Central African Republic</option>
  <option value="TD">Chad</option>
  <option value="CL">Chile</option>
  <option value="CN">China</option>
  <option value="CX">Christmas Island</option>
  <option value="CC">Cocos (Keeling) Islands</option>
  <option value="CO">Colombia</option>
  <option value="KM">Comoros</option>
  <option value="CG">Congo</option>
  <option value="CD">Congo, The Democratic Republic of the</option>
  <option value="CK">Cook Islands</option>
  <option value="CR">Costa Rica</option>
  <option value="CI">Côte d'Ivoire</option>
  <option value="HR">Croatia</option>
  <option value="CU">Cuba</option>
  <option value="CY">Cyprus</option>
  <option value="CZ">Czech Republic</option>
  <option value="DK">Denmark</option>
  <option value="DJ">Djibouti</option>
  <option value="DM">Dominica</option>
  <option value="DO">Dominican Republic</option>
  <option value="EC">Ecuador</option>
  <option value="EG">Egypt</option>
  <option value="SV">El Salvador</option>
  <option value="GQ">Equatorial Guinea</option>
  <option value="ER">Eritrea</option>
  <option value="EE">Estonia</option>
  <option value="ET">Ethiopia</option>
  <option value="FK">Falkland Islands (Malvinas)</option>
  <option value="FO">Faroe Islands</option>
  <option value="FJ">Fiji</option>
  <option value="FI">Finland</option>
  <option value="FR">France</option>
  <option value="GF">French Guiana</option>
  <option value="PF">French Polynesia</option>
  <option value="TF">French Southern Territories</option>
  <option value="GA">Gabon</option>
  <option value="GM">Gambia</option>
  <option value="GE">Georgia</option>
  <option value="DE" selected="selected">Germany</option>
  <option value="GH">Ghana</option>
  <option value="GI">Gibraltar</option>
  <option value="GR">Greece</option>
  <option value="GL">Greenland</option>
  <option value="GD">Grenada</option>
  <option value="GP">Guadeloupe</option>
  <option value="GU">Guam</option>
  <option value="GT">Guatemala</option>
  <option value="GG">Guernsey</option>
  <option value="GN">Guinea</option>
  <option value="GW">Guinea-Bissau</option>
  <option value="GY">Guyana</option>
  <option value="HT">Haiti</option>
  <option value="HM">Heard Island and McDonald Islands</option>
  <option value="VA">Holy See (Vatican City State)</option>
  <option value="HN">Honduras</option>
  <option value="HK">Hong Kong</option>
  <option value="HU">Hungary</option>
  <option value="IS">Iceland</option>
  <option value="IN">India</option>
  <option value="ID">Indonesia</option>
  <option value="IR">Iran, Islamic Republic of</option>
  <option value="IQ">Iraq</option>
  <option value="IE">Ireland</option>
  <option value="IM">Isle of Man</option>
  <option value="IL">Israel</option>
  <option value="IT">Italy</option>
  <option value="JM">Jamaica</option>
  <option value="JP">Japan</option>
  <option value="JE">Jersey</option>
  <option value="JO">Jordan</option>
  <option value="KZ">Kazakhstan</option>
  <option value="KE">Kenya</option>
  <option value="KI">Kiribati</option>
  <option value="KP">Korea, Democratic People's Republic of</option>
  <option value="KR">Korea, Republic of</option>
  <option value="KW">Kuwait</option>
  <option value="KG">Kyrgyzstan</option>
  <option value="LA">Lao People's Democratic Republic</option>
  <option value="LV">Latvia</option>
  <option value="LB">Lebanon</option>
  <option value="LS">Lesotho</option>
  <option value="LR">Liberia</option>
  <option value="LY">Libyan Arab Jamahiriya</option>
  <option value="LI">Liechtenstein</option>
  <option value="LT">Lithuania</option>
  <option value="LU">Luxembourg</option>
  <option value="MO">Macao</option>
  <option value="MK">Macedonia, The Former Yugoslav Republic of</option>
  <option value="MG">Madagascar</option>
  <option value="MW">Malawi</option>
  <option value="MY">Malaysia</option>
  <option value="MV">Maldives</option>
  <option value="ML">Mali</option>
  <option value="MT">Malta</option>
  <option value="MH">Marshall Islands</option>
  <option value="MQ">Martinique</option>
  <option value="MR">Mauritania</option>
  <option value="MU">Mauritius</option>
  <option value="YT">Mayotte</option>
  <option value="MX">Mexico</option>
  <option value="FM">Micronesia, Federated States of</option>
  <option value="MD">Moldova</option>
  <option value="MC">Monaco</option>
  <option value="MN">Mongolia</option>
  <option value="ME">Montenegro</option>
  <option value="MS">Montserrat</option>
  <option value="MA">Morocco</option>
  <option value="MZ">Mozambique</option>
  <option value="MM">Myanmar</option>
  <option value="NA">Namibia</option>
  <option value="NR">Nauru</option>
  <option value="NP">Nepal</option>
  <option value="NL">Netherlands</option>
  <option value="AN">Netherlands Antilles</option>
  <option value="NC">New Caledonia</option>
  <option value="NZ">New Zealand</option>
  <option value="NI">Nicaragua</option>
  <option value="NE">Niger</option>
  <option value="NG">Nigeria</option>
  <option value="NU">Niue</option>
  <option value="NF">Norfolk Island</option>
  <option value="MP">Northern Mariana Islands</option>
  <option value="NO">Norway</option>
  <option value="OM">Oman</option>
  <option value="PK">Pakistan</option>
  <option value="PW">Palau</option>
  <option value="PS">Palestinian Territory, Occupied</option>
  <option value="PA">Panama</option>
  <option value="PG">Papua New Guinea</option>
  <option value="PY">Paraguay</option>
  <option value="PE">Peru</option>
  <option value="PH">Philippines</option>
  <option value="PN">Pitcairn</option>
  <option value="PL">Poland</option>
  <option value="PT">Portugal</option>
  <option value="PR">Puerto Rico</option>
  <option value="QA">Qatar</option>
  <option value="RE">Réunion</option>
  <option value="RO">Romania</option>
  <option value="RU">Russian Federation</option>
  <option value="RW">Rwanda</option>
  <option value="BL">Saint Barthélemy</option>
  <option value="SH">Saint Helena</option>
  <option value="KN">Saint Kitts and Nevis</option>
  <option value="LC">Saint Lucia</option>
  <option value="MF">Saint Martin</option>
  <option value="PM">Saint Pierre and Miquelon</option>
  <option value="VC">Saint Vincent and the Grenadines</option>
  <option value="WS">Samoa</option>
  <option value="SM">San Marino</option>
  <option value="ST">Sao Tome and Principe</option>
  <option value="SA">Saudi Arabia</option>
  <option value="SN">Senegal</option>
  <option value="RS">Serbia</option>
  <option value="SC">Seychelles</option>
  <option value="SL">Sierra Leone</option>
  <option value="SG">Singapore</option>
  <option value="SK">Slovakia</option>
  <option value="SI">Slovenia</option>
  <option value="SB">Solomon Islands</option>
  <option value="SO">Somalia</option>
  <option value="ZA">South Africa</option>
  <option value="GS">South Georgia and the South Sandwich Islands</option>
  <option value="ES">Spain</option>
  <option value="LK">Sri Lanka</option>
  <option value="SD">Sudan</option>
  <option value="SR">Suriname</option>
  <option value="SJ">Svalbard and Jan Mayen</option>
  <option value="SZ">Swaziland</option>
  <option value="SE">Sweden</option>
  <option value="CH">Switzerland</option>
  <option value="SY">Syrian Arab Republic</option>
  <option value="TW">Taiwan, Province of China</option>
  <option value="TJ">Tajikistan</option>
  <option value="TZ">Tanzania, United Republic of</option>
  <option value="TH">Thailand</option>
  <option value="TL">Timor-Leste</option>
  <option value="TG">Togo</option>
  <option value="TK">Tokelau</option>
  <option value="TO">Tonga</option>
  <option value="TT">Trinidad and Tobago</option>
  <option value="TN">Tunisia</option>
  <option value="TR">Turkey</option>
  <option value="TM">Turkmenistan</option>
  <option value="TC">Turks and Caicos Islands</option>
  <option value="TV">Tuvalu</option>
  <option value="UG">Uganda</option>
  <option value="UA">Ukraine</option>
  <option value="AE">United Arab Emirates</option>
  <option value="GB">United Kingdom</option>
  <option value="US">United States</option>
  <option value="UM">United States Minor Outlying Islands</option>
  <option value="UY">Uruguay</option>
  <option value="UZ">Uzbekistan</option>
  <option value="VU">Vanuatu</option>
  <option value="VE">Venezuela</option>
  <option value="VN">Viet Nam</option>
  <option value="VG">Virgin Islands, British</option>
  <option value="VI">Virgin Islands, U.S.</option>
  <option value="WF">Wallis and Futuna</option>
  <option value="EH">Western Sahara</option>
  <option value="YE">Yemen</option>
  <option value="ZM">Zambia</option>
  <option value="ZW">Zimbabwe</option>
</select></td></tr>
<tr><td>Location:</td><td><input name="location" value="Walldorf"></td></tr>
<tr><td>Course:</td><td><input name="course" value="ADMxxx"></td></tr>
</table>
<br><input type="submit" value="Submit">
<br><a href="/">Home</a>
</form>
     """)

class Addhana(webapp.RequestHandler):
  def get(self):
   self.response.out.write("""
<form action="/add">
<p>Details about your HANA course running this week</p>
<table>
<tr><td>Event: </td><td><input name="event" value="71234567"></td></tr>
<tr><td>Country: </td><td><select name="country">
  <option value="AF">Afghanistan</option>
  <option value="AX">Åland Islands</option>
  <option value="AL">Albania</option>
  <option value="DZ">Algeria</option>
  <option value="AS">American Samoa</option>
  <option value="AD">Andorra</option>
  <option value="AO">Angola</option>
  <option value="AI">Anguilla</option>
  <option value="AQ">Antarctica</option>
  <option value="AG">Antigua and Barbuda</option>
  <option value="AR">Argentina</option>
  <option value="AM">Armenia</option>
  <option value="AW">Aruba</option>
  <option value="AU">Australia</option>
  <option value="AT">Austria</option>
  <option value="AZ">Azerbaijan</option>
  <option value="BS">Bahamas</option>
  <option value="BH">Bahrain</option>
  <option value="BD">Bangladesh</option>
  <option value="BB">Barbados</option>
  <option value="BY">Belarus</option>
  <option value="BE">Belgium</option>
  <option value="BZ">Belize</option>
  <option value="BJ">Benin</option>
  <option value="BM">Bermuda</option>
  <option value="BT">Bhutan</option>
  <option value="BO">Bolivia</option>
  <option value="BA">Bosnia and Herzegovina</option>
  <option value="BW">Botswana</option>
  <option value="BV">Bouvet Island</option>
  <option value="BR">Brazil</option>
  <option value="IO">British Indian Ocean Territory</option>
  <option value="BN">Brunei Darussalam</option>
  <option value="BG">Bulgaria</option>
  <option value="BF">Burkina Faso</option>
  <option value="BI">Burundi</option>
  <option value="KH">Cambodia</option>
  <option value="CM">Cameroon</option>
  <option value="CA">Canada</option>
  <option value="CV">Cape Verde</option>
  <option value="KY">Cayman Islands</option>
  <option value="CF">Central African Republic</option>
  <option value="TD">Chad</option>
  <option value="CL">Chile</option>
  <option value="CN">China</option>
  <option value="CX">Christmas Island</option>
  <option value="CC">Cocos (Keeling) Islands</option>
  <option value="CO">Colombia</option>
  <option value="KM">Comoros</option>
  <option value="CG">Congo</option>
  <option value="CD">Congo, The Democratic Republic of the</option>
  <option value="CK">Cook Islands</option>
  <option value="CR">Costa Rica</option>
  <option value="CI">Côte d'Ivoire</option>
  <option value="HR">Croatia</option>
  <option value="CU">Cuba</option>
  <option value="CY">Cyprus</option>
  <option value="CZ">Czech Republic</option>
  <option value="DK">Denmark</option>
  <option value="DJ">Djibouti</option>
  <option value="DM">Dominica</option>
  <option value="DO">Dominican Republic</option>
  <option value="EC">Ecuador</option>
  <option value="EG">Egypt</option>
  <option value="SV">El Salvador</option>
  <option value="GQ">Equatorial Guinea</option>
  <option value="ER">Eritrea</option>
  <option value="EE">Estonia</option>
  <option value="ET">Ethiopia</option>
  <option value="FK">Falkland Islands (Malvinas)</option>
  <option value="FO">Faroe Islands</option>
  <option value="FJ">Fiji</option>
  <option value="FI">Finland</option>
  <option value="FR">France</option>
  <option value="GF">French Guiana</option>
  <option value="PF">French Polynesia</option>
  <option value="TF">French Southern Territories</option>
  <option value="GA">Gabon</option>
  <option value="GM">Gambia</option>
  <option value="GE">Georgia</option>
  <option value="DE" selected="selected">Germany</option>
  <option value="GH">Ghana</option>
  <option value="GI">Gibraltar</option>
  <option value="GR">Greece</option>
  <option value="GL">Greenland</option>
  <option value="GD">Grenada</option>
  <option value="GP">Guadeloupe</option>
  <option value="GU">Guam</option>
  <option value="GT">Guatemala</option>
  <option value="GG">Guernsey</option>
  <option value="GN">Guinea</option>
  <option value="GW">Guinea-Bissau</option>
  <option value="GY">Guyana</option>
  <option value="HT">Haiti</option>
  <option value="HM">Heard Island and McDonald Islands</option>
  <option value="VA">Holy See (Vatican City State)</option>
  <option value="HN">Honduras</option>
  <option value="HK">Hong Kong</option>
  <option value="HU">Hungary</option>
  <option value="IS">Iceland</option>
  <option value="IN">India</option>
  <option value="ID">Indonesia</option>
  <option value="IR">Iran, Islamic Republic of</option>
  <option value="IQ">Iraq</option>
  <option value="IE">Ireland</option>
  <option value="IM">Isle of Man</option>
  <option value="IL">Israel</option>
  <option value="IT">Italy</option>
  <option value="JM">Jamaica</option>
  <option value="JP">Japan</option>
  <option value="JE">Jersey</option>
  <option value="JO">Jordan</option>
  <option value="KZ">Kazakhstan</option>
  <option value="KE">Kenya</option>
  <option value="KI">Kiribati</option>
  <option value="KP">Korea, Democratic People's Republic of</option>
  <option value="KR">Korea, Republic of</option>
  <option value="KW">Kuwait</option>
  <option value="KG">Kyrgyzstan</option>
  <option value="LA">Lao People's Democratic Republic</option>
  <option value="LV">Latvia</option>
  <option value="LB">Lebanon</option>
  <option value="LS">Lesotho</option>
  <option value="LR">Liberia</option>
  <option value="LY">Libyan Arab Jamahiriya</option>
  <option value="LI">Liechtenstein</option>
  <option value="LT">Lithuania</option>
  <option value="LU">Luxembourg</option>
  <option value="MO">Macao</option>
  <option value="MK">Macedonia, The Former Yugoslav Republic of</option>
  <option value="MG">Madagascar</option>
  <option value="MW">Malawi</option>
  <option value="MY">Malaysia</option>
  <option value="MV">Maldives</option>
  <option value="ML">Mali</option>
  <option value="MT">Malta</option>
  <option value="MH">Marshall Islands</option>
  <option value="MQ">Martinique</option>
  <option value="MR">Mauritania</option>
  <option value="MU">Mauritius</option>
  <option value="YT">Mayotte</option>
  <option value="MX">Mexico</option>
  <option value="FM">Micronesia, Federated States of</option>
  <option value="MD">Moldova</option>
  <option value="MC">Monaco</option>
  <option value="MN">Mongolia</option>
  <option value="ME">Montenegro</option>
  <option value="MS">Montserrat</option>
  <option value="MA">Morocco</option>
  <option value="MZ">Mozambique</option>
  <option value="MM">Myanmar</option>
  <option value="NA">Namibia</option>
  <option value="NR">Nauru</option>
  <option value="NP">Nepal</option>
  <option value="NL">Netherlands</option>
  <option value="AN">Netherlands Antilles</option>
  <option value="NC">New Caledonia</option>
  <option value="NZ">New Zealand</option>
  <option value="NI">Nicaragua</option>
  <option value="NE">Niger</option>
  <option value="NG">Nigeria</option>
  <option value="NU">Niue</option>
  <option value="NF">Norfolk Island</option>
  <option value="MP">Northern Mariana Islands</option>
  <option value="NO">Norway</option>
  <option value="OM">Oman</option>
  <option value="PK">Pakistan</option>
  <option value="PW">Palau</option>
  <option value="PS">Palestinian Territory, Occupied</option>
  <option value="PA">Panama</option>
  <option value="PG">Papua New Guinea</option>
  <option value="PY">Paraguay</option>
  <option value="PE">Peru</option>
  <option value="PH">Philippines</option>
  <option value="PN">Pitcairn</option>
  <option value="PL">Poland</option>
  <option value="PT">Portugal</option>
  <option value="PR">Puerto Rico</option>
  <option value="QA">Qatar</option>
  <option value="RE">Réunion</option>
  <option value="RO">Romania</option>
  <option value="RU">Russian Federation</option>
  <option value="RW">Rwanda</option>
  <option value="BL">Saint Barthélemy</option>
  <option value="SH">Saint Helena</option>
  <option value="KN">Saint Kitts and Nevis</option>
  <option value="LC">Saint Lucia</option>
  <option value="MF">Saint Martin</option>
  <option value="PM">Saint Pierre and Miquelon</option>
  <option value="VC">Saint Vincent and the Grenadines</option>
  <option value="WS">Samoa</option>
  <option value="SM">San Marino</option>
  <option value="ST">Sao Tome and Principe</option>
  <option value="SA">Saudi Arabia</option>
  <option value="SN">Senegal</option>
  <option value="RS">Serbia</option>
  <option value="SC">Seychelles</option>
  <option value="SL">Sierra Leone</option>
  <option value="SG">Singapore</option>
  <option value="SK">Slovakia</option>
  <option value="SI">Slovenia</option>
  <option value="SB">Solomon Islands</option>
  <option value="SO">Somalia</option>
  <option value="ZA">South Africa</option>
  <option value="GS">South Georgia and the South Sandwich Islands</option>
  <option value="ES">Spain</option>
  <option value="LK">Sri Lanka</option>
  <option value="SD">Sudan</option>
  <option value="SR">Suriname</option>
  <option value="SJ">Svalbard and Jan Mayen</option>
  <option value="SZ">Swaziland</option>
  <option value="SE">Sweden</option>
  <option value="CH">Switzerland</option>
  <option value="SY">Syrian Arab Republic</option>
  <option value="TW">Taiwan, Province of China</option>
  <option value="TJ">Tajikistan</option>
  <option value="TZ">Tanzania, United Republic of</option>
  <option value="TH">Thailand</option>
  <option value="TL">Timor-Leste</option>
  <option value="TG">Togo</option>
  <option value="TK">Tokelau</option>
  <option value="TO">Tonga</option>
  <option value="TT">Trinidad and Tobago</option>
  <option value="TN">Tunisia</option>
  <option value="TR">Turkey</option>
  <option value="TM">Turkmenistan</option>
  <option value="TC">Turks and Caicos Islands</option>
  <option value="TV">Tuvalu</option>
  <option value="UG">Uganda</option>
  <option value="UA">Ukraine</option>
  <option value="AE">United Arab Emirates</option>
  <option value="GB">United Kingdom</option>
  <option value="US">United States</option>
  <option value="UM">United States Minor Outlying Islands</option>
  <option value="UY">Uruguay</option>
  <option value="UZ">Uzbekistan</option>
  <option value="VU">Vanuatu</option>
  <option value="VE">Venezuela</option>
  <option value="VN">Viet Nam</option>
  <option value="VG">Virgin Islands, British</option>
  <option value="VI">Virgin Islands, U.S.</option>
  <option value="WF">Wallis and Futuna</option>
  <option value="EH">Western Sahara</option>
  <option value="YE">Yemen</option>
  <option value="ZM">Zambia</option>
  <option value="ZW">Zimbabwe</option>
</select></td></tr>
<tr><td>Location:</td><td><input name="location" value="Walldorf"></td></tr>
<tr><td>Course:</td><td><select name="course">
<option value="BW362">BW362</option>
<option value="BW462">BW462</option>
<option value="HA100" selected="selected">HA100</option>
<option value="HA150">HA150</option>
<option value="HA200">HA200</option>
<option value="HA201">HA201</option>
<option value="HA215">HA215</option>
<option value="HA240">HA240</option>
<option value="HA250">HA250</option>
<option value="HA300">HA300</option>
<option value="HA350">HA350</option>
<option value="HA400">HA400</option>
<option value="HA450">HA450</option>
<option value="SLT100">SLT100</option>

</select></td></tr>
</table>
<br><input type="submit" value="Submit">
<br><a href="/">Home</a>
</form>
     """)

class Downloads(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<script language="JavaScript">

window.location.href="/download_files/index.html";
</script> 
    """)
  
class Fb(webapp.RequestHandler):
  def get(self):
    self.response.out.write("""
<script language="JavaScript">

window.location.href="/fb/login.htm";
</script> 
    """)
class TwitterTags(webapp.RequestHandler):
  def get(self):
    self.response.out.write("<p>Twitter hashtags for scheduled locations</p>")
    locations = db.GqlQuery("SELECT * from ScheduleLocation order by location")
    self.response.out.write('<table border="1">')
    for location in locations:
       self.response.out.write("<tr><td><a href='http://twitter.com/search#search?q=%23SAPEducation"+location.location+"'>"+location.location+"</a>")
       self.response.out.write("</td><td><a href='http://search.twitter.com/search.atom?q=%23SAPEducation"+location.location+"'>Feed for "+location.location+"</a></td></tr>")
    self.response.out.write("</table>") 

class ShowHistory(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'application/csv'
    self.response.headers['Content-Disposition'] = 'attachment; filename=CourseHistory.csv'

    writer = csv.writer(self.response.out,dialect='excel')
    writer.writerow(['Country', 'Week', 'Course', 'Month', 'Count'])

    history = db.GqlQuery("SELECT * from History order by weeks")
    for hist in history:
        
            now = date.today()
	    td = timedelta(days = 3 + (hist.weeks * 7))
	    now = date(1970,1,1) + td
	    if hist.ccode <> 'XX' and hist.ccourse <> 'FUN' and hist.ccourse <> 'DUMMY':
              writer.writerow([hist.ccode, now.isoformat(), hist.ccourse, now.isoformat()[:7], 1])

class HandoutGen(webapp.RequestHandler):
  def get(self):
#    self.response.headers['Content-Type'] = 'application/msword'
    email = self.request.get('email').strip()
    genonly = self.request.get('genonly')
#    message = "No email address provided"
    hints = self.request.get('hints').strip()
    lang = self.request.get('lang')
    oes = self.request.get('oes')
    host = self.request.get('host')
    url = "http://sap-netweaver-training.appspot.com/handouts/"+lang+"/no_details.xml"
    if hints == "true":
       url = "http://sap-netweaver-training.appspot.com/handouts/"+lang+"/no_details_hints.xml"
    result = urlfetch.fetch(url)
    handout = result.content
    header = ""
    footer = ""
#    body = ""
    p1 = handout.find("<w:body>")
    p2 = handout.find("</w:body>")
    if p2 > p1:
        header=handout[0:p1+8]
        footer=handout[p2:]
        body=handout[p1+8:p2]
    newline = "</w:t><w:br/><w:t>"
    newItem = '</w:t></w:r></w:p><w:p><w:pPr><w:listPr><w:ilvl w:val="0"/><w:ilfo w:val="1"/></w:listPr></w:pPr><w:r><w:t>'
    preserveOn = '</w:t><w:t xml:space="preserve">'
    preserveOff = "</w:t><w:t>"
    boldOn = '</w:t></w:r><w:r><w:rPr><w:b w:val="on"/></w:rPr><w:t>'
    boldOff = "</w:t></w:r><w:r><w:t>"
    urlOff = boldOff
    urlOn = '</w:t></w:r><w:r><w:rPr><w:color w:val="0000FF" /> <w:u w:val="single" /></w:rPr><w:t>'
    italicOn = '</w:t></w:r><w:r><w:rPr><w:i w:val="on"/></w:rPr><w:t>'
    italicOff = boldOff
    newpage = '<w:br w:type="page"/>'
    sDesktop = getTemplate("Desktop",lang)
#    sInternal = getTemplate("Internal",lang)
#    sExternal = getTemplate("External",lang)
    sNew = getTemplate("Newaccess",lang)
    sCloud = getTemplate("Cloud",lang)
#    sSystemsList = getTemplate("SystemsList",lang)
    sFinally = getTemplate("Finally",lang)
    sSystem = getTemplate("System",lang)
    sInitcourse = getTemplate("Initcourse",lang)
    sOES = getTemplate("OES",lang)
    sBI = getTemplate("BI",lang)
    sHANA = getTemplate("HANA",lang)
    sVDI = getTemplate("VDI",lang)
    course = self.request.get('course').strip()
    dUser = self.request.get('dUser').strip()
    dPass = self.request.get('dPass').strip()
    cHost = self.request.get('cHost').strip()
    cUser = self.request.get('cUser').strip()
    cPass = self.request.get('cPass').strip()
    cUse = self.request.get('cUse').strip()
    csgUser = self.request.get('csgUser').strip()
    csgPass = self.request.get('csgPass').strip()
    oesUser = self.request.get('oesUser').strip()
    oesPass = self.request.get('oesPass').strip()
    reg = self.request.get('reg').strip()
    wts = self.request.get('wts').strip()
    systems = int(self.request.get('systems'))
    sid1 = self.request.get('sid1').strip()
    stype1 = self.request.get('stype1').strip()
    stype2 = self.request.get('stype2').strip()
    stype3 = self.request.get('stype3').strip()
    client1 = self.request.get('client1').strip()
    aname1 = self.request.get('aname1').strip()
    apass1 = self.request.get('apass1').strip()
    sid2 = self.request.get('sid2').strip()
    client2 = self.request.get('client2').strip()
    aname2 = self.request.get('aname2').strip()
    apass2 = self.request.get('apass2').strip()
    sid3 = self.request.get('sid3').strip()
    client3 = self.request.get('client3').strip()
    aname3 = self.request.get('aname3').strip()
    apass3 = self.request.get('apass3').strip()

#    icUse = self.request.get('icUse').strip()
    s = sDesktop
    if genonly == "true":
       s = newpage + sDesktop
#    if wts == "INTERNAL":
#       s = s + sInternal
#    if wts == "EXTERNAL":
#       s = s + sExternal
    if wts == "VDI7" or wts == "VDI8":
       s = s + sVDI
    if wts == "NEW":
       s = s + sNew
    if cUse == "false":
       s = s + sInitcourse
    if cUse == "true":
       s = s + sCloud
    if (systems >= 1):
      ss1 = sSystem
      if stype1 == "HANA":
         ss1 = sHANA
      if stype1 == "BI":
         ss1 = sBI
      ss1 = ss1.replace("<sid>",fixXML(sid1))
      ss1 = ss1.replace("<client>",fixXML(client1))
      ss1 = ss1.replace("<aname>",fixXML(aname1))
      ss1 = ss1.replace("<apass>",fixXML(apass1))
      s = s + ss1
    if (systems >= 2):
      ss2 = sSystem
      if stype2 == "HANA":
         ss2 = sHANA
      if stype2 == "BI":
         ss2 = sBI
      ss2 = ss2.replace("<sid>",fixXML(sid2))
      ss2 = ss2.replace("<client>",fixXML(client2))
      ss2 = ss2.replace("<aname>",fixXML(aname2))
      ss2 = ss2.replace("<apass>",fixXML(apass2))
      s = s + ss2
    if (systems >= 3):
      ss3 = sSystem
      if stype3 == "HANA":
         ss3 = sHANA
      if stype3 == "BI":
         ss3 = sBI
      ss3 = ss3.replace("<sid>",fixXML(sid3))
      ss3 = ss3.replace("<client>",fixXML(client3))
      ss3 = ss3.replace("<aname>",fixXML(aname3))
      ss3 = ss3.replace("<apass>",fixXML(apass3))
      s = s + ss3
    if oes == "y":
       s = s + sOES
    if oes == "p":
       s = s + newpage + sOES
    s = s + sFinally
    s = s.replace("<sl>", "")
    s = s.replace("<url>",urlOn)
    s = s.replace("<eurl>",urlOff)
    s = s.replace("<i>",italicOn)
    s = s.replace("<ei>",italicOff)
    s = s.replace("<region>",reg)
    s = s.replace("<nl>",newline)
    s = s.replace("<b>",boldOn)
    s = s.replace("<eb>",boldOff)
    s = s.replace("<csgu>",fixXML(csgUser))
    s = s.replace("<csgp>",fixXML(csgPass))
    s = s.replace("<cu>",fixXML(cUser))
    s = s.replace("<cp>",fixXML(cPass))
    s = s.replace("<ch>",fixXML(cHost))
    s = s.replace("<pres>",preserveOn);
    s = s.replace("<epres>",preserveOff)
    s = s.replace("<li>",newItem)
    s = s.replace("<du>",fixXML(dUser))
    s = s.replace("<dp>",fixXML(dPass))
    s = s.replace("<oesu>",fixXML(oesUser))
    s = s.replace("<oesp>",fixXML(oesPass))
    s = s.replace("<course>",fixXML(course))
#    s = s.replace("<sid>",fixXML(sid))
#    s = s.replace("<client>",fixXML(client))
#    s = s.replace("<aname>",fixXML(aname))
#    s = s.replace("<apass>",fixXML(apass))
#    handout = s
    body = body.replace("$ConnectionInstructions$",s)
    handout = body
    header = unicode(header,'UTF-8')
    footer = unicode(footer, 'UTF-8')
#    handout = "body is "+str(type(body))+", header is "+str(type(header))
#    handout = header+handout
#    handout = handout+footer
    handout = header+body+footer
#    handout = header+body.replace("$ConnectionInstructions$",str(p1)+"-"+str(p2))+footer
    if genonly == "true":
        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write(s)
        self.response.out.write("Instructions generated. use the button to add them to the handout.")
        ci = CI( key_name = host, host = host, instructions = db.Text(s))
        ci.put()
        ci = CI( key_name = host+"_full", host = host+"_full", instructions = db.Text(body))
        ci.put()
    if email == "":
       if genonly <> "true":
          self.response.headers['Content-Type'] = 'application/msword'
          self.response.out.write(handout)
    if email <> "":
      if genonly <> "true":
        try:
          message = "Email sent to "+email
          mail.send_mail(sender="me <i016416@gmail.com>", 
#          mail.send_mail(sender="donotreply <donotreply@sap-netweaver-training.appspotmail.com>",
              to=email, 
              subject="Course connection instructions for "+course, 
              body="Course connection instructions attached",
	      attachments=[("handout.doc",handout)])
        except:
          message = "Error sending email"
        self.response.out.write(message)

class HandoutGenHtml(webapp.RequestHandler):
  def get(self):
#    self.response.headers['Content-Type'] = 'application/msword'
    email = self.request.get('email').strip()
    lang = self.request.get('lang')
    if lang == "":
        lang = "en"
    course = self.request.get('course').strip()
    username = self.request.get('username').strip()
    password = self.request.get('password').strip()
    host = self.request.get('host').strip()
    instructor = self.request.get('instructor').strip()
    participants = self.request.get('participants').strip()
    region = self.request.get('region').strip()
    country = self.request.get('live').strip()
    template = self.request.get('template').strip()
    extra = self.request.get('extra').strip()
    extra = base64.standard_b64decode(extra)
    hist = CIHistory(   
          created = datetime.utcnow(),
          key_name=str(datetime.utcnow()),
          course = course,
   	  host = host,
   	  username = username,
   	  password = password)
#    hist.put()
    days = int(math.floor(time.time()/(60*60*24)))
    days = days - 3
    weeks = int(math.floor(days / 7))
    if country != 'No':
      c = country
      l = "SAP LIVE CLASS"
      cc = course
      newcountry = Country(key_name =  "C" + c + str(weeks),
                      ccode = c,
                      weeks = weeks)
      newcountry.put()
      newcourse = Course(key_name = c + l + cc + str(weeks),
                      ccode = c,
                      weeks = weeks,
                      location = l,
                      ccourse = cc)
      newcourse.put()
      newlocweek = LocWeeks(key_name = c + l + str(weeks),
                      ccode = c,
                      weeks = weeks,
                      location = l)
      newlocweek.put()
    url = "http://sap-netweaver-training.appspot.com/handouts/"+lang+"/template"+template+".html"
    result = urlfetch.fetch(url)
    skipcount = 7 - host.count(",")
    if host.count(",") == 0:
        skipcount = skipcount + 1
    skip = ""
    while skipcount >0:
       skip=skip+"<br>"
       skipcount=skipcount - 1
    multi = "," in host
    host = host.replace(",","</b><br>or <b>")
    if multi:
        host=host+"</b><br>(allocated by the instructor)"
    s = result.content
    s = s.decode('utf-8')
    s = s.replace("$instructor$", instructor)
    s = s.replace("$participants$", participants)
    s = s.replace("$username$",username+"-0##")
    s = s.replace("$password$",password)
    s = s.replace("$course$",course)
    s = s.replace("$region$",region)
    s = s.replace("$host$",host)
    s = s.replace("$extra$",extra)
    s = s.replace("$skip$",skip)
    handout = s
    if email == "":
#       if genonly <> "true":
          self.response.headers['Content-Type'] = 'text/html'
          self.response.out.write(handout)
    if email <> "":
#      if genonly <> "true":
        try:
          message = "Email sent to "+email
          mail.send_mail(sender="me <i016416@gmail.com>", 
#          mail.send_mail(sender="donotreply <donotreply@sap-netweaver-training.appspotmail.com>",
              to=email, 
              subject="Course connection instructions for "+course, 
              body="Course connection instructions attached",
	      attachments=[("handout.html",handout)])
        except:
          message = "Error sending email"
        self.response.out.write(message)


class Store(webapp.RequestHandler):
  def get(self):
#    self.response.out.write('<html><body>Added country:')
#    self.response.out.write(cgi.escape(self.request.get('country')))
#    self.response.out.write(str(int(time.time()/(60*60*24))))
#    self.response.out.write('</body></html>')
    days = int(math.floor(time.time()/(60*60*24)))
    days = days - 3
    weeks = int(math.floor(days / 7))
    c = self.request.get('country').strip()
    l = self.request.get('location').strip().strip().replace('"','')
    cc = self.request.get('course').strip()
# event stuff
    e_event = self.request.get('event').strip()
    e_instructor = self.request.get('instructor').strip().replace('"','')
    e_lastday = self.request.get('lastday').strip()
    e_groups = self.request.get('groups').strip()
    e_abappwd = self.request.get('abappwd').strip()
    e_ospwd = self.request.get('ospwd').strip()
    e_language = self.request.get('language').strip()
    e_decfmt = self.request.get('decfmt').strip()
    e_datefmt = self.request.get('datefmt').strip()
    e_clones = self.request.get('clones').strip()
    e_country = c
    e_location = l
    e_course = cc
    if len(e_event) > 0:
        runat = str(datetime.utcnow())
	new_history = EventHistory(key_name = e_event+runat,
            event = e_event,    
            runat = runat)
        new_history.put()
        new_event = Event(key_name = e_event,
		event = e_event,
    		instructor = e_instructor,
    		lastday = e_lastday,
    		groups = e_groups,
    		abappwd = e_abappwd,
    		ospwd = e_ospwd,
    		language = e_language,
    		decfmt = e_decfmt,
    		datefmt = e_datefmt,
                clones = e_clones,
    		country = e_country,
    		location = e_location,
    		course = e_course)
        new_event.put()
          
#
    c = c.upper()
    l = l.upper();

    aliases = db.GqlQuery("SELECT * from Alias where alias = :1", c+ l)
    
    for alias in aliases:
       c = alias.ccode.upper()
       l = alias.location.upper()
    if l.find("VIRTUAL") >= 0:
        l = "VIRTUAL"
    if len(c) == 2:
      country = Country(key_name =  "C" + c + str(weeks),
                      ccode = c,
                      weeks = weeks)
      country.put()
      self.response.out.write('<a href="/">Home</a>')
    
    lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3 and ccourse = :4", l, c, weeks,cc)
    matches = lcs.count()
    if len(l) > 0 and matches == 0:
       course = Course(key_name = c + l + cc + str(weeks),
                      ccode = c,
                      weeks = weeks,
                      location = l,
                      ccourse = cc)
       course.put()
       locweek = LocWeeks(key_name = c + l + str(weeks),
                      ccode = c,
                      weeks = weeks,
                      location = l)
       locweek.put()
       history = History(key_name = c + str(weeks) + cc,
                      ccode = c,
                      weeks = weeks,
                      ccourse = cc)
#       history.put()
#       mail.send_mail(sender="me <i016416@gmail.com>", 
#              to="Twitter <g0vg7j-pksfth@twittermail.com>", 
#              to="Twitter <tweet@tweetymail.com>",
#              subject="Setup ", 
#              body="for @SAPEDU course #" + cc+ " running in "+l+", "+c+ " run at  "+time.asctime(time.gmtime(time.time()+(10*60*60))))
#       mail.send_mail(sender="me <i016416@gmail.com>", 
#              to="me <michael.nicholls@sap.com>", 
#              subject="Course stored", 
#              body="Course " + cc+ " running in "+l+", "+c)
       locations = db.GqlQuery("SELECT * from Location where location = :1", c+ l)
       matching = 0
       for location in locations:
           matching = matching + 1
       if matching == 0:
	       mail.send_mail(sender="me <i016416@gmail.com>", 
        	 to="me <michael.nicholls@orange.fr>", 
              	 subject="Missing location", 
		 body="Missing location "+l+", "+c+" http://sap-netweaver-training.appspot.com/missingLocations")

class buildjson(webapp.RequestHandler):
  def get(self):
     days = int(math.floor(time.time()/(60*60*24)))
     days = days - 3
     weeks = int(math.floor(days / 7))
     counttext = "No courses have been setup this week"
     self.response.out.write("""
{
	"Spots" :
		[
     """)
     oldcourses = db.GqlQuery("SELECT * from LocWeeks where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Course where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
     oldcourses = db.GqlQuery("SELECT * from Country where weeks < :1", weeks)
     for oldcourse in oldcourses:
         oldcourse.delete();
         
     courses = db.GqlQuery("SELECT * from LocWeeks where weeks = :1", weeks)
     locationcount = 0
     countrycount = 0
     totalcourses = 0
     lastcountry = ""
     countries = ""
     allcourses = ""
     for course in courses:
        courselist = ""
        lcs = db.GqlQuery("SELECT * from Course where location = :1 and ccode = :2 and weeks = :3", course.location, course.ccode, course.weeks)
        coursecount = 0
#	locationcount = 0
#	countrycount = 0
        coursetext = "Course: "
        for lc in lcs:
#            totalcourses = totalcourses + 1
            coursecount = coursecount + 1
            if courselist <> "":
                coursetext = "Courses: "
                courselist = courselist + "\\n"
#                if (coursecount % 5) == 0:
#                     courselist = courselist+"<br>"
            courselist = courselist + lc.ccourse
        locations = db.GqlQuery("SELECT * from Location where location = :1", lc.ccode + lc.location)
        matching = 0
        for location in locations:
           disploc = lc.location.title().replace('Sap ','SAP ').replace('Vlc','VLC')
#           disploc = lc.location.title().replace('Vlc','VLC')
#	   disploc = disploc.replace("\'","&rsquo;")
           matching = matching + 1
        if matching > 0:
#           totalcourses = totalcourses + 1
           if lastcountry <> course.ccode and course.ccode <> 'XX':
              countrycount = countrycount + 1
              countries = countries+',{"Id":"'+course.ccode+'"}'
              lastcountry = course.ccode
	   coords = location.coords[1:len(location.coords)-1].replace(" ","").split(",")
	   if disploc == "SAP Live Access Cloud":
                random.seed()
                coords[0] = str(random.randint(-80,80))
                coords[1] = str(random.randint(-170,170))
#                coords = (randlong+","+randlat).split(",")
           if locationcount > 0:
               self.response.out.write(",")
#               allcourses = allcourses+","
           for lc in lcs: 
              totalcourses = totalcourses + 1
              if allcourses <> "":
                     allcourses = allcourses+","
              allcourses = allcourses+'{ "country":"'+course.ccode+'","text":"'+disploc+'","course":"'+lc.ccourse+'"}'
           self.response.out.write(' {"country":"'+course.ccode+'", "pos": "'+coords[1]+";"+coords[0]+'", "text":"' +disploc+'", "tooltip": "'+coursetext+courselist+'" }')
           locationcount = locationcount + 1
     if totalcourses > 0:
       locationtext = " locations" if locationcount > 1 else " location"
       countrytext = " countries" if countrycount != 1 else " country"
       coursetext = " courses" if totalcourses > 1 else " course"
       counttext = str(totalcourses) + coursetext + " at " +str(locationcount) + locationtext + " in " +str(countrycount)+ countrytext 
     self.response.out.write('],"count": "' + counttext + '", "Countries": [ { "Id":"Global"}')
     self.response.out.write(countries+'],"Courses":['+allcourses+']}')
#			{
#                "pos": "37.622882;55.755202;0",
#                "tooltip": "Moscow\\nwelcome\\n12\\n34\\nqeqeqeq\\n55555555",
#                "type": "Default",
#                "text": "Moscow"                	
#            },
      

class QuizDown(webapp.RequestHandler):
  def get(self):
       lastquiz = db.GqlQuery("SELECT * from QuizMail")
       quizfound = 0;
       lastsent = 0;
       now = datetime.utcnow();
       for q in lastquiz:
          quizfound = 1
 	  lastsent = q.lastSent
       if quizfound == 0:
            quiz = QuizMail(key_name='xxx',xxx='xxx',lastSent=0)
            quiz.put()
       quiz = QuizMail(key_name='xxx',xxx='xxx',lastSent=datetime.utcnow())
       quiz.put();
       diff = now - lastsent
       self.response.headers.add_header("Access-Control-Allow-Origin", "*")
       self.response.headers['Content-Type'] = 'text/plain'
       already = "already "
       if diff.total_seconds() > 3600: 
         mail.send_mail(sender="me <i016416@gmail.com>", 
       	   to="me <michael.nicholls@orange.fr>", 
 	   subject="Quiz down", 
	   body="The SAP Learning Rooms Quiz application is down")
         already = ""
       self.response.out.write("An email has "+already+"been sent to an administrator.")

class GetInstructions(webapp.RequestHandler):
  def get(self):
    host = self.request.get('host').strip()
    instructions = db.GqlQuery("SELECT * from CI where host = :1", host+"_full")
    self.response.headers['Content-Type'] = 'text/plain'
    s = ""    
    for instruction in instructions:    
       s = instruction.instructions
    self.response.out.write(s)

class ConnectionInstructions(webapp.RequestHandler):
  def get(self):
    coursein = self.request.get('course').strip()
    genonly = self.request.get('genonly').strip()
    hostin = self.request.get('host').strip()
#    hostin = 'test'
    if genonly != "true":
       genonly = "false"
    self.response.out.write("""

<html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ascii">
  </head>
<body>
    """)
    if genonly != "true":
      self.response.out.write("""
This form can be used to create instructions for connecting to the SAP Education training landscape.<br>
Enter the details and use the Submit button. If you have supplied an email address for the instructor, then<br>
the output will be be sent by email to that address. Otherwise, the instructions will be opened on your desktop.<br>
The content is generated using Word XML.
Feedback about the form <a href="mailto:michael.nicholls@orange.fr">here</a>
<br><b>There is a newer version, based on UI5, available </b> <a href="/ci2">here</a>
       """)
    
    self.response.out.write("""

<form action="http://sap-netweaver-training-hrd.appspot.com/connectionInstructions">
<table>
<tr><td>Course</td><td><input id="course" name="course" value="XXXNNN"></td></tr>
<tr id="showEmail"><td>Instructor's email</td><td><input name="email"></td><td colspan="2">Enter a value if you want the instructions emailed</td></tr>
<tr><td>Desktop username</td><td><input name="dUser" value="none"></td>
<td>Password  <input name="dPass" value="none"></td></tr>
<tr><td>WTS/VDI</td><td><select id="wts" name="wts" onChange="changeWTS()">
<option value="None">None</option>
<option value="NEW" selected="Selected">access.sap.com</option>
<!--<option value="INTERNAL">(old)Internal WTS</option>
<option value="EXTERNAL">(old)External WTS</option>
-->
<option value="VDI7">VDI Windows 7</option>
<option value="VDI8">VDI Windows 8</option>
</select></td><td colspan="2">Select the WTS or VDI infrastructure to be used</td></tr>
<tr id="reg"><td>Region</td><td><select id = "reglist" name="reg">
<option value="Americas">Americas</option>
<option value="Europe - Middle East - Africa" selected="selected">Europe - Middle East - Africa</option>
<option value="Asia - Pacific - Japan">Asia - Pacific - Japan</option>
</select></td><td colspan="2">Select the most appropriate WTS farm</td></tr>
<tr id="csgUser"><td><p id="CSGU">access.sap.com username</p></td><td><input id="csgUserVal" name="csgUser" value="<event>-0##"></td>
<td>Password <input name="csgPass" id="csgPass" value="xxx_<course>_NN"></td></tr>
<tr id="cUseShow"><td>Use cloud</td><td><select id="cUse" name="cUse" onChange="changeCloud()">
<option value="false">No</option>
<option value="true" selected="selected">Yes</option>
</select></td><td colspan="2">If you have been allocated a cloud server, enter the details</td></tr>
<tr id="cHost"><td>Cloud hostname</td><td><input name="cHost" value="CA-ECC6xx-nnn"></td></tr>
<tr id="cUser"><td>Cloud username</td><td><input name="cUser" value="train-##"></td>
<td>Password  <input name="cPass" value="initial"></td></tr>
<tr id="showOES"><td>Include OES</td><td><select id = "oes" name="oes">
<option value="n">No</option>
<option value="y" selected="selected">Yes</option>
<option value="p">On a new page</option></select></td><td colspan="2">Whether to include the OES details</td></tr>
<tr><td>OES username</td><td><input name="oesUser" id="oesUser" value="<event>-0##"></td>
<td>Password  <input name="oesPass" id="oesPass" value="xxx_<course>_NN"></td></tr>
<tr id="showSystems"><td>Systems</td><td><select name="systems" id="systems" onChange="changeSystems()">
<option value="0" selected="selected">0</option>
<option value="1">1</option>
<option value="2">2</option>
<option value="3">3</option>
</select></td><td colspan="2">Select the number of systems that the students will access and enter the connection details</td></tr>
<tr id="s1">
<td><select name="stype1" id="stype1" onChange="changeStype(1)">
<option value="ABAP" selected = "selected">ABAP</option>
<option value="HANA">HANA</option>
<option value="BI">BI</option>
</select></td><td>
<p id="text1">SID/client/username/password</p></td><td colspan="2"><input id="sid1" name="sid1" value="XXX" size="3"><input id="client1" name="client1" value="800" size="3"><input name="aname1" value="<course>-##" size="12"><input name="apass1" value="welcome"></td></tr>
<tr id="s2">
<td><select name="stype2" id="stype2" onChange="changeStype(2)">
<option value="ABAP" selected = "selected">ABAP</option>
<option value="HANA">HANA</option>
<option value="BI">BI</option>
</select></td>
<td><p id="text2">SID/client/username/password</p></td><td colspan="2"><input id="sid2" name="sid2" value="XXX" size="3"><input id="client2" name="client2" value="800" size="3"><input name="aname2" value="<course>-##" size="12"><input name="apass2" value="welcome"></td></tr>
<tr id="s3">
<td><select name="stype3" id="stype3" onChange="changeStype(3)">
<option value="ABAP" selected = "selected">ABAP</option>
<option value="HANA">HANA</option>
<option value="BI">BI</option>
</select></td>
<td><p id="text3">SID/client/username/password</p></td><td colspan="2"><input id="sid3" name="sid3" value="XXX" size="3"><input id="client3" name="client3" value="800" size="3"><input name="aname3" value="<course>-##" size="12"><input name="apass3" value="welcome"></td></tr>
<tr id="showHints"><td>Add hints</td><td><input type="checkbox" name="hints" value="true"/></td><td colspan="2">Select this checkbox to add some ABAP hints</td></tr>
</table>
<br><input type="submit" value="Submit">  <button type="button" onClick="copy2OES()">Copy WTS logon details to OES</button>
        """)
    self.response.out.write('<input type="hidden"  id="lang" name="lang" value="en"/>')
    self.response.out.write('<input type="hidden"  id="genonly" name="genonly" value="'+genonly+'"/>')
    self.response.out.write('<input type="hidden" id="coursein" name="coursein" value="'+coursein+'">')
    self.response.out.write('<input type="hidden" id="host" name="host" value="'+hostin+'">')
    self.response.out.write("""

</form>
<script>
    function copy2OES() {
   document.getElementById("oesUser").value = document.getElementById("csgUserVal").value;
   document.getElementById("oesPass").value = document.getElementById("csgPass").value;
   }
   function changeWTS() {
    if (document.getElementById("wts").value == "None") {
  document.getElementById("reg").style.display="none";
  document.getElementById("csgUser").style.display="none";
  document.getElementById("CSGU").innerHTML="CSG username"
   } else if  (document.getElementById("wts").value == "INTERNAL") {
  document.getElementById("reg").style.display="";
  document.getElementById("reglist").options.item(0).text = "AMERICAS";
  document.getElementById("reglist").options.item(0).value = "AMERICAS";
  document.getElementById("reglist").options.item(1).text = "EMEA";
  document.getElementById("reglist").options.item(1).value = "EMEA";
  document.getElementById("reglist").options.item(2).text = "APJ";
  document.getElementById("reglist").options.item(2).value = "APJ";
  document.getElementById("csgUser").style.display="none";
  document.getElementById("CSGU").innerHTML="CSG username"
      } else if (document.getElementById("wts").value == "VDI7") {
  document.getElementById("reg").style.display="none";
  document.getElementById("csgUser").style.display="";
  document.getElementById("CSGU").innerHTML="VDI username"
      } else if (document.getElementById("wts").value == "VDI8") {
  document.getElementById("reg").style.display="none";
  document.getElementById("csgUser").style.display="";
  document.getElementById("CSGU").innerHTML="VDI username"
      } else if (document.getElementById("wts").value == "NEW") {
  document.getElementById("reg").style.display="";
  document.getElementById("csgUser").style.display="";
  document.getElementById("reglist").options.item(0).text = "Americas";
  document.getElementById("reglist").options.item(0).value = "Americas";
  document.getElementById("reglist").options.item(1).text = "Europe - Middle East - Africa";
  document.getElementById("reglist").options.item(1).value = "Europe - Middle East - Africa";
  document.getElementById("reglist").options.item(2).text = "Asia - Pacific - Japan";
  document.getElementById("reglist").options.item(2).value = "Asia - Pacific - Japan";
  document.getElementById("CSGU").innerHTML="access.sap.com username"
      }  else {
  document.getElementById("reg").style.display="";
  document.getElementById("csgUser").style.display="";
  document.getElementById("CSGU").innerHTML="CSG username"
   }
  }
  function changeSystems() {
    if (document.getElementById("systems").value == "0") {
     document.getElementById("s1").style.display="none";
     document.getElementById("s2").style.display="none";
     document.getElementById("s3").style.display="none";
    }
    if (document.getElementById("systems").value == "1") {
     document.getElementById("s1").style.display="";
     document.getElementById("s2").style.display="none";
     document.getElementById("s3").style.display="none";
    }
    if (document.getElementById("systems").value == "2") {
     document.getElementById("s1").style.display="";
     document.getElementById("s2").style.display="";
     document.getElementById("s3").style.display="none";
    }
    if (document.getElementById("systems").value == "3") {
     document.getElementById("s1").style.display="";
     document.getElementById("s2").style.display="";
     document.getElementById("s3").style.display="";
    }
  }
  function changeStype(n) {
     snum = document.getElementById("stype"+n).value;
     if (snum == "ABAP") {
        document.getElementById("sid"+n).value = "XXX";     
        document.getElementById("sid"+n).size = 3;     
        document.getElementById("client"+n).value = "800";     
	}
     stext = "SID/client/username/password";
     if (snum == "HANA") {
        stext = "HANA host/instance/username/password" ;
        document.getElementById("sid"+n).value = "wdflbmtxxxx";     
        document.getElementById("sid"+n).size = 15;     
        document.getElementById("client"+n).value = "00";     
      }
     if (snum == "BI") {
       stext = "BI host/port/username/password";
        document.getElementById("sid"+n).value = "wdflbmtxxxx";     
        document.getElementById("sid"+n).size = 15;     
        document.getElementById("client"+n).value = "8080";     
      }
     document.getElementById("text"+n).innerHTML = stext;
   }
  function changeCloud() {
    if (document.getElementById("cUse").value == "false") {
  document.getElementById("cHost").style.display="none";
  document.getElementById("cUser").style.display="none";
   } else {
  document.getElementById("cHost").style.display="";
  document.getElementById("cUser").style.display="";
      }
  }
  document.getElementById("reg").style.display="";
  document.getElementById("csgUser").style.display="";
  document.getElementById("cHost").style.display="";
  document.getElementById("cUser").style.display="";
  document.getElementById("s1").style.display="none";
  document.getElementById("s2").style.display="none";
  document.getElementById("s3").style.display="none";
  if (document.getElementById("genonly").value == "true") {
    document.getElementById("course").value = document.getElementById("coursein").value;
    document.getElementById("cUse").value = "false";
    document.getElementById("showEmail").style.display="none";
    document.getElementById("cUseShow").style.display="none";
    document.getElementById("showSystems").style.display="none";
    document.getElementById("showHints").style.display="none";
    document.getElementById("cHost").style.display="none";
    document.getElementById("cUser").style.display="none";
    document.getElementById("oes").value = "p";
    }
</script>
</body>
        """)

class StoreSchedule(webapp.RequestHandler):
  def get(self):
    c = self.request.get('course').strip()
    l = self.request.get('location').strip()
    d = self.request.get('date').strip()
    s = self.request.get('status').strip()
    c = c.upper()
    if len(l) > 0 and len(s) > 0 and len(d) > 0  and len(c) > 0:
       mail.send_mail(sender="me <i016416@gmail.com>", 
#              to="Twitter <g0vg7j-pksfth@twittermail.com>", 
              to="Twitter <tweet@tweetymail.com>",
              subject="Twitter update", 
              body="Course " + c+ " " + s+ " to run in "+l+" starting on "+d+ " http://training.sap.com/search?query="+c+" #SAPEducation"+l)
       self.response.out.write("Tweet posted for <a href='http://twitter.com/search#search?q=%23SAPEducation"+l+
	"'>#SAPEducation"+l+"</a>")

application = webapp.WSGIApplication(     
         [('/', MainPage),
         ('/knownLocations', KnownLocations),
	 ('/coordsin', CoordsIn),
         ('/thisweekold', ThisWeekOld),
         ('/thisweeki', ThisWeeki),
         ('/thisweek', thisweekui5),
         ('/thisweekkml', ThisWeekKml),
         ('/thisweekjs', ThisWeekJs),
         ('/addSchedule', StoreSchedule),
         ('/add', Store),
	 ('/quizdown', QuizDown),
         ('/capture', Capture),
         ('/showtime', Showtime),
         ('/downloads', Downloads),
         ('/fb', Fb),
         ('/addprompt', Addprompt),
         ('/addhana', Addhana),
         ('/addscheduleprompt', Addscheduleprompt),
         ('/missingLocations', Missing),
         ('/modLocation', ModLocation),
         ('/sitemap.xml', sitemap),
         ('/twittertags', TwitterTags),
	 ('/history',ShowHistory),
	 ('/connectionInstructions',HandoutGen),
	 ('/connectionInstructionsHtml',HandoutGenHtml),
         ('/ci',ConnectionInstructions),
         ('/ciget',GetInstructions),
         ('/ciimport', StoreTemplates),
         ('/launchYahoo',launchYahoo),
         ('/thisweekjson', buildjson),
         ('/ci2', ci2),
         ('/getevent', getEvent),
         ('/thisweekui5', thisweekui5),
         ('/odata/.*', odata),
         ('/launchpad', Launchpad)],
    debug=True)

def main():  
   run_wsgi_app(application)

if __name__ == "__main__":  
   main()
