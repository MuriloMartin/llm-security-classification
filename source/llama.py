import json
import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')

def format_response(response):
    response = response.lower()
    if 'nfr' in response:
        return 'NFR'
    elif 'fr' in response:
        return 'FR'
    elif 'Non-Functional Requirement' in response:
        return 'NFR'
    elif 'Functional Requirement' in response:
        return 'FR'
    elif 'non functional requirement' in response:
        return 'NFR'
    elif 'functional requirement' in response:
        return 'FR'
    else:
        return response
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
            response = json.loads(str(response['response']))
            if 'result' in response:
                response = response['result']
            response = response['label']
            response = format_response(response)
            return response
        except:
            print(response)
            print('Error in response')
            return None

if __name__ == '__main__':
    sample_size = 100
    models = ['llama3','mistral', 'gemma']
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\PROMISE_exp_treated.json'

    for model in models:
        output_path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\DataSets\Promise_exp\results\{model}.json'
        with open(path, 'r') as file:
            data = json.load(file)
        for i in tqdm(data[:sample_size]):
            req = i['requirement']
            for strategy in strategys:   
                user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
                response = classify_nfr(user_prompt, 'llama3')
                if response is None:
                    continue

                if 'response' not in i:
                    i['response'] = {}
                i['response'][strategy] = response
        
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=4)



    

            
        