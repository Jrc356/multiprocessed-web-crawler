from multiprocessing import Pool, cpu_count
import requests
import bs4 as bs #BeautifulSoup
import string
import random
from collections import Counter

class Crawler:
    def __init__(self, saveFileName, cycles):
        self.saveFileName = saveFileName
        self.cycles = cycles
        self.totalLinkCount = 0

    #Worker
    def getLinks(self, url):
        baseUrl = "/".join(url.split("/")[:3])
        links = []
        print("Collecting links from {}".format(url))
        try:
            page = requests.get(url)
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

            print("{} links collected from {}".format(len(links), url))
            return links

        #Catch connection errors if url does not exist
        except ConnectionError as e:
            print(e)
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
        if len(linkList) > 0 and linkList[0] != None:
            flattened = []
            with open(self.saveFileName, "w", encoding="utf_8") as f:
                for links in linkList:
                    for link in links:
                        if link == None:
                            continue
                        f.write(link + "\n")
                        flattened.append(link)
                        self.totalLinkCount += 1
                linkList = flattened
        else:
            print("No links collected")

        return linkList
        

    def printSummary(self):
        print("\n" + "#"*75)
        print("{} total links found after {} cycles.".format(self.totalLinkCount, self.cycles))
        
        with open(self.saveFileName, "r") as f:
            counter = Counter(f.readlines())

        print("Most Common links found:\nCount|Link\n{}".format("\n".join("{}| {}".format(count, link.replace("\n", "")) for link, count in counter.most_common(5))))
        print("#"*75)


    def crawl(self, linkList):
        with Pool(cpu_count()-1) as p:
            for i in range(self.cycles):
                print("\nStart Pool #"+str(i+1))
                linkList = p.map(self.getLinks, linkList)

                linkList = self.writeLinks(linkList)
        print("testing")
        print("\nCompleted all cycles, generating summary...")
        self.printSummary()



if __name__ == '__main__':
    link_ls = ['https://en.wikipedia.org/wiki/Special:Random'] #wikipedia's random article link
    Crawler("links.txt", 3).crawl(link_ls)
    print("Complete")
