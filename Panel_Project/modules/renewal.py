import mysql.connector
mydb = mysql.connector.connect(
    host='94.130.224.50',
    user='flappeh',
    password="password",
    database='panel_db'
)


cursor = mydb.cursor()


def check_server(id):
    cursor.execute(f"SELECT * FROM servers where id={id};")
    row = ""
    for x in cursor:
        row =x
    return row

def set_renewable(id,duration):
    cursor.execute(f"UPDATE servers SET renewable=1 where id={id}")
    mydb.commit()
    cursor.execute(f"UPDATE servers SET renewal={int(duration)*30} where id={id}")
    mydb.commit()
    print(cursor.rowcount, "row updated")
    if cursor.rowcount > 0:
        return True
    else:
        return False

