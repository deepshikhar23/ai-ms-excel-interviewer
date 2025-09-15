import pandas as pd
import random
import os
from datetime import datetime, timedelta

def generate_task_data(data, filename="task_data.csv"):
    """Helper to create and save a task's CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

def generate_sales_data():
    products = ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"]
    regions = ["North", "South", "East", "West"]
    data = []
    for _ in range(50):
        data.append({
            "Date": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 200))).strftime("%Y-%m-%d"),
            "Region": random.choice(regions),
            "Product": random.choice(products),
            "Units Sold": random.randint(5, 50),
            "Price per Unit": random.randint(800, 15000),
        })
    return generate_task_data(data)

def generate_employee_data():
    ids = [f"EMP-{i:03d}" for i in range(1, 51)]
    data = [{"Employee ID": ids[i], "Department": random.choice(["HR", "Engineering", "Sales"]), "Salary": random.randint(50000, 120000)} for i in range(50)]
    return generate_task_data(data)

def generate_messy_inventory_data():
    items = ["T-Shirt", "Mug", "Pen", "Sticker"]
    data = []
    for item in items:
        # Create some intentional duplicates
        for _ in range(random.randint(2, 5)):
            data.append({"ItemID": f"ITEM-{items.index(item):02d}", "ItemName": item, "StockLevel": random.randint(0, 200)})
    return generate_task_data(data)
    
def generate_student_scores():
    data = [{"StudentID": f"Student_{i:02d}", "Score": random.randint(40, 100)} for i in range(1, 31)]
    return generate_task_data(data)

def generate_project_data():
    data = [{"ProjectID": f"PROJ-{i:03d}", "Status": random.choice(["Completed", "In Progress", "On Hold"]), "Budget": random.randint(10000, 50000)} for i in range(40)]
    return generate_task_data(data)

def generate_contact_list():
    data = [{"FirstName": random.choice(["John", "Jane", "Peter", "Mary"]), "LastName": random.choice(["Smith", "Doe", "Jones"])} for _ in range(20)]
    return generate_task_data(data)

def generate_order_data():
    data = [{"Product": random.choice(["Apples", "Bananas", "Cherries"]), "Price": f"$ {random.uniform(0.5, 3.0):.2f}"} for _ in range(60)]
    return generate_task_data(data)

# The main bank of 10 practical Excel challenges
TASK_BANK = {
    "task_1": {"title": "Regional Sales Calculation", "data_generator": generate_sales_data, "description": "Using the sales data, calculate the total revenue (Units Sold * Price per Unit) for the 'North' region. State the final number and show your formula or Pivot Table.", "evaluation_rubric": {"key_concepts": ["SUMPRODUCT", "SUMIF", "Pivot Table"]}},
    "task_2": {"title": "Employee Salary Lookup", "data_generator": generate_employee_data, "description": "Using the employee dataset, find the 'Salary' for 'EMP-033'. State the salary and show your VLOOKUP or XLOOKUP formula.", "evaluation_rubric": {"key_concepts": ["VLOOKUP", "XLOOKUP", "INDEX/MATCH"]}},
    "task_3": {"title": "Inventory Summary", "data_generator": generate_messy_inventory_data, "description": "The inventory data has duplicates. Remove rows with duplicate 'ItemID's, then create a Pivot Table showing the total 'StockLevel' for each 'ItemName'. Show your final Pivot Table.", "evaluation_rubric": {"key_concepts": ["Remove Duplicates", "Pivot Table", "Data Aggregation"]}},
    "task_4": {"title": "Assign Student Grades", "data_generator": generate_student_scores, "description": "Create a new 'Grade' column. Use an IF statement to assign 'Pass' if the 'Score' is 60 or greater, and 'Fail' otherwise. Show the formula for one cell.", "evaluation_rubric": {"key_concepts": ["IF function", "Conditional Logic"]}},
    "task_5": {"title": "Create Full Names", "data_generator": generate_contact_list, "description": "Create a 'FullName' column by combining 'FirstName' and 'LastName' with a space in between. Show your CONCAT or ampersand (&) formula.", "evaluation_rubric": {"key_concepts": ["CONCAT", "Ampersand (&)", "Text Manipulation"]}},
    "task_6": {"title": "Highlight High Scores", "data_generator": generate_student_scores, "description": "Apply Conditional Formatting to highlight all scores greater than 90 with a green fill. Show the formatted column and the rule you created.", "evaluation_rubric": {"key_concepts": ["Conditional Formatting", "Highlight Cells Rules"]}},
    "task_7": {"title": "Filter Completed Projects", "data_generator": generate_project_data, "description": "Use the FILTER function to create a new table on the same sheet that contains all projects with a 'Status' of 'Completed'. Show your FILTER formula.", "evaluation_rubric": {"key_concepts": ["FILTER function", "Dynamic Arrays"]}},
    "task_8": {"title": "Create a Sales Chart", "data_generator": generate_sales_data, "description": "Create a Bar Chart that shows the total 'Units Sold' for each 'Product'. Give the chart a title. Show your final chart.", "evaluation_rubric": {"key_concepts": ["Charting", "Data Visualization", "PivotChart"]}},
    "task_9": {"title": "Clean Numeric Data", "data_generator": generate_order_data, "description": "The 'Price' column is formatted as text (e.g., '$ 1.50'). Create a 'CleanPrice' column that converts this to a proper number. Show your formula.", "evaluation_rubric": {"key_concepts": ["SUBSTITUTE", "VALUE", "TRIM", "Text to Number"]}},
    "task_10": {"title": "Data Validation Dropdown", "data_generator": generate_project_data, "description": "Add a new 'Verification' column. Use Data Validation to create a dropdown list with the options: 'Verified', 'Pending', 'Rejected'. Show the dropdown arrow in a cell.", "evaluation_rubric": {"key_concepts": ["Data Validation", "Dropdown List"]}},
}