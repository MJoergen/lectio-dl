#!/bin/python -u
# -*- coding: utf-8 -*-
import requests
import os
import time
import getpass
import difflib
import logging

# Initialize global variables
BASEDIR  = "Lectio-Doc" # Mappe, hvor alle de hentede dokumenter bliver lagt.
cafile   = 'cacert.pem' # Bruges til at etablere en HTTPS (SSL) forbindelse til lectio.

# Global counters. Used only for statistics
sumFiles = 0
sumBytes = 0 
sumDirs  = 0

# Denne liste er taget fra adressen http://www.lectio.dk/lectio/login_list.aspx, den 15. maj 2016
skoler_liste = [
    [1,   u'Aurehøj Gymnasium'],
    [2,   u'Hvidovre Gymnasium og HF'],
    [3,   u'Bagsværd Kostskole og Gymnasium'],
    [5,   u'Christianshavns Gymnasium'],
    [6,   u'HF-Centret Efterslægten'],
    [7,   u'Falkonergårdens Gymnasium og HF'],
    [8,   u'Frederiksberg Gymnasium'],
    [9,   u'Gammel Hellerup Gymnasium'],
    [11,  u'Gladsaxe Gymnasium'],
    [12,  u'Herlev Gymnasium og HF'],
    [13,  u'Ingrid Jespersens Gymnasieskole'],
    [14,  u'Ingrid Jespersens Grundskole'],
    [15,  u'Johannesskolens Grundskole'],
    [16,  u'Johannesskolens Gymnasium'],
    [17,  u'Gefion Gymnasium'],
    [19,  u'N. Zahles Gymnasieskole'],
    [20,  u'Niels Steensens Gymnasium'],
    [21,  u'Nørre Gymnasium'],
    [22,  u'Ordrup Gymnasium'],
    [23,  u'Rysensteen Gymnasium'],
    [24,  u'Rødovre Gymnasium'],
    [25,  u'Sankt Annæ Gymnasium'],
    [26,  u'Ørestad Gymnasium'],
    [30,  u'Tårnby Gymnasium'],
    [31,  u'Nærum Gymnasium'],
    [32,  u'Københavns åbne Gymnasium'],
    [33,  u'Virum Gymnasium'],
    [34,  u'Øregård Gymnasium'],
    [36,  u'Høje-Taastrup Gymnasium'],
    [37,  u'Borupgaard Gymnasium'],
    [38,  u'Brøndby Gymnasium'],
    [40,  u'Det frie Gymnasium'],
    [43,  u'CPH WEST - Albertslund Gymnasium & HF'],
    [44,  u'CPH WEST - hhx, Ishøj og CPH10'],
    [45,  u'CPH WEST - HTX, Albertslund - ATG'],
    [46,  u'CPH WEST - htx, Ishøj'],
    [47,  u'CPH WEST - Ishøj Gymnasium'],
    [48,  u'CPH WEST Handelsgymnasiet i Ballerup'],
    [51,  u'Allerød Gymnasium'],
    [52,  u'Birkerød Gymnasium og HF'],
    [53,  u'Helsingør Gymnasium'],
    [54,  u'Frederiksborg Gymnasium og hf'],
    [55,  u'Frederikssund Gymnasium'],
    [57,  u'Espergærde Gymnasium og HF'],
    [58,  u'Marie Kruses Skole'],
    [59,  u'Rungsted Gymnasium'],
    [60,  u'Frederiksværk Gymnasium og HF'],
    [61,  u'Gribskov Gymnasium'],
    [62,  u'Egedal Gymnasium & HF'],
    [63,  u'Nordsjællands Grundskole og Gymnasium'],
    [71,  u'Greve Gymnasium'],
    [72,  u'Køge Gymnasium'],
    [73,  u'Roskilde Gymnasium'],
    [74,  u'Solrød Gymnasium'],
    [75,  u'Himmelev Gymnasium'],
    [76,  u'Roskilde Katedralskole'],
    [77,  u'Rungsted private Realskole'],
    [78,  u'Vestjysk Gymnasium Tarm'],
    [88,  u'Kriminalforsorgens Uddannelsescenter'],
    [91,  u'Midtsjællands Gymnasium'],
    [92,  u'Kalundborg Gymnasium og HF'],
    [93,  u'Slagelse Gymnasium'],
    [94,  u'Sorø Akademis Skole'],
    [95,  u'Stenhus Gymnasium og HF'],
    [96,  u'Odsherreds Gymnasium'],
    [97,  u'Høng Gymnasium og HF'],
    [111, u'Herlufsholm Skole'],
    [112, u'Maribo Gymnasium'],
    [114, u'Nykøbing Katedralskole'],
    [115, u'Næstved Gymnasium og HF'],
    [116, u'Vordingborg Gymnasium & HF'],
    [121, u'Aarhus Handelsgymnasium - Viby'],
    [122, u'Aarhus Handelsgymnasium - Vejlby'],
    [131, u'Køge Handelsgymnasium'],
    [133, u'Campus Bornholm HHX & HTX'],
    [135, u'Paul Petersens Idrætsinstitut'],
    [137, u'Campus Bornholm STX & HF'],
    [141, u'Middelfart Gymnasium'],
    [143, u'Mulernes Legatskole'],
    [144, u'Nyborg Gymnasium'],
    [148, u'Vestfyns Gymnasium'],
    [150, u'Faaborg Gymnasium'],
    [152, u'Oure Kostgymnasium'],
    [153, u'Skolerne i Oure Sport & Performance'],
    [155, u'ZBC Vordingborg EUD'],
    [156, u'ZBC Næstved'],
    [157, u'ZBC EUD'],
    [158, u'ZBC Ringsted'],
    [159, u'ZBC Ringsted EUD'],
    [160, u'ZBC Vordingborg'],
    [161, u'Alssundgymnasiet Sønderborg'],
    [162, u'Deutsches Gymnasium für Nordschleswig'],
    [163, u'Haderslev Katedralskole'],
    [164, u'Sønderborg Statsskole'],
    [166, u'Aabenraa Statsskole'],
    [181, u'Esbjerg Gymnasium'],
    [182, u'Rybners Gymnasium'],
    [184, u'Ribe Katedralskole'],
    [185, u'Varde Gymnasium og HF-kursus'],
    [186, u'Vejen Gymnasium og HF'],
    [201, u'Fredericia Gymnasium'],
    [202, u'Horsens Statsskole'],
    [203, u'Kolding Gymnasium'],
    [204, u'Rosborg Gymnasium og hf'],
    [205, u'Rødkilde Gymnasium'],
    [206, u'Vejlefjordskolen'],
    [207, u'Munkensdam Gymnasium'],
    [208, u'Tørring Gymnasium'],
    [209, u'Horsens Gymnasium'],
    [221, u'Herning Gymnasium'],
    [222, u'Holstebro Gymnasium og HF'],
    [223, u'Ikast-Brande Gymnasium'],
    [224, u'Struer Statsgymnasium'],
    [228, u'Det Kristne Gymnasium'],
    [238, u'K Nord Frederikssund'],
    [239, u'K Nord Hillerød'],
    [240, u'K Nord Lyngby'],
    [241, u'Grenaa Gymnasium'],
    [242, u'Langkaer Gymnasium/ HF/ IB World School'],
    [243, u'Marselisborg Gymnasium'],
    [245, u'Randers Statsskole'],
    [246, u'Risskov Gymnasium'],
    [247, u'Rønde Gymnasium'],
    [248, u'Silkeborg Gymnasium'],
    [249, u'Skanderborg Gymnasium'],
    [250, u'Viby Gymnasium'],
    [251, u'Aarhus Katedralskole'],
    [253, u'Paderup Gymnasium'],
    [254, u'Odder Gymnasium'],
    [256, u'Egaa Gymnasium'],
    [261, u'Morsø Gymnasium'],
    [262, u'Skive Gymnasium og HF'],
    [263, u'Thisted Gymnasium STX og HF'],
    [264, u'Viborg Gymnasium og HF'],
    [265, u'Viborg Katedralskole'],
    [266, u'Bjerringbro Gymnasium'],
    [281, u'Brønderslev Gymnasium og HF'],
    [282, u'Frederikshavn Gymnasium & HF-Kursus'],
    [283, u'Hasseris Gymnasium'],
    [284, u'Hjørring Gymnasium og HF'],
    [285, u'Mariagerfjord Gymnasium'],
    [286, u'Støvring Gymnasium'],
    [287, u'Nørresundby Gymnasium og HF'],
    [288, u'Vesthimmerlands Gymnasium og HF'],
    [289, u'Aalborg Katedralskole'],
    [290, u'Aalborghus Gymnasium'],
    [291, u'Fjerritslev Gymnasium'],
    [292, u'Dronninglund Gymnasium'],
    [304, u'Gentofte Studenterkursus'],
    [305, u'Learnmark Horsens Teknisk Gymnasium HTX'],
    [306, u'Learnmark Horsens Handelsgymnasium HHX'],
    [307, u'Studenterkurset i Sønderjylland'],
    [311, u'Århus Akademi'],
    [317, u'EUC NORD - HG'],
    [318, u'EUC NORD - HHX'],
    [319, u'EUC NORD - HTX Frederikshavn'],
    [320, u'EUC NORD - HTX Hjørring'],
    [345, u'Høje Taastrup Private Gymnasium'],
    [351, u'Frederiksberg HF-kursus'],
    [354, u'GU-Nuuk'],
    [355, u'Herning HF og VUC'],
    [360, u'Th. Langs HF & VUC'],
    [362, u'GU-Aasiaat'],
    [364, u'Campus Kujalleq'],
    [365, u'Gentofte HF'],
    [380, u'VUF - VoksenUddannelsescenter Frederiksberg'],
    [402, u'Nakskov Gymnasium og HF'],
    [411, u'VUC.nu'],
    [427, u'Teknisk Gymnasium Sønderjylland'],
    [454, u'HF & VUC København Syd, Amager afd.'],
    [455, u'HF & VUC København Syd, Hvidovre afd.'],
    [477, u'Svendborg Gymnasium og HF'],
    [483, u'Kværs Idræts Friskole'],
    [484, u'Københavns Private Gymnasium'],
    [500, u'SDU, Teoretisk Pædagogikum'],
    [501, u'K Nord Lyngby Erhvervsuddannelser'],
    [508, u'UCH Handelsgymnasium'],
    [509, u'UCH Teknisk Gymnasium'],
    [511, u'Handelsgymnasiet Vestfyn'],
    [513, u'Nordfyns Gymnasium'],
    [517, u'EUX Rødovre - Københavns Tekniske Skole'],
    [518, u'HTX Sukkertoppen - Københavns Tekniske Gymnasium'],
    [519, u'HTX Vibenhus - Københavns Tekniske Gymnasium'],
    [522, u'Roskilde Tekniske Skole - EUD'],
    [523, u'Roskilde Tekniske Gymnasium'],
    [524, u'Aalborg Tekniske Gymnasium'],
    [526, u'Læreruddannelsen i Silkeborg'],
    [529, u'Erhvervsskolerne Aars, hhx og htx'],
    [530, u'Københavns VUC'],
    [531, u'Søværnets Officersskole'],
    [532, u'HF & VUC Nordsjælland Helsingør'],
    [533, u'HF & VUC Nordsjælland Hillerød'],
    [534, u'Erhvervsskolerne Aars, KHF'],
    [536, u'VUC Vestegnen'],
    [537, u'VUC Lyngby'],
    [539, u'GUX - Sisimiut'],
    [541, u'Holbæk Handelsskole'],
    [542, u'VUC Vestsjælland Nord'],
    [544, u'Hou Maritime Idrætsefterskole'],
    [551, u'Aalborg Handelsskole - Saxogade'],
    [552, u'Aalborg Handelsskole - Turøgade'],
    [553, u'TietgenSkolen'],
    [555, u'Viborg Handelsgymnasium'],
    [556, u'Viborg Tekniske Gymnasium'],
    [557, u'Slotshaven Gymnasium'],
    [558, u'Skanderborg-Odder Center for uddannelse HG'],
    [560, u'Skanderborg-Odder Center for uddannelse HF & VUC'],
    [562, u'Skive Handelsskole'],
    [563, u'Skanderborg-Odder Center for uddannelse HHX'],
    [564, u'Tornbjerg Gymnasium'],
    [565, u'Vejle Handelsskole'],
    [566, u'Tradium, Minervavej'],
    [567, u'Tradium, Mariagerfjord'],
    [568, u'Folkekirkens Uddannelses- og Videnscenter'],
    [569, u'Skanderborg-Odder Center for uddannelse HTX SOCU'],
    [571, u'Tradium, Rådmands Boulevard'],
    [572, u'Tradium, Vester Allé'],
    [590, u'Sct. Knuds Gymnasium'],
    [600, u'Odense Katedralskole'],
    [627, u'Aarhus Private Gymnasium'],
    [641, u'Viden Djurs - VID Gymnasier'],
    [645, u'Akademisk Studenterkursus'],
    [669, u'UCN, Teknologi og Business'],
    [677, u'EUC Sjælland - HTX Køge'],
    [678, u'EUC Sjælland - HTX Næstved'],
    [679, u'H.C. Ørsted Gymnasiet - Frederiksberg'],
    [680, u'H.C. Ørsted Gymnasiet - Ballerup'],
    [681, u'H.C. Ørsted Gymnasiet - Lyngby'],
    [764, u'Skive Teknisk Gymnasium'],
    [765, u'HTX Gastro-science'],
    [768, u'Allikelund Gymnasium'],
    [771, u'Idrætsefterskolen Klintsøgaard'],
    [777, u'Hvidovre Kommune'],
    [782, u'UCVest'],
    [802, u'VIA Holstebro Pædagoguddannelsen'],
    [803, u'Peqqissaanermik Ilinniarfik, Nuuk'],
    [853, u'10 KCD'],
    [857, u'Odense Tekniske Gymnasium'],
    [877, u'Læreruddannelsen i Skive'],
    [902, u'Varde Handelsskole og Handelsgymnasium'],
    [914, u'Randlevskolen'],
    [917, u'Frederikshavn Handelsgymnasium'],
    [932, u'Køge Private Realskole, Gymnasium'],
    [941, u'IBC Aabenraa'],
    [942, u'IBC Fredericia Middelfart'],
    [943, u'IBC Kolding'],
    [945, u'Gram Efterskole'],
    [955, u'Midtfyns Gymnasium'],
    [988, u'Niuernermik Ilinniarfik, Nuuk'],
    [990, u'Forbedringsagentuddannelsen'],
    [992, u'ESNORD Gym - Erhvervsgymnasier Helsingør'],
    [993, u'ESNORD Gym - Teknisk Gymnasium Hillerød']
]

