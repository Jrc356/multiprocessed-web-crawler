from cli import createParser
from Crawler import Crawler

if __name__ == "__main__":
    parser = createParser()
    args = parser.parse_args()
    
    Crawler(args.savefile, args.cycles).crawl(args.links)