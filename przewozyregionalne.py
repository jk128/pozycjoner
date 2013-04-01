# pozycjoner: a python module for scraping position of public
# transport vehicles from different vendors
# https://github.com/niedakh/pozycjoner/
#
# Copyright (C) 2013  Piotr Szymanski <niedakh@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#    
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
from bs4 import BeautifulSoup
import parsedatetime as pdt
from datetime import datetime
import os,sys
import re

class PrzewozyRegionalnePositionier:
    """ TODO:description """
    
    def __init__(self):
        self.pkppr_url = 'http://82.160.42.14/opoznienia/'
        self.provider = 'PrzewozyRegionalne'
        self.dateparser = pdt.Calendar(pdt.Constants())
        
    def returnPKPPRTree(self, ):
        pass
    
    def parseDataItem(self, item):
        return {
            'linia' : item[0],
            'lat': item[1],
            'lng': item[2]
        }    
        
    def getAvailableLines(self):
        #session = requests.session()
        # pkppr_data_page = requests.get(self.mpk_list_url)
        
        test_file = open(os.path.dirname(__file__)+'\\testdata\\pkppr.htm', encoding='utf-8')
        
        #if (mpk_data_page.status_code != 200):
        #    pkppr.raise_for_status()
        
        pkppr_data_tree = BeautifulSoup(test_file.read())
        
                
        # data of available lines is stored in the DOM tree in the table.opoznienia, ex:
        # <tr id="tabela-n1 or tabela-n2">
        # 
        #    <td><a href="GOOGLE_MAPS_URL_WITH_POSITIONS" target="_blank">TRAIN_ID</a></td>
        #    <td>Poznan Glowny (18:50) - Kepno (22:01)</td>
        #    <td class="mw">15 min.</td> - delay
        #    <td>Solec Wielkopolski            </td> - closest station
        #    <td>2013-03-31 19:57:05</td> - data recording time
        ##</tr>
        #
        # The GOOGLE_MAPS_URL_WITH_POSITIONS looks like this:
        # http://maps.google.pl/maps?q=77532+++++@52.096100000,17.327171700&amp;t=m&amp;dirflg=r&amp;z=12
        # we can clearly see it is a format of:
        # http://maps.google.pl/maps?q=TRAIN_ID+++++@LAT,LNG
        # so what we basically need to scrape are all table.opoznienia tr a 
                
        link_regexp = re.compile('http\:\/\/maps\.google\.pl\/maps\?q=([^\+]+).*@([0-9\.]+),([0-9\.]+)')
        
        positions = [ self.parseDataItem(link_regexp.match(line_link['href']).groups())
                     for line_link in pkppr_data_tree.find_all(href=link_regexp)]

        return positions
    
    #def getPosition(self, line_number):
    #    lines = []
    #    if isinstance(line_number, int):
    #        lines.append(str(line_number).lower())
    #    elif isinstance(line_number, str):
    #        lines.append(line_number.lower())
    #    elif isinstance(line_number,list):
    #        for i in line_number:
    #            lines.append(str(i).lower())
    #    
    #    # The POST request expects an urlencoded version of
    #    # busList[bus][]=line number, like an array in PHP, ex:
    #    # busList[bus][]=5&busList[bus][]=6 etc.
    #    #
    #    # Because the Request API expects a dictionary, we creeate a
    #    # dictionary with one key and put a lines array as the value
    #    # the Requests API should convert this to a list of key=value pairs
    #    
    #    payload = {'busList[bus][]': lines}
    #    session = requests.session()
    #    r = requests.post(self.mpk_url, data=payload)
    #                      
    #    if (r.status_code != 200):
    #        r.raise_for_status()
    #        
    #    else:
    #        # pasazer.mpk.wroc.pl returns empty json's for all requests
    #        # TODO: will figure out a sensible parsed version of return data
    #        val = {
    #            # TODO: figure out how to return the received time - as a a datetime?
    #            'received': self.dateparser.parseDateText(r.headers['last-modified']),
    #            'json': r.json()
    #        }
    #        return val
  
if __name__ == "__main__":
    pkppr = PrzewozyRegionalnePositionier()
    lines = pkppr.getAvailableLines()
    print("Available lines:")
    print(lines)
    
    #print("MPK 125:")
    #print(mpk.getPosition(125))
    #
    #print("MPK A:")
    #print(mpk.getPosition('A'))
    #
    #print("MPK all:")
    #print(mpk.getPosition(lines))