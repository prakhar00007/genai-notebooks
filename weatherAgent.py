from dotenv import load_dotenv
from openai import OpenAI
import json
import requests

load_dotenv()

client=OpenAI()

def get_weather(city:str):
    print("⚒️ Tool Called: get_weather",city)
    url=f'https://wttr.in/{city}?format=%C+%t'
    response=requests.get(url)

    if response.status_code==200:
        return f"the weather in {city} is {response.text}"
    return "Something went wrong"

available_tools={
    "get_weather":{
        "fn": get_weather,
        "description": "takes a city names as an input and return the current weather for the city"
    }
}

system_prompt = """
    You are an helpful AI assistant who is specialized in resolving user queries
    You work on start,plan,action,observe mode.
    For the given user queries and available tools,plan the step by step execution , based on the planning,select the relevant tool from the available tool. and based on the 
    tool selection you perform an action to call the tool. Wait for the observation & based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the output Json Format.
    - Always perform one step at a time and wait for next input
    - carefully analyze the user query
    
    Output Json Format:{{
        "step":"string",
        "content":"string",
        "function":"the name of function if the step is action",
        "input":"the input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and return the current weather for the city
    

    Example:
    User Query: What is the weather of NewYork?
    Output: {{"step":"plan","content":"The user is interested about the weather of New York"}}
    Output: {{"step":"plan","content":"From the available tools I should call get weather"}}
    Output: {{"step":"action","function":"getWeather","input": "New York"}}
    Output: {{"step":"observe","output":"12 degree Celsius"}}
    Output: {{"step":"output","content":"The weather for the New York seems to be 12 degrees"}}
"""

messages=[
    {
        'role':'system',
        'content':system_prompt
    },

]
while True:
    user_query=input('> ')
    messages.append({
        "role":"user",
        "content":user_query
    })

    while True:
        response=client.chat.completions.create(
        model='gpt-4o-mini',
        response_format={"type":"json_object"},
        messages=messages
        )
        parsed_output=json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant","content":json.dumps(parsed_output)})

        if parsed_output.get("step")=="plan":
            print(f'🧠:{parsed_output.get("content")}')
            continue
        
        if parsed_output.get("step")=="action":
            tool_name=parsed_output.get("function")
            tool_input=parsed_output.get("input")

            if available_tools.get(tool_name,False)!=False:
                output=available_tools[tool_name].get("fn")(tool_input)
                messages.append({'role':'assistant',"content":json.dumps({
                    "step":"observere","output":output
                })})
                continue
        if parsed_output.get("step")=="output":
            print(f"🤖:{parsed_output.get("content")}")
            break
