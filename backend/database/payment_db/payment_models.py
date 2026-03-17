from sqlalchemy import Table,Column,Integer,String,MetaData,Boolean


metadata_obj = MetaData()

table = Table(
    "payment_table",
    metadata_obj,
    Column("payment_id",String,primary_key=True),
    Column("user_id",String),
    Column("price",Integer),
    Column("status",String)
)