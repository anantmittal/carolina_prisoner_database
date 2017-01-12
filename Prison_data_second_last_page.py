from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import pandas as pd
import urllib2

''' Converting .dta to .csv
data = pd.io.stata.read_stata('Comuna3_id.dta')
data.to_csv('list_of_ids.csv')
exit()
'''

## Global variables
# Links for page of each juzgado
links_j = [
         "http://procesos.ramajudicial.gov.co/jepms/medellinjepms/conectar.asp"]

# Location of every piece of information
places = [[1, 3], [1, 4], [1, 5], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14],
          [13,1],[13,6],[13,7],[13,8],[13,9],[13,10],[13,11],[13,12],[13,13],[13,14],[13,15],[13,16],[13,17],[13,19]]

# Variable names to be written into file (fix later.. or not?)
varnames="ID\t"



for i in xrange(1, len(places)+1):
    if i != len(places):
        varnames += "var_" + str(i) + "\t"
    else:
        varnames += "var_" + str(i) + "\n"

print varnames
## Functions
def get_links(link, id_number):
    '''
    Takes a link to the page and an id number.
    Returns a list of links for every page related to the given id number.
    '''
    if id_number=="":
        return []
    
    br = Browser()
    br.open(link)

    br.form = list(br.forms())[0]  

    if id_number!="": # If we have id number
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

    return links

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
            if coords[1] >= 6 and coords[1] <= 19 and coords[0] == 13:
                data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].find('input').get('value'))
            else:
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

# Get ids out of file
lines = [line.rstrip('\r\n').split('\t') for line in open('comunaid_small.csv', 'r')]
id_numbers = [lines[j][0] for j in xrange(1, len(lines))]

# Get links to pages for last name and every juzgado
links_page = []

# Get data from each link
data_text = ""

# This list will store all links that did not work, so that I can check them manually later
links_page2 = ""

# Writing the data to file
fw = open("Prison_second_last_form_data.txt", 'w')
fw.write(varnames) # Write variable names

#Writing left out links to a file
fw2 = open("Prison_second_last_form_corrupt_or_internal_server_error_links.txt", 'w')



counter = 1
for l_j in links_j:
    for id_number in id_numbers:
        links = get_links(l_j, id_number=id_number)
        for link in links:
            try:
                data_text = str(id_number)+"\t"+get_data(link)
                fw.write(data_text)
                print counter
                counter += 1
                add = 0
            except:
                add = 1

            if add:
                links_page2 = str(link) + "\n"
                fw2.write(links_page2)
                remove = 0

fw.close()
fw2.close()
print "Done!"
