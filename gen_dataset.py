from pydantic import ValidationError
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from utils import QuestionSetList, save_questions_to_json
from typing import List
from llm import LLM

TEXT_DIRECTORY = 'text_dataset'
QA_DIRECTORY = 'qa_dataset'

def generate_questions(text_file_path: str):
    llm = LLM().llm
    parser = PydanticOutputParser(pydantic_object=QuestionSetList)

    with open(text_file_path) as f:
        lines = f.readlines()

    # Collect all questions
    all_questions: List[QuestionSetList] = []

    for i in range(len(lines)//15-1):
        text = lines[i*15:i*15+30] # 1 page consists of 3 lines (page number, text, and empty line)
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in nuclear engineering. I want you to generate 6 multiple-choice questions (3 Easy, 2 Medium, 1 Hard) from the following textbook text. 
            The question must be in the level of nuclear Principles and Practice of Engineering exam. Don't say anything related to "according to the provided text". Assume the reader does not have access to the text.
            Each question should have four choices (A-D), an answer, and a difficulty label. The response must be in this multiple choice format and mention the difficulty of the question (Easy, Medium, Hard).

            {format_instructions}
            """),
            ("user",  "Here is the text: {text}")
        ])

        chain = prompt | llm | parser
        for _ in range(5):
            try:
                response = chain.invoke({
                    "text": text,
                    "format_instructions": parser.get_format_instructions()
                })
                break
            except Exception as e:
                print(f"[ERROR] Failed to generate questions, retrying (_/{5}): {e}")
        else:
            raise Exception(f"Failed to generate questions after 5 retries")

        all_questions.append(response)

        print(f'Generated questions for chunk {i+1} of {len(lines)//15-1}')
    
    return all_questions

if __name__ == '__main__':
    for i in range(2,12):
        print(f'Generating questions for chapter {i} of 11...')
        all_questions = generate_questions(f'{TEXT_DIRECTORY}/ch{i}_processed.txt')
        save_questions_to_json(all_questions, f'{QA_DIRECTORY}/ch{i}_qa_dataset_Lamarsh_baratta.json')
    
 