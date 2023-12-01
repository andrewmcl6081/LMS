from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "LMS.db"

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully connected to sqlite")
        
        sqlite_select_query = "SELECT * FROM BOOK;"
        cursor.execute(sqlite_select_query)
        data = cursor.fetchall()
        
        cursor.close()
        return jsonify({ "data": data})
    
    except Exception as e:
        print("Error while connecting to sqlite", e)


if __name__ == '__main__':
    app.run(debug=True)