########################################################################################################

def convert(s):
    s = s.replace('&#39;',  u"'")
    s = s.replace('&#230;', u"æ")
    s = s.replace('&#248;', u"ø")
    s = s.replace('&#229;', u"å")
    s = s.replace('&#198;', u"Æ")
    s = s.replace('&#216;', u"Ø")
    s = s.replace('&#197;', u"Å")
    s = s.replace('&#233;', u"é")
    s = s.replace('&#180;', u"i")
    return s


# The Node class is used to construct the directory tree.
# It has the following variables:
# dir_name : Directory name
# dir_id   : The lectio ID
# dir_sub  : Does this directory have sub directories?
class Node(object):
    def __init__(self, dir_name, dir_id, dir_sub):
        self.dir_name = dir_name
        self.dir_id   = dir_id
        self.dir_sub  = dir_sub
        self.children = []

    def append(self, obj):
        self.children.append(obj)

    def print_rec(self, form, level=0):
        print form.format(level, self.dir_id, self.dir_sub, self.dir_name)
        for c in self.children:
            c.print_rec(form, level+1)


def isChildInTree(child, node):
    if node.dir_name == child.dir_name and \
       node.dir_id   == child.dir_id   :
        return True
    for c in node.children:
        if isChildInTree(child, c):
            return True
    return False


