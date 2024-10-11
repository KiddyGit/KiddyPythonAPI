import pyodbc


UIDSalt = 'AB123CD'



def connection():
    
    connection_string = (
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=tcp:kiddysqlserver.database.windows.net,1433;'
        'Database=kiddyDatabase;'
        'Uid=kiddysqlserver;'
        'Pwd=Kiddy123sql;'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )

    try:
        conn = pyodbc.connect(connection_string)
        print("Connected to the database successfully!")
        return conn
    except pyodbc.Error as e:
        print("Error connecting to the database:", e)
        return None
