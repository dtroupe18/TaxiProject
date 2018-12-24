# TaxiProject
Project to Find Fraudulent Taxi Routes in GPS Trajectories



## Problem Discription
Due to many taxi cabs now having an embedded Global Positioning System (GPS) we can collect massive amounts of taxi trajectories throughout urban environments. These GPS records provide an opportunity for us to uncover taxi driving fraud events. In this paper we describe a method of detecting anomalous taxi trajectories. Sometimes taxi drivers can purposefully take longer routes to the destination in an attempt to get a higher fare. This can be a problem for the passengers who are forced to pay higher fares as well as the taxi company who might lose customers to competitors if such fleecing is discovered.



## Sample Data
Due to the sensitive nature of GPS data only a [sample](http://www-users.cs.umn.edu/~tianhe/BIGDATA/UrbanCPS/TaxiData/TaxiData) of GPS traces can be provided. The data comes from taxis operating in Shenzhen, China. For our project we focused on trajectories between the airport and train station. Our hypothesis was that tourists are the most likely victims of taxi fraud so we focused on areas likely to be visited by tourists.



## Process

1. Create GPS traces that map the routes recommended by Google Maps

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/JustGoogleMaps/Airport-to-train-google-maps.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/JustGoogleMaps/Train-to-airport-google-maps.png)

2. Graph those routes using [Matplotlib](https://matplotlib.org/) 

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/JustGoogleMaps/All%20Google%20Maps%20Routes.png)

3. [Filter](https://github.com/dtroupe18/TaxiProject/blob/master/Python-Scripts/find_relevant_trajectories.py) GPS trajectories by longitude and latitude so that only routes between the aiport and train station are left. You'll also have to worry about routes that have infrequent readings because it makes reconstructing their route impossible. 

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/Linear-Routes/Train%20to%20Airport%20Routes%20With%20Infrequent%20Readings.png)


4. Graph individual routes and compare them to Google Maps routes. 

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/All-Route-Graphs/Airport-To-Train-Route-Graphs/Airport%20to%20Train%20Route%20164730.png)

5. Create a baseline method to evaluate fraud. Our baseline method labeled routes that had above average time and distance as fraud. Our method was limited by the amount of data we had so we couldn't determine if these anamolous trajectories were the result of things such as traffic. Additionally, we were able to access historical data to determine if the driver is familiar with that area. 

-Baseline Images:
![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/BaselineImages/Airport%20to%20Train%20All%20Routes.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/BaselineImages/Train%20to%20Airport%20All%20Routes%20with%20Errors%20Colored.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/BaselineImages/Train%20to%20Airport%20All%20Routes%20without%20Errors.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/BaselineImages/Train%20to%20Airport%20All%20Routes.png)

6. Map GPS trajectories to cells based on their coordinates. This turns a trajectory into a series of cells that were visted. We then compared how similar every trajectories cell path was to the cell path of a Google Maps route. If less than 80% of the cells were the same we labeled that route fraudulent. 

-Fraud by Sub-Sequence

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/Sub-Sequence-Images/Airport%20to%20Train%20All%20Routes%20-%20Fraud%20by%20Sub-Sequence.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/Sub-Sequence-Images/Train%20to%20Airport%20All%20Routes%20-%20Fraud%20by%20Sub-Sequence%20with%20Errors%20Colored.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/Sub-Sequence-Images/Train%20to%20Airport%20All%20Routes%20-%20Fraud%20by%20Sub-Sequence%20without%20Errors.png)

![Alt Text](https://github.com/dtroupe18/TaxiProject/blob/master/Project-Images/Sub-Sequence-Images/Train%20to%20Airport%20All%20Routes%20-%20Fraud%20by%20Sub-Sequence.png)

