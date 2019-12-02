from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer #Trainer Lib
import os

app = Flask(__name__)

#Create the Chatbot
MedicalBot = ChatBot('Test1', storage_adapter="chatterbot.storage.SQLStorageAdapter",
                        preprocessors=['chatterbot.preprocessors.clean_whitespace'],
				logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.35,
            'default_response': 'I am sorry, but I do not understand.'
        } 
    ],
    trainer='chatterbot.trainers.ListTrainer'
	)

#Set the trainer
MedicalBot.set_trainer(ListTrainer)

"""
for _file in os.listdir('Diabetes Dialog'):
	#Read Training Data
	MedicalBotGreeting = open('Diabetes Dialog/greeting.txt', 'r' ).readlines()	
	MedicalBotAdvises = open('Diabetes Dialog/Advises.txt', 'r' ).readlines()
	
	#Train bot
	MedicalBot.train(MedicalBotGreeting)
	MedicalBot.train(MedicalBotAdvises)

"""

@app.route("/")
def home():
    return render_template("index3.html")
	#return render_template("index.backup.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(MedicalBot.get_response(userText))
	


if __name__ == "__main__":
    app.run(debug=True)