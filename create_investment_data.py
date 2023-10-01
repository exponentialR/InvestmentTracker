import sqlite3

table_dictionary  = {
    "Real Estate": """CREATE TABLE IF NOT EXISTS RealEstate (
                      Property_ID TEXT,
                      Property_Location TEXT,
                      Property_Type TEXT,
                      Purchase_Date TEXT,
                      Purchase_Price REAL,
                      Current_Valuation REAL,
                      Rent_Income REAL,
                      Expenses REAL,
                      Mortgage_Details TEXT
                      )""",
    "Agriculture": """CREATE TABLE IF NOT EXISTS Agriculture (
                      Farm_ID TEXT,
                      Location TEXT,
                      Type_of_Crop TEXT,
                      Sowing_Date TEXT,
                      Harvest_Date TEXT,
                      Investment_Cost REAL,
                      Revenue REAL,
                      Land_Size REAL
                      )""",
    "Stocks": """CREATE TABLE IF NOT EXISTS Stocks (
                 Stock_ID TEXT,
                 Ticker TEXT,
                 Purchase_Date TEXT,
                 Purchase_Price REAL,
                 Number_of_Shares REAL,
                 Current_Price REAL,
                 Dividends REAL
                 )""",
    "Cryptocurrency": """CREATE TABLE IF NOT EXISTS Cryptocurrency (
                         Crypto_ID TEXT,
                         Coin_Name TEXT,
                         Purchase_Date TEXT,
                         Purchase_Price REAL,
                         Quantity REAL,
                         Current_Price REAL,
                         Wallet_ID TEXT
                         )""",
    "Loan": """CREATE TABLE IF NOT EXISTS Loan (
               Loan_ID TEXT,
               Borrower_Name TEXT,
               Principal_Amount REAL,
               Interest_Rate REAL,
               Start_Date TEXT,
               End_Date TEXT,
               Repayment_Schedule TEXT,
               Outstanding_Amount REAL
               )"""
}


def create_investment_table(investment_type):
    conn = sqlite3.connect("investment_tracker.db")
    c = conn.cursor()

    if investment_type in table_dictionary:
        c.execute(table_dictionary[investment_type])
        conn.commit()
    conn.close()