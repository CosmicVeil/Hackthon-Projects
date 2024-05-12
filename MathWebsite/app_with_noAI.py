# Import necessary modules from Flask for building web applications and handling HTTP requests and responses.
from flask import Flask, render_template, request, jsonify
# Import the OpenAI library for accessing the OpenAI API.
import openai
import random


# Old dictionary with solutions which we convert to be more readable
old_solution_dict = {
    "x^2 + 5x + 6 = 0": "x=-2,-3",
    "x^2 + 6x + 5 = 0": "x=-1,-5",
    "2x^2 - 12x + 16 = 0": "x=4,2",
    "3x^2 + 16x + 20 = 0": "x=-2/3,-10",
    "5x^2 - 23x + 12 = 0": "x=12/5,1",
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
    "2x^2 - 8x + 8 = 0": "x=2",
    "3x^2 + 6x - 9 = 0": "x=1,-3",
    "x^2 - 15x + 54 = 0": "x=9,6",
    "4x^2 - 12x - 16 = 0": "x=4,-1",
    "5x^2 + 25x + 30 = 0": "x=-3,-2",
    "Solve the system: x + y = 2\nx - y = 0": "x=1, y=1",
    "Solve the system: 2x + 3y = 5\n4x - y = 3": "x=2, y=-1",
    "Solve the system: x - 2y = 1\n3x + 4y = 7": "x=3, y=1",
    "Solve the system: 5x + 2y = 4\nx + y = 1": "x=0, y=1",
    "Solve the system: x + 3y = 6\n2x - y = 1": "x=2, y=2",
    "Solve the system: 3x - y = 2\nx + 4y = 8": "x=3, y=1",
    "Solve the system: 2x + y = 20\n3x - 2y = 5": "x=10, y=0",
    "Solve the system: x + 2y = 4\n2x - 3y = 6": "x=6, y=-1",
    "Solve the system: 4x + y = 7\nx - 2y = 1": "x=2, y=3",
    "Solve the system: 3x + 3y = 9\nx - y = 1": "x=3, y=2",
    "Solve the system: 2x - 2y = 2\n5x + y = 11": "x=2, y=1",
    "Solve the system: x - y = 0\nx + y = 10": "x=5, y=5",
    "Solve the system: 6x - 3y = 12\n4x + 8y = 16": "x=4, y=2",
    "Solve the system: x + 5y = 10\n2x - y = 0": "x=2.5, y=1.5",
    "Solve the system: 3x + 2y = 6\nx - 4y = 10": "x=4, y=-1",
    "Solve the system: 4x + 4y = 8\n2x - 2y = 2": "x=2, y=1",
    "Solve the system: 5x - 5y = 10\nx + y = 2": "x=3, y=-1",
    "Solve the system: x + y = 3\n2x + 2y = 6": "x=1.5, y=1.5",
    "Solve the system: 2x + 2y = 8\n3x - y = 3": "x=3, y=1",
    "Solve the system: 4x - y = 1\nx + 3y = 9": "x=3, y=2",
    "Solve the system: 3x - 3y = 6\nx + 2y = 4": "x=3, y=0.5",
    "Solve the system: x - 2y = 0\n2x + 4y = 8": "x=4, y=2",
    "Solve the system: 4x + 2y = 12\nx - y = 1": "x=3, y=2",
    "Solve the system: 3x + y = 5\n5x - 2y = 10": "x=2, y=1",
    "Solve the system: x + 4y = 8\n2x + 3y = 10": "x=4, y=1",
    "Find the derivative: f(x) = x^2": "f'(x) = 2x",
    "Find the derivative: f(x) = 3x^3": "f'(x) = 9x^2",
    "Find the derivative: f(x) = 4x": "f'(x) = 4",
    "Find the derivative: f(x) = 5x^5": "f'(x) = 25x^4",
    "Find the derivative: f(x) = 6x^2 + 3x": "f'(x) = 12x + 3",
    "Find the derivative: f(x) = 7x^4 - x^2": "f'(x) = 28x^3 - 2x",
    "Find the derivative: f(x) = 8x^3 + 2x^2": "f'(x) = 24x^2 + 4x",
    "Find the derivative: f(x) = sin(x)": "f'(x) = cos(x)",
    "Find the derivative: f(x) = cos(x)": "f'(x) = -sin(x)",
    "Find the derivative: f(x) = e^x": "f'(x) = e^x",
    "Find the derivative: f(x) = ln(x)": "f'(x) = 1/x",
    "Find the derivative: f(x) = tan(x)": "f'(x) = sec^2(x)",
    "Find the derivative: f(x) = sec(x)": "f'(x) = sec(x)tan(x)",
    "Find the derivative: f(x) = csc(x)": "f'(x) = -csc(x)cot(x)",
    "Find the derivative: f(x) = cot(x)": "f'(x) = -csc^2(x)",
    "Find the derivative: f(x) = sqrt(x)": "f'(x) = 1/(2sqrt(x))",
    "Find the derivative: f(x) = 1/x": "f'(x) = -1/x^2",
    "Find the derivative: f(x) = x^(-2)": "f'(x) = -2x^(-3)",
    "Find the derivative: f(x) = 3x^2 + 5x - 2": "f'(x) = 6x + 5",
    "Find the derivative: f(x) = 4x^3 - 3x + 6": "f'(x) = 12x^2 - 3",
    "Find the derivative: f(x) = 5x^4 + 10x^3 - x": "f'(x) = 20x^3 + 30x^2 - 1",
    "Find the derivative: f(x) = 6x^5 - 4x^3 + 2x - 1": "f'(x) = 30x^4 - 12x^2 + 2",
    "Find the derivative: f(x) = e^(2x)": "f'(x) = 2e^(2x)",
    "Find the derivative: f(x) = x^2 * ln(x)": "f'(x) = 2x*ln(x) + x",
    "Find the derivative: f(x) = (x^3 + 1) / (x^2 - 1)": "f'(x) = ((3x^2)(x^2 - 1) - (x^3 + 1)(2x)) / (x^2 - 1)^2"
}
solution_dict = {}

