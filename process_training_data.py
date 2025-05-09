import os
import json

QA_DIRECTORY = 'qa_dataset'

# Combine all JSON objects into a list first
combined_data = []

for i in range(2, 12):
    file_path = f'{QA_DIRECTORY}/ch{i}_qa_dataset_Lamarsh_baratta.json'
    with open(file_path, 'r') as f:
        chapter_data = json.load(f)
        if isinstance(chapter_data, list):
            combined_data.extend(chapter_data)
        else:
            print(f"Warning: {file_path} does not contain a list.")

# Write the combined list to the output file
with open(f'{QA_DIRECTORY}/combined_qa_dataset_Lamarsh_baratta.json', 'w') as f:
    json.dump(combined_data, f, indent=2)

# %%
# Read and verify
with open(f'{QA_DIRECTORY}/combined_qa_dataset_Lamarsh_baratta.json', 'r') as f:
    data = json.load(f)

print(len(data))  # This should now print the number of chapters you combined


# %%

# Split 100 questions randomly from data and store as test data, remaining is training data
import random
random_data = random.sample(data, len(data))
test_data = random_data[:100]
train_data = random_data[100:]

print(len(test_data))
print(len(train_data))

# %%
# Save test and train data to JSON files
with open(f'{QA_DIRECTORY}/test_qa_dataset_Lamarsh_baratta.json', 'w') as f:
    json.dump(test_data, f, indent=2)

with open(f'{QA_DIRECTORY}/train_qa_dataset_Lamarsh_baratta.json', 'w') as f:
    json.dump(train_data, f, indent=2)

# %%

# Make csv training data with text_input to include question and choices and output to include answer
import pandas as pd
train_df = pd.DataFrame(train_data)
train_df['text_input'] = train_df.apply(lambda row: f"{row['question']}\nA: {row['choices']['A']}\nB: {row['choices']['B']}\nC: {row['choices']['C']}\nD: {row['choices']['D']}", axis=1)
train_df = train_df[['text_input', 'answer']]
train_df.columns = ['text_input', 'output']
train_df.to_csv(f'{QA_DIRECTORY}/train_qa_dataset_Lamarsh_baratta.csv', index=False)
# %%
