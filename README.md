# *Another* method for extracting tabular data in PDFs
Adapted from the Trap Range algorithm implemented in Java. Page [here](https://github.com/thoqbk/traprange).

## Introduction
This algorithm, written in Python, follows the idea of Trap Ranges detailed in the page above:
![Figure 1](https://github.com/thoqbk/traprange/raw/master/_Docs/join-sample.png "Figure 1")

The assumption is that tables follow a relatively grid-like structure with cells aligned to different horizontal and vertical ranges. 
I start from the top of the page, scanning for column names. 
Then, for every text fragment with a different y-coordinate, I start a new row and resolve each fragment to their respective column name. 

For this reason, I think that using this algorithm in combination with some form of object detection model would yield more generalized results across a wider range of table formats. 
Trap Range (or its Pythonic form as implemented here) is good at resolving text to some form of row or column, but further enhancements are still needed to better detect the approximate location of tables. 
This is something that an object detection model can do, and better. 

## Before extracting the table
[Poppler](https://poppler.freedesktop.org/) is used to extract textual information from the PDF page. 
However, other types of PDF-to-text libraries can be explored as I found an error involving text coordinates on the page. 
The detected page width exceeds the y-coordinate values for a handful of text fragments.

## After extracting the table
The data extracted is parsed into Python's datetime data type if possible, or left as is in strings or numerals.
Each column can be associated with a certain data-type - one simple way is if the column contains the word "Date", then data can very likely be parsed into datetime.
Conversely, I also use this method to filter out other irrelevant text that isn't part of the table, like footnotes. 

## Setting up and running the script

Running `setup.sh` under the scripts folder should suffice if there is conda installed. 
```
./scripts/setup.sh
```
The above should create and activate a conda environment. 
After specifying the respective folders and paths in `main.py`, run:
```
python main.py
```
