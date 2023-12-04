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

    return render_template('index.html', books=data)

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
        
        new_card_no = data[0][0]
        
        # At this point we have inserted a new borrower and obtained their card_no
        # ToDo: return the new_card_no to the frontend
        
        return render_template('borrower.html', new_card_no=new_card_no)
    except Exception as e:
        print('Error: ', e)
        
    return redirect(url_for('borrower'))
    
@app.route('/book', methods=['GET'])
def book():
    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully connected: BOOK")
        
        # Select Query
        select_query = """
                SELECT branch_id, branch_name
                FROM Library_Branch;
                """
        cursor.execute(select_query)
        data = cursor.fetchall()

        cursor.close()
        sqliteConnection.close()
    except Exception as e:
        print("Error: ", e)

    return render_template('book.html', branches=data)

@app.route('/new_book', methods=['POST'])
def new_book():
    print('in new book route')
    branch_ids = request.form.getlist('branch_ids')  # This will be a list of branch IDs

    book_title = request.form.get('booktitle')
    author = request.form.get('author')
    publisher = request.form.get('publisher')

    # Add to Book and required tables table
    try:
        sqliteConnection = sqlite3.connect('LMS.db')
        cursor = sqliteConnection.cursor()
        print("Database successfully connected: NEW BOOK")
        
        # Insert into Book table query
        insert_book_query = """
                INSERT INTO Book(title, book_publisher)
                VALUES(?, ?);
                """

        cursor.execute(insert_book_query, (book_title, publisher))
        sqliteConnection.commit()

        # Select new book id query
        select_id_query = """
                SELECT book_id
                FROM Book
                WHERE title = ? AND book_publisher = ?;
                """
        
        cursor.execute(select_id_query, (book_title, publisher))
        new_book_id = cursor.fetchall()[0][0]
    
        # Insert into Author table query
        insert_author_query = """
                INSERT INTO Book_Authors(book_id, author_name)
                VALUES(?, ?);
                """

        cursor.execute(insert_author_query, (new_book_id, author))
        sqliteConnection.commit()

        for branch_id in branch_ids:
            checkbox_name = f"branchCheck_{branch_id}"
            copies_name = f"noCopies_{branch_id}"

            # Check if the checkbox was checked
            checkbox_checked = checkbox_name in request.form

            if checkbox_checked:
                # Get the value of the text input
                no_copies = request.form.get(copies_name)

                # Insert into Copies table query
                insert_copies_query = """
                    INSERT INTO Book_Copies(book_id, branch_id, no_of_copies)
                    VALUES(?, ?, ?);
                    """
                
                cursor.execute(insert_copies_query, (new_book_id, branch_id, no_copies))
                sqliteConnection.commit()

            # Now you have the checkbox state and the number of copies for this branch ID
            print(f"Branch ID: {branch_id}, Checked: {checkbox_checked}, No. of Copies: {no_copies}")

        cursor.close() 
        sqliteConnection.close()
    except Exception as e:
        print("Error: ", e)

    return redirect(url_for('home'))

@app.route('/find_book', methods=['GET', 'POST'])
def find_book():
    booktitle = request.form.get("booktitle")
    
    if booktitle:
        try:
            sqliteConnection = sqlite3.connect('LMS.db')
            cursor = sqliteConnection.cursor()
            
            select_query = """
                    SELECT B.title, BC.branch_id, BC.no_of_copies
                    FROM Book B
                    JOIN Book_Copies BC ON B.book_id=BC.book_id
                    WHERE B.title=?;
                    """
            
            cursor.execute(select_query, (booktitle,))
            data = cursor.fetchall()
            
            cursor.close()
            sqliteConnection.close()
            
            return render_template('findBook.html', data_search_result=data)
        except Exception as e:
            print('Error: ', e)
    
    return render_template('findBook.html')

@app.route('/find_loan', methods=['GET', 'POST'])
def find_loan():
    return render_template('lookUpLoan.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)