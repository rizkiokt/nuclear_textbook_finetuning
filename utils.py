from pydantic import BaseModel, Field
from typing import List, Dict
import json

# Define Pydantic model for a single question
class QuestionSet(BaseModel):
    question: str
    choices: Dict[str, str]
    answer: str = Field(..., pattern="^[A-D]$", description="Answer must be A, B, C, or D")
    difficulty: str = Field(..., pattern="^(Easy|Medium|Hard)$", description="Difficulty must be Easy, Medium, or Hard")

class QuestionSetList(BaseModel):
    questions: List[QuestionSet]

def save_questions_to_json(questions_list: List[QuestionSetList], output_file: str) -> None:
    """Save the generated questions to a JSON file.
    
    Args:
        questions_list: List of QuestionSetList objects
        output_file: Path to save the JSON file
    """
    # Convert the questions to a list of dictionaries
    questions_data = []
    for question_set_list in questions_list:
        for question_set in question_set_list.questions:
            questions_data.append(question_set.model_dump())
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(questions_data, f, indent=2)
    
    print(f'Saved {len(questions_data)} questions to {output_file}')