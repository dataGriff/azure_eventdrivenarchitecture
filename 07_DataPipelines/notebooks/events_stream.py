# Databricks notebook source
# MAGIC %run ./events_tools

# COMMAND ----------

eventhub_conn_customer = "Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=MH5z8b0Hkf5hKViER/vTyytoamDtscNL/z1VezFZG9o=;EntityPath=customer"

eventhub_conn_lead ="Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=H4drHBjrfWm3Pcv6bFPyI0Pvnw8p5ddJkt7IURNEpcc=;EntityPath=lead"

eventhub_conn_sale ="Endpoint=sb://events001-ehns-eun-griff2.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=/mlxpw+ujWxJyJOpOx3v2YfxVjmIPs+VeUQDTYUh0MM=;EntityPath=sale"
 
consumer_group = 'datalake'

# COMMAND ----------

# DBTITLE 1,Customer
connection_properties = build_eventhub_connectionproperties(eventhub_conn_customer,consumer_group)
df_customer = query_eventhub(connection_properties)
display(df_customer.selectExpr("cast(Body as string) as Body"))

# COMMAND ----------

# DBTITLE 1,Lead
connection_properties = build_eventhub_connectionproperties(eventhub_conn_lead,consumer_group)
df_lead = query_eventhub(connection_properties)
display(df_lead.selectExpr("cast(Body as string) as Body"))

# COMMAND ----------

# DBTITLE 1,Sale
connection_properties = build_eventhub_connectionproperties(eventhub_conn_sale,consumer_group)
df_sale = query_eventhub(connection_properties)
display(df_sale.selectExpr("cast(Body as string) as Body"))