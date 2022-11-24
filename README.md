# CleanText-API <br>
API will be used to clean tweets and saved to database automatically. <br>
API will receive two endpoints both text and file. Text is cleaned by typing the sentence on the UI, however, for file, after uploding the file, column having column name **Tweet** will be cleaned, cencored, and subsitute with respective word. <br> <br>
In order to get the whole process, please find on the architecture <br>
## System Architecture
<img width="872" alt="image" src="https://user-images.githubusercontent.com/26571248/203693956-6f005d3c-7b07-4af2-a32e-27e19eb75ace.png">

## File Explanation
1. app.py : the main program for cleaning text and file
2. re_dataset.csv : the sample input file to be cleaned
3. Data_Analysis.ipynb : code for analysis the result e.q visualization and statictical analysis
4. main.db : main database
5. docs : directory consisted yml file

## Result Example
Result of the cleaned data will be represented by Raw_text and Clean_text
### 1. Text clean
The abusive words will be cencored with *** and non-standarized words will be subsituted with standarized one
<br>
<img width="1387" alt="image" src="https://user-images.githubusercontent.com/26571248/203695909-c39dee49-da0a-4f82-9969-f96347fab51c.png">
### 2. File clean
The result is the same with the text, the difference is only from the input file which is uploaded file.
<br>
<img width="1382" alt="image" src="https://user-images.githubusercontent.com/26571248/203696244-fb4fff44-b479-44ed-8f5a-b8255581d2a9.png">
