# %%
import google.generativeai as genai
import os
import csv
from datetime import datetime

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

base_model = [
    m for m in genai.list_models()
    if "createTunedModel" in m.supported_generation_methods and
    "flash" in m.name][0]

#%%
date = datetime.now().strftime("%Y%m%d")
name = f"nuc-eng-tuned-model-{date}"
print(name)

# %%
with open("qa_dataset/train_qa_dataset_Lamarsh_baratta.csv") as f:
    training_data = [{k: v for k,v in row.items()} for row in csv.DictReader(f)]
print(training_data)
# %%

operation = genai.create_tuned_model(
    # You can use a tuned model here too. Set `source_model="tunedModels/..."`
    source_model=base_model.name,
    training_data=training_data,
    id = name,
    epoch_count = 5,
    batch_size=8,
    learning_rate=0.0002,
)
# %%

operation.metadata

# %%
import time

for status in operation.wait_bar():
  time.sleep(30)


# %%

import pandas as pd
import seaborn as sns

model = operation.result()

snapshots = pd.DataFrame(model.tuning_task.snapshots)

sns.lineplot(data=snapshots, x = 'epoch', y='mean_loss')
