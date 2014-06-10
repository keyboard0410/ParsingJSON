'''
Created on Jun 8, 2014

@author: zhang
'''
# parse pricing information from HTML 
from lxml import etree
from lxml.html.clean import clean_html

def getCleanHTML(data):
    if(data.get('html') != ""):
        htmlRaw = data.get('html')
        #print "Now processing this website ######################################################################################"
        #print data.get('link_url')
        try:
            htmlTree = etree.HTML(htmlRaw)
        except ValueError:
            print "ValueError!!!! Need XMLParser to parse XML file"
            pass
        result = etree.tostring(htmlTree, pretty_print=True, method="html")
        html_Cleaned = clean_html(result)
        return html_Cleaned
    else:
        pass
    
def getDictValue(html_Cleaned):
    moneyUnit = ['$']
    for unit in moneyUnit:
        startIndexOfValue = html_Cleaned.find(unit)
        if (startIndexOfValue != -1):
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
            valueAndIndex = [value, startIndexOfValue, endIndexOfValue]
            return valueAndIndex




