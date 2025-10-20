# db.py

import sqlite3
from logger import logger 

class ExpenseDB:
    def __init__(self, DB_NAME="expenses.db"):
        self.DB_NAME = DB_NAME
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_table_expenses()

    def create_table_expenses(self):
        """Create the expenses table if it does not exist"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                note TEXT
            )
        """)
        self.conn.commit()
        
    def add_expense(self, date, category, amount, note=""):
        """Add a new expense in the expenses table"""
        if amount < 0:
            print("A negative amount is not valid")
            logger.error(f"Attempt to enter a negative amount: {amount}")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO expenses (date, category, amount, note)
                VALUES (?, ?, ?, ?)
            """, (date, category, amount, note))
            self.conn.commit()
            print(f"Expense added in category {category} - {amount:.2f}")
            logger.info(f"Expense added: Date={date}, Category={category}, Amount={amount}, Note={note}")
        except Exception as e:
            print("Error adding a new expense:", e)
            logger.error(f"Error in add_expense: {e}")
    
    def get_expenses(self, order_by_amount=None):
        """Returns all the expenses from the database. Data can optionally be ordered by amount (ASC or DESC)."""
        try:
            if order_by_amount == "asc":
                self.cursor.execute("SELECT * FROM expenses ORDER BY amount ASC")
            elif order_by_amount == "desc":
                self.cursor.execute("SELECT * FROM expenses ORDER BY amount DESC")
            else:
                self.cursor.execute("SELECT * FROM expenses")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error retrieving the expenses:", e)
            logger.error(f"Error in get_expenses: {e}")
            return []
    
    def delete_expense(self, expense_id):
        """Delete an expense by its ID."""
        try: 
            self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                print(f"No expense with the entered ID found {expense_id}")
                logger.warning(f"Attempt to delete an expense with the ID={expense_id}. Not found.")
            else:
                print(f"Expense with ID={expense_id} successfully deleted.")
                logger.info(f"Expense with ID={expense_id} successfully deleted")
        except Exception as e:
            print(f"Error deleting the expense: {e}")
            logger.error(f"Error in delete_expense. ID={expense_id}: {e}")
    
    def update_expense(self, expense_id, date=None, category=None, amount=None, note=None):
        """Updates an expense by its ID and allows to modify all the fields in the table"""
        try:
            if amount is not None and amount < 0:
                print("A negative amount is not valid.")
                logger.error(f"Attempt to enter a negative amount: {amount}")
                return
            
            updates = []
            parameters = []
            
            if date: 
                updates.append("date=?")
                parameters.append(date)
            if category:
                updates.append("category=?")
                parameters.append(category)                
            if amount is not None:
                updates.append("amount=?")
                parameters.append(amount)
            if note:
                updates.append("note=?")
                parameters.append(note)
            if not updates:
                print("No data available to update.")
                logger.warning(f"Attempt to update the expense with ID={expense_id}. No new data provided.")
                return
            
            parameters.append(expense_id)
            sql = f"UPDATE expenses SET {', '.join(updates)} WHERE id=?"
            
            self.cursor.execute(sql, tuple(parameters))
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                print(f"No expense found with ID {expense_id}.")
                logger.warning(f"Attempt to update an expense with ID={expense_id}. Expense not found")
            else:
                print(f"Expense with ID={expense_id} successfully updated")
                logger.info(f"Updated expense: ID={expense_id}, "
                            f"Date={date}, "f"Category={category}, Amount={amount}, Note={note}")
            
        except Exception as e:
            print(f"Error updating the expense: {e}")
            logger.error(f"Error in update_expense: ID={expense_id}: {e}")
        
    def get_expenses_by_category(self, category, order_by_amount=None):
        """Return all the expenses filtered by category, optionally data it can be ordered by amount (ASC or DESC)."""
        try:
            if order_by_amount == "asc":
                self.cursor.execute("SELECT * FROM expenses WHERE category=? ORDER BY amount ASC", (category,))
            elif order_by_amount == "desc":
                self.cursor.execute("SELECT * FROM expenses WHERE category=? ORDER BY amount DESC", (category,))
            else:
                self.cursor.execute("SELECT * FROM expenses WHERE category=?", (category,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving expenses by category: {e}")
            logger.error(f"Error in get_expenses_by_category: {e}")
            return []

    def get_expenses_between_dates(self, start_date, end_date, order_by_amount=None):
        """Return all the expenses between two dates, optionally data it can be ordered by amount (ASC or DESC)."""
        try:
            if order_by_amount == "asc":
                self.cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY amount ASC", (start_date, end_date))
            elif order_by_amount == "desc":
                self.cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY amount DESC", (start_date, end_date))
            else:
                self.cursor.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ?", (start_date, end_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving expenses by date range: {e}")
            logger.error(f"Error in get_expenses_between_dates: {e}")
            return []
        
    def get_report_category(self):
        """Return the total expenses grouped by category."""
        try:
            self.cursor.execute("""
                SELECT category, SUM(amount)
                FROM expenses
                GROUP BY category
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error generating the category report: {e}")
            logger.error(f"Error in get_report_by_category: {e}")
            return []
    
    def get_report_by_date_range(self, start, end):
        """Return the total amount, the number of expenses and the average within a date range."""
        try:
            self.cursor.execute("""
                SELECT SUM(amount), COUNT(*), AVG(amount)
                FROM expenses
                WHERE date BETWEEN ? AND ?
                """, (start, end))
            return self.cursor.fetchone()
        except Exception as e:
            print("Error generating the date range report:", e)
            logger.error(f"Error in get_report_by_date_range: {e}")
            return None
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
        
        
