import gzip
import json
from pprint import pprint

from lxml import etree
from lxml.html.clean import clean_html
import re

#def generatePricingInfo():
with gzip.open("I:\gangLiu\everstring\pricing_data_set.json", "r") as infile:
    pricingInformation = []
    try:
        for i, line in enumerate(infile):
            data = json.loads(line.strip())
            #pprint (data)
            if(data.get('html') != ""):
                htmlRaw = data.get('html')
            #print "Now processing this website ######################################################################################"
            #print data.get('link_url')
                print i
                try:
                    htmlTree = etree.HTML(htmlRaw)
                except ValueError:
                    print "ValueError!!!! Need XMLParser to parse XML file"
                    pass
                result = etree.tostring(htmlTree, pretty_print=True, method="html")
                html_Cleaned = clean_html(result)
            else:
                pass
            eachDict = {}
            eachDict['link_url'] = data.get('link_url')
            
            if(data['link_text'].lower().find('pricing') != -1 or data['link_text'].lower().find('rates') != -1):
                startIndexOfValue = html_Cleaned.find('$')
                if(startIndexOfValue != -1):
                    endIndexOfValue = startIndexOfValue + 1
                    while(endIndexOfValue < len(html_Cleaned)):
                        if(html_Cleaned[endIndexOfValue] >= '0' and html_Cleaned[endIndexOfValue] <= '9'):
                            endIndexOfValue = endIndexOfValue + 1
                        elif(html_Cleaned[endIndexOfValue] == '.'):
                            endIndexOfValue = endIndexOfValue + 1
                        elif(html_Cleaned[endIndexOfValue] == ','):
                            endIndexOfValue = endIndexOfValue + 1
                        elif(html_Cleaned[endIndexOfValue] == '+'):
                            endIndexOfValue = endIndexOfValue + 1
                        else:
                            break
                    value = html_Cleaned[startIndexOfValue:endIndexOfValue]
                if(html_Cleaned[startIndexOfValue-1] == '>' and html_Cleaned[endIndexOfValue] == '<'):
                    tagsEndOfField = ['</strong>', '</span>', '</font>', '</div>', '</h1>', '</h2>', '</h3>', '</h4>']
                    for tag in tagsEndOfField:
                        startIndexOfTag = html_Cleaned.rfind(tag, 0, startIndexOfValue-1)
                        if (startIndexOfTag != -1):
                            startIndexOfField = startIndexOfTag - 1
                            indexOfTagPair = html_Cleaned.rfind('>', 0, startIndexOfTag)
                            strTemp = html_Cleaned[indexOfTagPair+1:startIndexOfTag]
                            field1 = re.search('>[\w\s*]+<', strTemp)
                            try:
                                field = field1.group(0)[1:-1]
                                eachDict[field] = value
                                print eachDict
                            except AttributeError:
                                pass 
                        ###########modify   
                            
                elif(html_Cleaned[startIndexOfValue-1] != '>'):
                    startIndexOfField = startIndexOfValue-1
                    while(html_Cleaned[startIndexOfField] != '>'):
                        startIndexOfField = startIndexOfField - 1
                    startIndexOfField = startIndexOfField + 1
                    field = html_Cleaned[startIndexOfField:startIndexOfValue]
                    eachDict[field] = value
                    print eachDict
                    
                elif(html_Cleaned[endIndexOfValue] != '<'):
                    endIndexOfField = endIndexOfValue
                    while(html_Cleaned[endIndexOfField] != '<'):
                        endIndexOfField = endIndexOfField + 1
                    field = html_Cleaned[endIndexOfValue:endIndexOfField]
                    eachDict[field] = value
                    print eachDict
                    
            else:
                eachDict['product/service/solution'] = 'Need a quote to get pricinginfo'   
            #print eachDict
            pricingInformation.append(eachDict)
            raw_input("enter to continue")
    except IOError:
        print "Error: cannot find file or read data"
    
        
        
        #print pricingInformation
            
        #return pricingInformation
        
        
        
