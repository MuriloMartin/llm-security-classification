import pandas as pd
from prompt import strategys

def rq1_eda(df: pd.DataFrame):
    df = df[df['class'] == 'sec']
    df.set_index(['model'], inplace=True)
    columns = [col for col in df.columns if col != 'support'] + ['support']
    df = df[columns]
    caption = f"Acuracy metrics by model in zero-shot approach"
    df['support'] = df['support'].astype(int)
    df.drop(columns=['class'], inplace=True)
    latex_table = df.to_latex(index=True, caption=caption, label="tab:rq1", 
                             float_format="%.2f")
    
    latex_table = latex_table.replace("_",r"-")
    
    print(latex_table)


def rq2_eda(df: pd.DataFrame):
    df = df[df['class'] == 'sec']
    df.drop(columns=['class'], inplace=True)
    df.set_index(['strategy', 'model'], inplace=True)
    desired_order = ['few_shot', 'zero_shot_cot', 'raw_inst']
    strategy_order = pd.CategoricalDtype(categories=desired_order, ordered=True)
    df = df.reorder_levels(['strategy', 'model']).sort_index(level='strategy', key=lambda x: x.astype(strategy_order))
    df['support'] = df['support'].astype(int)
    latex_table = df.to_latex(index=True, caption="Acurary by strategy and model", label="tab:metrics", float_format="%.2f", na_rep="NA")
    latex_table = latex_table.replace("_",r"-")
    print(latex_table)


def rq2_best_improvement(df_1,df_2):
    diff = pd.DataFrame()
    models = df_1['model'].unique().tolist()
    classes = df_1['class'].unique().tolist()
    df_1[['precision', 'recall', 'f1_score', 'accuracy']] = df_1[['precision', 'recall', 'f1_score', 'accuracy']].astype(float)
    df_2[['precision', 'recall', 'f1_score', 'accuracy']] = df_2[['precision', 'recall', 'f1_score', 'accuracy']].astype(float)
    for model in models:
        for cls in classes:
            baseline = df_1[(df_1['model'] == model) & (df_1['class'] == cls)]
            for strategy in strategys:
                if strategy == 'zero_shot':
                    continue
                current_result = df_2[(df_2['model'] == model) & (df_2['class'] == cls) & (df_2['strategy'] == strategy)]
                precision_improv = current_result['precision'].iloc[0] - baseline['precision'].iloc[0]
                recall_improv = current_result['recall'].iloc[0] - baseline['recall'].iloc[0]
                f1_score_improve = current_result['f1_score'].iloc[0] - baseline['f1_score'].iloc[0]
                accuracy_improve = current_result['accuracy'].iloc[0] - baseline['accuracy'].iloc[0]
                diff_dict = {
                    'model': model,
                    'class': cls,
                    'strategy': strategy,
                    "precision diff": precision_improv,
                    "recall diff": recall_improv,
                    "f1 diff": f1_score_improve,
                    "accuracy diff": accuracy_improve
                }
                diff = pd.concat([diff, pd.DataFrame([diff_dict])], ignore_index=True)
    diff_sec = diff[diff['class'] == 'sec']
    diff_sec.sort_values(by='f1 diff', ascending=False, inplace=True)
    diff_sec = diff_sec.head(10)
    diff_sec.drop(columns='class', inplace=True)
    latex_diff_sec = diff_sec.to_latex(index=False, caption="Most improved f1-score for class 'sec'",label="tab:sec_improv", float_format="%.2f", na_rep="NA")
    print('latex_diff_sec\n',latex_diff_sec.replace('_', r'\_'))
    
    diff_nonsec = diff[diff['class'] == 'nonsec']
    diff_nonsec.sort_values(by='f1 diff', ascending=False, inplace=True)
    diff_nonsec = diff_nonsec.head(5)
    diff_nonsec.drop(columns='class', inplace=True)
    latex_diff_nonsec = diff_nonsec.to_latex(index=False, caption="Most improved f1-score for class 'nonsec'",label="tab:nonsec_improv", float_format="%.2f", na_rep="NA")
    print('latex_diff_nonsec\n',latex_diff_nonsec.replace('_', r'\_'))


