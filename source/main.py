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
    
def classify_nfr(user_proompt, model, response_logs):
        while True:
            try:
                response = ollama.generate(
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
        try:
            response = json.loads(str(response['response']))
            response_logs.append({"reponse": response, "status": "ok"})
            if 'result' in response:
                response = response['result']
            response = response['label']
            response = format_response(response)
            return response
        except:
            response_logs.append({"reponse": response, "status": "error"})
            print('Error in response')
            return None

if __name__ == '__main__':
    sample_size = 10
    models = ['llama3','mistral', 'gemma']
    path = r'C:\Users\Murilo\Desktop\Projetos\TCC\ConsolidatedData\data.json'

    for model in models:
        response_logs = []
        response_logs_path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\response_logs_{model}.json'
        output_path = rf'C:\Users\Murilo\Desktop\Projetos\TCC\results\{model}.json'
        with open(path, 'r') as file:
            data = json.load(file)
        for i in tqdm(data[:sample_size]):
            req = i['requirement']
            for strategy in strategys:   
                user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
                response = classify_nfr(user_prompt, model, response_logs)
                if response is None:
                    continue

                if 'response' not in i:
                    i['response'] = {}
                i['response'][strategy] = response
        
        with open(output_path, 'w+') as file:
            json.dump(data[:sample_size], file, indent=4)
        with open(response_logs_path, 'w+') as file:
            json.dump(response_logs, file, indent=4)



    

            
        