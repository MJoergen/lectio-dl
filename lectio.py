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
    [1,   'Aurehøj Gymnasium'],
    [2,   'Hvidovre Gymnasium og HF'],
    [3,   'Bagsværd Kostskole og Gymnasium'],
    [5,   'Christianshavns Gymnasium'],
    [6,   'HF-Centret Efterslægten'],
    [7,   'Falkonergårdens Gymnasium og HF'],
    [8,   'Frederiksberg Gymnasium'],
    [9,   'Gammel Hellerup Gymnasium'],
    [11,  'Gladsaxe Gymnasium'],
    [12,  'Herlev Gymnasium og HF'],
    [13,  'Ingrid Jespersens Gymnasieskole'],
    [14,  'Ingrid Jespersens Grundskole'],
    [15,  'Johannesskolens Grundskole'],
    [16,  'Johannesskolens Gymnasium'],
    [17,  'Gefion Gymnasium'],
    [19,  'N. Zahles Gymnasieskole'],
    [20,  'Niels Steensens Gymnasium'],
    [21,  'Nørre Gymnasium'],
    [22,  'Ordrup Gymnasium'],
    [23,  'Rysensteen Gymnasium'],
    [24,  'Rødovre Gymnasium'],
    [25,  'Sankt Annæ Gymnasium'],
    [26,  'Ørestad Gymnasium'],
    [30,  'Tårnby Gymnasium'],
    [31,  'Nærum Gymnasium'],
    [32,  'Københavns åbne Gymnasium'],
    [33,  'Virum Gymnasium'],
    [34,  'Øregård Gymnasium'],
    [36,  'Høje-Taastrup Gymnasium'],
    [37,  'Borupgaard Gymnasium'],
    [38,  'Brøndby Gymnasium'],
    [40,  'Det frie Gymnasium'],
    [43,  'CPH WEST - Albertslund Gymnasium & HF'],
    [44,  'CPH WEST - hhx, Ishøj og CPH10'],
    [45,  'CPH WEST - HTX, Albertslund - ATG'],
    [46,  'CPH WEST - htx, Ishøj'],
    [47,  'CPH WEST - Ishøj Gymnasium'],
    [48,  'CPH WEST Handelsgymnasiet i Ballerup'],
    [51,  'Allerød Gymnasium'],
    [52,  'Birkerød Gymnasium og HF'],
    [53,  'Helsingør Gymnasium'],
    [54,  'Frederiksborg Gymnasium og hf'],
    [55,  'Frederikssund Gymnasium'],
    [57,  'Espergærde Gymnasium og HF'],
    [58,  'Marie Kruses Skole'],
    [59,  'Rungsted Gymnasium'],
    [60,  'Frederiksværk Gymnasium og HF'],
    [61,  'Gribskov Gymnasium'],
    [62,  'Egedal Gymnasium & HF'],
    [63,  'Nordsjællands Grundskole og Gymnasium'],
    [71,  'Greve Gymnasium'],
    [72,  'Køge Gymnasium'],
    [73,  'Roskilde Gymnasium'],
    [74,  'Solrød Gymnasium'],
    [75,  'Himmelev Gymnasium'],
    [76,  'Roskilde Katedralskole'],
    [77,  'Rungsted private Realskole'],
    [78,  'Vestjysk Gymnasium Tarm'],
    [88,  'Kriminalforsorgens Uddannelsescenter'],
    [91,  'Midtsjællands Gymnasium'],
    [92,  'Kalundborg Gymnasium og HF'],
    [93,  'Slagelse Gymnasium'],
    [94,  'Sorø Akademis Skole'],
    [95,  'Stenhus Gymnasium og HF'],
    [96,  'Odsherreds Gymnasium'],
    [97,  'Høng Gymnasium og HF'],
    [111, 'Herlufsholm Skole'],
    [112, 'Maribo Gymnasium'],
    [114, 'Nykøbing Katedralskole'],
    [115, 'Næstved Gymnasium og HF'],
    [116, 'Vordingborg Gymnasium & HF'],
    [121, 'Aarhus Handelsgymnasium - Viby'],
    [122, 'Aarhus Handelsgymnasium - Vejlby'],
    [131, 'Køge Handelsgymnasium'],
    [133, 'Campus Bornholm HHX & HTX'],
    [135, 'Paul Petersens Idrætsinstitut'],
    [137, 'Campus Bornholm STX & HF'],
    [141, 'Middelfart Gymnasium'],
    [143, 'Mulernes Legatskole'],
    [144, 'Nyborg Gymnasium'],
    [148, 'Vestfyns Gymnasium'],
    [150, 'Faaborg Gymnasium'],
    [152, 'Oure Kostgymnasium'],
    [153, 'Skolerne i Oure Sport & Performance'],
    [155, 'ZBC Vordingborg EUD'],
    [156, 'ZBC Næstved'],
    [157, 'ZBC EUD'],
    [158, 'ZBC Ringsted'],
    [159, 'ZBC Ringsted EUD'],
    [160, 'ZBC Vordingborg'],
    [161, 'Alssundgymnasiet Sønderborg'],
    [162, 'Deutsches Gymnasium für Nordschleswig'],
    [163, 'Haderslev Katedralskole'],
    [164, 'Sønderborg Statsskole'],
    [166, 'Aabenraa Statsskole'],
    [181, 'Esbjerg Gymnasium'],
    [182, 'Rybners Gymnasium'],
    [184, 'Ribe Katedralskole'],
    [185, 'Varde Gymnasium og HF-kursus'],
    [186, 'Vejen Gymnasium og HF'],
    [201, 'Fredericia Gymnasium'],
    [202, 'Horsens Statsskole'],
    [203, 'Kolding Gymnasium'],
    [204, 'Rosborg Gymnasium og hf'],
    [205, 'Rødkilde Gymnasium'],
    [206, 'Vejlefjordskolen'],
    [207, 'Munkensdam Gymnasium'],
    [208, 'Tørring Gymnasium'],
    [209, 'Horsens Gymnasium'],
    [221, 'Herning Gymnasium'],
    [222, 'Holstebro Gymnasium og HF'],
    [223, 'Ikast-Brande Gymnasium'],
    [224, 'Struer Statsgymnasium'],
    [228, 'Det Kristne Gymnasium'],
    [238, 'K Nord Frederikssund'],
    [239, 'K Nord Hillerød'],
    [240, 'K Nord Lyngby'],
    [241, 'Grenaa Gymnasium'],
    [242, 'Langkaer Gymnasium/ HF/ IB World School'],
    [243, 'Marselisborg Gymnasium'],
    [245, 'Randers Statsskole'],
    [246, 'Risskov Gymnasium'],
    [247, 'Rønde Gymnasium'],
    [248, 'Silkeborg Gymnasium'],
    [249, 'Skanderborg Gymnasium'],
    [250, 'Viby Gymnasium'],
    [251, 'Aarhus Katedralskole'],
    [253, 'Paderup Gymnasium'],
    [254, 'Odder Gymnasium'],
    [256, 'Egaa Gymnasium'],
    [261, 'Morsø Gymnasium'],
    [262, 'Skive Gymnasium og HF'],
    [263, 'Thisted Gymnasium STX og HF'],
    [264, 'Viborg Gymnasium og HF'],
    [265, 'Viborg Katedralskole'],
    [266, 'Bjerringbro Gymnasium'],
    [281, 'Brønderslev Gymnasium og HF'],
    [282, 'Frederikshavn Gymnasium & HF-Kursus'],
    [283, 'Hasseris Gymnasium'],
    [284, 'Hjørring Gymnasium og HF'],
    [285, 'Mariagerfjord Gymnasium'],
    [286, 'Støvring Gymnasium'],
    [287, 'Nørresundby Gymnasium og HF'],
    [288, 'Vesthimmerlands Gymnasium og HF'],
    [289, 'Aalborg Katedralskole'],
    [290, 'Aalborghus Gymnasium'],
    [291, 'Fjerritslev Gymnasium'],
    [292, 'Dronninglund Gymnasium'],
    [304, 'Gentofte Studenterkursus'],
    [305, 'Learnmark Horsens Teknisk Gymnasium HTX'],
    [306, 'Learnmark Horsens Handelsgymnasium HHX'],
    [307, 'Studenterkurset i Sønderjylland'],
    [311, 'Århus Akademi'],
    [317, 'EUC NORD - HG'],
    [318, 'EUC NORD - HHX'],
    [319, 'EUC NORD - HTX Frederikshavn'],
    [320, 'EUC NORD - HTX Hjørring'],
    [345, 'Høje Taastrup Private Gymnasium'],
    [351, 'Frederiksberg HF-kursus'],
    [354, 'GU-Nuuk'],
    [355, 'Herning HF og VUC'],
    [360, 'Th. Langs HF & VUC'],
    [362, 'GU-Aasiaat'],
    [364, 'Campus Kujalleq'],
    [365, 'Gentofte HF'],
    [380, 'VUF - VoksenUddannelsescenter Frederiksberg'],
    [402, 'Nakskov Gymnasium og HF'],
    [411, 'VUC.nu'],
    [427, 'Teknisk Gymnasium Sønderjylland'],
    [454, 'HF & VUC København Syd, Amager afd.'],
    [455, 'HF & VUC København Syd, Hvidovre afd.'],
    [477, 'Svendborg Gymnasium og HF'],
    [483, 'Kværs Idræts Friskole'],
    [484, 'Københavns Private Gymnasium'],
    [500, 'SDU, Teoretisk Pædagogikum'],
    [501, 'K Nord Lyngby Erhvervsuddannelser'],
    [508, 'UCH Handelsgymnasium'],
    [509, 'UCH Teknisk Gymnasium'],
    [511, 'Handelsgymnasiet Vestfyn'],
    [513, 'Nordfyns Gymnasium'],
    [517, 'EUX Rødovre - Københavns Tekniske Skole'],
    [518, 'HTX Sukkertoppen - Københavns Tekniske Gymnasium'],
    [519, 'HTX Vibenhus - Københavns Tekniske Gymnasium'],
    [522, 'Roskilde Tekniske Skole - EUD'],
    [523, 'Roskilde Tekniske Gymnasium'],
    [524, 'Aalborg Tekniske Gymnasium'],
    [526, 'Læreruddannelsen i Silkeborg'],
    [529, 'Erhvervsskolerne Aars, hhx og htx'],
    [530, 'Københavns VUC'],
    [531, 'Søværnets Officersskole'],
    [532, 'HF & VUC Nordsjælland Helsingør'],
    [533, 'HF & VUC Nordsjælland Hillerød'],
    [534, 'Erhvervsskolerne Aars, KHF'],
    [536, 'VUC Vestegnen'],
    [537, 'VUC Lyngby'],
    [539, 'GUX - Sisimiut'],
    [541, 'Holbæk Handelsskole'],
    [542, 'VUC Vestsjælland Nord'],
    [544, 'Hou Maritime Idrætsefterskole'],
    [551, 'Aalborg Handelsskole - Saxogade'],
    [552, 'Aalborg Handelsskole - Turøgade'],
    [553, 'TietgenSkolen'],
    [555, 'Viborg Handelsgymnasium'],
    [556, 'Viborg Tekniske Gymnasium'],
    [557, 'Slotshaven Gymnasium'],
    [558, 'Skanderborg-Odder Center for uddannelse HG'],
    [560, 'Skanderborg-Odder Center for uddannelse HF & VUC'],
    [562, 'Skive Handelsskole'],
    [563, 'Skanderborg-Odder Center for uddannelse HHX'],
    [564, 'Tornbjerg Gymnasium'],
    [565, 'Vejle Handelsskole'],
    [566, 'Tradium, Minervavej'],
    [567, 'Tradium, Mariagerfjord'],
    [568, 'Folkekirkens Uddannelses- og Videnscenter'],
    [569, 'Skanderborg-Odder Center for uddannelse HTX SOCU'],
    [571, 'Tradium, Rådmands Boulevard'],
    [572, 'Tradium, Vester Allé'],
    [590, 'Sct. Knuds Gymnasium'],
    [600, 'Odense Katedralskole'],
    [627, 'Aarhus Private Gymnasium'],
    [641, 'Viden Djurs - VID Gymnasier'],
    [645, 'Akademisk Studenterkursus'],
    [669, 'UCN, Teknologi og Business'],
    [677, 'EUC Sjælland - HTX Køge'],
    [678, 'EUC Sjælland - HTX Næstved'],
    [679, 'H.C. Ørsted Gymnasiet - Frederiksberg'],
    [680, 'H.C. Ørsted Gymnasiet - Ballerup'],
    [681, 'H.C. Ørsted Gymnasiet - Lyngby'],
    [764, 'Skive Teknisk Gymnasium'],
    [765, 'HTX Gastro-science'],
    [768, 'Allikelund Gymnasium'],
    [771, 'Idrætsefterskolen Klintsøgaard'],
    [777, 'Hvidovre Kommune'],
    [782, 'UCVest'],
    [802, 'VIA Holstebro Pædagoguddannelsen'],
    [803, 'Peqqissaanermik Ilinniarfik, Nuuk'],
    [853, '10 KCD'],
    [857, 'Odense Tekniske Gymnasium'],
    [877, 'Læreruddannelsen i Skive'],
    [902, 'Varde Handelsskole og Handelsgymnasium'],
    [914, 'Randlevskolen'],
    [917, 'Frederikshavn Handelsgymnasium'],
    [932, 'Køge Private Realskole, Gymnasium'],
    [941, 'IBC Aabenraa'],
    [942, 'IBC Fredericia Middelfart'],
    [943, 'IBC Kolding'],
    [945, 'Gram Efterskole'],
    [955, 'Midtfyns Gymnasium'],
    [988, 'Niuernermik Ilinniarfik, Nuuk'],
    [990, 'Forbedringsagentuddannelsen'],
    [992, 'ESNORD Gym - Erhvervsgymnasier Helsingør'],
    [993, 'ESNORD Gym - Teknisk Gymnasium Hillerød']
]

