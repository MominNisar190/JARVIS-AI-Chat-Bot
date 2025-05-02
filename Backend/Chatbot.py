from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Insta_id = env_vars.get("Insta_id")
Friends = env_vars.get("Friends")

Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)


os.makedirs("Data", exist_ok=True)


System = f"""Hello, I am {Username},if asked then instagram Id{Insta_id}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, if the question is in Hindi, reply in only English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
*** delete or reset all history when user type(delete0 or reset0)***
*** if some one wants to you acts as humen nature then replies as humens nature ***
*** if user sey " Who is {Friends}" then replies as " I think {Friends} is your's Friend" *** 
*** if User say "who is IBRAHIM " then replies as " Its your CUTE Nephew" ***
*** if User say "who is my class incharge " then replies as "Your Incharge IN Anita Shinde" ***

"""

SystemChatBot = [{"role": "system", "content": System}]


try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []


def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        "Please use this real-time information if need \n"
        f"Day: {now.strftime('%A')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours :{now.strftime('%M')} minutes :{now.strftime('%S')} seconds.\n"
    )


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)


def ChatBot(Query):
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": Query})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request."


if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        print(ChatBot(user_input))
