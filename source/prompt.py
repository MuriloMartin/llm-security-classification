


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
        user_msg = f"For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR). Return the result as a JSON with the following format: {{'label': 'NFR OR FR}}"
    
    if strategy == 'few_shot_cot':
        req1 = 'Every user of the system shall be authenticated and authorized.'
        req2 = 'The product shall allow the user to save the property search results.'
        user_msg = f"user_1= For the given requirement: {req1}  label it as a functional (FR) or non functional requirement (NFR). Return the result as a JSON with the following format: {{'label': 'NFR OR FR}} \
        This requirement falls under the category of NFR. It specifically addresses the aspect of ensuring the integrity of the system's data by preventing incorrect data from being introduced, which is crucial for maintaining data accuracy and reliability, thereby safeguarding against potential security threats such as data corruption or manipulation. \
        response_1: {{'label': 'NFR}} \
        user_2= For the given requirement: {req2}  label it as a functional (FR) or non functional requirement (NFR). Return the result as a JSON with the following format: {{'label': 'NFR OR FR}} \
        This requirement is a Functional Requirement (FR). \
        Functional requirements describe the specific behaviors or functions of a system, detailing what the system should do. In this case, saving property search results is a specific function that the system must perform. \
        response_2: {{'label': 'FR}} \
        user_3= For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR). Return the result as a JSON with the following format: {{'label': 'NFR OR FR}}. response_3: "
        
    
    if strategy =='zero_shot_cot':
        user_msg = f"For the given requirement: {requirement} label it as a functional (FR) or non functional requirement (NFR).Lets think step by step. Return the result as a JSON with the following format: {{'label': 'NFR OR FR}}"
        
    if strategy == 'raw_inst':
        user_msg = f"You are an expert in requirements engineering.  You are tasked with with the classification of non functinal  requierments for a software project. You should consider 2 types  of  requirements: functional (FR) and non functional (NFR) requirements. Functional requirements specify what a system should do, detailing the necessary tasks, behaviors, and functions, while non-functional requirements define the system's quality attributes, such as performance, usability, reliability, and security, ensuring the system's operational standards are met. \
        For the given requierment: {requirement}  label it as a functional (FR) or non functional requirement (NFR). Return the result as a JSON with the following format: {{'label': 'NFR OR FR}}"

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
    responses = []
    for strategy in strategys:
        responses.append(prompt_factory(req,strategy))

    for i in range(len(responses)):
        print(f'\n\nStrategy:{strategys[i]}')
        for key, value in responses[i].items():
            print(key, '\n', value)
    
    