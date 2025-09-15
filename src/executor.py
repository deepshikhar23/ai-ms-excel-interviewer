# Create this new file: src/executor.py
import pandas as pd
import json
from typing import Optional
from src.agents import get_llm # We'll reuse our LLM initializer

def extract_answer_from_text(text: str) -> Optional[float]:
    """Uses the LLM to find and extract a numerical answer from the user's text."""
    print("---EXECUTOR: Extracting number from text---")
    extraction_prompt = f"""
    Analyze the following text. Find the final numerical answer the user has stated.
    Respond with ONLY a valid JSON object with one key, "answer", which should be the number you found.
    If no specific final number is mentioned, the value should be null.
    
    Text to analyze: "{text}"
    """
    try:
        model = get_llm()
        response = model.invoke(extraction_prompt)
        result = json.loads(str(response.content))
        answer = result.get("answer")
        if isinstance(answer, (int, float)):
            print(f"Extracted number: {answer}")
            return float(answer)
    except Exception as e:
        print(f"Could not extract number: {e}")
    return None

def calculate_correct_answer(task_id: str, df: pd.DataFrame) -> Optional[float]:
    """Calculates the known correct answer for a given task using Pandas."""
    print(f"---EXECUTOR: Calculating correct answer for {task_id}---")
    if task_id == "task_1":
        df['Revenue'] = df['Units Sold'] * df['Price per Unit']
        return df[df['Region'] == 'North']['Revenue'].sum()
    elif task_id == "task_2":
        return df[df['Employee ID'] == 'EMP-025']['Salary'].iloc[0]
    # For tasks without a single numerical answer, we return None
    return None

def verify_user_answer(task_id: str, csv_path: str, user_answer: float) -> str:
    """Loads data, calculates the correct answer, and verifies the user's number."""
    try:
        df = pd.read_csv(csv_path)
        correct_answer = calculate_correct_answer(task_id, df)
        
        if correct_answer is not None:
            # Compare results with a small tolerance for floating point numbers
            if abs(user_answer - correct_answer) < 0.01:
                return "Correct"
            else:
                return f"Incorrect (Correct Answer: {correct_answer:.2f})"
    except Exception as e:
        print(f"Verification failed: {e}")
    return "Not Applicable"