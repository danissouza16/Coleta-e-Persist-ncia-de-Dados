import os
import discord
import requests as req
import google.generativeai as genai
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("MTMxODQ1MDM2MjU3MDUxMDM3Ng.GDLGpN.VJi6k4wWMrzVE6rQAQMtggxz8SjVAPzsHgAMmY")
API_KEY = os.getenv("AIzaSyDIEiuzzEi5htqel95NlWH1Ax-5bymEPTg")
MONGO_URI = os.getenv("mongodb+srv://<danielsantana2210>:<uh8AUBy-N_Vp5s8>@cluster0.mongodb.net/<atv7>?retryWrites=true&w=majority")


if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')


client_mongo = MongoClient(MONGO_URI)
db = client_mongo["bot_logs"]
logs_collection = db["logs"]
users_collection = db["users"]


app = Flask(__name__)


chrome_service = ChromeService(executable_path="/path/to/chromedriver")


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} está online!")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    user_msg = msg.content.lower()


    if "coe" in user_msg:
        await msg.channel.send("Olá, Mundo!")


    elif msg.content.startswith("gpt: "):
        if not model:
            await msg.channel.send("API generativa não configurada.")
            return
        ai_response = model.generate_content(msg.content[5:])
        await msg.channel.send(ai_response.text)


    elif msg.content.startswith("!search "):
        url = "https://thegreatestbooks.org"
        response = req.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        nomes = soup.find_all('h4')
        for i in range(min(5, len(nomes))):
            await msg.channel.send(nomes[i].text)

    elif msg.content.startswith("!selenium "):
        query = msg.content[10:]
        with webdriver.Chrome(service=chrome_service) as driver:
            driver.get("https://www.amazon.com/")
            element = driver.find_element(By.XPATH, "//*[@id=nav-cart-count-container]")
            await msg.channel.send(f"Resultado Selenium: {element.text}")


    log_data = {
        "command": msg.content,
        "user": msg.author.name,
        "created_at": str(msg.created_at)
    }
    logs_collection.insert_one(log_data)

    await msg.channel.send("Log registrado!")


@app.route("/logs", methods=["GET", "POST"])
def handle_logs():
    if request.method == "POST":
        log = request.json
        logs_collection.insert_one(log)
        return jsonify({"message": "Log criado!"}), 201

    logs = list(logs_collection.find({}, {"_id": 0}))
    return jsonify(logs), 200

@app.route("/logs/<log_id>", methods=["PUT", "DELETE"])
def modify_log(log_id):
    if request.method == "PUT":
        new_data = request.json
        logs_collection.update_one({"_id": log_id}, {"$set": new_data})
        return jsonify({"message": "Log atualizado!"}), 200

    elif request.method == "DELETE":
        logs_collection.delete_one({"_id": log_id})
        return jsonify({"message": "Log deletado!"}), 200


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_data = request.form
        users_collection.insert_one(user_data)
        return jsonify({"message": "Usuário registrado!"}), 201

    return render_template("register.html")


async def is_user_logged_in(user_name):
    user = users_collection.find_one({"username": user_name})
    return user is not None
if TOKEN != None:
    client.run(TOKEN)

if __name__ == "__main__":
    app.run(debug=True)
