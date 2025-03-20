from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_ollama import ChatOllama  # Updated import
import json
# Define the Ollama model
MODEL_NAME = "llama3.2"


with open("main_system_prompt.txt", "r", encoding="utf-8") as file:
    content_prompt = file.read()

#print(content_prompt )  # This will print the file content

def generate_response(name: str = None, purpose: str = None, personality: str = None, 
                      general_instruction: str = None, guard_rails: str = None, other_resources: str = None, user_prompt:str = None):
    """
    Generate a response based on general input using LangChain's Runnable API.
    
    Args:
        name (str, optional): Base or reference name (if any).
        purpose (str, optional): Purpose or goal behind the request.
        personality (str, optional): Desired tone or style (e.g., professional, casual).
        general_instruction (str, optional): Additional instructions for the AI.
        guard_rails (str, optional): Rules or restrictions to follow.
        other_resources (str, optional): Additional context or data to consider.
    
    Returns:
        str: AI-generated response.
    """

    # Initialize the Ollama model
    llm = ChatOllama(model=MODEL_NAME, temperature=0.7)

    # Define the system message to provide general context
    system_message = SystemMessagePromptTemplate.from_template(content_prompt )

    # Use a simple human message
    human_message = HumanMessagePromptTemplate.from_template(user_prompt)

    # Create a chat prompt template
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message,
        human_message
    ])

    # Create a RunnableSequence
    response_chain = chat_prompt | llm 

    # Prepare input data
    input_data = {
        "name": name or "Not specified",
        "purpose": purpose or "Not specified",
        "personality": personality or "Not specified",
        "general_instruction": general_instruction or "",
        "guard_rails": guard_rails or "",
        "other_resources": other_resources or ""
    }

    # Run the chain and get the response
    response = response_chain.invoke(input_data)
    content = response.content

    return content


# Load data from JSON file
def load_data_from_json(file_path, agent_num):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data[agent_num]  # Load the first object from the array


def select_agent_and_give_prompt(agent, prompt):
    agent_map = {
        "Creative Muse": 0,
        "Code Auditor": 1,
        "FitCoach": 2,
        "SupportBot": 3,
        "MoneyMaster": 4
    }
    
    agent_index = agent_map.get(agent)

    data = load_data_from_json('agents.json', agent_index)
    response  = (generate_response(
        name=data["name"],
        purpose=data["purpose"],
        personality=data["personality"],
        general_instruction=data["general_instruction"],
        guard_rails=data["guard_rails"],
        other_resources=data["other_resources"],
        user_prompt=prompt
    ))

    return  response


# Run the function if script is executed directly
if __name__ == "__main__":
    print(select_agent_and_give_prompt("FitCoach","what are you"))


