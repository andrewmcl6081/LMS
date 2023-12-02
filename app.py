from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "LMS.db"

@app.route('/', methods=['GET'])
def home():
    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully connected: INITIAL")
        
        sqlite_select_query = "SELECT * FROM User_View;"
        cursor.execute(sqlite_select_query)

        data = cursor.fetchall()
        cursor.close()
        sqliteConnection.close()
        
    except Exception as e:
        print("Error while connecting to sqlite", e)

    return render_template('books.html', books=data)

@app.route('/checkout/', methods=['POST'])
def checkout():
    bookid = request.form.get('bookid')
    cardno = request.form.get('cardno')
    branchid = request.form.get('branchid')

    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully connected: CHECKOUT")
        
        query = """
                INSERT INTO Book_Loans(book_id, branch_id, card_no, date_out, due_date)
                VALUES(?, ?, ?, CURRENT_DATE, date('now', '+30 days'));
            """
        
        cursor.execute(query, (bookid, branchid, cardno))
        sqliteConnection.commit()

        cursor.close()
        sqliteConnection.close()
    
    except Exception as e:
        print("Error while connecting to sqlite", e)

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)