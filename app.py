import streamlit as st
import random

st.set_page_config(page_title="FunLearn Pro", page_icon="🎮")

st.title("🎮 FunLearn Pro")

# ===== SESSION STATE =====
if "xp" not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1
    st.session_state.streak = 0
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = ""
    st.session_state.answer = None
    st.session_state.word = None

# ===== FUNCTIONS =====
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

def new_question(mode, difficulty):
    if mode == "Math":
        q, a = generate_math(difficulty)
        st.session_state.question = q
        st.session_state.answer = a
        st.session_state.word = None
    elif mode == "Vocabulary":
        w = generate_word()
        st.session_state.word = w
        st.session_state.question = ""
    else:
        if random.random() > 0.5:
            q, a = generate_math(difficulty)
            st.session_state.question = q
            st.session_state.answer = a
            st.session_state.word = None
        else:
            w = generate_word()
            st.session_state.word = w
            st.session_state.question = ""

# ===== UI STATS =====
col1, col2, col3 = st.columns(3)
col1.metric("🏆 Level", st.session_state.level)
col2.metric("✨ XP", st.session_state.xp)
col3.metric("🔥 Streak", st.session_state.streak)

st.progress((st.session_state.xp % 100) / 100)

# ===== SETTINGS =====
mode = st.selectbox("Choose Mode", ["Math", "Vocabulary", "Mixed"])
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# ===== INIT QUESTION =====
if st.session_state.question == "" and st.session_state.word is None:
    new_question(mode, difficulty)

# ===== DISPLAY =====
if st.session_state.question:
    st.subheader("🧮 Math Challenge")
    st.write(f"{st.session_state.question} = ?")
    user_input = st.number_input("Your answer", step=1)

elif st.session_state.word:
    st.subheader("🔤 Vocabulary Challenge")
    st.write(f"Hint: {st.session_state.word['hint']}")
    user_input = st.text_input("Your answer")

# ===== SUBMIT =====
if st.button("Submit"):
    correct = False

    if st.session_state.question:
        if str(user_input) == str(st.session_state.answer):
            correct = True
    else:
        if user_input and user_input.lower() == st.session_state.word["answer"]:
            correct = True

    if correct:
        st.success("✅ Correct!")
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.xp += 10
    else:
        st.error("❌ Wrong!")
        st.session_state.streak = 0

    # LEVEL UP
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1
        st.balloons()

    new_question(mode, difficulty)

# ===== SCORE =====
st.write(f"🎯 Score: {st.session_state.score}")
