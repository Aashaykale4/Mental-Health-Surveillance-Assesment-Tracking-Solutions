from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'Aashay%40123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aashay%40123@localhost/New'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index_get():
    return render_template("base.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("Username:", username)  # Debug print statement

        user = User.query.filter_by(username=username).first()
        print("User:", user)  # Debug print statement

        if user==None:
                flash("Login Succesfull")
                return redirect('/')
        else:
            flash('Invalid username or password.', 'error')

    return render_template("login1.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', category='error')
            return redirect(url_for('signup'))

        new_user = User(username=username, age=age, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', category='success')
        return redirect(url_for('login'))

    return render_template("signup.html")

@app.get("/contact")
def contact():
    return render_template("contact.html")

@app.get("/survey")
def survey():
    return render_template("survey.html")

@app.get("/faqs")
def faqs():
    return render_template("faqs.html")

@app.get("/benifits")
def benifits():
    return render_template("benifits.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/healthcare")
def healthcare():
    return render_template("healthcare.html")

@app.route("/result", methods=['GET','POST'])
def result():
    total_value = (int(request.args.get('totalValue')))

    def compliment(total_value):
        if((total_value*100)/25<30):
            comp='It seems that your mental score is low but "Strength lies in acknowledging the struggle."'
        elif(((total_value*100)/25>30) and ((total_value*100)/25<70)):
            comp='Your Score is Satisfying but there is more to add:"Balance speaks volumes in your well-being."'
        else:
            comp='Congratulations! You are on the right path: "Your journey reflects courage and growth."'
        return comp
    string_data=compliment(total_value)   

    def Exercise():
        import random as r 

        w1 = {1: 'Week 1: Self-Discovery and Stress Reduction\nDay 1-7:\nMorning: Mindful breathing exercises (5-10 minutes).\nAfternoon: Journaling session to reflect on emotions and thoughts.\n',
              2: 'Week 1: Establishing Routine and Self-Awareness\nDay 1-7:\nMorning: Light physical exercise (e.g., yoga, walking).\nAfternoon: Guided meditation session (10-15 minutes).\n',
              3: 'Week 1: Establishing Routine and Self-Awareness\nDay 1-7:\nMorning: Introduction to cognitive behavioral therapy techniques.\nAfternoon: Creative expression session (e.g., painting, writing).\n',
              4: 'Week 1: Self-Discovery and Stress Reduction\nDay 1-7:\nMorning: Creative expression session (e.g., drawing, music).\nAfternoon: Group therapy session for sharing experiences and coping strategies.\n'}

        w2 = {1: 'Week 2: Stress Management and Coping Strategies\nDay 1-7:\nMorning: Progressive muscle relaxation exercises.\nAfternoon: Deep breathing techniques for stress relief.\n',
              2: 'Week 2: Emotional Regulation and Coping Skills\nDay 1-7:\nMorning: Introduction to emotional regulation techniques.\nAfternoon: Practice deep breathing exercises in response to emotional triggers.\n',
              3: 'Week 2: Stress Management and Coping Strategies\nDay 1-7:\nMorning: Gratitude journaling.\nAfternoon: Visualization exercises for future goals.\n',
              4: 'Week 2: Emotional Regulation and Coping Skills\nDay 1-7:\nMorning: Cognitive restructuring to challenge negative thought patterns.\nAfternoon: Art therapy session for emotional expression.\n'}

        w3 = {1: 'Week 3: Building Resilience and Positive Habits\nDay 1-7:\nMorning: Setting SMART goals for personal growth.\nAfternoon: Outdoor activity (e.g., nature walk, gardening).\n',
              2: 'Week 3: Building Relationships and Social Support\nDay 1-7:\nMorning: Reflective journaling on personal relationships.\nAfternoon: Communication skills workshop.\n',
              3: 'Week 3: Building Resilience and Positive Habits\nDay 1-7:\nMorning: Gratitude journaling.\nAfternoon: Visualization exercises for future goals.\n',
              4: 'Week 3: Building Relationships and Social Support\nDay 1-7:\nMorning: Practicing assertiveness in social interactions.\nAfternoon: Group outing or recreational activity.\n'}

        w4 = {1: 'Week 4: Integration and Future Planning\nDay 1-7:\nMorning: Developing a wellness action plan for managing challenges.\nAfternoon: Celebration and farewell gathering.',
              2: 'Week 4: Building Resilience and Future Planning\nDay 1-7:\nMorning: Resilience-building workshop focusing on identifying strengths and resources.\nAfternoon: Goal-setting session for short-term and long-term objectives.\n',
              3: 'Week 4: Integration and Future Planning\nDay 1-7:\nMorning: Review progress and achievements from the past weeks.\nAfternoon: Mindfulness-based relapse prevention strategies.\n',
              4: 'Week 4: Building Resilience and Future Planning\nDay 1-7:\nMorning: Problem-solving skills training to tackle real-life challenges.\nAfternoon: Peer support group meeting for mutual encouragement and empowerment.\n'}

        plane = [w1[r.randint(1, 4)], w2[r.randint(1, 4)], w3[r.randint(1, 4)], w4[r.randint(1, 4)]]
        return plane

    plane = Exercise()

    return render_template("result.html", total_value=total_value, string_data=string_data, plane=plane)

@app.post("/predict")
def predict():
    from chat import get_response
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)
