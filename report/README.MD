# Processing steps -- report/main.py

## Input files -- clean.py
* starting from 5 WoS and Scopus CSV files supplied by Shannon
* create new files with simpler names:
    * shannon0.csv
    * shannon1.csv
    * shannon2.csv
    * shannon3.csv
    * shannon4.csv
* decode from Latin-1 into utf-8
* remove the summaries at the bottom of the data
* output list of original file names and new names:
    * fileOrigins.csv

### Second batch of files -- clean2.py
* 3 new files from Shannon that include all UW publications not just OA
* create new files with names: shannon-Aug2019n.csv
* decode from Latin-1 into utf-8
* replace DOS endlines (with dos2unix) which is creating double spacing
* remove metadata at head and tail of CSV files

## Filter and deduplicate files -- combine.py
* for the new files listed in:
    * fileOrigins.csv
* remove items without DOIs
* filter the rows for the fields that have been requested
* combine rows with the same DOI into one line
* keep track which files each DOI comes from
* write out the combined and filtered files to:
    * combined.csv

## Get Crossref data -- xrefLookup.py
* for each DOI in:
    * combined.csv
* from Crossref data select fields:
    * publisher
    * is-referenced-by-count
    * container-title
    * subject
* add time delay in loop
* use URL `https://api.crossref.org/works/{doi}?mailto=libxrefclient@library.uwaterloo.ca`
* cache data (to avoid unnecessarily taxing Crossref API) in:
    * xrefData.json
* if reponse is 404, meaning no Crossref data for that DOI:
    * query Crossref for agency that registered the DOI
    * output agency for each DOI to:
        * xrefErrors.json
    * if reponse to agency query is 404, output DOIs to:
        * xref404.csv

## convert json Crossref data to CSV -- json2csv.py
* take each line in the json file:
    * xrefData.json
* convert them to dictionaries and write data out as a CSV file:
    * xrefData.csv
* take each line from the agency lookup json:
    * xrefErrors.json
* convert to dictionaries and write data out as CSV file:
    * xrefAgencies.csv
