import gzip
import json
from pprint import pprint
from HTMLParser import HTMLParser



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
    pricingInformationDictionary = []
    for i, line in enumerate(infile):
        parser = MyHTMLParser()
        data = json.loads(line.strip())
        #pprint (data)
        eachDict = {}
        ##the following one-line code can be added to correlate the parsed info with its source file
        #eachDict['link_url'] = data.get('link_url')
         
        ####parse html file using HTMLParser
        if (data['link_text'].lower().find('pricing') != -1 or data['link_text'].lower().find('rates') != -1):
            if(data.get('html') != ""):
                parser.feed(data.get('html'))
                sList = parser.list
                index = 0
                newString = ''
                while(index < len(sList)):
                    if(sList[index].tag_name == 'data' and sList[index].data_value.find('$')!=-1):
                        pos_dollar = sList[index].data_value.find('$')
                        if(pos_dollar < len(sList[index].data_value)-1 and sList[index].data_value[pos_dollar+1].isdigit()):
                            ##case1: there are some words ahead of $***; the words are product/service/solution;
                            if(pos_dollar > 5):
                                #print "product/service/solution:" + sList[index].data_value[0:pos_dollar]  ## A pricingInfoDict will be as a return, to print just for easily checking parsing results
                                #print "pricingInfo:" + sList[index].data_value[pos_dollar:]
                                eachDict[sList[index].data_value[0:pos_dollar]] = sList[index].data_value[pos_dollar:]
                            ##case2: no words ahead of $****; need to search for the previous line until matching 
                            ##1)there is only one data within startTag and endTag 
                            ##2)length of the data is less than some value 
                            ##3)there is no prince in this data;
                            elif(pos_dollar == 0 or len(sList[index].data_value[0:pos_dollar].split()) == 0):
                                t = index - 2
                                while(t >= 0):
                                    if('$' not in sList[t].data_value and len(sList[t].data_value.split()) > 0 and sList[t-1].tag_name == 'startTag' and sList[t+1].tag_name == 'endTag'):
                                        #print "product/service/solution:" + sList[t].data_value
                                        #print "pricingInfo:" + sList[index].data_value[pos_dollar:]
                                        eachDict[sList[t].data_value] = sList[index].data_value[pos_dollar:]
                                        break
                                    else:
                                        t = t -1
                    index = index + 1
        else:
            ##the following one-line code can be added to count pages need a quote to get pricinginfo
            #eachDict['product/service/solution'] = 'Need a quote to get pricinginfo'
            pass
        print eachDict
        pricingInformationDictionary.append(eachDict)
        parser.i=0
        del parser
        raw_input("----------------------enter to continue----------------------")
    

 
        
            
        
        
        
                                    