from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
class Models:
    def __init__(self):
        self.engine = create_engine(os.environ.get('DB_URL', 'postgresql://postgres:dd20@localhost:5432/POS'))

    def executeRawSql(self, statement, params={}):
        out = None
        with self.engine.connect() as con:
            out = con.execute(text(statement), params)
        return out

    def addUser(self, value):
        return self.executeRawSql("""INSERT INTO user_register (email, password) VALUES(:email, :password);""", value)

    def addBook(self, value):
        # value has the form { "isbn": 2, "title": "The Silmarillion", "author": "Tolkien" }
        return self.executeRawSql("""INSERT INTO book(isbn, title, author) VALUES(:isbn, :title, :author);""", value)

    def updateAssignment(self, value):
        return self.executeRawSql("""UPDATE assignment SET email=:email WHERE isbn=:isbn;""", value)
    
    def addAssignment(self, value):
        return self.executeRawSql("""INSERT INTO assignment(email, isbn) VALUES(:email, :isbn);""", value)

    def getAllAssignments(self):
        return self.executeRawSql("SELECT * FROM assignment;").mappings().all()

    def deleteAssignment(self, value):
        return self.executeRawSql("DELETE FROM assignment where email=:email and isbn=:isbn;", value)

    def getAssignment(self, value):
        values = self.executeRawSql("""SELECT * FROM assignment WHERE email=:email and isbn=:isbn;""", value).mappings().all()
        if len(values) == 0:
            raise Exception("Book {} has not been assignment by {}".format(value["isbn"], value["email"]))
        return values[0]
    
    def getDayStatistics(self):
        return self.executeRawSql(
            """Select pd.Product_Description,p.Store_Key,dd.Date_NUM,
            SUM(Sales_Quantity) as total_quantity, 
            SUM(Sales_Dollar_Amount) as total_sales, 
            SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
            FROM POS_Retail_Sales_Transaction_Fact P 
            join Product_Dimension pd 
            ON p.Product_Key = pd.Product_Key
            join Date_dimension dd
            ON P.Date_key = dd.Date_key
            Group by dd.Date_NUM, p.product_key, p.store_key, pd.product_description
            order by dd.Date_NUM""")
    
    def getStoreTotalSales(self):
        return self.executeRawSql(
            """Select s.store_name, sum(po.sales_dollar_amount) AS total_sales
            FROM store_dimension s, pos_retail_sales_transaction_fact po
            WHERE po.store_key = s.store_key 
            GROUP BY s.store_name"""
        )
    
    def getMonthStatistics(self):
        return self.executeRawSql(
            """Select pd.Product_Description,
            p.Store_Key,
            dd.calendar_month,
            SUM(Sales_Quantity) as total_quantity, 
            SUM(Sales_Dollar_Amount) as total_sales, 
            SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
            
            FROM POS_Retail_Sales_Transaction_Fact P 
            join Product_Dimension pd 
            ON p.Product_Key = pd.Product_Key
            join Date_dimension dd
            ON P.Date_key = dd.Date_key
            Group by dd.calendar_month, p.product_key, p.store_key, pd.product_description
            order by dd.calendar_month ASC;"""
        )

    def getProductSales(self):
        return self.executeRawSql(
            """Select p.product_description, sum(po.sales_dollar_amount) AS total_sales
            FROM product_dimension p, pos_retail_sales_transaction_fact po
            WHERE po.product_key = p.product_key
            GROUP BY p.product_description""")

    def getStoreMonth(self):
        return self.executeRawSql(
            """Select s.store_name,dd.calendar_month,
            SUM(Sales_Quantity) as total_quantity, 
            SUM(Sales_Dollar_Amount) as total_sales,
            SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
            FROM POS_Retail_Sales_Transaction_Fact P 
            join Product_Dimension pd 
            ON p.Product_Key = pd.Product_Key
            join Date_dimension dd
            ON P.Date_key = dd.Date_key
            join Store_dimension s
            ON p.store_key = s.store_key
            Group by dd.calendar_month, s.store_name
            order by dd.calendar_month ASC;"""
        )

    def getStoreDay(self):
        return self.executeRawSql("""Select s.store_name,dd.Date_NUM,
        SUM(Sales_Quantity) as total_quantity, 
        SUM(Sales_Dollar_Amount) as total_sales, 
        SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
        FROM POS_Retail_Sales_Transaction_Fact P 
        join Product_Dimension pd 
        ON p.Product_Key = pd.Product_Key
        join Date_dimension dd
        ON P.Date_key = dd.Date_key
        join Store_dimension s
        ON p.store_key = s.store_key
        Group by dd.Date_NUM, s.store_name
        order by dd.Date_NUM""")

    def getProductDay(self):
        return self.executeRawSql("""Select pd.product_description,dd.Date_NUM,
            SUM(Sales_Quantity) as total_quantity, 
            SUM(Sales_Dollar_Amount) as total_sales, 
            SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
            FROM POS_Retail_Sales_Transaction_Fact P 
            join Product_Dimension pd 
            ON p.Product_Key = pd.Product_Key
            join Date_dimension dd
            ON P.Date_key = dd.Date_key
            Group by dd.Date_NUM, pd.product_description
            order by dd.Date_NUM;""")

    def getProductMonth(self):
        return self.executeRawSql("""Select pd.Product_Description,dd.calendar_month,
            SUM(Sales_Quantity) as total_quantity, 
            SUM(Sales_Dollar_Amount) as total_sales, 
            SUM(Gross_Profit_Dollar_Amount) as total_gross_profit
            FROM POS_Retail_Sales_Transaction_Fact P 
            join Product_Dimension pd 
            ON p.Product_Key = pd.Product_Key
            join Date_dimension dd
            ON P.Date_key = dd.Date_key
            Group by dd.calendar_month, pd.product_description
            order by dd.calendar_month ASC;""")


    def getAllStore(self):
        return self.executeRawSql("SELECT * FROM store_dimension;").mappings().all()

    def getAllDate(self):
        return self.executeRawSql("SELECT * FROM Date_Dimension;").mappings().all()

    def getAllProduct(self):
        return self.executeRawSql("SELECT * FROM Product_Dimension;").mappings().all()

    def getAllPos(self):
        return self.executeRawSql("SELECT * FROM POS_Retail_Sales_Transaction_Fact;").mappings().all()

    def getUserByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM user_register WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("User {} does not exist".format(email))
        return values[0]

    def getStudentByEmail(self, email):
        values = self.executeRawSql("""SELECT * FROM student WHERE email=:email;""", {"email": email}).mappings().all()
        if len(values) == 0:
            raise Exception("Student {} does not exist".format(email))
        return values[0]

    def createModels(self):
        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS user_register (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL);
        """)

        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS Product_Dimension (
            Product_Key NUMERIC PRIMARY KEY,
            Product_Description VARCHAR(64) NOT NULL,
            Category_Description VARCHAR(64) NOT NULL,
            Department_Description VARCHAR(64) NOT NULL,
            Price NUMERIC NOT NULL,
            Cost_ NUMERIC NOT NULL,
            Fat_Content VARCHAR(64) NOT NULL);
        """)

        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS Date_dimension (
            Date_Key NUMERIC PRIMARY KEY,
            Date_NUM DATE NOT NULL,
            Day_of_Week VARCHAR(64) NOT NULL,
            Calendar_Month VARCHAR(64) NOT NULL,
            Calendar_Year VARCHAR(64) NOT NULL,
            Weekday_Indicator VARCHAR(64) NOT NULL);
        """)

        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS Store_dimension (
            Store_Key NUMERIC PRIMARY KEY,
            Store_Name VARCHAR(64) NOT NULL,
            Store_Number NUMERIC(64) NOT NULL,
            Store_Region VARCHAR(64) NOT NULL);
        """)

        self.executeRawSql(
        """CREATE TABLE IF NOT EXISTS POS_Retail_Sales_Transaction_Fact (
            Product_Key NUMERIC REFERENCES Product_Dimension (Product_Key)
            ON UPDATE CASCADE ON DELETE CASCADE
            DEFERRABLE INITIALLY DEFERRED,
            Store_Key NUMERIC REFERENCES Product_Dimension (Product_Key)
            ON UPDATE CASCADE ON DELETE CASCADE
            DEFERRABLE INITIALLY DEFERRED,
            POS_Transaction_Number VARCHAR(64) PRIMARY KEY,
            Sales_Quantity NUMERIC NOT NULL,
            Sales_Dollar_Amount NUMERIC NOT NULL,
            Gross_Profit_Dollar_Amount NUMERIC NOT NULL,
            Date_Key NUMERIC NOT NULL,
            FOREIGN KEY (Date_Key) REFERENCES Date_dimension (Date_Key)
            ON UPDATE CASCADE ON DELETE CASCADE
            DEFERRABLE INITIALLY DEFERRED);
        """)
