# Processing steps -- report/main.py

## Input files -- clean.py
* starting from 5 WoS and Scopus CSV files supplied by Shannon
* create new files with simpler names:
    * shannon0.csv
    * shannon1.csv
    * shannon2.csv
    * shannon3.csv
    * shannon4.csv
* decode from windows-1251 into utf-8
* remove the summaries at the bottom of the data
* output list of original file names and new names:
    * fileOrigins.csv

## Filter and deduplicate files -- combine.py
* for the new files listed in:
    * fileOrigins.csv
* remove items without DOIs
* filter the rows for the fields that have been requested
* combine rows with the same DOI into one line
* keep track in which files each DOI comes from
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
* use URL https://api.crossref.org/works/{doi}?mailto=libxrefclient@library.uwaterloo.ca
* output data as:
    * xrefData.json
* if reponse is 404, meaning no Crossref data for that DOI:
    * query Crossref for agency that registered the DOI
    * output agency for each DOI to:
        * xrefErrors.json
    * if reponse to agency query is 404
        * output 404 DOIs to:
	    * xref404.csv
    