########################################################################################################

def convert(s):
    s = s.replace('&#39;',  "'")
    s = s.replace('&#230;', "æ")
    s = s.replace('&#248;', "ø")
    s = s.replace('&#229;', "å")
    s = s.replace('&#198;', "Æ")
    s = s.replace('&#216;', "Ø")
    s = s.replace('&#197;', "Å")
    s = s.replace('&#233;', "é")
    s = s.replace('&#180;', "i")
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
        filnavn = id[i].split('&nbsp;')[1].split('</a>')[0]
        fname = convert(dir_name + "/" + filnavn)
        logging.info("Læser dokument ID %s til %s", docid, fname)
        print "Læser document ID", docid, "til", fname
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
    logging.info("readRecursively, dir_name=%d", node.dir_name)
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

print "Velkommen!"
print "Dette lille program vil hente alle dine dokumenter fra lectio og gemme på din computer mappen '"+BASEDIR+"'."
print "P.t. bliver opgaver og lectier ikke gemt. Kun det som findes under Dokumenter bliver gemt."
print

if os.path.isdir(BASEDIR):
    print "Fejl!"
    print "Der findes allerede en mappe med navnet '"+BASEDIR+"'"
    print "Du skal først fjerne eller omdøbe denne mappe, og så genstarte dette program"
    os._exit(1)

