# Databricks notebook source
# DBTITLE 1,Import Dependencies
from pyspark.sql.functions import DataFrame

# COMMAND ----------

# DBTITLE 1,Build Event Hub Connection Properties
def build_eventhub_connectionproperties (connection_string: str, consumer_group: str) -> dict:
    "Builds event hub connection properties"
    
    connectionproperties = {
      'eventhubs.connectionString' :  sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connection_string),
      'eventhubs.consumerGroup' : consumer_group
    }
    
    return connectionproperties

# COMMAND ----------

# DBTITLE 1,Query Event Hub
def query_eventhub(connectionproperties: dict) -> DataFrame:
    "Queries event hub based on connection properties passed in and returns a data frame. Must be a consumer group present."
    
    try:
        if not(connectionproperties['eventhubs.consumerGroup']):
            raise Exception("Must specify a consumer group to read event hub.")
    
        df = (spark
             .readStream
             .format("eventhubs")
             .options(**connectionproperties)
             .load() 
             )
    
        return df
    except Exception as e:
        raise Exception('Function query_eventhub has failed') from e.with_traceback(e.__traceback__)