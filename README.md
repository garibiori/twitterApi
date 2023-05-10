# twitter

In this program, I prompt the user to enter two search terms. Upon entering these two search terms, the program accesses the Twitter API and pulls the first 1000 tweets that contain the first search term. After compiling all these tweets, the program calculates the sentiment score for the first search term, using these first 1000 tweets as its parameters. After getting the sentiment score for the first search term, the program does the same to the second search term. It compiles the first 1000 tweets for the second search term and then passes these tweets as parameters to determine the second search term's sentiment score. Once the sentiment score for both search terms is available, the search term that has the higher positive sentiment on Twitter is determined and its results printed for the user to see.

## Identifying Information

* Name: Ori Garibi
* Student ID: 2367830
* Email: garibi@chapman.edu
* Course: CPSC 353
* Assignment: PA03 Twitter

## Source Files  

* sentiment.py
* sentiment.input

## References

* None, other than class material

## Known Errors

* No known errors

## Build Insructions

* flake8 sentiment.py

## Execution Instructions

* python3 sentiment.py < sentiment.input
