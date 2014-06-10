import gzip
import json
from pprint import pprint

from lxml import etree
from lxml.html.clean import clean_html
import re
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


class Node():
    def __init__(self):
        self.tag_name =''
        self.data_value=''
    
class MyHTMLParser(HTMLParser):
 
    
    list=[]
    i =0
    def handle_starttag(self, tag, attrs):
        if(self.i==0):
            self.list=[];
            self.i=1
        mynode=Node();
        #print "Encountered a start tag:", tag
        mynode.tag_name  = 'startTag'
        mynode.data_value = tag
        self.list.append(mynode)
        
    def handle_data(self, data):
        #print "Encountered some data  :", data
        mynode=Node();
        mynode.tag_name  = 'data'
        mynode.data_value = data
        self.list.append(mynode)
        
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        mynode=Node();
        mynode.tag_name  = 'endTag'
        mynode.data_value = tag
        self.list.append(mynode)
        



with gzip.open("I:\gangLiu\everstring\pricing_data_set.json", "r") as infile:
    pricingInformation = []
    for i, line in enumerate(infile):
        parser = MyHTMLParser()
        data = json.loads(line.strip())
        #pprint (data)
        if(data.get('html') != ""):
            parser.feed(data.get('html'))
            #print i
            
            sList = parser.list
            index = 0
            newString = ''
            
            ###process each html data in sList
            ##case1: before $*** there are some words; the words is the service name;
            
            
            ##case2: no words beofore $****; search for the previous line. until 1)there is only one data within startTag and endTag and 2)length of the data is less than some value 3) there is no prince in this data eg: 30 note: 1) 2)and 3) all true;  
            ##      
            
            
            while(index < len(sList)):
                if(sList[index].tag_name == 'data' and sList[index].data_value.find('$')!=-1):
                    
                    pos_dollar = sList[index].data_value.find('$')
                    if(sList[index].data_value[pos_dollar+1].isdigit() and pos_dollar > 0 ):
                        print "iterm:" + sList[index].data_value[0:pos_dollar]
                        
                        
                        print "price:" + sList[index].data_value[pos_dollar:len(sList[index].data_value)-1]
                    
                    
                
                index = index + 1
                
                
                
        else:
            pass
        
        parser.i=0
        del parser
    
        raw_input("----------------------enter to continue")
    
    
    #print newString
 
        
            
        
        
        
                                    