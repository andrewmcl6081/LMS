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
        print("Error: ", e)

    return render_template('books.html', books=data)

@app.route('/checkout', methods=['POST'])
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
        print("Error: ", e)

    return redirect(url_for('home'))

@app.route('/borrower', methods=['GET'])
def borrower():
    return render_template('borrower.html')

@app.route('/new_borrower', methods=['POST'])
def new_borrower():
    fullname = request.form.get('fullname')
    address = request.form.get('address')
    phone = request.form.get('phone')
    
    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        
        # Insert Query
        insert_query = """
                INSERT INTO Borrower(name, address, phone)
                VALUES(?, ?, ?);
                """

        cursor.execute(insert_query, (fullname, address, phone))
        sqliteConnection.commit()
        
        # Select Query
        select_query = """
                SELECT card_no
                FROM Borrower
                WHERE name=? AND address=? AND phone=?;
                """
        
        cursor.execute(select_query, (fullname, address, phone))
        data = cursor.fetchall()
        
        cursor.close()
        sqliteConnection.close()
        
        # At this point we have inserted a new borrower and obtained their card_no
        # ToDo: return the card_no to the frontend that the variable data contains
    except Exception as e:
        print('Error: ', e)
        
    return redirect(url_for('borrower'))
    

if __name__ == '__main__':
    app.run(debug=True, port=3000)