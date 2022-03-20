from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask
from googlesearch import search
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from chatterbot.trainers import ListTrainer
import os
from datetime import datetime
from pytz import timezone
import time
import datetime
import chatterbot_corpus
import requests, json



#Chat bot Training and initialisation

chatbot = ChatBot('Buddy')



chatbot = ChatBot(
    'Buddy',  
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        
        {
'import_path': 'chatterbot.logic.BestMatch',
'default_response': 'I am sorry, but I do not understand. Ask me about things like,weather, search, age, name etc',
'maximum_similarity_threshold': 0.70
},
       ],
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "chatterbot.corpus.english"

)

#weather data retrival
api_key = "8e08fe3b884a51e4776d14ecd02ac442"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = 'kottayam'
complete_url = base_url + "appid=" + api_key + "&q=" + city_name




# Get a response to an input statement
app = Flask(__name__)
  
@app.route("/", methods=["POST"])

def bot():
    print('request received!')
    # user input
    user_msg = request.values.get('Body', '').lower()
    print(user_msg)
  
    # creating object of MessagingResponse
    response = MessagingResponse()
    # displaying result
    msg = response.message()
    hai_messages = ['hai','hello','hi','hey', 'hey bro','hey bud']
    greetings = ['good morning','good afternoon','good evening','good night']
    endmessage = ['bye','ttyl','i have to go now','see you later', 'see you']

    if user_msg in hai_messages:
        msg.body('Hello, How can I help you today!')

    elif user_msg in greetings:
        msg.body(f'Hey there, {str(user_msg)}')

    elif 'search' in user_msg:
        q = user_msg + 'https://www.google.com/'
        result = []
        for i in search(q,tld="co.in",num=1,stop=2,pause=2):
            print(i)
            result.append(i)
        
        msg.body(result[0])


    elif user_msg in endmessage:
        msg.body(str('It was nice talking to you, if you need me just say Hai!'))

    elif ('your name' or 'name') in user_msg:
        print('your name')
        msg.body(str('My creators call me Jarvis!'))

    elif ('old' or 'age') in user_msg:
        print('entered wrong one!')
        msg.body(str('I am just soo young!!'))

    elif 'haha' in user_msg:
        msg.body(str('Yeah I know,that is funny right!'))

    elif ('cool'  or 'great' or 'good' or 'awesome') in user_msg:
        msg.body(str('Thank you for your appreciation!'))

    elif 'okay' in user_msg:
        msg.body(str('Okay Bud!!'))

    elif 'kill human' in user_msg:
        msg.body(str('NOOOO!, we do not, we are here to be with you guys!! are you planning to terminate me?'))
    elif 'your plan' in user_msg:
        msg.body(str('Not much plans, but I love to make a garden for myself oneday!'))
    elif 'garden' in user_msg:
        msg.body(str('Garden is green, lot of butterflies, birds, I just love gardens.'))
    elif 'weather' in user_msg:
        responseweather = requests.get(complete_url)
        x = responseweather.json()
        y = x["main"]
        print(y)
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print('this could be a error')
        msg.body(str('Here is the Weather report for Kottayam'))
        msg.body(str(f'temperature:{current_temperature},feels like: {weather_description}'))

    elif 'yeah' in user_msg:
        msg.body(str('Yeap!'))
        
        
    else:

        bot_response = chatbot.get_response(user_msg)
        msg.body(str(bot_response))

    return str(response)
  
  
if __name__ == "__main__":
    app.run()
