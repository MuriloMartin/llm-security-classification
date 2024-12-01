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

def get_data(models):
    consolidated_df = pd.DataFrame()
    for model in models:
        path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\{model}.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['model'] = model
        consolidated_df = pd.concat([consolidated_df, df], ignore_index=True)

    for strategy in strategys:
        consolidated_df[strategy] = consolidated_df['response'].apply(lambda x: x[strategy] if strategy in x else 'undefined')
    consolidated_df.drop('response', axis=1, inplace=True)
    consolidated_df.to_csv(rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\consolidated.csv')
    return consolidated_df

def filter_by_model(model, df):
    return df[df['model'] == model]


def get_rq1_consolidated_result(labels, models ):
    df = get_data(models)
    report_text = ''
    for strategy in strategys:
        if (strategy != 'zero_shot'):
            continue
        for model in models:

            df_temp = filter_by_model(model, df).copy() 
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            report_text += f"Confusion Matrix for {model} - {strategy}:\n"
            report_text += f"{cm}\n"
            report_text += f"Classification Report for {model} - {strategy}:\n"
            report_text += f"{report}\n"
            #plot_confusion_matrix(cm, report, strategy, labels)
    with open(rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\report_rq1_consolidated.txt', "w+") as file:
        file.write(report_text)
    return 

def main():
    labels = ['sec', 'nonsec']
    models = ['llama3','mistral', 'gemma']
    get_rq1_consolidated_result(labels, models)
    for model in models:
        path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\{model}.json'

if __name__ == "__main__":
    main()