import pandas as pd
import json

input_manifest = r'data/train/output.manifest'
data = []

#parsing the .manifest file
with open(input_manifest, 'r', encoding='utf-8') as file:
    for line in file:
        entry = json.loads(line)
        
        # Extracting text
        text = entry['source'].split(',', 1)[1].strip("\"")
        
        # update as per your aws
        label = entry['amolkerkarturmerik-metadata']['class-name']
        data.append([text, label])

df = pd.DataFrame(data, columns=['Text', 'Label'])

# Saving
output_csv = 'data/train/aws_output_labels.csv'
df.to_csv(output_csv, index=False)

print(f'Data saved to {output_csv}')
