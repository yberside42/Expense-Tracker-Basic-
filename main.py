# Main.py

from db import ExpenseDB
from config import CATEGORIES
from datetime import datetime
from utils import *
from logger import logger

def main():
    """Displays an interactive menu to access the program's functions."""
    db = ExpenseDB()
    
    while True:
        print("\n --- Expense Tracker Menu ---")
        print("1.- View all expenses.")
        print("2.- Add a new expense.")
        print("3.- Delete an expense.")
        print("4.- Update an expense.")
        print("5.- Search expenses by category.")
        print("6.- Search expenses by a date range.")
        print("7.- Export expenses to a CSV file.")
        print("8.- Export expenses by category to a CSV file.")
        print("9.- Export expenses by date range to a CSV file")
        print("10.- Generate a report by category.")
        print("11.- Generate a report by date range.")
        print("12.- Exit the program.")
        
        opc = input("Select an option (1-12): ")
        
        if opc == "1":
            print("\nOption 1: View all expenses.")
            
            order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
            if order_choice not in ["asc", "desc"]:
                order_choice = None
                
            expenses = db.get_expenses(order_by_amount=order_choice)
            
            if expenses: 
                print_expenses(expenses)
                logger.info(f"{len(expenses)} expenses displayed (order: {order_choice or 'none'}).")
            else:
                print("No expenses found.")
                logger.warning("Attempt to view the expenses, but the expenses list is empty.")
        
        elif opc == "2":
            print("\nOption 2: Add an expense.")
            
            date = input("Date (YYYY-MM-DD): ")
            
            print("\nAvailable Categories:")
            for i, cat in enumerate(CATEGORIES, start=1):
                print(f"{i}.{cat}")
            
            try:
                category_choice = int(input("Please choose a category (number): "))
                if 1 <= category_choice <= len(CATEGORIES):
                    category = CATEGORIES[category_choice - 1]
                else:
                    print("Invalid Input. Operation canceled.")
                    logger.warning(f"Invalid category: {category_choice}")
                    continue
            except ValueError:
                print("Invalid Input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
            
            try: 
                amount = float(input("Amount: "))
                if amount < 0:
                    print("A negative amount is not valid.")
                    logger.error(f"Attempt to enter a negative amount: {amount}.")
                    continue
            except ValueError:
                print("Invalid Input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
            
            note = input("Note (Optional / press Enter to skip): ")
            
            db.add_expense(date, category, amount, note)
            print(f"Expense succesfully added to the category: {category}.")
            logger.info(f"Expense added: Date={date}, Category={category}, Amount={amount:.2f}, Note={note}")
        
        elif opc == "3":
            print("\nOption 3: Delete an expense.")
            try:
                expense_id = int(input("Enter the expense ID you want to delete: "))
                confirm = input(f"Are you sure you want to delete the expense ID: {expense_id}? (y/n): ").lower()
                if confirm != "y":
                    print("Operation canceled")
                    logger.info(f"User canceled the operation. (id={expense_id}).")
                    continue
                
                db.delete_expense(expense_id)
                
            except ValueError:
                print("Invalid Input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
                
        elif opc == "4":
            print("\nOption 4: Update an expense.")
            
            try:
                expense_id = int(input("Enter the expense ID you want to update: "))
            except ValueError:
                print("Invalid Input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
            
            print("\nAvailable Categories:")
            for i, cat in enumerate(CATEGORIES, start=1):
                print(f"{i}.{cat}")
                
            category_choice = input("Please choose a new category (number or press Enter to skip):")
            new_category = None
            if category_choice.strip():
                try:
                    category_choice = int(category_choice)
                    if 1 <= category_choice <= len(CATEGORIES):
                        new_category = CATEGORIES[category_choice - 1]
                    else:
                        print("Invalid Input: Operation canceled.")
                        logger.warning(f"Out of range category entered: {category_choice}.")
                        continue
                except ValueError:
                    print("Invalid Input: Please enter a valid number.")
                    logger.error("Error: Invalid input was entered.")
                    continue

            new_amount = input("Please choose a new amount (press Enter to skip):")
            amount_value = None
            if new_amount.strip():
                try:
                    amount_value = float(new_amount)
                    if amount_value < 0:
                        print("A negative amount is not valid.")
                        logger.error(f"Attempt to enter a negative amount: {amount_value}.")
                        continue
                except ValueError:
                    print("Invalid input: Please enter a valid number")
                    logger.error(f"Error: Invalid input was entered: {new_amount}.")
                    continue
            
            new_note = input("New note (Optional / press Enter to skip): ")
    
            confirm = input("Are you sure you want to update the expense? (y/n): ").lower()
            if confirm != "y":
                print("Operation canceled.")
                logger.info(f"User canceled the operation (id={expense_id}).")
                continue
    
            db.update_expense(
                expense_id,
                category = new_category,
                amount = amount_value,
                note=new_note if new_note else None
            )
            
            print("Processing operation...")
        
        elif opc == "5":
            print("\nOption 5: Search expenses by category.")
            
            print("\nAvailable Categories:")
            for i, cat in enumerate(CATEGORIES, start=1):
                print(f"{i}.{cat}")
                
            try:
                category_choice = int(input("Please choose a category you want to see (number):"))
                if 1 <= category_choice <= len(CATEGORIES): 
                    category = CATEGORIES[category_choice - 1]
                    order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
                    if order_choice not in ["asc", "desc"]:
                        order_choice = None
                    expenses = db.get_expenses_by_category(category, order_by_amount=order_choice)
                    if expenses:
                        print(f"\nExpenses in the cateogry: '{category}':")
                        print_expenses(expenses)
                        logger.info(f"{len(expenses)} expenses returned in the cateogry: {category}")
                    else:
                        print(f"No expenses found in the category: '{category}'.")
                        logger.warning(f"No expenses found in the category: {category}.")
                else:
                    print("Invalid input: Operation canceled.")
                    logger.warning(f"Out of range category entered: {category_choice}.")
                    continue
            except ValueError:
                print("Invalid input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
            
        elif opc == "6":
            print("Option 6: Search expenses by a date range.")
            
            start, end = None, None
            try:
                start = input("\nEnter the start date (YYYY-MM-DD): ")
                end = input("Enter the end date (YYYY-MM-DD): ")
                
                datetime.strptime(start, "%Y-%m-%d")
                datetime.strptime(end, "%Y-%m-%d")
                
                order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
                if order_choice not in ["asc", "desc"]:
                    order_choice = None
                    
                expense_range = db.get_expenses_between_dates(start, end, order_by_amount=order_choice)
                
                if expense_range:
                    print(f"\nExpenses between {start} and {end}:")
                    print_expenses(expense_range)
                    logger.info(f"{len(expense_range)} expenses returned between {start} and {end}")
                else:
                    print(f"No expenses found between the dates: {start} and {end}")
                    logger.warning(f"No expenses found between the dates: {start} and {end}")
                        
            except ValueError:
                print("Invalid input: Please use the format YYYY-MM-DD.")
                logger.error(f"Invalid date entered: start={start}, end={end}")
                continue
            
        elif opc == "7":
            print("\nOption 7: Export expenses to a CSV file.")
            
            filename = input("Enter the file name (press Enter to use 'expenses.csv'): ").strip()
            if not filename:
                filename = "expenses.csv"
                
            expenses = db.get_expenses()
            export_to_csv(expenses, filename)
            print(f"Expenses successfuly exported to '{filename}'.")
            logger.info(f"Expenses exported to file: {filename}.")
            
        elif opc == "8":
            print("\nOption 8: Export expenses by category to a CSV file.")
            
            print("\nAvailable Categories:")
            for i, cat in enumerate(CATEGORIES, start=1):
                print(f"{i}. {cat}")
                
            try:
                choice = int(input("Please choose a category you want to export (number):"))
                if 1 <= choice <= len(CATEGORIES): # 
                    category = CATEGORIES[choice - 1]
                    order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
                    if order_choice not in ["asc", "desc"]:
                        order_choice = None
                        
                    expenses = db.get_expenses_by_category(category, order_by_amount=order_choice)
                    
                    if expenses:
                        filename = f"expenses_{category}.csv"
                        export_to_csv(expenses, filename=filename)
                        print(f"Expenses from category '{category} successfully exported to '{filename}'")
                        logger.info(f"{len(expenses)} expenses exported in category: {category}, file: {filename}")
                    else:
                        print(f"No expenses found in the category {category}.")
                        logger.warning(f"No expenses found to export in the category: {category}")
                else:
                    print("Invalid input: Operation canceled.")
                    logger.warning(f"Out of range category entered: {choice}.")
                    continue
            except ValueError:
                print("Invalid input: Please enter a valid number.")
                logger.error("Error: Invalid input was entered.")
                continue
        
        elif opc == "9":
            print("\nOption 9: Export expenses by date range to a CSV file.")

            start, end = None, None
            try:
                start = input("\nEnter the start date (YYYY-MM-DD): ")
                end = input("Enter the end date (YYYY-MM-DD): ")
        
                datetime.strptime(start, "%Y-%m-%d")
                datetime.strptime(end, "%Y-%m-%d")
                
                order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
                if order_choice not in ["asc", "desc"]:
                    order_choice = None

                expense_range = db.get_expenses_between_dates(start, end, order_by_amount=order_choice)
                
                if expense_range:
                    filename = f"expenses_{start}_to_{end}.csv"
                    export_to_csv(expense_range, filename=filename)
                    print(f"Expenses between {start} and {end} successfully exported to '{filename}'")
                    logger.info(f"{len(expense_range)} expenses exported between {start} and {end}, file: {filename}")
                else:
                    print(f"No expenses found between {start} and {end}.")
                    logger.warning(f"No expenses found between {start} and {end}.")
            except ValueError:
                print("Invalid input: Please use the format YYYY-MM-DD.")
                logger.error(f"Invalid date entered: start={start}, end={end}")
                continue
            
        elif opc == "10":
            print("\nOption 10: Generate a report by category.")
            
            report = db.get_report_category()
            if report:
                print_report_category(report)
                logger.info("Category report successfully generated.")
            else: 
                print("No data available to generate a report.")
                logger.warning("Attempt to generate a category report. No data available.")
        
        elif opc == "11":
            print("\nOption 11: Generate a report by date range.")
            
            start, end = None, None
            try:
                start = input("\nEnter the start date (YYYY-MM-DD): ")
                end = input("Enter the end date (YYYY-MM-DD): ")
                
                datetime.strptime(start, "%Y-%m-%d")
                datetime.strptime(end, "%Y-%m-%d")
                
                order_choice = input("Sort the expenses by amount? (asc / desc / none): ").lower()
                if order_choice not in ["asc", "desc"]:
                    order_choice = None
                
                report = db.get_report_by_date_range(start, end, order_by_amount=order_choice)
                
                if report and report[0]:
                    print_report_date_range(report, start, end)
                    logger.info(f"Date range report successfully generated: {start} to {end}, Total={report[0]:.2f}")
                else:
                    print(f"No data available to generate a report between {start} and {end}")
                    logger.warning(f"No data available to generate a report: {start} to {end}")
            except ValueError:
                print("Invalid input: Please use the format YYYY-MM-DD.")
                logger.error(f"Invalid date entered: start={start}, end={end}")
                continue
            
        elif opc == "12":
            print("\nExiting the program...")
            logger.info("Program terminated by the user.")
            break
        else:
            print("Invalid option: Please select a number between 1 and 12")
            logger.warning("Invalid menu option selected.")

if __name__ == "__main__":
    main()
