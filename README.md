# Titanic Logistic Regression
*Ryan Kazmerik (Student ID: 170826410)*

## Running this Project:
### Start Spark master node using following command:
    spark-class.cmd org.apache.spark.deploy.master.Master

### Start Spark worker node using following command:
    spark-class.cmd org.apache.spark.deploy.worker.Worker spark://10.211.55.3:7077

### Deploy titanicEAR package to Wildfly 10.x server:
    C:\Users\ryankazmerik\cp630\final\titanicEAR

### Visit the web service index at:
    http://localhost:8180/titanicWS

## Architecture


## Main Components
1. Logistic Regression Algorithm : titanic.py
* This algorithm was written in Python, and executed on Spark using the PySpark
    connector. First it trains a model using a dataset of ±1500 passenger records
    including the known survival. Then it predicts the user inputted data to determine
    if the given passenger would survive or not.
* Input: 4 parameters (Ticket class, Sex, No. spouses aboard, No. children aboard).
* Output: A prediction (0.0 or 1.0) regarding if the passenger would have survived.

2. EJB Stateless Bean : titanicEJB
* Description: This EJB stateless bean receives the query string parameters from the web service
    and creates a CSV file in the /data/ directory called 'userInput.csv'. It then executes a command to submit the titanic.py job to Spark using spark-submit.
* Input: The 4 query string parameters from the RESTful web service.
* Output: A string containing the result of the prediction ("Survived" or "Not Survived").

3. REST Web Service : titanicWS
* Description: This RESTful web service recieves 4 input parameters from it's index.html page
    and calls the EJB stateless bean. 
* Input: 4 parameters (Pclass, Sex, SibSp, Parch).
* Output: A string containing the result of the prediction ("Survived" or "Not Survived").

4. EAR Deployment : titanicEAR
* Description: This enterprise application project packages the titanicEJB and titanicWS projects
    together in a single package to be deployed to the Wildfly 10.x server.
* Inputs: titanicEJB, titanicWS