def rq2_improvement_by_strategy(df_1,df_2):
    diff_few = pd.DataFrame()
    diff_raw = pd.DataFrame()
    diff_cot = pd.DataFrame()
    dfs_list = [diff_few, diff_cot, diff_raw]
    models = df_1['model'].unique().tolist()
    df_1[['precision', 'recall', 'f1_score']] = df_1[['precision', 'recall', 'f1_score']].astype(float)
    df_2[['precision', 'recall', 'f1_score']] = df_2[['precision', 'recall', 'f1_score']].astype(float)
    df_1 = df_1[df_1['class'] == 'sec']
    df_2 = df_2[df_2['class'] == 'sec']
    df_1.drop(columns=['class'], inplace=True)
    df_2.drop(columns=['class'], inplace=True)
    for model in models:
        
        baseline = df_1[(df_1['model'] == model)]
        for strategy in strategys:
            if strategy == 'zero_shot':
                continue
            current_result = df_2[(df_2['model'] == model) & (df_2['strategy'] == strategy)]
            precision_improv = current_result['precision'].iloc[0] - baseline['precision'].iloc[0]
            recall_improv = current_result['recall'].iloc[0] - baseline['recall'].iloc[0]
            f1_score_improve = current_result['f1_score'].iloc[0] - baseline['f1_score'].iloc[0]
            diff_dict = {
                'model': model,
                'strategy': strategy,
                "precision diff": precision_improv,
                "recall diff": recall_improv,
                "f1 diff": f1_score_improve,
            }
            if strategy == 'few_shot':
                dfs_list[0] = pd.concat([dfs_list[0], pd.DataFrame([diff_dict])], ignore_index=True)
            if strategy == 'zero_shot_cot':
                dfs_list[1] = pd.concat([dfs_list[1], pd.DataFrame([diff_dict])], ignore_index=True)
            if strategy == 'raw_inst':
                dfs_list[2] = pd.concat([dfs_list[2], pd.DataFrame([diff_dict])], ignore_index=True)

    df = pd.concat(dfs_list, ignore_index=True)
    df.sort_values(by='f1 diff', ascending=False, inplace=True)
    df.set_index(['strategy', 'model'], inplace=True)
    desired_order = ['few_shot', 'zero_shot_cot', 'raw_inst']
    strategy_order = pd.CategoricalDtype(categories=desired_order, ordered=True)
    df = df.reorder_levels(['strategy', 'model']).sort_index(level='strategy', key=lambda x: x.astype(strategy_order))
    print(df)

    latex_df = df.to_latex(index=True, caption="Difference in accuracy by strategy compared to the baseline approach",label="tab:accuracyDiff", float_format="%.2f", na_rep="NA")
    print('latex_diff_nonsec\n',latex_df.replace('_', r'-').replace('zero-shot-cot','auto-CoT'))

def rq3_individual(df):
    df_orig = df.copy()
    df = df_orig[((df_orig['model'] == 'mistral-nemo') | (df_orig['model'] == 'mistral')) & (df_orig['strategy'] == 'raw_inst')]
    df = df[df['class'] == 'sec']
    print(df)
    df = df[['model','project','precision','recall','f1_score']]
    df.sort_values(by=['model','project','f1_score'], ascending=False, inplace=True)
    latex_df = df.to_latex(index=False, caption="",label="tab:literature_comparison", float_format="%.2f", na_rep="NA")
    print(latex_df)
    
    

def rq3_consolidated(df):
    df_orig = df.copy()
    print("Top SECReq approaches for for class sec")
    df = df_orig[df_orig['class'] == 'sec']
    df.sort_values(by=['f1_score'], ascending=False, inplace=True)
    print(df.head(10))
    



def format_number(number):
    signal = '+' if number >= 0 else '-'
    return f"{signal}{abs(number):.2f}"  # Format with two decimal places
