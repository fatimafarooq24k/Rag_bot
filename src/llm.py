from groq import Groq
import src.config as cnfg

client = Groq(api_key=cnfg.GROQ_API_KEY)

def generate_response(prompt):

    if not isinstance(prompt, str):
        raise TypeError("The prompt should be a String.")

    if prompt.strip()  == "":
        raise ValueError("Please enter the prompt.")

    model_check = client.chat.completions.create(
        model=cnfg.MODEL,
        messages = [
           { 
            "role" : "user",
            "content" : prompt
            }
        ],
        temperature=cnfg.TEMPERATURE,
        max_tokens=cnfg.MAX_TOKENS
    )

    return model_check.choices[0].message.content