from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import pandas as pd
import joblib

# Load ML model
model = joblib.load("ml/anomaly_model.pkl")

spark = SparkSession.builder \
    .appName("ElectricityAIStreaming") \
    .getOrCreate()

# Schema
schema = StructType([
    StructField("voltage", IntegerType()),
    StructField("current", DoubleType()),
    StructField("temperature", DoubleType()),
    StructField("machine_status", IntegerType())
])

# Read Kafka stream
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "factory_data") \
    .load()

# Convert Kafka value to string
json_df = df.selectExpr("CAST(value AS STRING) as json")

# Parse JSON
parsed_df = json_df.select(
    from_json(col("json"), schema).alias("data")
).select("data.*")

# Calculate power
final_df = parsed_df.withColumn(
    "power",
    col("voltage") * col("current")
)

# ML Prediction Function
# ML Prediction Function
def predict_anomaly(batch_df, batch_id):

    pandas_df = batch_df.toPandas()

    if len(pandas_df) > 0:

        features = pandas_df[
            ["voltage", "current", "temperature", "power"]
        ]

        predictions = model.predict(features)

        pandas_df["prediction"] = predictions

        pandas_df["status"] = pandas_df["prediction"].apply(
            lambda x: "ANOMALY" if x == -1 else "NORMAL"
        )

        print("\n========== AI PREDICTIONS ==========")
        print(pandas_df)

        # Save to CSV
        pandas_df.to_csv(
            "dashboard/live_data.csv",
            mode="a",
            header=False,
            index=False
        )

# Streaming query
query = final_df.writeStream \
    .foreachBatch(predict_anomaly) \
    .outputMode("append") \
    .start()

query.awaitTermination()