from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import sys

print("Python executable:", sys.executable)


load_dotenv()

@tool
def calculator(a:float, b: float, operation:str) -> str:
    """Useful for performing basic arethmetic with hnumbers"""
    print("Calculator tool has been called")
    if operation == "+":
        result = a + b
        op_name = "sum"
    elif operation == "-":
        result = a - b
        op_name = "difference"
    elif operation == "*":
        result = a * b
        op_name = "product"
    elif operation == "/":
        if b == 0:
            return "Error: Division by zero is undefined."
        result = a / b
        op_name = "quotient"
    else:
        return f"Unsupported operation '{operation}'. Please use '+', '-', '*', or '/'."

    return f"The {op_name} of {a} and {b} is {result}"

def sayHello(name:str) -> str:
    """Greeting the User"""
    print("Hello has been called")
    return f"Hello {name}, I hope you're having a great day today!"

def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator, sayHello]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()