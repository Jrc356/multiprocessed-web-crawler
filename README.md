# Title
Multiprocessed-web-crawler (very original I know)  
# Description
A command line tool and python package to parse a list of websites for links to other sites, then these links are then parsed for their links to sites, and this cycle continues for the specified number of cycles. The links are gathered and stored in the specified file for later use.
# Installation  
To do  

# Usage
## In python:  
Import the Crawler from the package  
`from <to do> import Crawler`  

Now to crawl the sites, create a list of starting points  
`startingPoints = ["www.wikipedia.com"]`  

From here, specify the output file name (use a json file) and the number of cycles and let er go:  
`Crawler("my_save_file.json", 3).crawl(startingPoints)`  

The links are written to the file after every iteration.

## CLI:  
To do

# Some things/issues to keep in mind as of now  
1. The crawler does not ignore duplicate links
2. Utilizes multiprocessing.cpu_count() - 1 to limit the number of processes run