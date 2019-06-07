# Processing steps -- report/main.py

## Input files
* starting from 4 WoS CSV files supplied by Shannon
* create new files with simpler names: wos0.csv. wos1.csv, etc.
* decode from windows-1251 into utf-8
* remove the summaries at the bottom of the data
* output list of original file names and new names: fileOrigins.csv

## Filter and deduplicate files
* for each of the new files remove items without DOIs
* filter the lines for the fields that have been requested
* combine rows with the same DOI into one line
* keep track in which files each DOI appears
* write out the combined and filtered files to combined.csv file

## Get Crossref data
* fields: publisher, is-referenced-by-count, container-title, subject
* add time delay in loop
* User-Agent: UWLibraryAPC/0.1 (mailto:libxrefclient@library.uwaterloo.ca) or use URL https://api.crossref.org/works/{doi}?select=mailto=libxrefclient@library.uwaterloo.ca