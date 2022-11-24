# CleanText-API <br>
API will be used to clean tweets and saved to database automatically. <br>
API will receive two endpoints both text and file. Text is cleaned by typing the sentence on the UI, however, for file, after uploding the file, column having column name **Tweet** will be cleaned, cencored, and subsitute with respective word. <br> <br>
In order to get the whole process, please find on the architecture <br>
## System Architecture
<img width="872" alt="image" src="https://user-images.githubusercontent.com/26571248/203693956-6f005d3c-7b07-4af2-a32e-27e19eb75ace.png">
<br>
## Result Example
### Text clean
<br>
The abusive words will be cencored with *** and non-standarized words will be subsituted with standarized one
<br>
<img width="1387" alt="image" src="https://user-images.githubusercontent.com/26571248/203695909-c39dee49-da0a-4f82-9969-f96347fab51c.png">
<br>
### File clean
The result is the same with the text, the difference is only from the input file which is uploaded file.
<br>
<img width="1382" alt="image" src="https://user-images.githubusercontent.com/26571248/203696244-fb4fff44-b479-44ed-8f5a-b8255581d2a9.png">


