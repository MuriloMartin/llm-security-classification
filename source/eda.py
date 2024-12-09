import pandas as pd
from prompt import strategys

def rq1_eda(df: pd.DataFrame):
    ordered_sec_df = df[df['class'] =='sec'].sort_values(by='accuracy', ascending=False)
    ordered_nonsec_df = df[df['class'] =='nonsec'].sort_values(by='accuracy', ascending=False)

    df.set_index(['class', 'model'], inplace=True)
    columns = [col for col in df.columns if col != 'support'] + ['support']
    df = df[columns]
    df =  df.sort_values(by=['class', 'model'], ascending=False)
    caption = f"Performance Metrics by model (zero_shot)"
    df['support'] = df['support'].astype(int)
    latex_table = df.to_latex(index=True, caption=caption, label="tab:rq1", 
                             float_format="%.2f")
    
    latex_table = latex_table.replace("_",r"\_")
    
    # print(latex_table)


def rq2_eda(df: pd.DataFrame):
    df_grouped = df.groupby('strategy')
    for strategy, group in df_grouped:
        group.set_index(['class', 'model'], inplace=True)
        
        columns = [col for col in group.columns if col != 'support'] + ['support']
        group = group[columns]
        
        group.drop(columns='strategy', inplace=True)
        group = group.sort_values(by=['class', 'model'], ascending=False)
        
        caption = f"Performance Metrics by model ({strategy})"
        caption = caption.replace('_', r'\_')

        group['support'] = group['support'].astype(int)

        latex_table = group.to_latex(index=True, caption=caption, label="tab:metrics", 
                                      float_format="%.2f", na_rep="NA")

        # print(f'\n\n\nStrategy: {strategy}\n')
        # print(latex_table)
        # print("\n")

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
    diff_sec = diff_sec.head(5)
    diff_sec.drop(columns='class', inplace=True)
    latex_diff_sec = diff_sec.to_latex(index=False, caption="Most improved f1-score for class 'sec'",label="tab:sec_improv", float_format="%.2f", na_rep="NA")
    print('latex_diff_sec\n',latex_diff_sec.replace('_', r'\_'))
    
    diff_nonsec = diff[diff['class'] == 'nonsec']
    diff_nonsec.sort_values(by='f1 diff', ascending=False, inplace=True)
    diff_nonsec = diff_nonsec.head(5)
    diff_nonsec.drop(columns='class', inplace=True)
    latex_diff_nonsec = diff_nonsec.to_latex(index=False, caption="Most improved f1-score for class 'nonsec'",label="tab:nonsec_improv", float_format="%.2f", na_rep="NA")
    print('latex_diff_nonsec\n',latex_diff_nonsec.replace('_', r'\_'))





def format_number(number):
    signal = '+' if number >= 0 else '-'
    return f"{signal}{abs(number):.2f}"  # Format with two decimal places