print "Du skal først skrive navnet på din skole og verificere dette. Dernæst vil programmet"
print "bede om dit brugernavn og dit kodeord til lectio. Hvis du vil, så kan du gå ind på "
print "lectio og ændre dit kodeord til en ny midlertidig kode."
print

skole = raw_input("Indtast navnet på din skole: ").rstrip()

navne = map(list, zip(*skoler_liste))[1] # Dette er en liste af alle skolers navne.

skole_korr_liste = difflib.get_close_matches(skole, navne)
if (len(skole_korr_liste) == 0):
    print "Jeg kunne ikke finde nogen skole med det navn."
    print "Vi stopper her."
    print "Prøv at starte programmet forfra."
    os._exit(1)

skole_korr = skole_korr_liste[0]

if (skole != skole_korr):
    # Skolenavnet passede ikke 100 %, få brugerens bekræftelse
    bek = raw_input("Mente du: " + skole_korr + " (j/n)? ")
    if (not bek[0] in ('j', 'J', 'y', 'Y')):
        print "Ok, vi stopper her."
        print "Prøv at starte programmet forfra."
        os._exit(1)


skole_index = navne.index(skole_korr)
lectio_nummer = skoler_liste[skole_index][0]

print
print "Ok. Du har valgt ", skole_korr
print "Nu skal du indtaste dit brugernavn og kodeord til lectio."
print

