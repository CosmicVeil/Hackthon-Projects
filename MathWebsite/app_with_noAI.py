# Import necessary modules from Flask for building web applications and handling HTTP requests and responses.
from flask import Flask, render_template, request, jsonify
# Import the OpenAI library for accessing the OpenAI API.
import openai
import random

solution_dict = {
    "Solve x^2+5x+6=0": "x=-2,-3",
    "Solve x^2+6x+5=0": "x=-1,-5",
    "Solve 2x^2-12x+16=0": "x=4,2",
    "Solve 3x^2+16x+20=0": "x=-2/3,-10",
    "Solve 5x^2-23x+12=0": "x=12/5,1",
    "x^2 + 6x + 5 = 0": "x=-1,-5",
    "x^2 - 3x - 4 = 0": "x=4,-1",
    "2x^2 + 8x + 6 = 0": "x=-1,-3",
    "x^2 - 5x + 6 = 0": "x=2,3",
    "3x^2 - 6x - 9 = 0": "x=3,-1",
    "x^2 + 2x - 8 = 0": "x=2,-4",
    "x^2 - 7x + 12 = 0": "x=3,4",
    "4x^2 + 16x + 15 = 0": "x=-3/4,-5",
    "x^2 - 8x + 15 = 0": "x=5,3",
    "5x^2 + 5x - 30 = 0": "x=3,-2",
    "x^2 - 4x - 21 = 0": "x=7,-3",
    "x^2 + 10x + 25 = 0": "x=-5",
    "6x^2 - 12x - 18 = 0": "x=3,-1",
    "x^2 - 9x + 20 = 0": "x=5,4",
    "2x^2 - 2x - 4 = 0": "x=2,-1",
    "x^2 + x - 20 = 0": "x=4,-5",
    "3x^2 + 3x - 18 = 0": "x=3,-2",
    "x^2 - 10x + 25 = 0": "x=5",
    "4x^2 - 8x - 32 = 0": "x=4,-2",
    "x^2 + 3x - 18 = 0": "x=3,-6",
    "2x^2 + 4x - 16 = 0": "x=2,-4",
    "x^2 - 11x + 30 = 0": "x=6,5",
    "3x^2 + 12x + 12 = 0": "x=-2",
    "x^2 - 6x + 8 = 0": "x=4,2",
    "5x^2 - 15x - 50 = 0": "x=10,-1",
    "x^2 + 4x - 32 = 0": "x=4,-8",
    "2x^2 - 10x + 12 = 0": "x=3,2",
    "3x^2 - 9x + 6 = 0": "x=2,1",
    "x^2 - 2x - 15 = 0": "x=5,-3",
    "4x^2 + 20x + 25 = 0": "x=-5/2",
    "x^2 - 12x + 36 = 0": "x=6",
    "5x^2 + 20x + 15 = 0": "x=-1,-3",
    "x^2 + 5x - 14 = 0": "x=2,-7",
    "2x^2 - 4x - 6 = 0": "x=3,-1",
    "3x^2 + 9x - 30 = 0": "x=3,-10/3",
    "x^2 + 7x + 10 = 0": "x=-2,-5",
    "4x^2 - 16x + 15 = 0": "x=5/4,3",
    "x^2 - 13x + 42 = 0": "x=6,7",
    "5x^2 - 10x - 75 = 0": "x=5,-3",
    "x^2 + 8x + 16 = 0": "x=-4",
    "2x^2 + 10x + 12 = 0": "x=-2,-3",
    "3x^2 - 15x - 18 = 0": "x=6,-1",
    "x^2 - 14x + 49 = 0": "x=7",
    "4x^2 + 4x - 32 = 0": "x=2,-4",
    "x^2 + 9x + 20 = 0": "x=-4,-5",
    "2x^2 - 8x + 8 = 0": "x=2,2",
    "3x^2 + 6x - 9 = 0": "x=1,-3",
    "x^2 - 15x + 54 = 0": "x=9,6",
    "4x^2 - 12x - 16 = 0": "x=4,-1",
    "5x^2 + 25x + 30 = 0": "x=-3,-2"
}

