import json
import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')


def classify_nfr(user_proompt, model):
        while True:
            try:
                response = ollama.generate(
                model=model,
                format="json",
                options={
                    "temperature": 1,
                    "num_ctx": 8192,
                    "num_predict": -1
                },
                stream=False,
                prompt=f"""{user_proompt}"""
            )
            except:
                continue
            break
        try:
            return json.loads(str(response['response']))['label']
        except:
            print(response['response'])
            print('Error in response')

if __name__ == '__main__':
    sample_size = 200
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\PROMISE_exp_treated.json'
    output_path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\results\zero_shot_llama3.json'
    with open(path, 'r') as file:
        data = json.load(file)


    for i in tqdm(data[:sample_size]):
        req = i['requirement']
        for strategy in strategys:   
            user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
            response = classify_nfr(user_prompt, 'llama3')
            if 'response' not in i:
                i['response'] = {}
            i['response'][strategy] = response
    
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)



    

            
        