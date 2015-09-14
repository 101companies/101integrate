## General

This folder contains the nessecary files for the analytics-step

## Files

- *.generic.R:	A generic version of the generated R files (broken)
- buildPopularScatterdTermsTable.R	compares the book's scattered Terms (generated)
- buildPopularTermsTable.R	gets the most common Terms across all books (generated)
- csv2tex.py	Converts the csv-files which are generated during the analytics-step into tex-files
- dependencies.R	Installs the R-package-dependencies for the other scripts 
- frequencies.R		Extracts "scattered" Terms and generates chapter-Profiles
- rank.R	Reads the common English word rank generated in the mining phase and removes all but the 30 most common terms