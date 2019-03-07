import argparse

def createParser():
    parser = argparse.ArgumentParser(description="Crawl and scrape links from specified links")
    parser.add_argument("links", metavar="N", type=str, nargs="+", help="Starting links to start crawling from")
    parser.add_argument("--cycles", dest="cycles", type=int, help="The number of iterations out from the starting point to crawl")
    parser.add_argument("--savefile", dest="savefile", type=str, help="The filename to save the links to (use a .json file for this)")
    #parser.add_argument("-v", dest="verbose", action="store_const", const=True, default=False, help="Toggle verbose output")
    return parser

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()
    print(args)