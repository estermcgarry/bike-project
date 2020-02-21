import sqlalchemy

connect_string = 'mysql://admin:picanha123@bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com/BikeData'
1
sql_engine = sqlalchemy.create_engine(connect_string)
