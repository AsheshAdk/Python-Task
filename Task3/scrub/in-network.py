from pyspark.sql import SparkSession

from pyspark.sql.functions import explode,col,expr,array,when
from pyspark.sql.types import ArrayType, IntegerType, ShortType

spark = SparkSession.builder.appName("task1")
spark = SparkSession.builder.appName('Network').config("spark.driver.memory", "4g").getOrCreate()

spark

df_pyspark = spark.read.option('multiline','true').json('rate.json')

df_pyspark.printSchema()

negotiated_rates_df = df_pyspark.withColumn("row1",explode("negotiated_rates"))
negotiated_new = negotiated_rates_df.withColumn("id",explode("row1.provider_references"))
negotiated_prices_df = negotiated_new.withColumn("row2",explode("row1.negotiated_prices"))

rate_df = negotiated_prices_df.select("billing_code","billing_code_type","negotiation_arrangement",
                                      col("row2.billing_code_modifier").alias("billing_code_modifier"),
                                      col("row2.billing_class").alias("billing_class"),
                                      col("row2.negotiated_rate").alias("negotiated_rate"),
                                      col("row2.service_code").alias("service_code"),
                                      col("id").alias("provider_group_id"),
                                      col("row2.negotiated_type").alias("negotiated_type"))
rate_df.printSchema()

rate_df.show(10)

rate_df.printSchema()

net_cast = rate_df.withColumn("service_code", col("service_code").cast(ArrayType(IntegerType())))

net_cast.write.parquet('net_output.parquet')

net_cast.printSchema()