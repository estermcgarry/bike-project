import mysql.connector

cnx = mysql.connector.connect(user='admin', password='picanha123',
                              host='bailebikesdb.ck068lrxfgr6.us-east-1.rds.amazonaws.com',
                              database='')
cnx.close()