from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import pandas as pd
import urllib2


## Global variables
# Links for page of each juzgado
links_j = ["http://procesos.ramajudicial.gov.co/jepms/medellinjepms/conectar.asp"]

#ids = ['18560161','70602450','71332502']
lines = [line.rstrip('\n').split('\t') for line in open('comunaid_small.csv', 'r')]
id_numbers = [lines[j][0] for j in xrange(1, len(lines))]

for link in links_j:
    for id in id_numbers:
        br = Browser()
        br.open("http://procesos.ramajudicial.gov.co/jepms/medellinjepms/conectar.asp")

        br.form = list(br.forms())[0]

        id_number = str(id)

        if id_number != "":  # If we have id number
            control = br.form.find_control("cbadju")
            if control.type == "select":  # make sure it is the right one
                control.value = ['3']

            control = br.form.find_control("norad")
            if control.type == "text":  # make sure it is the right one
                control.value = id_number

        response = br.submit()

        soup2 = BeautifulSoup(response)
        links = []  # This will store the links that appear after the first search

        for l in br.links():
            l2 = l.absolute_url
            if l2 != "http://www.ramajudicial.gov.co":  # Not useful
                links.append(l2)

        links2 = []  # This will store the final link, the one we are actually interested in
        for link in links:
            br.open(link)
            for l in br.links():
                links2.append(l.absolute_url)

        print links2