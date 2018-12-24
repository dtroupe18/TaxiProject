# TaxiProject
Project to find fraudulent taxi routes in GPS trajectories from Shenzhen, China. 

We evaluated routes between the [North train station](https://www.google.com/maps/place/%E6%B7%B1%E5%9C%B3%E5%8C%97/@22.609247,114.02878,15z/data=!4m5!3m4!1s0x0:0x8b45ae202baadf7!8m2!3d22.609247!4d114.02878) and the [airport](https://www.google.com/maps/place/Shenzhen+Bao'an+International+Airport/@22.636828,113.814606,15z/data=!4m2!3m1!1s0x0:0xfc263ee96a7dc355?ved=2ahUKEwi8oMvntrnfAhV5wcQHHfKuAE0Q_BIwDXoECAUQCA) in both directions. 

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/Train-to-airport-google-maps.png" width="600">


Additionally, we evaluated routes between the [west railway station](https://www.google.com/maps/place/Railway+Station+%EF%BC%88West%EF%BC%89+Exit/@22.5342536,114.1092764,16.87z/data=!4m12!1m6!3m5!1s0x340387c818047d83:0x19d70ddf7e3f5cfb!2sHOME+INN+SHENZHEN+RAILWAY+STATION!8m2!3d22.533691!4d114.111333!3m4!1s0x0:0x7e0a7ba85352fcba!8m2!3d22.5345792!4d114.1104855) and the [North train station](https://www.google.com/maps/place/%E6%B7%B1%E5%9C%B3%E5%8C%97/@22.609247,114.02878,15z/data=!4m5!3m4!1s0x0:0x8b45ae202baadf7!8m2!3d22.609247!4d114.02878) in both directions. 

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/SummaryImages/West-To-North-Google-Maps-Image.png" width="600">




## Problem Discription
Due to many taxi cabs now having an embedded Global Positioning System (GPS) we can collect massive amounts of taxi trajectories throughout urban environments. These GPS records provide an opportunity for us to uncover taxi driving fraud events. In this paper we describe a method of detecting anomalous taxi trajectories. Sometimes taxi drivers can purposefully take longer routes to the destination in an attempt to get a higher fare. This can be a problem for the passengers who are forced to pay higher fares as well as the taxi company who might lose customers to competitors if such fleecing is discovered.



## Sample Data
Due to the sensitive nature of GPS data only a [sample](http://www-users.cs.umn.edu/~tianhe/BIGDATA/UrbanCPS/TaxiData/TaxiData) of GPS traces can be provided. The data comes from taxis operating in Shenzhen, China. For our project we focused on trajectories between the airport and train station. Our hypothesis was that tourists are the most likely victims of taxi fraud so we focused on areas likely to be visited by tourists.



## Process

1. Create GPS traces that map the routes recommended by Google Maps


<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/Airport-to-train-google-maps.png" width="300">

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/Train%20to%20Airport%20Station%20Google%20Maps.png" width="300">


<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/SummaryImages/West-To-North-Google-Maps-Image.png" width="300">

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/SummaryImages/Train%20Station%20West%20to%20Train%20Station%20North%20Google%20Maps%20Routes.png" width="300">


2. [Filter](https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Python-Scripts/find_relevant_trajectories.py) GPS trajectories by longitude and latitude so that only routes between the aiport and train station or north and west train stations are left. You'll also have to worry about routes that have infrequent readings because it makes reconstructing their true route impossible. 


3. Graph those routes using [Matplotlib](https://matplotlib.org/) and compare them to Google Maps routes. [All airport to train station routes](https://github.com/dtroupe18/TaxiProject/tree/master/AirToTrain/Images/All-Route-Graphs) [All train to train routes](https://github.com/dtroupe18/TaxiProject/tree/master/TrainToTrain/Images)

Sample:

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/NorthToWestImages/All-Routes/North%20to%20West%20Train%20Route%20622571.png" width="300">


4. Create a baseline method to evaluate fraud. Our baseline method labeled routes that had above average time and distance as fraud. Our method was limited by the amount of data we had so we couldn't determine if these anamolous trajectories were the result of things such as traffic. Additionally, we weren't able to access historical data to determine if the driver is familiar with that area. 

-Airport to train station routes vs Google maps:
<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/Train%20to%20Airport%20Station%20Google%20Maps%20vs%20Actual.png" width="300">

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/Airport%20to%20Train%20Station%20Google%20Maps%20vs%20Actual.png" width="300">

-Train to train station routes vs Google maps:
<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/SummaryImages/North%20to%20West%20Train%20Station%20Google%20Maps%20vs%20Actual.png" width="300">

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/SummaryImages/West%20to%20North%20Train%20Station%20Google%20Maps%20vs%20Actual.png" width="300">

-Sample fraud based on baseline method (above average time and distance)

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Images/All-Route-Graphs/Suspected-Air-Fraud/Airport%20to%20Train%20Route%20329370.png" width="300">

<img src="https://github.com/dtroupe18/TaxiProject/blob/master/TrainToTrain/Images/NorthToWestImages/Fraud-By-Time-Distance/North%20to%20West%20Train%20Route%20509935.png" width="300">


6. [Map GPS trajectories to cells](https://github.com/dtroupe18/TaxiProject/blob/master/AirToTrain/Python-Scripts/map_gps_to_cells.py) based on their coordinates. This turns a trajectory into a series of cells that were visted. We then compared how similar every trajectories cell path was to the cell path of a Google Maps route. If less than 80% of the cells were the same we labeled that route fraudulent. 




