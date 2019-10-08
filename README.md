# Site is http://www.rjgoptions.com 

## The Main Folder
https://github.com/hfwebbed/Stock-Option-Analytics/tree/master/rjgoptionssite/flasky


## You will find CSS here 
https://github.com/hfwebbed/Stock-Option-Analytics/tree/master/rjgoptionssite/flasky/static


## Excel prototypes here (the basis of this being built)
https://github.com/hfwebbed/Stock-Option-Analytics/blob/master/DecisionOptions_RG%20(1).xlsm

## For the 8th tab. The ML Requirements I was looking to do
https://github.com/hfwebbed/Stock-Option-Analytics/blob/master/GAME_stock_Frozen.pptx

This site is based on an excel prototype I made. It also has pieces of excel I have extracted across the web and used here.

My Stock Prediction Project (in the link below) contains the following elements (It's just data, no fancy CSS). - Analytics - Data Science - Recommendation Engine - Decision Making & Prediction - A bit of Game Theory - Machine Learning (soon-to-be)

##### 1st Tab...Summary Analysis
simply type in the symbol. It does tell based on historical volatility what the price may be in 30 days or even a year. It also gives an algorthmic view into if its a bull or bear based on the Wycoff Method. Have not made full use of it or know that I am using it right.

##### 2nd Tab...Recommendation
This is similar to anyone who has Yahoo Fantasy Sports and the end of the match they give you an analytical write up.

##### 3rd Tab...Prediction
It attempts to pick, over a time period where the stock will be. The obvious goof ids that it is random in terms of whether a stock will go up or down. Maybe Sentiment would help here. The 2nd graph is to pick the buckets of price (frequency) in which it will be at during that period.

##### 4th tab...Options
Option Calculator

##### 5th tab...Profit
A profit calculator when purchasing options to see how much you may gain or lose

##### 6th tab...Industry
Although functionally not a great UI, the intention is that companies are dependent, interdependent, or have no relation. An example is a car company. If no one is buying a Tesla, that affects car part manufacturures, which affects some software companies, etc. We can show a graphical representation

##### 7th tab...Raw Data

##### 8th tab...Stock Game
All based on Game Theory. This tries to pick which stock is the best and safest in terms of betting on.
The current state is you can see the the prediction chart similiar to the 3rd tab
The ideal state, non-existent, is that you see this prediction. The app takes a snapshot of this prediction
Over time you see the real/actual movement of the stock as as 2nd line.
A 3rd line is a Machine Learning chart that adapts over time and adjusts the predictive algorithm as we get new data and the days pass, adding to the moving raw data of 4 years (or some factor)
