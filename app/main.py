from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

# Dictionary to store user journal entries
user_journal = ""

@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint with a simple response system to prevent hallucinations
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    predefined_responses = {
        "hello": "Hello! How can I support you today?",
        "hi": "Hi there! How are you feeling?",
        "how are you": "I'm here to support you! How can I help?",
        "help": "I can assist you with mindfulness, journaling, and emotional support. What do you need?",
    }

    response = predefined_responses.get(user_message.lower(), "I'm here to listen. Tell me more.")
    return jsonify({"response": response})

# Journal functionality
@app.route("/journal", methods=["POST"])
def journal():
    global user_journal
    user_journal = request.json.get("entry", "")
    return jsonify({"response": "Your journal entry has been saved."})

@app.route("/get_journal", methods=["GET"])
def get_journal():
    return jsonify({"entry": user_journal})

# Button actions
@app.route("/button_action", methods=["POST"])
def button_action():
    button_id = request.json.get("button_id")

    if button_id == "journal":
        return jsonify({"response": "Opening your journal...", "open_journal": True})
    
    response_map = {
        "chat": "Opening chat section...",
        "progress": "Here is your progress update.",
        "settings": "Accessing settings...",
        "emergency-support": "Contacting emergency support. If you need urgent help, call 988.",
        "feeling-great": "I'm glad you're feeling great! 😊",
        "feeling-good": "Happy to hear you're doing good! 😊",
        "feeling-okay": "It's okay to have an 'okay' day. I'm here for you!",
        "feeling-bad": "Sorry to hear you're feeling bad. Let's talk about it.",
        "feeling-terrible": "I'm so sorry you're feeling terrible. Take a deep breath—I'm here to help.",
        "breathing-exercise": "Try this deep breathing exercise: Inhale for 4 seconds, hold for 4, exhale for 4.",
        "mindfulness": "Check out this mindfulness guide: https://www.mindful.org/meditation/mindfulness-getting-started/",
        "coping-strategies": "Here are some coping strategies: https://www.helpguide.org/articles/stress/stress-management.htm",
        "crisis-resources": "Find crisis resources here: https://www.samhsa.gov/find-help/national-helpline",
        "daily-goals": "Setting your daily goals. Stay motivated!"
    }

    response = response_map.get(button_id, "Unknown button action.")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
