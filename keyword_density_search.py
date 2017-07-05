

#########################################################################################
##	Developed by: Amol Kokje, akokje@asu.edu	
##	Description: Takes KW as input and searches through list of URLs to find the occurance
#########################################################################################

## NOTES: 
## Currently, takes URL list as input in a file. TO FIX: Skips the URLs which it is unable to load
## TO DO: Should find the list of URLs automatically from google, yahoo and bing searches. 


import os, sys, re, time
import urllib
from bs4 import BeautifulSoup
import selenium
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import threading
##from selenium import NoSuchElementException 



def main():

	## INPUTS ------------------
    keyword="gold ira scams" ##"supply chain"
    fileName='yahoo_hgeo_links'
    tagList=['title', 'head', 'body','meta','a','p','img']
	## 
    urlListFile=fileName+'.txt'
    dumpFile=fileName+'_report.csv'
	
    print "Keyword="+keyword  
    print "Input URL List File="+urlListFile
    print "Output Report File="+dumpFile
    raw_input("Press Enter to Continue ...")
    
	
	## PROCESSING ------------------
    print "Reading file: "+urlListFile+" ..."
    fh=open(urlListFile,"r")
    urlList=fh.readlines()
    fh.close()
    
    modUrlList=list()    
    for url in urlList:
        url=url.rstrip('\r\n')
        modUrlList.append(url)
        ##print "URL FOUND='"+url+"'"
    ##raw_input("Press Enter to Continue ...")
    
            
    fh2=open(dumpFile,"w")
    fh2.write("URL,")
    for t in tagList:
        fh2.write(t+",")
    fh2.write("\n")    
        
    for url in modUrlList:    
        writeLine=''
        dumpLine=''
        writeLine=writeLine+"URL="+url+", "
        dumpLine=dumpLine+url+","
        if (url.endswith(".pdf") or (url.endswith(".htm"))):
            print "SKIPPING URL="+url
            continue
        try: 
            handle = urllib.urlopen(url)
            htmlData =  handle.read()
            ##print htmlData
            ##sys.exit()
            soup = BeautifulSoup(htmlData, 'html.parser')
            for tagName in tagList:
                occ=find_occurance(soup, tagName, keyword)
                writeLine=writeLine+tagName+"="+str(occ)+", "
                dumpLine=dumpLine+str(occ)+","
            print writeLine    
            fh2.write(dumpLine)
            fh2.write("\n")
            
        except Exception as ex:
            print "EXCEPTION: "+ex.message
            print "SKIPPING URL="+url
            continue 
            
            
          
    
def find_occurance(soup, tagName, keyword):
    kc=0
    tagOccurancesList=soup.find_all(tagName) 
    for tagOccurance in tagOccurancesList:
        for content in tagOccurance.contents:
            contentLowerCase=''
            try: 
                contentLowerCase=str(content).lower()                  
            except UnicodeEncodeError as ex:
                encodedString=content.encode('utf-8')
                contentLowerCase=encodedString.lower()                
            
            if keyword in contentLowerCase:
                for m in re.finditer(keyword, contentLowerCase):
                    kc=kc+1
    return kc 
    
      
if __name__ == "__main__":
    main()