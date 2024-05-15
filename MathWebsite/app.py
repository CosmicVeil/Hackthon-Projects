# Import necessary modules from Flask for building web applications and handling HTTP requests and responses.
from flask import Flask, render_template, request, jsonify
# Import the OpenAI library for accessing the OpenAI API.
from openai import OpenAI
client = OpenAI(api_key='GET KEY FROM DISCORD')


app = Flask(__name__)# Initialize a Flask application.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/biology.html')
def english():
    return render_template('biology.html')

@app.route('/physics.html')
def physics():
    return render_template('physics.html')


@app.route('/chemistry.html')
def chemistry():
    return render_template('chemistry.html')

@app.route('/math.html', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def math():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions(topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('math.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('math.html', questions=[])# Render the index.html template with an empty list of questions.

@app.route('/biology.html', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def bio():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = int(request.form['difficulty_level'])

    
        questions = generate_questions(topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('biology.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('biology.html', questions=[])# Render the index.html template with an empty list of questions.

def generate_questions(topic, num_questions, difficulty):# Define a function to generate questions about a given topic using the OpenAI ChatCompletion model.
    try:
        
        response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "user", "content": f"Create {num_questions} questions about {topic} with grade {difficulty} difficulty. Remove most fluff, and each question should be on a new line. note that we are on python, so special character wont work. "}
  ])
        print(difficulty)
# Send a prompt to the OpenAI API asking to generate a specific number of questions about the given topic.
        
        text = response.choices[0].message.content# Extract and return the generated questions from the API response.
        return text.split('\n')
    except Exception as e:

        return [str(e)]# If an error occurs, return the error message.
    print("DHruv has a unibrow")


@app.route('/solve', methods=['POST'])# Define a route for solving questions. It accepts POST requests.
def solve():# Receive the question from the request data.
    
    data = request.json
    question = data["question"]
    try:# Send a prompt to the OpenAI API asking to solve the given question.
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": f"Create a answer to the question {question}, and show your steps. note that we are on python, so special characters such as \\ or () wont work."}
            ])
        
        solution = response.choices[0].message.content# Extract and return the solution from the API response.
        return jsonify({'solution': solution})
    except Exception as e:

        return jsonify({'error': str(e)})# If an error occurs, return the error message.


if __name__ == '__main__': # Main execution: Start the Flask application in debug mode if the script is run directly.
    app.run(debug=True)
