from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import certifi

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://Harini:shreydurr@project-loginpage.izmcg2a.mongodb.net/?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile=certifi.where()
)
db = client["mood_support_db"]
users_collection = db["users"]
mood_collection = db["recommendations"]

# Insert mood data once
if mood_collection.count_documents({}) == 0:
    mood_data = [
        {
            "mood": "Happy",
            "movies": ["Zindagi Na Milegi Dobara", "Yeh Jawaani Hai Deewani", "The Intern", "Paddington 2", "Queen"],
            "music": ["Happy – Pharrell Williams", "Uptown Funk – Bruno Mars", "Can't Stop the Feeling – JT", "Good Life – OneRepublic", "Shake It Off – Taylor Swift"],
            "articles": ["10 Ways to Stay Happy", "Embrace Positivity", "Happiness Hacks", "Science of Joy", "Gratitude & Brain"]
        },
        {
            "mood": "Sad",
            "movies": ["The Pursuit of Happyness", "Dear Zindagi", "The Fault in Our Stars", "Inside Out", "A Beautiful Mind"],
            "music": ["Fix You – Coldplay", "Let Her Go – Passenger", "Someone Like You – Adele", "Jeene Bhi De – Arijit Singh", "Say You Won’t Let Go – James Arthur"],
            "articles": ["Dealing with Sadness", "Mental Health Tips", "Coping with Emotional Pain", "Journaling for Clarity", "Healing Emotionally"]
        },
        {
            "mood": "Stressed",
            "movies": ["Chhichhore", "Good Will Hunting", "Eat Pray Love", "The Secret", "Peaceful Warrior"],
            "music": ["Lo-fi Chill Beats", "Weightless – Marconi Union", "River Flows in You", "Ocean Sounds", "Dreamscape"],
            "articles": ["5-Minute Stress Relief", "Breathing Exercises", "Guide to Meditation", "Time Management", "Yoga for Focus"]
        },
        {
            "mood": "Calm",
            "movies": ["Barfi!", "The Secret Life of Walter Mitty", "Life of Pi", "The Hundred-Foot Journey", "Finding Nemo"],
            "music": ["Sunrise – Norah Jones", "Bloom – The Paper Kites", "Breezeblocks – Alt-J", "Indian Flute", "Chillstep Vibes"],
            "articles": ["Staying Present", "Benefits of Silence", "Calm Mornings", "Minimalism & Peace", "Slowness in Life"]
        }
    ]
    mood_collection.insert_many(mood_data)

# Routes
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    user = users_collection.find_one({"email": email, "password": password})

    if user:
        session["user"] = email
        return redirect("/dashboard")
    else:
        return render_template("login.html", msg="Invalid credentials")

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    if users_collection.find_one({"email": email}):
        return render_template("login.html", msg="Email already exists")
    users_collection.insert_one({"name": name, "email": email, "password": password})
    return render_template("login.html", msg="Signup successful. Please log in.")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    recommendations = None
    mood = ""

    if request.method == "POST":
        mood = request.form.get("mood")
        mood_doc = mood_collection.find_one({"mood": mood})
        if mood_doc:
            recommendations = {
                "movies": mood_doc.get("movies", []),
                "music": mood_doc.get("music", []),
                "articles": mood_doc.get("articles", [])
            }

    return render_template("dashboard.html", mood=mood, recommendations=recommendations, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
