from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
import re
from datetime import datetime
import wikipediaapi
import requests

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["taskab"]
collection = db["schedules"]

class Task(BaseModel):
    task: str
    time: str
class Query(BaseModel):
    ques: str


@app.post("/schedule_task/")
async def schedule_task(query: Query):
    try:
        ques = query.ques.lower()
        if "task" in ques or "schedule" in ques or "scheduler" in ques:
            result = await task_scheduler(ques)
            return result
        elif "hi" in ques:
            return "Hi, I am your personal chatbot here to assist you."
        elif "hello" in ques:
            return "Hello, I am your personal chatbot here to assist you."
        elif "hey" in ques:
            return "Hey, I am your personal chatbot here to assist you."
        elif "your purpose" in ques:
            return "I am a personal chatbot. I can assist you with scheduling tasks and informing you with general knowledge."
        else:
            result = await wiki_answer(ques)
            return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def wiki_answer(command: str):
    if 'who is' in command:
        wiki = command.replace('who is', '').strip()
    elif 'what is' in command:
        wiki = command.replace('what is', '').strip()
    elif 'where is' in command:
        wiki = command.replace('where is', '').strip()
    elif 'when is' in command:
        wiki = command.replace('when is', '').strip()
    elif 'why is' in command:
        wiki = command.replace('why is', '').strip()
    elif 'tell me about' in command:
        wiki = command.replace('tell me about', '').strip()
    elif 'what are' in command:
        wiki = command.replace('what are', '').strip()
    elif 'who are' in command:
        wiki = command.replace('who are', '').strip()
    elif 'where are' in command:
        wiki = command.replace('where are', '').strip()
    elif 'when are' in command:
        wiki = command.replace('when are', '').strip()
    elif 'why are' in command:
        wiki = command.replace('why are', '').strip()
    elif 'tell me about' in command:
        wiki = command.replace('tell me about', '').strip()
    elif 'define' in command.lower():
        wiki = command.replace('define', '', re.IGNORECASE).strip()
    else:
        return "Sorry, I didn't understand the question."
    info = get_wikipedia_summary(wiki)
    return info

def get_wikipedia_summary(query: str, sentences: int = 2) -> str:
    try:
        headers = {
            'User-Agent': 'main/1.0 (kalkeeshjamipics@gmail.com)'
        }
        response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}", headers=headers)
        data = response.json()
        if 'extract' in data:
            summary = data['extract']
            summary_sentences = '. '.join(summary.split('. ')[:sentences])
            return summary_sentences
        else:
            return "Sorry, I couldn't find any information on that topic."
    except Exception as e:
        return f"An error occurred: {e}"

async def task_scheduler(ques: str):
    task_match = re.search(r'-(.*?)\sat', ques)
    task = task_match.group(1).strip() if task_match else "No specific task mentioned"
    time_match = re.search(r'\b\d{1,2}:\d{2}\s*[APMapm]{2}\b', ques.upper())
    
    if not time_match:
        raise ValueError("No valid time format found in the query.")
    
    time_str = time_match.group(0).strip().upper()
    time_obj = datetime.strptime(time_str, '%I:%M %p')
    formatted_time = time_obj.strftime('%I:%M %p')
    
    # Store the task and time in MongoDB
    task_data = {"task": task, "time": formatted_time}
    collection.insert_one(task_data)
    
    return {"task": task, "time": formatted_time}

@app.get("/tasks/")
async def get_tasks():
    tasks = list(collection.find())
    for task in tasks:
        task['_id'] = str(task['_id'])
    return tasks

@app.delete("/delete_task/")
async def delete_task(task_name: str):
    result = collection.delete_one({"task": task_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}