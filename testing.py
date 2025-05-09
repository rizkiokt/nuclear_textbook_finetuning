from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import json
import google.generativeai as genai
import time
from llm import LLM

TEXT_DIRECTORY = 'text_dataset'
QA_DIRECTORY = 'qa_dataset'

def generate_answers(model_name: str, text_input: str):

    llm = LLM(model_name=model_name).llm

    prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in nuclear engineering. I want you to answer a multiple choice question (A, B, C, D) from a nuclear engineering textbook.
            Just answer the question in 1 letter, i.e. A, B, C, or D. Don't say anything else.
            """),
            ("user",  "Here is the question: {text_input}")
    ])

    chain = prompt | llm
    for _ in range(5):
        try:
            response = chain.invoke({
                "text_input": text_input,
            })
            break
        except Exception as e:

            print(f"[ERROR] Failed to generate answers, retrying (_/{5}): {e}")
    else:
        raise Exception(f"Failed to generate answers after 5 retries")

    answers = response.content

    return answers

def generate_answers_tuned(model_name: str, text_input: str):
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""You are an expert in nuclear engineering. I want you to answer a multiple choice question (A, B, C, D) from a nuclear engineering textbook.
            Just answer the question in 1 letter, i.e. A, B, C, or D. Don't say anything else.

            The question is:
            {text_input}
            """

    for _ in range(5):
        try:
            response = model.generate_content(prompt)
            answers = response.text
            break
        except Exception as e:
            time.sleep(5)
            print(f"[ERROR] Failed to generate answers, retrying (_/{5}): {e}")
    else:
        print(f"Failed to generate answers after 5 retries, returning empty string")
        answers = ''

    return answers
    

def evaluate_answers(answers: str, correct_answers: str):
    return sum([1 for a, ca in zip(answers, correct_answers) if a == ca])

    

def generate_evaluate_answers(test_data_json: str, model_name: str = "gemini-2.5-flash-preview-04-17"):

    with open(test_data_json) as f:
        test_data = json.load(f)

    total_score = 0
    batch_size = 1
    for i in range(len(test_data)//batch_size):
        print(f"Processing chunk {i+1} of {len(test_data)//batch_size}")
        text_input = ""
        correct_answers = ""
        for j in range(batch_size):
            text_input += test_data[i*batch_size+j]['question'] + '\n' + str(test_data[i*batch_size+j]['choices']) + '\n'
            correct_answers += test_data[i*batch_size+j]['answer']
        
        if model_name.startswith("tuned"):
            answers = generate_answers_tuned(model_name, text_input)
        else:
            answers = generate_answers(model_name, text_input)

        score = evaluate_answers(answers, correct_answers)
        print(f"Score: {score}/{batch_size}")
        total_score += score

    print(f"Total score: {total_score}/{len(test_data)//batch_size*batch_size}")

    return total_score

if __name__ == '__main__':
    date = datetime.now().strftime("%Y%m%d")
    name = f"nuc-eng-tuned-model-{date}"
    tuned_model = f'tunedModels/{name}'
    test_data_json = f'{QA_DIRECTORY}/test_qa_dataset_Lamarsh_baratta.json'

    model_names = [tuned_model, "gemini-1.5-flash", "gemini-2.5-flash-preview-04-17"]

    score_dict = {}
    for model_name in model_names:
        total_score = generate_evaluate_answers(test_data_json, model_name)
        score_dict[model_name] = total_score
    
    print(score_dict)
    # store score_dict to json
    with open(f'results/score_dict_Lamarsh_baratta_{date}.json', 'w') as f:
        json.dump(score_dict, f)
    
 