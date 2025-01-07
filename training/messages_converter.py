import pandas as pd

with open('mails.txt', 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 2:
        data.append(parts)

df = pd.DataFrame(data, columns=['label', 'message'])

df.to_csv('spam.csv', index=False)

print("Le fichier CSV a été créé avec succès : spam.csv")
