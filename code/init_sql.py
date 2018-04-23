from sqlalchemy import create_engine

import mysql.connector
import pandas as pd

class PropertyDatabase:
   def __init__(self):
    #    self.engine = create_engine('mysql+mysqlconnector://patrickkennedy:root@127.0.0.1/spaceDirect')
    self.engine = mysql.connector.connect(
            user='root',
            password='My Pass F0r MySQL',
            host='127.0.0.1',
            database='spaceDirect')


   def query_sql(self, SQL_statement):
       return pd.read_sql(SQL_statement,self.engine)

   def write_to_sql(self, df,table_name, drop_append = 'append'):
       df.to_sql(table_name, self.engine, if_exists=drop_append)
       print 'Succesfully wrote {} rows to the table {}'.format(df.shape[0], table_name)







#
# conn = mysql.connector.connect(
#         user='root',
#         password='My Pass F0r MySQL',
#         host='127.0.0.1',
#         database='spaceDirect')
#
# cur = conn.cursor()
#
# query = ("SELECT ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable, PropertyDescription FROM listingstemp_dt LIMIT 1")
#
# cur.execute(query)
#
# for (ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable, PropertyDescription) in cur:
#     print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable,  PropertyDescription))
#
# cur.close()
# conn.close()
