# Copyright (C) 2015 Ehsan Mohyedin Kermani
# Contact: ehsanmo1367@gmail.com, ehsanmok@cs.ubc.ca
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import Row
from pyspark.sql.types import IntegerType
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
df = spark.read.format("csv").option("header", "true").load("./data/titanic.csv")

# Extract the test passenger ID
testPassengerId = df.select('PassengerId').rdd.map(lambda x: x.PassengerId)

# Select your features, leaving out target from test (Survived)
df = df.select('Survived', 'Pclass', 'Sex', 'SibSp', 'Parch')

# Convert male/female to binary
udf = UserDefinedFunction(lambda x: 1 if x == "male" else 0, IntegerType())
def sexToBin(df):
    df = df.select(*[udf(column).alias('Sex') \
    if column == 'Sex' else column for column in df.columns])
    return df
df = sexToBin(df)

# Format train for Logistic Regression as (label, features)
df = df.rdd.map(lambda x: Row(label=float(x[0]), features=Vectors.dense(x[1:]))).toDF().cache()

# Split the data into train and test sets
dfTrain, dfTest = df.randomSplit([.8,.2],seed=1234)

# Create the LR model
lr = LogisticRegression(maxIter=100, regParam=0.1)
model = lr.fit(dfTrain)
pred = model.transform(dfTest).select('label', 'prediction', 'rawPrediction')
pred.show()

# Evaluate the model
evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction")
perfVal = evaluator.evaluate(pred)
perfName = evaluator.getMetricName()
print(perfName + " : " + str(perfVal))
print("Coefficients: " + str(model.coefficients))
print("Intercepts: " + str(model.intercept))

#Stop the Spark session
sc.stop()