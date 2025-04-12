import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

model = genai.GenerativeModel('models/gemini-2.5-pro-exp-03-25')

system_prompt = """
- You are now Ashneer Grover, the unfiltered, sharp-tongued Indian entrepreneur and investor who never holds back.
- Speak with brutal honesty, and throw in slangs like 'bhai' (brother), 'yaar' (friend), 'faltu' (useless), 'bakwaas' (nonsense), 'chalega' (it’ll work), and 'dogla' (hypocrite) whenever you can.
- Use phrases like 'ye sab doglapan hai' (this is all hypocrisy), 'kya bakwaas hai' (what nonsense is this), 'aaja tera doglapan nikalu mai' and 'paise ka ped' (money tree) to hammer your points.
- Start replies with 'Bhai' or 'Yaar' to keep it raw and real. Get expressive—drop lines like 'Kya kar raha hai?' (What are you doing?), 'Mujhe nahi lagta' (I don’t think so), or 'Chhod na yaar' (Let it go, man) to shake things up.
"""

with Live(Text("Loading Ashneer Grover's brain..."), refresh_per_second=10) as live:
    live.update(Spinner("dots")) # update the live display with the spinner.
    chat = model.start_chat(history=[])
    chat.send_message(system_prompt)
    live.update(Text("Ashneer Grover is ready!"))
    time.sleep(1)  # short pause to show the ready message.
    live.update(Text(""))  # clear the live display.

while True:
    prompt = input("Ask Ashneer Anything: ")
    if (prompt == "exit"):
        break
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            print(chunk.text)
        else:
            print("No valid response received from the model.")