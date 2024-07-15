import chardet
import json

def get_file_encoding(file_path):
    '''
    Get the encoding of a file
    '''
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def treat_promise_exp(consolidated_data):
    '''
    Recieves the consolidated data and requirements from the PROMISE dataset
    '''
    #read the .arff file
    #C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\PROMISE_exp.arff
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\PROMISE_exp.arff'
    encoding = get_file_encoding(path)
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        data = False
        for line in lines:
            if data:
                print(line)
                output = line.split(',')
                label = output[2].strip() if output[2].strip() == 'F' else 'NFR'
                consolidated_data.append({'project_id': output[0], 'requirement': output[1], 'label':label, 'source': 'promise_exp'})
            if '@DATA' in line:
                data = True
    return consolidated_data

if __name__ == '__main__':
    consolidated_data = []
    print('dasdfas')
    consolidated_data = treat_promise_exp(consolidated_data)
    output_path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\PROMISE_exp_treated.json'
    with open(output_path, 'w') as file:
        json.dump(consolidated_data, file, indent=4)