# This parses a page and reads the files. No recursion!
def readFiles(page, cookies, dir_name):
    global sumFiles
    global sumBytes 
    global sumDirs
    os.makedirs(dir_name)
    # Parse list
    id = page.split('documentid=')
    for i in range(1,len(id)):
        docid = id[i].split('"')[0]
        filnavn = id[i].split('&nbsp;')[1].split('</a>')[0].decode('cp850', 'ignore')
        fname = convert(dir_name + "/" + filnavn)
        logging.info(u"Læser dokument ID %s til %s", docid, fname)
        print u"Læser document ID", docid, "til", fname
        r = requests.get('https://www.lectio.dk/lectio/91/dokumenthent.aspx?documentid='+docid, \
                         cookies = cookies, verify = cafile)
        f = open(fname, "wb") # On windows, we must use binary mode.
        f.write(r.content)
        time.sleep(0.1) # Avoid stressing the servers at lectio.
        sumFiles += 1
        sumBytes += len(r.content)
    sumDirs += 1


# This reads the hidden form values from lines like:
# <input type="hidden" name="time" id="time" value="0" />
def getHiddenValues(page):
    vals = dict()
    s = page.split('"hidden"')
    for i in range(1,len(s)):
        fname = s[i].split("name=")
        if (len(fname) > 1):
            name = fname[1].split('"')[1]

            fval = s[i].split("value=")
            if (len(fval) > 1):
                value = fval[1].split('"')[1]

                vals[name] = value
    return vals


