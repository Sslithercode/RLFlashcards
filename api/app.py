from flask import Flask, request
from flask_jwt_extended import create_access_token, JWTManager, jwt_required,unset_jwt_cookies,get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas
import numpy  as np
import datetime

print(sqlalchemy.__version__)
print(flask_sqlalchemy.__version__)

df  = pandas.read_csv("capitals.csv")
countries    = df["country"]
capitals = df["capital"]




selected_flashcards =  {}
for country , capital in zip(countries[:10],capitals[:10]):
    selected_flashcards[country] =  capital

    


class  QLearn:
    def __init__(self):
        self.flashcards = selected_flashcards
        self.num_flashcards = len(self.flashcards)
        self.flashcard_counts =  {c:0 for c in self.flashcards}
        self.episode  = 0 
        self.correct = 0
        self.q_table = np.zeros((self.num_flashcards, self.num_flashcards))
        self.learning_rate = 0.1
        self.discount_factor = 0.99
        self.exploration_rate = 1.0
        self.exploration_decay = 0.1
        self.current_flashcard = np.random.choice(self.num_flashcards)

    def  next_flashcard(self,reward):
        self.episode +=1 
        # Update Q value 
        action = np.argmax(self.q_table[self.current_flashcard])
        self.q_table[self.current_flashcard, action] += self.learning_rate * (reward + self.discount_factor * np.max(self.q_table[action]) - self.q_table[self.current_flashcard, action])

        # update parameter
        self.exploration_rate *= 1 - self.exploration_decay

        #  epsilon-greedy policy
        if np.random.random() < self.exploration_rate:
            self.current_flashcard = np.random.choice(self.num_flashcards)
        else:
            self.current_flashcard = np.argmax(self.q_table[self.current_flashcard])

q_agent  =  QLearn()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '234a32ij49#$**RY$#(R() $#OHR)$#RH#$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

agents =  {}



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

db.create_all()


@app.route("/validate_token",methods=['POST'])
@jwt_required()
def validate_token():
    return {"valid":True},200

@app.route("/logout", methods=["POST"])
def logout():
    response = {"msg": "logout successful"}
    unset_jwt_cookies(response)
    return response

@jwt.unauthorized_loader
def unauthorized_response(error):
    return{
        'message': 'You are not authorized to access this resource'
    },401

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {'message': 'Invalid username or password'}, 401
    
    access_token = create_access_token(identity=user.id,expires_delta=datetime.timedelta(hours=10))
    return {'access_token': access_token}, 200


@app.route('/register', methods=['POST'])
def register():
    body   = request.get_json()
    req_username =  body['username']
    req_password =  body['password']

    if not req_username or not req_password:
        return {'message': 'Username and password are required'}, 400
    if User.query.filter_by(username=req_username).first():
        return {'message': 'Username already taken'}, 400
    user = User(username=req_username)
    user.set_password(req_password)
    db.session.add(user)
    db.session.commit()
    return {'message': 'User created successfully'}

@app.route("/flashcard/generate_question",methods=["GET"])
@jwt_required()
def generate_question():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if(user.username in agents):
        q_agent = agents[user.username]
    else:
        agents[user.username] = QLearn()
        q_agent = agents[user.username]

    current_question, current_answer = list(q_agent.flashcards.items())[q_agent.current_flashcard]
    return {"question": current_question , "answer":current_answer}
  
    

@app.route("/flashcard/recv_answer",methods=["POST"])
@jwt_required()
def recv_answer():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    body  =  request.get_json()
    usr_answer  =  body['user_answer']
    question  = body['question']
    correct_answer   = body['correct_answer']
    if usr_answer  == correct_answer:
        correct  = True
        reward =  -1

    else:
        correct = False 
        reward = 2 

    q_agent  = agents[user.username]

    q_agent.next_flashcard(reward)
    print(f""" 
    user: {user.username}
    Episode:  {q_agent.episode}
    q value: {q_agent.q_table[q_agent.current_flashcard]}
    Exploration Rate: {q_agent.exploration_rate}
    Average Accuracy: {round((q_agent.correct/q_agent.episode)*100)}%

    
    """)


    #selected_card = agent.flashcards[datahandler.get_var("selected_card_index")]
    #correct , avg_score  = agent.check_answer(usr_answer,selected_card)
    return {"correct":correct,"answer":correct_answer}
    



    



if __name__ == "__main__":
    app.run(debug=True)