# Converting to make it more readable
for val in old_solution_dict:
    new_val = val.replace("\n",", ")
    solution_dict[new_val] = old_solution_dict[val]

# Lists of different topics and the questions
quadratics = ["x^2 + 5x + 6 = 0", "x^2 + 6x + 5 = 0", "2x^2 - 12x + 16 = 0", "3x^2 + 16x + 20 = 0", "5x^2 - 23x + 12 = 0", "x^2 + 6x + 5 = 0",
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
    "5x^2 + 25x + 30 = 0",
]
basicOperations = ["1+1","2+2","3+3","4+4","5+5"]
linear_systems = [
    "Solve the system: x + y = 2\nx - y = 0",
    "Solve the system: 2x + 3y = 5\n4x - y = 3",
    "Solve the system: x - 2y = 1\n3x + 4y = 7",
    "Solve the system: 5x + 2y = 4\nx + y = 1",
    "Solve the system: x + 3y = 6\n2x - y = 1",
    "Solve the system: 3x - y = 2\nx + 4y = 8",
    "Solve the system: 2x + y = 20\n3x - 2y = 5",
    "Solve the system: x + 2y = 4\n2x - 3y = 6",
    "Solve the system: 4x + y = 7\nx - 2y = 1",
    "Solve the system: 3x + 3y = 9\nx - y = 1",
    "Solve the system: 2x - 2y = 2\n5x + y = 11",
    "Solve the system: x - y = 0\nx + y = 10",
    "Solve the system: 6x - 3y = 12\n4x + 8y = 16",
    "Solve the system: x + 5y = 10\n2x - y = 0",
    "Solve the system: 3x + 2y = 6\nx - 4y = 10",
    "Solve the system: 4x + 4y = 8\n2x - 2y = 2",
    "Solve the system: 5x - 5y = 10\nx + y = 2",
    "Solve the system: x + y = 3\n2x + 2y = 6",
    "Solve the system: 2x + 2y = 8\n3x - y = 3",
    "Solve the system: 4x - y = 1\nx + 3y = 9",
    "Solve the system: 3x - 3y = 6\nx + 2y = 4",
    "Solve the system: x - 2y = 0\n2x + 4y = 8",
    "Solve the system: 4x + 2y = 12\nx - y = 1",
    "Solve the system: 3x + y = 5\n5x - 2y = 10",
    "Solve the system: x + 4y = 8\n2x + 3y = 10"
]
derivatives = [
    "Find the derivative: f(x) = x^2",
    "Find the derivative: f(x) = 3x^3",
    "Find the derivative: f(x) = 4x",
    "Find the derivative: f(x) = 5x^5",
    "Find the derivative: f(x) = 6x^2 + 3x",
    "Find the derivative: f(x) = 7x^4 - x^2",
    "Find the derivative: f(x) = 8x^3 + 2x^2",
    "Find the derivative: f(x) = sin(x)",
    "Find the derivative: f(x) = cos(x)",
    "Find the derivative: f(x) = e^x",
    "Find the derivative: f(x) = ln(x)",
    "Find the derivative: f(x) = tan(x)",
    "Find the derivative: f(x) = sec(x)",
    "Find the derivative: f(x) = csc(x)",
    "Find the derivative: f(x) = cot(x)",
    "Find the derivative: f(x) = sqrt(x)",
    "Find the derivative: f(x) = 1/x",
    "Find the derivative: f(x) = x^(-2)",
    "Find the derivative: f(x) = 3x^2 + 5x - 2",
    "Find the derivative: f(x) = 4x^3 - 3x + 6",
    "Find the derivative: f(x) = 5x^4 + 10x^3 - x",
    "Find the derivative: f(x) = 6x^5 - 4x^3 + 2x - 1",
    "Find the derivative: f(x) = e^(2x)",
    "Find the derivative: f(x) = x^2 * ln(x)",
    "Find the derivative: f(x) = (x^3 + 1) / (x^2 - 1)"
]

