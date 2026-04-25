import dash
from dash import html, dcc, Input, Output, State
import random

app = dash.Dash(__name__)
server = app.server

# ===== GLOBAL STATE (simple demo) =====
xp = 0
level = 1
streak = 0
score = 0

def generate_math(diff):
    if diff == "Easy":
        a, b = random.randint(0, 10), random.randint(0, 10)
    elif diff == "Medium":
        a, b = random.randint(10, 50), random.randint(10, 50)
    else:
        a, b = random.randint(50, 100), random.randint(1, 50)
    op = random.choice(["+", "-", "*"])
    return f"{a} {op} {b}", eval(f"{a}{op}{b}")

def generate_word():
    words = [
        {"hint": "Animal that says meow", "answer": "cat"},
        {"hint": "Animal that barks", "answer": "dog"},
        {"hint": "Yellow fruit", "answer": "banana"},
        {"hint": "Vehicle with 4 wheels", "answer": "car"},
    ]
    return random.choice(words)

# ===== INITIAL =====
question, answer = generate_math("Easy")
word = generate_word()

# ===== UI =====
app.layout = html.Div([
    html.H1("🎮 FunLearn Pro", style={"textAlign": "center"}),

    html.Div([
        html.Div(id="level", children="Level: 1", className="card"),
        html.Div(id="xp", children="XP: 0", className="card"),
        html.Div(id="streak", children="Streak: 0", className="card"),
    ], style={"display": "flex", "justifyContent": "space-around"}),

    html.Br(),

    dcc.Dropdown(["Math", "Vocabulary", "Mixed"], "Math", id="mode"),
    dcc.Dropdown(["Easy", "Medium", "Hard"], "Easy", id="difficulty"),

    html.Div(id="question-box", className="card"),

    dcc.Input(id="user-input", placeholder="Your answer...", type="text"),
    html.Button("Submit", id="submit"),

    html.Div(id="feedback"),
    html.Div(id="score-display"),

], style={"width": "50%", "margin": "auto"})

# ===== CALLBACK =====
@app.callback(
    Output("question-box", "children"),
    Output("feedback", "children"),
    Output("score-display", "children"),
    Output("level", "children"),
    Output("xp", "children"),
    Output("streak", "children"),
    Input("submit", "n_clicks"),
    State("user-input", "value"),
    State("mode", "value"),
    State("difficulty", "value"),
)
def update(n, user_input, mode, difficulty):
    global xp, level, streak, score, question, answer, word

    if n is None:
        return f"Question: {question}", "", "", f"Level: {level}", f"XP: {xp}", f"Streak: {streak}"

    feedback = ""

    # ===== CHECK ANSWER =====
    if mode == "Math":
        if str(user_input) == str(answer):
            feedback = "✅ Correct!"
            score += 1
            streak += 1
            xp += 10
        else:
            feedback = f"❌ Wrong! Answer: {answer}"
            streak = 0

    elif mode == "Vocabulary":
        if user_input and user_input.lower() == word["answer"]:
            feedback = "✅ Correct!"
            score += 1
            streak += 1
            xp += 10
        else:
            feedback = f"❌ Wrong! Answer: {word['answer']}"
            streak = 0

    else:  # Mixed
        if random.random() > 0.5:
            if str(user_input) == str(answer):
                feedback = "✅ Correct!"
                xp += 10
                streak += 1
            else:
                feedback = f"❌ Wrong! {answer}"
                streak = 0
        else:
            if user_input and user_input.lower() == word["answer"]:
                feedback = "✅ Correct!"
                xp += 10
                streak += 1
            else:
                feedback = f"❌ Wrong! {word['answer']}"
                streak = 0

    # ===== LEVEL UP =====
    if xp >= level * 100:
        level += 1

    # ===== NEW QUESTION =====
    if mode == "Math":
        question, answer = generate_math(difficulty)
        display = f"{question} = ?"
    elif mode == "Vocabulary":
        word = generate_word()
        display = f"Hint: {word['hint']}"
    else:
        if random.random() > 0.5:
            question, answer = generate_math(difficulty)
            display = f"{question} = ?"
        else:
            word = generate_word()
            display = f"Hint: {word['hint']}"

    return (
        display,
        feedback,
        f"Score: {score}",
        f"Level: {level}",
        f"XP: {xp}",
        f"Streak: {streak}",
    )

# ===== CSS (inline) =====
app.index_string = """
<!DOCTYPE html>
<html>
<head>
    <title>FunLearn Pro</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(to right, #ffecd2, #fcb69f);
        }
        .card {
            background: white;
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
    </footer>
</body>
</html>
"""

# ===== RUN =====
if __name__ == "__main__":
    app.run(debug=True)
