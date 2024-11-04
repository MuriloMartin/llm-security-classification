


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
        user_msg = f"For the given requirement: {requirement} label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}}"
    
    if strategy =='few_shot':
        req1 = 'Every user of the system shall be authenticated and authorized.'
        req2 = 'The product shall allow the user to save the property search results.'
        user_msg = f"user_1= For the given requirement: {req1} label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}} \
        response_1: {{'label': 'sec'}} \
        user_2= For the given requirement: {req2} label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}} \
        response_2: {{'label': 'nonsec'}} \
        user_3= For the given requirement: {requirement} label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}}. \
        response_3: "
        
    if strategy == 'Few_Shot_Cot':
        req1 = 'Every user of the system shall be authenticated and authorized.'
        req2 = 'The product shall allow the user to save the property search results.'
        user_msg = f"user_1= For the given requirement: {req1}  label it as a security-related requirement (sec) or non security-related requirement (nonsec). Lets think step by step.Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}} \
        This requirement falls under the category of security-related requirement. Reasoning: It specifically addresses core aspects of security by ensuring that users are who they claim to be and that they have the appropriate permissions to perform actions within the system. \
        response_1: {{'label': 'sec'}} \
        user_2= For the given requirement: {req2}  label it as a security-related requirement (sec) or non security-related requirement (nonsec). Lets think step by step. Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}} \
        This requirement is a non security-related requirement (nonsec). \
        While the requirement is essential for functionality, it does not explicitly address security concerns and is therefore classified as a functional requirement rather than a security-related requirement. If security measures were explicitly stated, such as ensuring that saved results are encrypted or accessible only to authenticated users, then it could be classified as security-related.
        response_2: {{'label': 'nonsec'}} \
        user_3= For the given requirement: {requirement} label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}}. \
        response_3: "
        
        
    if strategy == 'raw_inst':
        user_msg = f"You are an expert in requirements engineering.  You are tasked with with the classification of requierments for a software project. You should consider 2 types  of  requirements: security-related requirement (sec) and non security-related requirements (nonsec). Security-related requirements are those that explicitly address the protection of a system's data, resources, and functionalities from unauthorized access, threats, or vulnerabilities. They encompass aspects such as user authentication, data encryption, access controls, and compliance with security standards. In contrast, non-security-related requirements pertain to the general functionality and performance of a system without specific considerations for security. These may include operational features, usability, and system performance metrics that do not inherently involve safeguarding against security risks. \
        For the given requierment: {requirement}  label it as a security-related requirement (sec) or non security-related requirement (nonsec). Return the result as a JSON with the following format: {{'label': 'sec' OR 'nonsec'}}"


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
    
    