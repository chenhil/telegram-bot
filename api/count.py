import os
import psycopg2

def count(command):
    url = 'postgres://whkrhdwpenhhym:598bb25bd018891284d02f939948b0b25a06df4508c251143f98fe1671a12f43@ec2-54-164-22-242.compute-1.amazonaws.com:5432/d5i6go6su3sf1h'
    connection = psycopg2.connect(url,sslmode='require')
    cursor = connection.cursor()

    query = "UPDATE command set count = count + 1 WHERE command = '{}' or command_2 = '{}';".format(command, command)
    cursor.execute(query)
    connection.commit()
    connection.close()

