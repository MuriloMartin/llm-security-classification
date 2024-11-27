import json
import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')

def extract_label(response):
    if 'label' in response:
        return response['label']
    if 'result' in response and 'label' in response['result']:
        return response['result']['label']
    
    #for few shot strategy
    if "user_3" in response and 'label' in response['user_3']:
        return response['user_3']['label']
    
def classify_req(user_proompt, model, response_logs):
        while True:
            try:
                model_output = ollama.generate(
                model=model,
                format="json",
                options={
                    "temperature": 0,
                    "num_ctx": 8192,
                    "num_predict": -1
                },
                stream=False,
                prompt=f"""{user_proompt}"""
            )
            except:
                continue
            break
        response_logs.append(model_output)
        try:
            response = json.loads(str(model_output['response']))
            label = extract_label(response)
            if label == None:
                raise
            return label
        except:
            print("Error")
            response_logs.append("^^^^^^^^^^ ERROR ^^^^^^^^^^")
            return None

if __name__ == '__main__':
    models = ['llama3','mistral', 'gemma']
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\ConsolidatedData\data.json'

    for model in models:
        response_logs = []
        response_logs_path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\response_logs_{model}.json'
        output_path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\{model}.json'
        with open(path, 'r') as file:
            data = json.load(file)
        sample_size = len(data)
        for i in tqdm(data[:sample_size]):
            req = i['requirement']
            for strategy in strategys:   
                user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
                response = classify_req(user_prompt, model, response_logs)

                if 'response' not in i:
                    i['response'] = {}

                i['response'][strategy] = response
        
        with open(output_path, 'w+') as file:
            json.dump(data[:sample_size], file, indent=4)
        with open(response_logs_path, 'w+') as file:
            json.dump(response_logs, file, indent=4)



    

            
        