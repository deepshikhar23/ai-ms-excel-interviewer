import os
import json
import re
import base64
import io
from typing import Optional
from dotenv import load_dotenv
from PIL import Image

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def get_llm():
    """Initializes and returns the LangChain Google AI model."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key, timeout=120)

def image_to_base64_url(img: Image.Image) -> str:
    """Converts a PIL Image to a Base64 data URL for API submission."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    b64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{b64_string}"

def evaluate_candidate_response(task_rubric: dict, explanation: Optional[str] = None, image: Optional[Image.Image] = None):
    """
    Evaluates a candidate's submission (text, image, or both) against a rubric.
    Returns a JSON object with a score and feedback.
    """
    try:
        model = get_llm()
        
        base_prompt = f"**RUBRIC - Key Concepts:** {task_rubric['key_concepts']}\n"
        content = []
        submission_prompt = ""

        if explanation and image:
            submission_prompt = f'**SUBMISSION (Text & Image):**\n- Explanation: "{explanation}"\n**INSTRUCTIONS:** Analyze BOTH the text and image.'
            content.extend([{"type": "text", "text": ""}, {"type": "image_url", "image_url": image_to_base64_url(image)}])
        elif explanation:
            submission_prompt = f'**SUBMISSION (Text Only):**\n- Explanation: "{explanation}"\n**INSTRUCTIONS:** Evaluate the text on its own.'
            content.append({"type": "text", "text": ""})
        elif image:
            submission_prompt = "**SUBMISSION (Image Only):**\n**INSTRUCTIONS:** Evaluate the image on its own."
            content.extend([{"type": "text", "text": ""}, {"type": "image_url", "image_url": image_to_base64_url(image)}])
        else:
            return {"score": 0, "feedback": "No submission provided."}

        final_instructions = "\nGive a score from 1-10. Your response MUST be ONLY a valid JSON object with keys \"score\" (int) and \"feedback\" (str)."
        content[0]['text'] = base_prompt + submission_prompt + final_instructions
        
        message = HumanMessage(content=content)
        
        print("Evaluating response...")
        response = model.invoke([message])
        text = str(response.content)
        print(f"Raw model response: {text}")

        # A robust way to find JSON, even if the model adds extra text
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            return {"score": 0, "feedback": "Evaluation error: No valid JSON found."}

    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] JSON parsing failed: {e}")
        return {"score": 0, "feedback": "Evaluation error: The AI's response was malformed."}
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return {"score": 0, "feedback": "An unexpected error occurred during evaluation."}