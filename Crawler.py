from multiprocessing import Pool
import requests
import bs4 as bs #BeautifulSoup
import string
import random

#Worker
def getLinks(url):
    links = []
    print("Working...")
    try:
        page = requests.get(url)
        soup = bs.BeautifulSoup(page.text, 'lxml')
        for link in soup.find_all('a'):
            link = link.get('href')
            #if there are no links on the page
            if link == None:
                continue
            #add the wikipedia link to the front of relative links
            if link[0] == "/":
                link = "https://en.wikipedia.org" + link
            #don't care for anchor links
            elif "#" in link:
                continue

            links.append(link)
        print("Links for " + url + " collected")
        return links
    #Catch connection errors if link does not exist
    except ConnectionError as e:
        print(e)
        print("Connection Error to " + url)
        return []
    #Catch the rest of exceptions in a rather unfavorable way
    except Exception as e:
        print(e)
        return []


###Unused but optional use to generate an amount amt of random links of length length
def generateLinks(amt, length):
    link_ls = []
    com = ".com"
    for i in range(amt):
        link = "http://www."
        for j in range(length):
            link += random.choice(string.ascii_lowercase)
        link += com
        link_ls.append(link)
    return link_ls


def main(link_ls, cycles):
    for i in range():
        #links = generateLinks(50, 3)
        p = Pool(4)
        print("Start Pool"+str(i+1))
        link_ls = p.map(getLinks, link_ls)

        link_ls_temp = []
        #Write links to file
        if len(link_ls2) > 0 and link_ls2[0] != None:
            with open("links.txt", "a", encoding="utf_8") as f:
                for links in link_ls:
                    for link in links:
                        if link == None:
                            continue
                        f.write(link + "\n")
                        #add link to the new list to run through
                        link_ls_temp.append(link)
        else:
            print("No links collected")



if __name__ == '__main__':
    link_ls = ['https://en.wikipedia.org/wiki/Special:Random'] #wikipedia's random article link
    main(link_ls, 5)
    print("Complete")