# Convert a string to a dictionary
def convertToDict(s):
    res = dict()
    for i in s.split(";"):
        (k, v) = i.split("=")
        k = k.strip()
        res[k] = v
    return res


# Now comes the hard part! We have to recursively descend through all the directories,
# by parsing the page returned from lectio.
# The function is called with a freshly loaded page.
# It will recursively descend into all sub directories.
# "fname" is the name of the expanded folder, if any.
# If set, only descend recursively through folders below this one.
def readRecursively(cookies, page, tid, node, path, readFrom=""):
    logging.info("readRecursively, dir_name=%s", node.dir_name)
    post_vars = getHiddenValues(page)
    if readFrom:
        fpage = page.split(readFrom)
        if len(fpage) < 2:
            print "Der opstod en fejl, se i filen log.txt"
            logging.error("readFrom: ======")
            logging.error(readFrom)
            logging.error("------")
            logging.error("len(fpage) = %s", len(fpage))
            logging.error("------")
            logging.error("page: -----")
            logging.error(page)
            logging.error("======")
            print "Vi stopper nu."
            os._exit(1)
        page = fpage[-1]

    id = page.split('lectio/img')
    logging.info("len(id)=%s", len(id))
    for i in range(1,len(id)):
        fdir = id[i].split("TREECLICKED")
        if len(fdir) > 1:
            dir_id = "TREECLICKED" + fdir[1].split('&')[0]
            dir_name = fdir[1].split('">')[1].split('<')[0]
            expand = "Expand" in id[i-1]
            child = Node(dir_name, dir_id, expand)
            if isChildInTree(child, root) and i == 1:
                logging.info("Skipping %s", dir_name)
                continue
            if isChildInTree(child, root) and i != 1:
                logging.info("Returning, found %s", dir_name)
                break
            logging.info("Adding node {0:38} : {1:2} : {2}".format(dir_id, expand, dir_name))
            node.append(child)

    # Loop through all children of node
    logging.info("len(node.children)=%s", len(node.children))
    for child in node.children:
        post_vars.update({"__EVENTTARGET": "__Page", "__EVENTARGUMENT": child.dir_id})
        r = requests.post('https://www.lectio.dk/lectio/91/DokumentOversigt.aspx?laererid='+tid,
                cookies = cookies, data = post_vars, verify = cafile)
        fullname = child.dir_name
        fname = r.content.split('FolderCommentsLabel">Mappenavn: ')
        if len(fname) > 1:
            fullname = fname[-1].split("\n")[0]
        newpath = convert(path + "/" + fullname)
        logging.info("Reading files from {0:38} : {1:2} : {2}".format(child.dir_id, child.dir_sub, newpath))
        readFiles(r.content, cookies, newpath)
        if child.dir_sub:
            readFrom = '"Collapse ' + child.dir_name.replace('&', '&amp;') + '"'
            readRecursively(cookies, r.content, tid, child, newpath, readFrom)


