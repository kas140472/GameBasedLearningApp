from flask import Flask, render_template, request, redirect, url_for, session
from flask import jsonify

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Replace with your actual secret_key

users = {}  # Dictionary to store user profiles


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        users[name] = {'points': 0, 'modules': []}
        return redirect(url_for('profile'))
    return render_template('index.html')

# Change the leaderboard route to serve JSON data
@app.route('/leaderboard')
def leaderboard_json():
    sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)
    return jsonify([{'name': name, 'points': user_data['points']} for name, user_data in sorted_users])

@app.route('/profile')
def profile():
    name = session.get('name')
    if not name:
        return redirect(url_for('index'))
    user_data = users.get(name, {})
    return render_template('profile.html', name=name, user_data=user_data)

@app.route('/module1', methods=['GET', 'POST'])
def module1():
    if request.method == 'POST':
        return redirect(url_for('game'))
    return render_template('module1.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        name = session.get('name')
        if not name:
            return redirect(url_for('index'))

        # Handle coordinate input
        user_input_x = request.form.get('input_x', type=int)
        user_input_y = request.form.get('input_y', type=int)
        feedback, points, show_second_field = check_guess(user_input_x, user_input_y)
        
        if show_second_field:
            # Handle the answer input
            answer = request.form.get('answer')
            if answer == 'print("Hello World")':
                users[name]['points'] += 20
                feedback = "Congratulations! You've completed level 1 and earned 20 points!"
            else:
                feedback = "Incorrect answer. Please try again."
            return render_template('game.html', feedback=feedback, show_second_field=True)

        # Update points and feedback
        if name:
            users[name]['points'] += points
        
        return render_template('game.html', feedback=feedback)
    return render_template('game.html')

def check_guess(x, y):
    correct_positions = [(0, 0), (1, 1), (2, 2), (3, 3)]
    clues = {
        (0, 0): "Jiraiya: Oh! you found me, okay let's learn how to display 'Hello World'. For that we should use 'print' statement. Now find where Kakashi sensei is in the image",
        (1, 1): "Kakashi: Hmm we have to use print statement with a bracket like this 'print()'. Now find Itachi from the image",
        (2, 2): "Itachi: You have to use \"\" inside the round bracket. The problem is to print 'Hello World' using the above clues. Solve the problem and win your Haki",
        (3, 3): "You've found the final clue! Enter the correct print statement below to complete level 1."
    }
    if (x, y) in correct_positions:
        feedback = clues[(x, y)]
        show_second_field = (x, y) == (3, 3)
        return feedback, 10, show_second_field
    else:
        return "Wrong location", 0, False

@app.route('/image')
def image():
    pic1_path = url_for('static', filename='pic1.jpeg')
    return render_template('image.html', pic1_path=pic1_path)


if __name__ == '__main__':
    app.run(debug=True)
