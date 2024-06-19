


def prompt_factory(requirement: str, strategy: str) -> dict:
    """
    Generates a user_msg for a given requirement and strategy.

    Args:
        requirement (str): A string of the requirement we want to classify.
        strategy (str): The strategy to use. Must be one of the following:
                        'zero_shot', 'few_shot_cot', 'zero_shot_cot', 'raw_inst',
                        'sys_inst', 'both_inst'.

    Returns:
        dict: System message (sys_msg) and User message (user_msg)
    """
    sys_msg = ''
    user_msg = ''

    if strategy == 'zero_shot':
        user_msg = f"For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR). Answer must be only the label. Do not add any additional information."
    
    if strategy == 'few_shot_cot':
        req = '1 - Every user of the system shall be authenticated and authorized.'
        user_msg = f"user_1= For the given requirement: {req}  label it as a functional (FR) or non functional requirement (NFR). Answer in the following format: Number , Label \
        assistent_1=This requirement falls under the category of NFR. It specifically addresses the aspect of ensuring the integrity of the system's data by preventing incorrect data from being introduced, which is crucial for maintaining data accuracy and reliability, thereby safeguarding against potential security threats such as data corruption or manipulation. \
        answer_1 = 1,FNR \
        user_2= For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR). Answer in the following format: Number , Label"
        
    
    if strategy =='zero_shot_cot':
        user_msg = f"For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR). Answer in the following format: Number , Label. Lets think step by step"
        
    if strategy == 'raw_inst':
        user_msg = f"You are an expert in requirements engineering.  You are tasked with with the classification of non functinal  requierments for a software project. You should consider 2 types  of  requirements: functional (FR) and non functional (NFR) requirements. Functional requirements specify what a system should do, detailing the necessary tasks, behaviors, and functions, while non-functional requirements define the system's quality attributes, such as performance, usability, reliability, and security, ensuring the system's operational standards are met. \
        For the given requierment: {requirement}  label it as a functional (FR) or non functional requirement (NFR). Answer in the following format: Number , Label"

    # if strategy == 'sys_inst':
    #     sys_msg = "You are an expert in requirements engineering. You are tasked with with the classification of non functinal requierments for a software project. You should consider  2 types  of  requirements: functional (FR) and non functional (NFR) requirements. Answer in the following format: Number , Label"
    #     user_msg = f"For the given requierment: {requirement} label it as a functional (FR) or non functional requirement (NFR)."
        
    # if strategy == 'both_inst':
    #     sys_msg = "You are an expert in requirements engineering. You are tasked with with the classification of non functinal requierments for a software project. You should consider  2 types  of  requirements: functional (FR) and non functional (NFR) requirements."
    #     user_msg = f"Functional requirements specify what a system should do, detailing the necessary tasks, behaviors, and functions, while non-functional requirements define the system's quality attributes, such as performance, usability, reliability, and security, ensuring the system's operational standards are met. For the given requierment: {requirement} label it as a functional (FR) or non functional requirement (NFR). "
 
        

        
    return {'sys_msg': sys_msg, 'user_msg':user_msg}
        
strategys = ['zero_shot', 'few_shot_cot', 'zero_shot_cot', 'raw_inst']       
    

if __name__ == '__main__':
    req = 'The system shall refresh the display every 60 seconds.'
    strategys = ['zero_shot', 'few_shot_cot', 'zero_shot_cot', 'raw_inst']
    responses = []
    for strategy in strategys:
        responses.append(prompt_factory(req,strategy))

    for i in range(len(responses)):
        print(f'\n\nStrategy:{strategys[i]}')
        for key, value in responses[i].items():
            print(key, '\n', value)
    
    