import os
import sys
import time
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from dotenv import load_dotenv
from utils.prompts import (
    splitter_prompt,
    scheduler_prompt,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


KEY = os.getenv("GROQ_API_KEY")
model = "llama3-70b-8192"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", splitter_prompt),
        ("human", "{crop_name} {total_days} {current_date} {sowing_date}"),
    ]
)
llm = ChatGroq(
    model=model,
    api_key=KEY,
)
chain = prompt | llm


def getSplit(crop_name, total_days):
    res = chain.invoke(
        {
            "crop_name": crop_name,
            "total_days": total_days,
            "current_date": time.strftime("%Y-%m-%d"),
            "sowing_date": time.strftime("%Y-%m-%d"),
        }
    )
    # return res.content
    res = res.content
    first = res.find("```json")
    last = res.rfind("```")
    # print(repr(res[first + 7 : last].strip()))
    json_str = json.loads(res[first + 7 : last].strip())
    return json_str


if __name__ == "__main__":
    print(getSplit("Paddy", 140))