teacher  = raw_input("Lectio brugernavn: ").rstrip()
password = getpass.getpass("Lectio kodeord: ")

print
print "Ok. Jeg prøver nu at logge ind som " + teacher + " med det angivne brugernavn"

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
    print "Det var ikke muligt at logge ind."
    print "Det er sandsynligvis fejl i brugernavn og/eller kodeord."
    print "Vi stopper her."
    print "Prøv at starte programmet forfra."
    os._exit(1)

tid = r.content.split('laererid=',1)[1].split('"')[0]
print "Jeg er nu logget ind på lectio som " + teacher + "."
print

logging.info("Logget på %s med brugernavn %s", skole_korr, teacher)

# Convert session cookie to a dictionary
c = r.request.headers['Cookie']
cookies = convertToDict(c)

# Get list of documents
r = requests.get('https://www.lectio.dk/lectio/91/DokumentOversigt.aspx?laererid='+tid, \
                 cookies = cookies, verify = cafile)
root = Node('Root', '', True)

readRecursively(cookies, r.content, tid, root, BASEDIR, 'newdocs')

root.print_rec("{0} {1:38} : {2:2} : {3}")

# Udskriv afsluttende statistik

print "Tillykke!"
print "Du har nu hentet i alle dine dokumenter ned fra lectio."
print "De ligger i mappen '"+BASEDIR+"'."
print 
print "Lidt statistik:"
print "Du har hentet i alt", sumFiles, "filer"
print "Fordelt på i alt", sumDirs, "mapper"
print "Tilsammen i alt", sumBytes, "bytes"
print
print "Slut!"
