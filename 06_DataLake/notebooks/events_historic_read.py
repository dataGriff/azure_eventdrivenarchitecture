# Databricks notebook source
account_name = "events001saeungriff2"
key = "9edptIYkUwq7SVVqwuyz8mPgffjja1mXR7f1L/tWN3wpaI6H0941KcVIGuXGCC1sz9ktappJdn7ai5OLV9G38w=="

# COMMAND ----------

spark.conf.set(f"""fs.azure.account.key.{account_name}.blob.core.windows.net""",
              f"""{key}""")

# COMMAND ----------

event = "sale"
prefix = f"""wasbs://{event}@events001saeungriff2.blob.core.windows.net/"""
path = f"""{prefix}*/*/*/*/*/*.avro"""

# COMMAND ----------

from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("spark-avro-json-sample") \
    .config('spark.hadoop.avro.mapred.ignore.inputs.without.extension', 'false') \
    .getOrCreate()
#storage->avro
avroDf = spark.read.format("com.databricks.spark.avro").load(path)
#avro->json
jsonRdd = avroDf.select(avroDf.Body.cast("string")).rdd.map(lambda x: x[0])
data = spark.read.json(jsonRdd) # in real world it's better to 
display(data)