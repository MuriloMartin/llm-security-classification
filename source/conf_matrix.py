
# example data
# [
#     {
#         "project_id": "1",
#         "requirement": "'The system shall refresh the display every 60 seconds.'",
#         "label": "NFR",
#         "source": "promise_exp",
#         "response": {
#             "zero_shot": "NFR",
#             "few_shot_cot": "FR",
#             "zero_shot_cot": "NFR"
#         }
#     },
#     {
#         "project_id": "1",
#         "requirement": "'The application shall match the color of the schema set forth by Department of Homeland Security'",
#         "label": "NFR",
#         "source": "promise_exp",
#         "response": {
#             "zero_shot": "NFR",
#             "few_shot_cot": "FR",
#             "zero_shot_cot": "NFR"
#         }
#     },
#     {
#         "project_id": "1",
#         "requirement": "'If projected  the data must be readable.  On a 10x10 projection screen  90% of viewers must be able to read Event / Activity data from a viewing distance of 30'",
#         "label": "NFR",
#         "source": "promise_exp",
#         "response": {
#             "zero_shot": "FR",
#             "few_shot_cot": "FR",
#             "zero_shot_cot": "FR"
#         }
#     }
# ]

from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from prompt import strategys

def get_files_names():
    folder_path = 'data'
    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
    files_names = [file.split('.')[0] for file in json_files]
    return files_names

def get_label(message):
    try:
        return message["part2_aggregate"]["polarity"] if message["part2_aggregate"]["polarity"] != "undefined" else message["discussion_polarity"]
    except KeyError:
        return "undefined"  # Substitua por um valor padrão conforme necessário

def get_predicted_polarity(row, model_name):
    return row['tools'].get(model_name, 'undefined')

def plot_confusion_matrix(cm, report, strategy , labels):
    plt.figure(figsize=(17, 7))  # Aumentando a figura para incluir o texto ao lado
    plt.subplot(1, 2, 1)  # Matriz de confusão à esquerda
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(f'Confusion Matrix for Prompt: {strategy}')
    plt.subplot(1, 2, 2)  # Relatório de classificação à direita
    plt.axis('off')  # Desativando os eixos para o texto
    plt.text(0.5, 0.5, report, ha='center', va='center', fontsize=12)
    plt.show()

def confusion_matrix_for_models(file_path, labels,sample_size):
    with open(f'{file_path}', encoding='utf-8') as f:
        data = json.load(f)
        data = data[:sample_size]
        
    df = pd.DataFrame(data)
    for strategy in strategys:
        df[strategy] = df['response'].apply(lambda x: x[strategy])
    print(df.head())

    df = df[df['label'].isin(labels)]

    df_temp = df.copy()
    for strategy in strategys:
        df_temp['predicted_label'] = df_temp[strategy]
        df_temp = df_temp[df_temp['predicted_label'].isin(labels)]  # Filtrando apenas as polaridades esperadas
        cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
        report = classification_report(df_temp['label'], df_temp['predicted_label'], target_names=labels)
        print(f"Confusion Matrix for {strategy}:")
        print(cm)
        print(f"Classification Report for {strategy}:\n{report}")
        plot_confusion_matrix(cm, report, strategy, labels)

def main():
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\results\llama3_v2.json'
    labels = ['NFR', 'FR']
    sample_size = 200
    confusion_matrix_for_models(path, labels, sample_size)

if __name__ == "__main__":
    main()