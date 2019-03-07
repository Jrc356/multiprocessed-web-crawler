from multiprocessing import Pool, cpu_count, Queue
import requests
from requests.exceptions import ConnectionError
import bs4 as bs #BeautifulSoup
import string
import random
from collections import Counter
import json
from os.path import exists

class Crawler:
    def __init__(self, saveFileName, cycles):
        self.saveFileName = "../" + saveFileName
        self.cycles = cycles
        self.currentCycle = 0
        self.totalLinkCount = 0

    #Worker
    def worker(self, url):
        try:
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "http://" + url
            page = requests.get(url)
            print("Collecting links from {}".format(page.url))
            baseUrl = "/".join(page.url.split("/")[:3])
            links = []
            soup = bs.BeautifulSoup(page.text, 'lxml')
            for link in soup.find_all('a'):
                linkRef = link.get('href')
                #if there are no links on the page
                if linkRef == None or linkRef == "" or "#" in linkRef:
                    continue
                #add the base link to the front of relative links
                if linkRef[0] == "/":
                    if len(linkRef) > 1 and linkRef[1] == "/":
                        linkRef = "https:" + linkRef
                    else:
                        linkRef = baseUrl + linkRef

                links.append(linkRef)

            print("{} links collected from {}".format(len(links), page.url))
            return {page.url:links}

        #Catch connection errors if url does not exist
        except ConnectionError as e:
            print("Connection Error to " + url)
            return []
        #Catch the rest of exceptions in a rather unfavorable way
        except Exception as e:
            raise e

    ###Unused but optional use to generate an amount (amt) of random links of length (length)
    def generateLinks(self, amt, length):
        print("Generating {} links of {} length")
        link_ls = []
        for _ in range(amt):
            link = "https://www."
            for _ in range(length):
                link += random.choice(string.ascii_lowercase)
            link += ".com"
            link_ls.append(link)
        return link_ls

    def writeLinks(self, linkList):
        #Write links to file
        flattened = []
        for d in linkList:
            v = next(iter(d.values()))
            if len(v) > 0 and v[0] != None:
                mode = "w"
                if exists(self.saveFileName) and self.currentCycle > 1:
                    mode = "a"

                with open(self.saveFileName, mode, encoding="utf_8") as f:
                    if mode == "a":
                        f.write(",")
                    json.dump(d, f)
                
                for link in v:
                    if link == None:
                        continue
                    flattened.append(link)
                    self.totalLinkCount += 1
        
            else:
                print("No links collected")

        return flattened
        

    def printSummary(self):
        print("\n" + "#"*75)
        print("{} total links found after {} cycles.".format(self.totalLinkCount, self.cycles))
        print("#"*75)


    def crawl(self, linkList):
        with Pool(cpu_count()-1) as p:
            for i in range(self.cycles):
                self.currentCycle += 1
                print("\nStart Pool #"+str(i+1))
                linkList = p.map(self.worker, linkList)
                linkList = self.writeLinks(linkList)

        print("\nCompleted all cycles, generating summary...")
        self.printSummary()



if __name__ == '__main__':
    link_ls = ['https://en.wikipedia.org/wiki/Special:Random'] #wikipedia's random article link
    Crawler("links.json", 2).crawl(link_ls)
    print("Complete")