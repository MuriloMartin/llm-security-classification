import pandas as pd

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
    


    print(latex_table)


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