########################################################################################################

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', filename='log.txt')

print u"Velkommen!"
print u"Dette lille program vil hente alle dine dokumenter fra lectio og gemme på din computer mappen '"+BASEDIR+"'."
print u"P.t. bliver opgaver og lectier ikke gemt. Kun det som findes under Dokumenter bliver gemt."
print

if os.path.isdir(BASEDIR):
    print u"Fejl!"
    print u"Der findes allerede en mappe med navnet '"+BASEDIR+"'"
    print u"Du skal først fjerne eller omdøbe denne mappe, og så genstarte dette program"
    os._exit(1)

print u"Du skal først skrive navnet på din skole og verificere dette. Dernæst vil programmet"
print u"bede om dit brugernavn og dit kodeord til lectio. Hvis du vil, så kan du gå ind på "
print u"lectio og ændre dit kodeord til en ny midlertidig kode."
print

print u"Indtast navnet på din skole:",
skole = raw_input().rstrip().decode('utf-8', 'ignore')

navne = map(list, zip(*skoler_liste))[1] # Dette er en liste af alle skolers navne.

skole_korr_liste = difflib.get_close_matches(skole, navne)
if (len(skole_korr_liste) == 0):
    print u"Jeg kunne ikke finde nogen skole med det navn."
    print u"Vi stopper her."
    print u"Prøv at starte programmet forfra."
    os._exit(1)

