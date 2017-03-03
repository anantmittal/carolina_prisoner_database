from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import urllib2
import time

links_j = [ "http://procesos.ramajudicial.gov.co/jepms/florenciajepms/conectar.asp",
   ]

# Location of every piece of information
places_second = [[1, 3], [1, 4], [1, 5], [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14], [7, 1], [7, 3], [7, 5], [7, 7],
          [7, 9], [7, 11], [7, 13], [7, 15], [7, 17], [7, 19], [7, 21], [7, 23], [9, 5], [9, 8], [9, 9], [9, 10], [9, 11],
          [9, 12], [10, 1], [10, 2], [11, 1], [12, 2], [12, 4], [12, 6], [12, 8], [12, 11], [12, 13], [12, 15], [12, 17],
          [14, 12], [14, 13], [14, 14], [14, 15], [14, 16], [14, 17], [14, 18], [14, 19], [14, 21], [14, 22], [14, 23],
          [14, 24], [14, 25], [14, 26], [14, 27], [14, 28], [15, 0], [15, 2], [15, 5], [15, 10], [15, 13], [15, 16], [15, 18], [15, 19],
          [15, 20], [15, 21], [15, 23], [15, 26], [15, 28], [15, 29], [15, 30], [15, 31], [15, 33], [15, 35], [15, 37], [15, 38],
          [15, 39], [15, 40], [15, 42], [15, 44], [15, 46], [15, 49], [15, 51], [15, 53], [15, 54], [15, 55], [15, 57], [15, 59],
          [15, 61], [15, 63], [15, 65], [15, 72], [15, 74], [15, 76], [15, 77], [15, 78], [15, 79], [15, 82], [15, 84]]

places_first = [[1, 3], [1, 4], [1, 5],
                [3, 8], [3, 9], [3, 10], [3, 11], [3, 12], [3, 13], [3, 14],
                [7,2],[7,3],
                [9,1],[9,2],[9,3],[9,4],[9,5],[9,6],[9,7],[9,8],[9,9],[9,10],
                [10,1],[10,3],[10,5],[10,7],
                [13,1],[13,6],[13,7],[13,8],[13,9],[13,10],[13,11],[13,12],[13,13],[13,14],[13,15],[13,16],[13,17],[13,19],[15,1],[15,2]]


# Variable names to be written into file (fix later.. or not?)
varnames_first="ID\t"
varnames_second="ID\t"

for i in xrange(1, len(places_first)+1):
    if i != len(places_first):
        varnames_first += "var_" + str(i) + "\t"
    else:
        varnames_first += "var_" + str(i) + "\n"

for i in xrange(1, len(places_second) + 1):
    if i != len(places_second):
        varnames_second += "var_" + str(i) + "\t"
    else:
        varnames_second += "var_" + str(i) + "\n"


def get_data_first(link):
    '''
    This function takes the link to the webpage and
    collects the data
    '''

    page = urllib2.urlopen(link).read()
    soup = BeautifulSoup(page)
    data = []  # I will start storing the data in a list and then convert to text

    for coords in places_first:  # Places is a list of the position of each piece of information
        try:
            if coords[0] == 13 and coords[1] >= 6 and coords[1] <= 19:
                data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].find('input').get('value'))
            else:
                data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].text)
        except:
            pass

    data_text = ""  # I will convert data to text so it can be directly written into the file
    for i, dat in enumerate(data):
        if i != len(data) - 1:
            # print "not last"
            data_text += dat.encode('utf-8') + "\t"
        else:
            data_text += dat.encode('utf-8') + "\n"

    return data_text


def get_data_second(link):
    '''
    This function takes the link to the webpage and
    collects the data
    '''

    page = urllib2.urlopen(link).read()
    soup = BeautifulSoup(page)
    data = []  # I will start storing the data in a list and then convert to text

    for coords in places_second:  # Places is a list of the position of each piece of information
        try:
            if ((coords[0] == 9 and coords[1] >= 11 and coords[1] <= 12) or (coords[0] == 15 and coords[1] == 82)):
                data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].find('input').get('value'))
            else:
                data.append(soup.findAll("table")[coords[0]].findAll("td")[coords[1]].text)
        except:
            pass

    data_text = ""  # I will convert data to text so it can be directly written into the file
    for i, dat in enumerate(data):
        if i != len(data) - 1:
            # print "not last"
            data_text += dat.encode('utf-8') + "\t"
        else:
            data_text += dat.encode('utf-8') + "\n"

    return data_text


# Get ids out of file
lines = [line.rstrip('\r\n').split('\t') for line in open('florbc.csv', 'r')]
id_numbers = [lines[j][0] for j in xrange(1, len(lines))]

# Get data from each link
data_text = ""

# Writing the data to file
fw_first = open("FirstPrisonDataflorbc.csv", 'w')
fw_first_error = open("FirstPrisonData_ERRORflorbc.csv", 'w')
fw_first.write(varnames_first) # Write variable names

fw_second = open("SecondPrisonDataflorbc.csv", 'w')
fw_second_error = open("SecondPrisonData_ERRORflorbc.csv", 'w')
fw_second.write(varnames_second) # Write variable names


counter = 1
for link_j in links_j:
    for id_number in id_numbers:
        print str(counter) + "\t" + link_j + "\t" + id_number
        counter += 1
        br = Browser()
        try:
            br.open(link_j)
        except:
            print "Exception while opening" + str(link_j) + "\nSleeping for 10 minutes"
            time.sleep(600)
            continue
        br.form = list(br.forms())[0]

        control = br.form.find_control("cbadju")
        if control.type == "select":  # make sure it is the right one
            control.value = ['3']

        control = br.form.find_control("norad")
        if control.type == "text":  # make sure it is the right one
            control.value = id_number

        try:
            response = br.submit()
        except:
            print "Exception while submitting" + str(id_number) + "\nSleeping for 10 minutes"
            time.sleep(600)
            continue

        soup2 = BeautifulSoup(response)
        links_first = []  # This will store the links that appear after the first search

        for l in br.links():
            l1 = l.absolute_url
            if l1 != "http://www.ramajudicial.gov.co":  # Not useful
                links_first.append(l1)
                try:
                    data_text = str(id_number) + "\t" + get_data_first(l1)
                    fw_first.write(data_text)  # Write data
                    add = 0
                except:
                    add = 1

                if add:
                    links_page_first_error = str(l1) + "\n"
                    fw_first_error.write(links_page_first_error)
                    remove = 0

        for link in links_first:
            br.open(link)
            for l in br.links():
                l2 = l.absolute_url
                try:
                    data_text = str(id_number) + "\t" + get_data_second(l2)
                    fw_second.write(data_text)  # Write data
                    add = 0
                except:
                    add = 1

                if add:
                    links_page_second_error = str(l2) + "\n"
                    fw_second_error.write(links_page_second_error)
                    remove = 0

fw_first.close()
fw_first_error.close()
fw_second.close()
fw_second_error.close()
print "Done!"
