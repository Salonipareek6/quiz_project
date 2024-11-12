import random
import streamlit as st
from PIL import Image
import os

# Categories and words
word_categories = {
    "Fruits": ["apple", "banana", "kiwi", "strawberry", "mango", "lemon", "dragonfruit", "grapes", "watermelon", "cherry"],
    "Colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "gray"],
    "Vegetables": ["carrot", "broccoli", "spinach", "pepper", "onion", "potato", "tomato", "pea", "pumpkin"],
    "Animals": ["cat", "dog", "elephant", "tiger", "lion", "giraffe", "zebra", "rabbit", "bear", "wolf"],
    "Birds": ["eagle", "parrot", "sparrow", "penguin", "owl", "pigeon", "peacock", "flamingo"],
    "Insects": ["bee", "ant", "butterfly", "ladybug", "dragonfly", "grasshopper", "mosquito", "spider", "cockroach", "grasshopper"],
    "Sports": ["football", "basketball", "tennis", "volleyball", "cricket", "hockey", "baseball", "archery", "swimming"],
    "Vehicles": ["car", "bus", "bicycle", "motorcycle", "train", "airplane", "ship", "helicopter", "scooter", "truck"]
}

image_folder = "path_to_images"  # Update with your images folder path

# Initialize or reset session states
if 'word' not in st.session_state:
    st.session_state['word'] = ""
if 'guesses' not in st.session_state:
    st.session_state['guesses'] = ""
if 'turns' not in st.session_state:
    st.session_state['turns'] = 5
if 'name' not in st.session_state:
    st.session_state['name'] = ""
if 'displayed_word' not in st.session_state:
    st.session_state['displayed_word'] = ""

# Function to reset game
def reset_game():
    st.session_state['word'] = ""
    st.session_state['guesses'] = ""
    st.session_state['turns'] = 5
    st.session_state['name'] = ""
    st.session_state['displayed_word'] = ""

# Start game function
def start_game():
    st.session_state['name'] = st.text_input("Enter your name", key="name")
    category = st.selectbox("Choose a category:", list(word_categories.keys()), key="category")
    st.session_state['word'] = random.choice(word_categories[category])
    st.session_state['guesses'] = ""
    st.session_state['turns'] = 5
    st.session_state['displayed_word'] = "_ " * len(st.session_state['word'])
    st.write(f"Hello, {st.session_state['name']}! Let’s start the game.")
    show_image_hint()

# Display image hint function
def show_image_hint():
    word_image = f"{st.session_state['word']}.jpg"
    image_path = os.path.join(image_folder, word_image)
    if os.path.exists(image_path):
        img = Image.open(image_path)
        st.image(img, caption="Hint Image", width=200)
    else:
        st.warning("No hint image available for this word.")

# Make guess function
def make_guess(guess):
    guess = guess.lower()
    if guess in st.session_state['guesses']:
        st.info("You already guessed that letter.")
    elif len(guess) == 1 and guess.isalpha():
        st.session_state['guesses'] += guess
        if guess not in st.session_state['word']:
            st.session_state['turns'] -= 1
            st.info(f"'{guess}' is not in the word.")
    update_display()

# Update display
def update_display():
    st.session_state['displayed_word'] = " ".join(char if char in st.session_state['guesses'] else "_" for char in st.session_state['word'])
    st.write("Word to guess:", st.session_state['displayed_word'])
    st.write("Turns left:", st.session_state['turns'])
    st.write("Guessed letters:", ", ".join(st.session_state['guesses']))

    if "_" not in st.session_state['displayed_word']:
        st.success(f"Congratulations! You guessed the word: '{st.session_state['word']}'")
        reset_game()
    elif st.session_state['turns'] == 0:
        st.error(f"Game Over! The word was: '{st.session_state['word']}'")
        reset_game()

# Streamlit app UI
st.title("Word Guessing Game for KIDS")

if st.button("Start New Game"):
    start_game()

if st.session_state['word']:
    guess = st.text_input("Enter a letter to guess", max_chars=1, key="guess")
    if st.button("Submit Guess"):
        make_guess(guess)

update_display()
