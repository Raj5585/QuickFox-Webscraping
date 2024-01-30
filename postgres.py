#connect and store news to postgresdatabase

import psycopg2
from psycopg2 import sql
from datetime import datetime

def sendtodb(newsdict, domain):
    current_datetime = datetime.now()
    current_date = current_datetime.date()

    # Replace these with your actual database connection details
    db_params = {
        'host': 'localhost',
        'database': 'samachar',
        'user': 'postgres',
        'password': 'rajkumar2056',
    }

    conn = psycopg2.connect(**db_params)
    if(conn):
        print("connection sucessful! ")

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    for key in newsdict.keys():
    # print(key)
        print(key)
        if(len(newsdict[key]) != 0):
            insert_query = f"""
                INSERT INTO newsbase  (title, link, keyword,domain,Date)
                VALUES ( '{newsdict[key][0]}', '{newsdict[key][1]}', '{key}','{domain}','{current_date}') """
            cursor.execute(insert_query)
            conn.commit()
        
    for key in newsdict.keys():
        if(len(newsdict[key]) != 0):
            insert_query = f"""
                INSERT INTO newsbase  (title, link, keyword,domain,Date)
                VALUES ( '{newsdict[key][0]}', '{newsdict[key][1]}', '{key}','{domain}','{current_date}') """
            cursor.execute(insert_query)
            conn.commit()
            


        # Close the cursor and connection
    cursor.close()
    print("connection close")
    conn.close()