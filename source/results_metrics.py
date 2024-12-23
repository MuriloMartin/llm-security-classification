from sklearn.metrics import classification_report
import pandas as pd
import json
from prompt import strategys
from data_analysis import rq1_eda, rq2_eda, rq2_best_improvement, rq2_improvement_by_strategy, rq3_individual,rq3_consolidated


def get_data(models):
    consolidated_df = pd.DataFrame()
    for model in models:
        path = rf'./results/{model.replace(':','_')}.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['model'] = model
        consolidated_df = pd.concat([consolidated_df, df], ignore_index=True)

    for strategy in strategys:
        consolidated_df[strategy] = consolidated_df['response'].apply(lambda x: x[strategy] if strategy in x else 'undefined')
    consolidated_df.drop('response', axis=1, inplace=True)
    consolidated_df.to_csv(rf'./results/consolidated.csv')
    return consolidated_df

def filter_by_model(model, df):
    return df[df['model'] == model]

def filter_by_project_id(id, df):
    if type(id) == list:
        return df[df['project_id'].isin(id)]
    return df[df['project_id'] == id]

def filter_out_projects(ids, df):
    filtered_rows = []  
    for _, row in df.iterrows():
        if row['project_id'] not in ids:
            filtered_rows.append(row)
    
    return pd.DataFrame(filtered_rows)

def get_df_from_report(report):
    report_data = []
    lines = report.split('/n')
    for line in lines[2:4]:
        row = {}
        row_data = line.split(' ') 
        row_data = list(filter(None, row_data))
        row['class'] = row_data[0]
        row['precision'] = float(row_data[1])
        row['recall'] = float(row_data[2])
        row['f1_score'] = float(row_data[3])
        row['support'] = int(row_data[4])
        report_data.append(row)

    return pd.DataFrame.from_dict(report_data)

def get_rq1_consolidated_result(labels, models ):
    df = get_data(models)
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy != 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model       
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)

    return consolidated_results_df

def get_rq2_consolidated_result(labels, models ):
    df = get_data(models)
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model 
            df_aux['strategy'] = strategy     
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
            
    return consolidated_results_df

def get_rq3_individual_secreq_result(labels, models ):
    project_dict = {
        50: "CPN",
        51: "ePurse",
        52: "GPS"
    }
    df = get_data(models)
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            for projectId in [50,51,52]:
                df_temp = filter_by_model(model, df).copy() 
                df_temp = filter_by_project_id(projectId, df_temp).copy()
                df_temp['predicted_label'] = df_temp[strategy]
                df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
                df_temp = df_temp.drop(columns=strategys)
                report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
                df_aux = get_df_from_report(report)    
                df_aux['model'] = model 
                df_aux['strategy'] = strategy     
                df_aux['project'] = project_dict[projectId]
                df_aux['project_id'] = projectId
                consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
                
    return consolidated_results_df

def get_rq3_consolidated_secreq_result(labels, models ):
    df = get_data(models)
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp = filter_by_project_id([50,51,52], df_temp).copy()
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model 
            df_aux['strategy'] = strategy     
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)

    return consolidated_results_df


def main():
    labels = ['sec', 'nonsec']
    #models = ['gemma', 'gemma2_27b', 'gpt-4o-mini', 'llama3', 'llama3.1', 'llama3.2-vision', 'mistral', 'mistral-nemo', 'mistral-small']
    models = ['gemma:2b']
    df_rq1 = get_rq1_consolidated_result(labels, models)
    df_rq2 = get_rq2_consolidated_result(labels, models)
    df_rq3_individual_sec_req = get_rq3_individual_secreq_result(labels, models)
    df_rq3_consolidated_sec_req = get_rq3_consolidated_secreq_result(labels, models)
    print('df_rq1 head:\n',df_rq1.head())
    print('df_rq2 head:\n',df_rq2.head())
    print('df_rq3_individual_sec_req head:\n',df_rq3_individual_sec_req.head())
    print('df_rq3_consolidated_sec_req head:\n',df_rq3_consolidated_sec_req.head())
    rq1_eda(df_rq1)
    rq2_eda(df_rq2)
    rq2_best_improvement(df_rq1,df_rq2)
    rq2_improvement_by_strategy(df_rq1,df_rq2)
    rq3_individual(df_rq3_individual_sec_req)
    rq3_consolidated(df_rq3_consolidated_sec_req)
    rq3_individual(df_rq3_individual_sec_req)

if __name__ == "__main__":
    main()