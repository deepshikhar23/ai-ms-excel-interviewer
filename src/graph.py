import random
from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import StateGraph, END
from src.tasks import TASK_BANK
from src.agents import evaluate_candidate_response, get_llm

class GraphState(TypedDict):
    task_id: str
    task_description: str
    task_file_path: str
    user_explanation: Optional[str]
    user_screenshot: Optional[Any]
    evaluation: Optional[Dict[str, Any]]
    interview_history: List[Dict[str, Any]]
    tasks_completed: List[str]
    final_report: Optional[str]

def select_task_node(state: GraphState):
    """Picks a random, uncompleted task from the bank."""
    completed = state.get("tasks_completed", [])
    uncompleted = [tid for tid in TASK_BANK if tid not in completed]
    return {"task_id": random.choice(uncompleted)} if uncompleted else {"task_id": "ALL_DONE"}

def present_task_node(state: GraphState):
    """Gets the description and data for the selected task."""
    task_id = state["task_id"]
    task = TASK_BANK[task_id]
    filename = task["data_generator"]()
    return {"task_description": task["description"], "task_file_path": filename}

def evaluate_response_node(state: GraphState):
    """Sends the user's submission to the AI agent for evaluation."""
    task_id = state["task_id"]
    
    # FIX: Use the correct parameter names ('explanation' and 'image') that the agent function expects
    evaluation = evaluate_candidate_response(
        task_rubric=TASK_BANK[task_id]["evaluation_rubric"],
        explanation=state.get("user_explanation"),
        image=state.get("user_screenshot")
    )
    
    history_entry = {"task_id": task_id, "title": TASK_BANK[task_id]['title'], "evaluation": evaluation}
    return {
        "evaluation": evaluation, 
        "interview_history": state.get("interview_history", []) + [history_entry], 
        "tasks_completed": state.get("tasks_completed", []) + [task_id]
    }
    
def generate_final_report_node(state: GraphState):
    """Generates a final summary report at the end of the interview."""
    history = state["interview_history"]
    score = sum(entry["evaluation"]["score"] for entry in history)
    max_score = len(history) * 10
    
    summary_prompt = f"""
    Synthesize the results of this Excel test into a short, analytical summary.
    Final Score: {score} / {max_score}.
    Detailed Results: {history}
    Your output MUST be a concise summary. DO NOT write an email or sign-offs.
    Structure your response with these exact markdown headings:
    - **Overall Performance:** (A one-sentence overview)
    - **Key Strengths:** (Bulleted list)
    - **Areas for Improvement:** (Bulleted list)
    """
    model = get_llm()
    response = model.invoke(summary_prompt)
    report_text = f"## Interview Summary\n\n**Final Score: {score} / {max_score}**\n\n" + str(response.content)
    return {"final_report": report_text}

def should_continue_node(state: GraphState):
    """Checks if the interview should continue or end."""
    # TODO: Make the number of tasks configurable
    return "finish" if len(state.get("tasks_completed", [])) >= 5 else "continue"

def decide_entry_node(state: GraphState):
    """Routes the graph to the correct starting node."""
    return "evaluate_response" if state.get("user_explanation") or state.get("user_screenshot") else "select_task"

def build_graph():
    """Assembles and compiles the full interview workflow."""
    workflow = StateGraph(GraphState)
    
    workflow.add_node("select_task", select_task_node)
    workflow.add_node("present_task", present_task_node)
    workflow.add_node("evaluate_response", evaluate_response_node)
    workflow.add_node("generate_final_report", generate_final_report_node)

    workflow.set_conditional_entry_point(decide_entry_node, {
        "select_task": "select_task", 
        "evaluate_response": "evaluate_response"
    })
    
    workflow.add_conditional_edges("select_task", lambda state: END if state["task_id"] == "ALL_DONE" else "present_task")
    workflow.add_edge("present_task", END)
    workflow.add_conditional_edges("evaluate_response", should_continue_node, {
        "continue": "select_task", 
        "finish": "generate_final_report"
    })
    workflow.add_edge("generate_final_report", END)

    return workflow.compile()

interview_graph = build_graph()