app = Flask(__name__)# Initialize a Flask application.

openai.api_key = 'sk-proj-0lxWLZ0arP8k1r7eg54lT3BlbkFJMnuSkYQa2iRR5dGYABXc'# Set the OpenAI API key to authenticate requests.



@app.route('/')
def home():
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

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>  (REMEMBER THE REQUEST FORM IS FROM THE ID ONLY)

        difficulty = int(request.form['difficulty_level'])

        questions = generate_questions(topic, num_questions, difficulty)# Generate questions using the generate_questions function.


        return render_template('math.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('math.html', questions=[])# Render the index.html template with an empty list of questions.


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

    # Based on the topic, return a list of questions in that topic

    # All the lists with C's in front of them are copies of the OG lists, where we remove vals already chosen
    # This keeps all questions given to the user unique
    if topic.lower() == "basic math":
        return basicOperations
    elif topic.lower() == "quadratics":
        questions = []

        c_quadratics = quadratics[:]
        for _ in range(num_questions):
            option = random.choice(c_quadratics)
            questions.append(option)
            c_quadratics.remove(option)

    elif topic.lower() == "linear systems":
        questions = []
        c_linear = linear_systems[:]
        for _ in range(num_questions):
            option = random.choice(c_linear)
            c_linear.remove(option)
            option = option.replace('\n', ", ")
            questions.append(option)
    elif topic.lower() == "derivatives":
        questions = []
        c_deriv = derivatives[:]
        for _ in range(num_questions):
            option = random.choice(c_deriv)
            questions.append(option)
            c_deriv.remove(option)
            
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
