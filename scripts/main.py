

# 1. ChatGPT API - https://platform.openai.com/docs/overview
chatgpt_api_key = "sk-proj-xHxMzyrwkKIiym9bUnsmT3BlbkFJQm2bjxY4KokodOeiaBis"
# 3. Gemini API - https://ai.google.dev/gemini-api/docs/get-started/python
gemini_api_key = "AIzaSyCJvxcJsJGE9KqUkyJ62fcD084bsjkK9AM"




#F,A,L,LF,MN,O,PE,SC,SE,US,FT,PO

prompt = "model='You are Frederick, an expert in requirements engineering. You are tasked with with the classification of non functinal requierments for a software project. You should consider 4 types of non functional requirements: Usability, Security,Performance, and Maintainability\
user_1 = Usability refers to the ease with which users can interact with a system to achieve their goals effectively and efficiently. Key aspects of usability include intuitiveness, learnability, efficiency, memorability, and user satisfaction. \
Usability requirements often involve factors such as user interface design, accessibility, error handling, and documentation clarity.\
Examples of usability requirements include response time for user interactions, navigation simplicity, and support for users with disabilities. \
Security requirements are concerned with protecting the system and its data from unauthorized access, data breaches, and other security threats. \
They encompass measures to ensure confidentiality, integrity, authentication, authorization, and non-repudiation of data and system resources. \Security requirements may include encryption standards, access control mechanisms, audit trails, and compliance with regulatory standards such as GDPR or HIPAA.\
Examples of security requirements include password complexity rules, role-based access controls, and secure transmission protocols (e.g., HTTPS) \
Performance requirements address the responsiveness, scalability, throughput, and resource utilization of a system under various conditions. \
They specify the acceptable levels of system performance in terms of response time, processing speed, and capacity. \
Performance requirements often include metrics such as response time thresholds, maximum concurrent users, and transaction throughput rates. \
Examples of performance requirements include system load time, database query response time, and server uptime/downtime thresholds \
Maintainability requirements focus on the ease with which a system can be modified, enhanced, debugged, and repaired over its lifecycle. They encompass factors such as code readability, modularity documentation quality, and adherence to coding standards. \
Maintainability requirements aim to minimize the cost and effort required for ongoing system maintenance and evolution. \
Examples of maintainability requirements include code commenting standards, version control practices, and system documentation completeness. \
user 2 = Great! Let's begin then :) \
For the given requierment, label it as Usability, Security,Performance, and Maintainability. You must answer step by step \
\
\
requirement: The product shall prevent its data from incorrect data being introduced. \
"
req = 'mock req'
prompt = f"For the given requirements: {req} \
					label it as Usability, Security,Performance, or Maintainability."

print(prompt)
