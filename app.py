from flask import Flask, render_template, request, jsonify
import random
import datetime
from textblob import TextBlob

app = Flask(__name__)

# Store conversation memory
dialogue_memory = {}

def analyze_sentiment(message):
    analysis = TextBlob(message)
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"

# Enhanced chatbot logic with more responses and advanced features
def chatbot_response(user_id, message):
    responses = {
        "hi": ["Hello! How can I assist you today?", "Hi there! How’s your day going?"],
        "hello": ["Hey! What’s up?", "Hi! How can I help you today?"],
        "how are you": ["I'm just a bot, but I'm doing great! How about you?"],
        "bye": ["Goodbye! Have a wonderful day!", "See you later! Stay safe!"],
        "what is your name": ["I'm ChatBot, your virtual assistant!"],
        "what time is it": [datetime.datetime.now().strftime("The current time is %H:%M:%S")],
        "what's today's date": [datetime.datetime.now().strftime("Today's date is %Y-%m-%d")],
        "tell me a joke": [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? Because they don't have the guts!",
            "Why do cows have hooves instead of feet? Because they lactose!"
        ],
        "motivate me": [
            "Believe in yourself! Every journey begins with a single step.",
            "You are capable of achieving great things! Keep pushing forward!"
        ],
        "fun fact": [
            "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat!",
            "Octopuses have three hearts! Two pump blood to the gills, while the third pumps it to the rest of the body."
        ]
    }
    
    message_lower = message.lower()
    if message_lower in responses:
        return random.choice(responses[message_lower])
    
    sentiment = analyze_sentiment(message)
    if sentiment == "positive":
        return "I'm glad you're feeling good! 😊"
    elif sentiment == "negative":
        return "I'm here to help. If you're feeling down, just know that better days are ahead. 💙"
    
    return "I'm still learning! Can you ask me something else?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get("user_id", "default")
    user_message = request.json.get("message")
    
    if user_id not in dialogue_memory:
        dialogue_memory[user_id] = []
    
    bot_response = chatbot_response(user_id, user_message)
    dialogue_memory[user_id].append({"user": user_message, "bot": bot_response})
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
