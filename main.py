import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory

# -------------------------------
# API KEY (PASTE YOUR KEY HERE)
# -------------------------------
api_key = "your-api-key"

# -------------------------------
# LLM (WORKING MODEL)
# -------------------------------
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)

# -------------------------------
# BMI TOOL
# -------------------------------
def bmi_calculator(input_text):
    try:
        weight, height = map(float, input_text.split())
        bmi = weight / (height ** 2)
        return f"FINAL ANSWER: Your BMI is {round(bmi, 2)}"
    except:
        return "Enter: weight height (e.g., 70 1.75)"

# -------------------------------
# CALORIE TOOL
# -------------------------------
def calorie_calculator(input_text):
    try:
        age, weight, height = map(float, input_text.split())
        calories = 10*weight + 6.25*height - 5*age + 5
        return f"FINAL ANSWER: Calories needed: {round(calories, 2)} kcal"
    except:
        return "Enter: age weight height"

# -------------------------------
# WORKOUT TOOL
# -------------------------------
def workout_recommender(goal):
    goal = goal.lower()

    if "weight loss" in goal:
        return "FINAL ANSWER: Cardio + HIIT (5 days/week)"
    elif "muscle gain" in goal:
        return "FINAL ANSWER: Strength training + protein diet"
    else:
        return "FINAL ANSWER: Balanced fitness routine"

# -------------------------------
# TOOLS
# -------------------------------
tools = [
    Tool(
        name="BMI Calculator",
        func=bmi_calculator,
        description="Use this tool when user provides weight and height. Input: weight height"
    ),
    Tool(
        name="Calorie Calculator",
        func=calorie_calculator,
        description="Use this tool when user provides age, weight, height"
    ),
    Tool(
        name="Workout Recommender",
        func=workout_recommender,
        description="Use this tool when user asks for workout"
    )
]

# -------------------------------
# MEMORY
# -------------------------------
memory = ConversationBufferMemory(memory_key="chat_history")

# -------------------------------
# AGENT
# -------------------------------
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="conversational-react-description",
    memory=memory,
    verbose=False,
    handle_parsing_errors=True
)

# -------------------------------
# RUN
# -------------------------------
print("🏋️ Fitness AI Agent Running...")
print("Type 'exit' to stop\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent.invoke({"input": user_input})
    print(response["output"])
