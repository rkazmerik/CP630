# Copyright (C) 2015 Ehsan Mohyedin Kermani
# Contact: ehsanmo1367@gmail.com, ehsanmok@cs.ubc.ca
import sys
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql.functions import UserDefinedFunction
from pyspark.ml.linalg import Vectors

print("STARTING TITANIC SIM:")
print(" ")

# Build the SparkSession
spark = SparkSession.builder.master("local") \
   .appName("Titanic Survival Model") \
   .config("spark.executor.memory", "2gb") \
   .getOrCreate()
   
sc = spark.sparkContext

# Create data frames for the train / test data
df = spark.read.format("csv").option("header", "true").load("/Users/ryankazmerik/cp630/final/CP630/data/titanic.csv")
df2 = spark.read.format("csv").option("header", "true").load("/Users/ryankazmerik/cp630/final/CP630/data/userInput.csv")

# Select your features, with the target first
df = df.select('Survived', 'Pclass', 'Sex', 'SibSp', 'Parch')
df2 = df2.select('Survived', 'Pclass', 'Sex', 'SibSp', 'Parch')

# Convert male/female to binary
udf = UserDefinedFunction(lambda x: 1 if x == "male" else 0, IntegerType())
def sexToBin(df):
    df = df.select(*[udf(column).alias('Sex') \
    if column == 'Sex' else column for column in df.columns])
    return df
df = sexToBin(df)
df2 = sexToBin(df2)

# Format train for Logistic Regression as (label, features)
dfTrain = df.rdd.map(lambda x: Row(label=float(x[0]), features=Vectors.dense(x[1:]))).toDF().cache()
dfTest = df2.rdd.map(lambda x: Row(features=Vectors.dense(x[1:]))).toDF().cache()

# Create the LR model
lr = LogisticRegression(maxIter=100, regParam=0.1)
model = lr.fit(dfTrain)
pred = model.transform(dfTest).select('prediction')

print(" ")
result = pred.first()
print(result)

#Stop the Spark session
sc.stop()