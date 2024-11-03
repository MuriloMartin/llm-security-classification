import pandas as pd
if __name__ == '__main__':
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\ConsolidatedData\data.json'
    with open(output_path, 'w') as file:
        json.dump(consolidated_data, file, indent=4)