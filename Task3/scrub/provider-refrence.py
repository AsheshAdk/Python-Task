from pyspark.sql import SparkSession

from pyspark.sql.functions import explode,col,expr,array,when
from pyspark.sql.types import ArrayType, IntegerType, ShortType

spark = SparkSession.builder.appName("task").getOrCreate()

spark

df_pyspark = spark.read.option('multiline','true').json('provider.json')

df_pyspark.printSchema()

provider_group = df_pyspark.withColumn("new_provider", explode("provider_groups"))
provider_new = provider_group.withColumn("npi",explode("new_provider.npi"))
provider_again = provider_new.select(
    "provider_group_id",
    col("npi").alias("npi"),
    col("new_provider.tin.type").alias("tin_type"),
    col("new_provider.tin.value").alias("tin")
)

provider_again.printSchema()

provider_again.show()

provider_cast = provider_again.withColumn("tin_type", col("tin_type").cast(ShortType()))

provider_cast.printSchema()

provider_cast.write.parquet('provider_output.parquet')