# Summary

This repo contributes to the 101companies Project. 101integrate is a framework for the integration of knowledge resources. At this point, the framework specifically addresses vocabulary integration and cross-referencing betweem textbooks and 101wiki. Currently, 4 Haskell and 4 Python textbooks are supported.

# Tool dependencies

Make sure all dependencies are installed.

You need System R: http://www.r-project.org/

You need pyhton-antlr (not available throw pipi):  [Ubuntu](https://launchpad.net/ubuntu/+source/antlr) , [sonstige](https://theantlrguy.atlassian.net/wiki/display/ANTLR3/Python+runtime)

You need a bunch of Python packages and some NLP support. This is taken care of by this command:

    make download-deps

# Online textbooks

Some of the supported textbooks are available online. They are not included into the repo. They must be downloaded with the following command:

    make download-books

You can download tagged Books e.g. the Haskell-Books with the following command:

    make download-books BOOKS="haskell"

The available Tags can be looked up in docs/Tagset.md .

# Offline textbooks

2 of the supported textbooks are not available online. If you have offline access to them, please link them as demonstrated by the make target "link-books". That is, if the books' sources are available per a "haskellbooks" folder in your dropbox, then the following command suffices:

    make link-books

# Mining and analyzing

Run these commands:

    make mine
    make analyze

These commands will create various data files in data/allbooks and data/perbook/*.

# Backlinking

Run this commands:
  
    make backlink
    
This will create the mapping.json and baklinks.json in data/allbooks which are used by the external environment

# Integrate

Run this commands:
  
    make integrate
    
This will create various data in data/summary, data/languages und data/themes