from pyspark.sql import SparkSession

import psycopg2

spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.eventLog.gcMetrics.youngGenerationGarbageCollectors", "G1 Young Generation") \
    .config("spark.eventLog.gcMetrics.oldGenerationGarbageCollectors", "G1 Old Generation") \
    .getOrCreate()

df = spark.read.parquet("/home/zaki/Pictures/provider_output.parquet")
df1=spark.read.parquet("/home/zaki/Pictures/net_output.parquet")

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Ashesh",
    host="localhost",
    port=5432
)

jdbc_url = "jdbc:postgresql://localhost:5432/postgres"
connection_properties = {
    "user": "postgres",
    "password": "Ashesh",
    "driver": "org.postgresql.Driver"
}

df1.printSchema()

cur = conn.cursor()
create_table_query = """
DROP TABLE IF EXISTS in_network_data;
CREATE TABLE IF NOT EXISTS in_network_data (
    billing_code TEXT,
    billing_code_type TEXT,
    negotiation_arrangement TEXT,
    billing_code_modifier TEXT[],
    billing_class TEXT,
    negotiated_rate DOUBLE PRECISION,
    service_code INTEGER[],
    provider_group_id BIGINT,
    negotiated_type TEXT
);
"""

cur.execute(create_table_query)
conn.commit()

df1.write.jdbc(url=jdbc_url,table="in_network_data",mode="append", properties=connection_properties)
conn.commit()

cursor = conn.cursor()
provider_table = """
CREATE TABLE IF NOT EXISTS provider_table(
    provider_group_id BIGINT,
    npi BIGINT,
    tin_type SMALLINT,
    tin TEXT
);
"""
cursor.execute(provider_table)
conn.commit()

df.write.jdbc(url=jdbc_url,table="provider_table",mode="append", properties=connection_properties)
conn.commit()