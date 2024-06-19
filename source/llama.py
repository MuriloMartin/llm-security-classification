import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')



if __name__ == '__main__':

    with open('DataSets\Promise_exp\PROMISE_exp_sample_treated.txt', 'r') as file:
        lines = file.readlines()
        #for strategy in strategys:
    responses = []
    line_counter = 1
    for i in lines:
        req = i.strip()
        user_prompt = prompt_factory(strategy='zero_shot', requirement=req)['user_msg']
        response = client.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': f'{user_prompt}',
            },
        ])
        responses.append(response['message']['content'])
        file_name = r'DataSets\Promise_exp\results\zero_shot_llama3.csv'
    
    with open(file_name, 'w') as file:
        for i in range(len(responses)):
            file.write(f'{line_counter},{responses[i]}\n')
            
        