quadratics = ["Solve x^2+5x+6=0", "Solve x^2+6x+5=0", "Solve 2x^2-12x+16=0", "Solve 3x^2+16x+20=0", "Solve 5x^2-23x+12=0", "x^2 + 6x + 5 = 0",
    "x^2 - 3x - 4 = 0",
    "2x^2 + 8x + 6 = 0",
    "x^2 - 5x + 6 = 0",
    "3x^2 - 6x - 9 = 0",
    "x^2 + 2x - 8 = 0",
    "x^2 - 7x + 12 = 0",
    "4x^2 + 16x + 15 = 0",
    "x^2 - 8x + 15 = 0",
    "5x^2 + 5x - 30 = 0",
    "x^2 - 4x - 21 = 0",
    "x^2 + 10x + 25 = 0",
    "6x^2 - 12x - 18 = 0",
    "x^2 - 9x + 20 = 0",
    "2x^2 - 2x - 4 = 0",
    "x^2 + x - 20 = 0",
    "3x^2 + 3x - 18 = 0",
    "x^2 - 10x + 25 = 0",
    "4x^2 - 8x - 32 = 0",
    "x^2 + 3x - 18 = 0",
    "2x^2 + 4x - 16 = 0",
    "x^2 - 11x + 30 = 0",
    "3x^2 + 12x + 12 = 0",
    "x^2 - 6x + 8 = 0",
    "5x^2 - 15x - 50 = 0",
    "x^2 + 4x - 32 = 0",
    "2x^2 - 10x + 12 = 0",
    "3x^2 - 9x + 6 = 0",
    "x^2 - 2x - 15 = 0",
    "4x^2 + 20x + 25 = 0",
    "x^2 - 12x + 36 = 0",
    "5x^2 + 20x + 15 = 0",
    "x^2 + 5x - 14 = 0",
    "2x^2 - 4x - 6 = 0",
    "3x^2 + 9x - 30 = 0",
    "x^2 + 7x + 10 = 0",
    "4x^2 - 16x + 15 = 0",
    "x^2 - 13x + 42 = 0",
    "5x^2 - 10x - 75 = 0",
    "x^2 + 8x + 16 = 0",
    "2x^2 + 10x + 12 = 0",
    "3x^2 - 15x - 18 = 0",
    "x^2 - 14x + 49 = 0",
    "4x^2 + 4x - 32 = 0",
    "x^2 + 9x + 20 = 0",
    "2x^2 - 8x + 8 = 0",
    "3x^2 + 6x - 9 = 0",
    "x^2 - 15x + 54 = 0",
    "4x^2 - 12x - 16 = 0",
    "5x^2 + 25x + 30 = 0"
]
quadraticsAns = ["x=-3,-2", "x=-5,-1", "x=2,4", "x=-2,-10/3", "x=4,3/5"]
basicOperations = ["1+1","2+2","3+3","4+4","5+5"]
basicOperationsAns = ["2","4","6","8","10"]
linear_systems = []

app = Flask(__name__)# Initialize a Flask application.

openai.api_key = 'sk-proj-0lxWLZ0arP8k1r7eg54lT3BlbkFJMnuSkYQa2iRR5dGYABXc'# Set the OpenAI API key to authenticate requests.


@app.route('/', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def index():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = request.form['difficulty']

    
        questions = generate_questions(topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('index.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('index.html', questions=[])# Render the index.html template with an empty list of questions.


# def generate_questions(topic, num_questions, difficulty):# Define a function to generate questions about a given topic using the OpenAI ChatCompletion model.
#     try:
        
#         response = openai.ChatCompletion.create(
#             model="davinci-002",
#             prompt=f"Generate {num_questions} questions about {topic} with grade {difficulty} difficulty level",
#             max_tokens=150
#         )# Send a prompt to the OpenAI API asking to generate a specific number of questions about the given topic.
        
#         text = response['choices'][0]['text'].strip()# Extract and return the generated questions from the API response.
#         return text.split('\n')
#     except Exception as e:

#         return [str(e)]# If an error occurs, return the error message.
#     print("Dhurv has a unibrow")

def generate_questions(topic,num_questions,difficulty):
    if topic.lower() == "basic math":
        return basicOperations
    elif topic.lower() == "quadratics":
        questions = []
        for i in range(num_questions):
            questions.append(random.choice(quadratics))
    return questions

# Define a route for solving questions. It accepts POST requests.
# @app.route('/solve', methods=['POST'])
# def solve():# Receive the question from the request data.
    
#     question = request.form['question']
#     try:# Send a prompt to the OpenAI API asking to solve the given question.
        
#         response = openai.Completion.create(
#             model="davinci-002",
#             prompt=f"Solve the question: {question}",
#             max_tokens=150
#         )
        
#         solution = response['choices'][0]['text'].strip()# Extract and return the solution from the API response.
#         return jsonify({'solution': solution})
#     except Exception as e:

#         return jsonify({'error': str(e)})# If an error occurs, return the error message.
@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    question = data["question"]
    return jsonify({'solution': solution_dict[question]})


if __name__ == '__main__': # Main execution: Start the Flask application in debug mode if the script is run directly.
    app.run(debug=True)
