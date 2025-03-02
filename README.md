# MiNeD-Hackathon

## Team Name - Team Tensor 
## Topic - Stock Market Analysis (Track - 3)

The Given Program helps to identify the following patterns:
1. Head and Shoulder 
2. Reverse Head and Shoulder
3. Double Top 
4. Double Bottom

Data is read from 4 CSV files that contain the Open, High, Low and Close value corresponding to a specific date and time. Data for every 5 minutes is provided in the CSV files. Also the ground truth about the pattern the stock shows for a day is provided in other 4 CSV files. These 8 files , 4 of data and other 4 of ground truth is used for training purpose. For a user to identify the stock pattern , user needs to provide a CSV file as input that contains Open, High , Close and Low value with specific date and time.


## Approach -
As stock pattern are a time - series data , so to identify the stock pattern initally we have used the concept of Perceptually Important Point (PIP) and sliding window. At first we have created data from each individaul day from the given input CSV file. Then for data of each day we have used a sliding window , the window traverse across on the entire data and then on the identified PIP points we have used the Spearman's Coefficent and Rule Based approach to identify which pattern the identified PIP points does show.

To idenifty the Reverse Head and Shoulder pattern and Head and Shoulder pattern we have used 7 PIP points, and for Double Top and Double Bottom we have used 5 PIP point.

The window slides over entire data for a day , the pattern which has the set of PIP points which show highest Spearman's Coefficent is further checked on a set of conditions in the Rules created (Rule Based Approach) and on the basis of this Rule, we identify the pattern shown by the given data.

## Steps -
1. Download the main.py file
2. Keep main.py file and the CSV file for testing in same directory.
3. Now in Command Prompt type -> "python main.py <filename (with .csv)>" and press enter.
4. The Output file "Pattern_" will be generated and stored in the same directory.

## Required Modules:
(For installation, use pip)

1. python==3.9.15 or higher
2. fastpip==1.6.1 (pip install python-fastpip)
3. numpy==1.24.2 (pip install numpy)
4. pandas==1.4.2 (pip install pandas)
5. scipy==1.8.0 (pip install scipy)
