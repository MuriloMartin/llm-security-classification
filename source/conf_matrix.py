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

def confusion_matrix_for_models(file_path, labels,sample_size, model_name ):
    with open(f'{file_path}', encoding='utf-8') as f:
        data = json.load(f)
        data = data[:sample_size]
        
    df = pd.DataFrame(data)
    #print(df['response'])
    for strategy in strategys:
        df[strategy] = df['response'].apply(lambda x: x[strategy] if strategy in x else 'undefined')

    df = df[df['label'].isin(labels)]

    
    df_temp = df.copy()
    report_text = ''
    for strategy in strategys:
        df_temp['predicted_label'] = df_temp[strategy]
        df_temp = df_temp[df_temp['predicted_label'].isin(labels)]  # Filtrando apenas as polaridades esperadas
        df_temp.to_csv(f'{model_name}_{strategy}.csv', index=False)
        cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
        report = classification_report(df_temp['label'], df_temp['predicted_label'], target_names=labels)
        report_text += f"Confusion Matrix for {model_name} - {strategy}:\n"
        report_text += f"{cm}\n"
        report_text += f"Classification Report for {model_name} - {strategy}:\n"
        report_text += f"{report}\n"
        plot_confusion_matrix(cm, report, strategy, labels)
    return report_text

def main():
    labels = ['NFR', 'FR']
    sample_size = 100
    models = ['llama3','mistral', 'gemma']
    report_text = ''
    for model in models:
        path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\results\{model}.json'
        report_text += confusion_matrix_for_models(path, labels, sample_size, model)
        # Save the report to a .txt file
    with open(rf'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\results\report.txt', "w") as file:
        file.write(report_text)
    

if __name__ == "__main__":
    main()