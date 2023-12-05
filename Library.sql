DROP TABLE IF EXISTS Publisher;
CREATE TABLE Publisher (
    publisher_name  VARCHAR(40) PRIMARY KEY,
    phone           VARCHAR(15) NOT NULL,
    address         VARCHAR(50) NOT NULL   
);

DROP TABLE IF EXISTS Library_Branch;
CREATE TABLE Library_Branch (
    branch_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name     VARCHAR(15) NOT NULL,
    branch_address  VARCHAR(50) NOT NULL,
    late_fee        FLOAT
);

DROP TABLE IF EXISTS Borrower;
CREATE TABLE Borrower (
    card_no         INTEGER PRIMARY KEY AUTOINCREMENT,
    name            VARCHAR(25) NOT NULL,
    address         VARCHAR(50) NOT NULL,
    phone           VARCHAR(15) NOT NULL
);

DROP TABLE IF EXISTS Book;
CREATE TABLE Book (
    book_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title           VARCHAR(50) NOT NULL,
    book_publisher  VARCHAR(25),
    FOREIGN KEY(book_publisher) REFERENCES Publisher(publisher_name)
);

DROP TABLE IF EXISTS Book_Loans;
CREATE TABLE Book_Loans (
    book_id         INT NOT NULL,
    branch_id       INT,
    card_no         VARCHAR(20) NOT NULL,
    date_out        Date,
    due_date        Date,
    returned_date   Date,
    late            INT,
    PRIMARY KEY(book_id, branch_id, card_no),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(branch_id) REFERENCES Library_Branch(branch_id),
    FOREIGN KEY(card_no) REFERENCES Borrower(card_no)
);

DROP TABLE IF EXISTS Book_Copies;
CREATE TABLE Book_Copies (
    book_id         INT NOT NULL,
    branch_id       INT,
    no_of_copies    INT NOT NULL,
    PRIMARY KEY(book_id, branch_id),
    FOREIGN KEY(book_id) REFERENCES Book(book_id),
    FOREIGN KEY(branch_id) REFERENCES Library_Branch(branch_id)
);

DROP TABLE IF EXISTS Book_Authors;
CREATE TABLE Book_Authors (
    book_id         INT NOT NULL,
    author_name     VARCHAR(25) NOT NULL,
    PRIMARY KEY(book_id, author_name)
    FOREIGN KEY(book_id) REFERENCES Book(book_id)
);

-- #1
-- UPDATE Book_Loans
-- SET late=1
-- WHERE (returned_date > due_date);

-- UPDATE Book_Loans
-- SET late=0
-- WHERE returned_date <= due_date;

-- -- #2
-- UPDATE Library_Branch SET late_fee=1.00 WHERE branch_name='Main Branch';
-- UPDATE Library_Branch SET late_fee=1.50 WHERE branch_name='West Branch';
-- UPDATE Library_Branch SET late_fee=2.00 WHERE branch_name='East Branch';

-- #3
CREATE VIEW vBookLoanInfo AS
SELECT 
    BL.card_no, 
    BR.name, 
    BL.date_out, 
    BL.due_date, 
    BL.returned_date,
    (julianday(COALESCE(BL.returned_date, CURRENT_DATE)) - julianday(BL.date_out)) AS TotalDays,
    B.title,
    CASE
        WHEN BL.returned_date <= BL.due_date THEN 0
        WHEN BL.returned_date IS NULL THEN julianday(CURRENT_DATE) - julianday(BL.due_date)
        ELSE julianday(BL.returned_date) - julianday(BL.due_date)
    END AS days_late,
    BL.branch_id,
    CASE
        WHEN BL.late=1 AND BL.returned_date IS NULL THEN LB.late_fee * (julianday(CURRENT_DATE) - julianday(BL.due_date)) 
        WHEN BL.late=1 AND BL.returned_date IS NOT NULL THEN LB.late_fee * (julianday(BL.returned_date) - julianday(BL.due_date))
        ELSE 0.00
    END AS late_fee_balance
FROM Book_Loans BL
JOIN Borrower BR ON BL.card_no=BR.card_no
JOIN Book B ON B.book_id=BL.book_id
JOIN Library_Branch LB on LB.branch_id=BL.branch_id;


-- CREATE TRIGGER reduce_copies_trigger
-- AFTER INSERT ON Book_Loans
-- FOR EACH ROW
-- BEGIN
--     UPDATE Book_Copies
--     SET no_of_copies = no_of_copies - 1
--     WHERE book_id=NEW.book_id AND branch_id=NEW.branch_id;
-- END;


CREATE VIEW User_View AS
SELECT B.book_id, BC.branch_id, B.book_publisher, B.title, BC.no_of_copies
FROM Book B
JOIN Book_Copies BC ON B.book_id=BC.book_id;


-- SELECT B.title, BC.branch_id, BC.no_of_copies
-- FROM Book B
-- JOIN Book_Copies BC ON B.book_id=BC.book_id
-- WHERE B.title='A Tale of Two Cities';