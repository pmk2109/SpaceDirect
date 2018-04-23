import mysql.connector

conn = mysql.connector.connect(
        user='root',
        password='My Pass F0r MySQL',
        host='127.0.0.1',
        database='spaceDirect')

cur = conn.cursor()

query = ("SELECT ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable, PropertyDescription FROM listingstemp_dt LIMIT 1")

cur.execute(query)

for (ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable, PropertyDescription) in cur:
    print("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(ListingType, StreetAddress, City, State, ZipCode, SuiteNumber, AvailableSF, DateAvailable,  PropertyDescription))

cur.close()
conn.close()

