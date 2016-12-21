from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import pandas as pd
import urllib2

## Global variables
# Links for page of each juzgado
links_j = [ "http://procesos.ramajudicial.gov.co/jepms/armeniajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/bogotajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/bucaramangajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/bugajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/florenciajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/ibaguejepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/manizalesjepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/medellinjepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/neivajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/palmirajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/pastojepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/pereirajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/popayanjepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/calijepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/tunjajepms/conectar.asp",
         "http://procesos.ramajudicial.gov.co/jepms/villavicenciojepms/conectar.asp"]

# Location of every piece of information
places = [[1, 3], [1, 4], [1, 5], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [7, 1], [7, 3], [7, 5], [7, 7],
          [7, 9], [7, 11], [7, 13], [7, 15], [7, 17], [7, 19], [7, 21], [7, 23], [9, 5], [9, 8], [9, 9], [9, 10], [9, 11], 
          [9, 12], [10, 1], [10, 2], [11, 1], [12, 2], [12, 4], [12, 6], [12, 8], [12, 11], [12, 13], [12, 15], [12, 17], 
          [14, 12], [14, 13], [14, 14], [14, 15], [14, 16], [14, 17], [14, 18], [14, 19], [14, 21], [14, 22], [14, 23], 
          [14, 24], [14, 25], [14, 26], [14, 27], [14, 28], [15, 2], [15, 5], [15, 10], [15, 13], [15, 16], [15, 18], [15, 19],
          [15, 20], [15, 21], [15, 23], [15, 26], [15, 28], [15, 29], [15, 30], [15, 31], [15, 33], [15, 35], [15, 37], [15, 38],
          [15, 39], [15, 40], [15, 42], [15, 44], [15, 46], [15, 49], [15, 51], [15, 53], [15, 54], [15, 55], [15, 57], [15, 59],
          [15, 61], [15, 63], [15, 65], [15, 72], [15, 74], [15, 76], [15, 77], [15, 78], [15, 79], [15, 82], [15, 84]]

# Variable names to be written into file (fix later.. or not?)
varnames=""
for i in xrange(1, len(places)+1):
    if i != len(places):
        varnames += "var_" + str(i) + "\t"
    else:
        varnames += "var_" + str(i) + "\n"


## Functions
def get_links(link="", name="", id_number=""):
    '''
    Takes a link to the page and a last name or an id number.
    Returns a list of links for every page related to the given
    last name or id number.
    '''

    if id_number=="" and name=="":
        return []
    
    br = Browser()
    br.open(link)

    br.form = list(br.forms())[0]  

    if id_number=="" and name!="": # If we have last name
        control = br.form.find_control("norad")
        if control.type == "text":  # make sure it is the right one
            control.value = name
    
    if id_number!="" and name=="": # If we have id number 
        control = br.form.find_control("cbadju")
        if control.type == "select":  # make sure it is the right one
            control.value = ['3']
        
        control = br.form.find_control("norad")
        if control.type == "text":  # make sure it is the right one
            control.value = id_number

    response = br.submit()

    soup2 = BeautifulSoup(response)
    links = [] # This will store the links that appear after the first search
    for l in br.links():
        l2 = l.absolute_url
        if l2 != "http://www.ramajudicial.gov.co": #Not useful
            links.append(l2)

    links2=[] # This will store the final link, the one we are actually interested in
    for link in links:
        br.open(link)
        for l in br.links():
            links2.append(l.absolute_url)

    return links2

def get_data(link):
    '''
    This function takes the link to the webpage and 
    collects the data
    '''
    page = urllib2.urlopen(link).read()
    soup = BeautifulSoup(page)

    data = [] # I will start storing the data in a list and then convert to text

    for coords in places: # Places is a list of the position of each piece of information
        try:
            data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].text)
        except:
            pass
        
    data_text = "" # I will convert data to text so it can be directly written into the file
    for i, dat in enumerate(data):
        if i != len(data) - 1:
            #print "not last"
            data_text += dat.encode('utf-8') + "\t"
        else:
            data_text += dat.encode('utf-8') + "\n"
            
    return data_text


## Creating the data file

# Name of the datafile        
title = "Prison_data"        
k = 1 + 1 # So that I can have different versions
title_new = title + "_" + str(k) +".txt"

# Get names out of file
lines = [line.rstrip('\n').split('\t') for line in open('names.txt', 'r')] 
# names.txt is a tab delimited file that has last names and id numbers in columns 2 and 3
#           and starts in the second row (first row has variable names).



apellidos = [lines[j][1] for j in xrange(1, len(lines))]
id_numbers = [lines[j][2] for j in xrange(1, len(lines))]

# Get links to pages for last name and every juzgado
links_page = []
for l_j in links_j:
    for apellido in apellidos:
        links_page += get_links(l_j, name=apellido, id_number="")
    for id_number in id_numbers:
        links_page += get_links(l_j, name="", id_number=id_number)

links_page = list(set(links_page)) # Remove duplicates


with open('links.txt', 'w') as f_links: # Write a file with each webpage address we will use, so that we can skip the steps above if needed.
    for link in links_page:
        f_links.write("%s\n" % link)

# Get data from each link
data_text = ""
links_page2 = [] # This list will store all links that did not work, so that I can check them manually later
for link in links_page:
    links_page2.append(link)
    try:
        data_text += get_data(link)
        remove = 1
    except:
        remove = 0
    
    if remove:
        links_page2.remove(link)
        remove = 0

# Writing the data to file
fw = open(title_new, 'w')
fw.write(varnames) # Write variable names

fw.write(data_text) # Write data
fw.close()

print "Done!"
