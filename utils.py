# utils.py

import csv
from logger import logger

def print_expenses(expenses):
    """Display all the expenses in a user-friendly tabular format."""
    if not expenses:
        print("No expenses to display.")
        return

    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Note'}")
    print("-" * 60)
    
    for exp in expenses:
        print(f"{exp[0]:<5} {exp[1]:<12} {exp[2]:<15} {exp[3]:<10.2f} {exp[4] or ''}")
    
def export_to_csv(expenses, filename="expenses.csv"):
    """Export a list of expenses to a CSV file."""
    try:
        if not expenses:
            print("No expense to export.")
            logger.warning("Attempt to export expenses. No data available.")
            return
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Category", "Amount", "Note"])
            for exp in expenses:
                writer.writerow(exp)
                
        print(f"Expenses successfully exported. File saved as: {filename}.")
        logger.info(f"{len(expenses)} expenses exported to {filename}")
    
    except Exception as e:
        print(f"Error exporting expenses: {e}")
        logger.error(f"Error in export_to_csv: {filename}: {e}")

def print_report_category(report_data):
    """Display the expense report grouped by cateogry."""
    if not report_data:
        print("No expenses available to display in the report.")
        return
    
    print("\nExpenses by cateogry report:")
    print("-" * 40)
    print(f"{'Category':<20} {'Total':>10}")
    print("-" * 40)
    
    for category, total in report_data:
        print(f"{category:<20} {total:>10.2f}")
        
def print_report_date_range(report_data, start, end):
    """Display the expenses report for a given date range."""
    if not report_data or report_data[0] is None:
        print(f"No data available between {start} and {end}")
        return
    
    total, count, avg = report_data
    print(f"\nDate range report: {start} and {end}")
    print("-" * 40)
    print(f"Total spent:      {total:.2f}")
    print(f"Number of expenses:   {count}")
    print(f"Average per expense: {avg:.2f}")
           