skole_korr = skole_korr_liste[0]

if (skole != skole_korr):
    # Skolenavnet passede ikke 100 %, få brugerens bekræftelse
    print u"Mente du: " + skole_korr + " (j/n)?",
    bek = raw_input()
    if (not bek[0] in ('j', 'J', 'y', 'Y')):
        print u"Ok, vi stopper her."
        print u"Prøv at starte programmet forfra."
        os._exit(1)


skole_index = navne.index(skole_korr)
lectio_nummer = skoler_liste[skole_index][0]

print
print u"Ok. Du har valgt ", skole_korr
print u"Nu skal du indtaste dit brugernavn og kodeord til lectio."
print

teacher  = raw_input("Lectio brugernavn: ").rstrip()
password = getpass.getpass("Lectio kodeord: ")

print
print u"Ok. Jeg prøver nu at logge ind som " + teacher + " med det angivne brugernavn"

# Get session data
s = requests.Session()
r = s.get('https://www.lectio.dk/lectio/91/login.aspx', verify = cafile)
session = getHiddenValues(r.content)

# Login
payload = dict([
    ("__EVENTTARGET",       "m$Content$submitbtn2"),
    ("__EVENTARGUMENT",     ""),
    ("m$Content$username2", teacher),
    ("m$Content$passwordHidden", password)])
payload.update(session)
r = s.post('https://www.lectio.dk/lectio/' + str(lectio_nummer) + '/login.aspx', \
               data=payload, verify = cafile)

# Get teacher ID
ftid = r.content.split('laererid=',1)
if len(ftid) == 1:
    print u"Det var ikke muligt at logge ind."
    print u"Det er sandsynligvis fejl i brugernavn og/eller kodeord."
    print u"Vi stopper her."
    print u"Prøv at starte programmet forfra."
    os._exit(1)

tid = r.content.split('laererid=',1)[1].split('"')[0]
print u"Jeg er nu logget ind på lectio som " + teacher + "."
print

logging.info(u"Logget på %s med brugernavn %s", skole_korr, teacher)

# Convert session cookie to a dictionary
c = r.request.headers['Cookie']
cookies = convertToDict(c)

# Get list of documents
r = requests.get('https://www.lectio.dk/lectio/91/DokumentOversigt.aspx?laererid='+tid, \
                 cookies = cookies, verify = cafile)
root = Node('Root', '', True)

t1 = time.time()
readRecursively(cookies, r.content, tid, root, BASEDIR, 'newdocs')
t2 = time.time()

minutter = int((t2-t1)/60) # Udregn den brugte tid i minutter

# Udskriv afsluttende statistik

print
print u"Færdig!"
print u"Du har nu hentet i alle dine dokumenter ned fra lectio."
print u"De ligger alle i mappen '"+BASEDIR+"'."
print 
print u"Lidt statistik:"
print u"Du har hentet i alt:", repr(sumFiles).rjust(4), "filer"
print u"Fordelt på i alt:   ", repr(sumDirs).rjust(4), "mapper"
print u"Tilsammen fylder de:", repr(sumBytes/1024/1024).rjust(4), "MB"
print u"Tid brugt i alt:    ", repr(minutter).rjust(4), "minutter"
print
print u"Slut!"

