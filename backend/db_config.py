import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='bay9r1xqivp65pupciyt-mysql.services.clever-cloud.com',           
        user='uetsbhu157iqoriu',
        password='your_pwd',
        database='bay9r1xqivp65pupciyt',
        port=3306              
    )
