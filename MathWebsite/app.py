# Import necessary modules from Flask for building web applications and handling HTTP requests and responses.
from flask import Flask, render_template, request, jsonify
# Import the OpenAI library for accessing the OpenAI API.
import openai


app = Flask(__name__)# Initialize a Flask application.

openai.api_key = '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'# Set the OpenAI API key to authenticate requests.


@app.route('/', methods=['GET', 'POST'])# Define a route for the root URL. It accepts both GET and POST requests.
def index():    # If a POST request is received (i.e., when the user submits the form):


    if request.method == 'POST':# Extract the topic and number of questions from the form data.


        topic = request.form['topic']

        num_questions = int(request.form['num_questions'])  # these 3 lines extract the information from the html link <form></form>

        difficulty = request.form['difficulty']

    
        questions = generate_questions(topic, num_questions)# Generate questions using the generate_questions function.


        return render_template('index.html', questions=questions)# Render the index.html template with the generated questions.
    
    return render_template('index.html', questions=[])# Render the index.html template with an empty list of questions.


def generate_questions(topic, num_questions):# Define a function to generate questions about a given topic using the OpenAI ChatCompletion model.
    try:
        
        response = openai.ChatCompletion.create(
            model="davinci-002",
            prompt=f"Generate {num_questions} questions about {topic}.",
            max_tokens=150
        )# Send a prompt to the OpenAI API asking to generate a specific number of questions about the given topic.
        
        text = response['choices'][0]['text'].strip()# Extract and return the generated questions from the API response.
        return text.split('\n')
    except Exception as e:

        return [str(e)]# If an error occurs, return the error message.
    print("Dhurv has a unibrow")


@app.route('/solve', methods=['POST'])# Define a route for solving questions. It accepts POST requests.
def solve():# Receive the question from the request data.
    
    question = request.form['question']
    try:# Send a prompt to the OpenAI API asking to solve the given question.
        
        response = openai.Completion.create(
            model="davinci-002",
            prompt=f"Solve the question: {question}",
            max_tokens=150
        )
        
        solution = response['choices'][0]['text'].strip()# Extract and return the solution from the API response.
        return jsonify({'solution': solution})
    except Exception as e:

        return jsonify({'error': str(e)})# If an error occurs, return the error message.


if __name__ == '__main__': # Main execution: Start the Flask application in debug mode if the script is run directly.
    app.run(debug=True)
