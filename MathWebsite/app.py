from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = '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'
difficulty_counter=3

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        num_questions = int(request.form['num_questions'])
        questions = generate_questions(topic, num_questions)
        return render_template('index.html', questions=questions)
    return render_template('index.html', questions=[])

def generate_questions(topic, num_questions):
    try:
        response = openai.ChatCompletion.create(
            model="davinci-002",
            prompt=f"Generate {num_questions} questions about {topic}. Make them {difficulty_calc()}",
            max_tokens=150
        )
        text = response['choices'][0]['text'].strip()
        return text.split('\n')
    except Exception as e:
        return [str(e)]

@app.route('/solve', methods=['POST'])
def solve():
    question = request.form['question']
    try:
        response = openai.Completion.create(
            model="davinci-002",
            prompt=f"Solve the question: {question}",
            max_tokens=150
        )
        solution = response['choices'][0]['text'].strip()
        return jsonify({'solution': solution})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/feedback', methods=['POST'])
def feedback():
    global difficulty_counter  # Use the global counter
    data = request.json
    if data['difficulty'] == 'hard':
        difficulty_counter -= 1  # Decrease counter if question was too hard
    elif data['difficulty'] == 'easy':
        difficulty_counter += 1  # Increase counter if question was too easy
    # print(f"Received feedback: {data['question']} is {data['difficulty']}")
    # print(f"Current difficulty counter: {difficulty_counter}")
    return jsonify({'status': 'success', 'message': 'Feedback received'})

def difficulty_calc():
    global difficulty_counter

    if difficulty_counter >= 1:
        return "very easy"
    elif difficulty_counter ==2:
        return "easy"
    elif difficulty_counter == 3:
        return "normal difficulty"
    elif difficulty_counter == 4:
        return "hard"
    else:
        return "very hard"


if __name__ == '__main__':
    app.run(debug=True)
