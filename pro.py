import streamlit as st
import random
import os
from PIL import Image

# Categories for words
word_categories = {
    "Fruits": ["apple", "banana", "kiwi", "strawberry", "mango", "lemon", "dragonfruit", "grapes", "watermelon", "cherry"],
    "Colors": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "gray"],
    "Vegetables": ["carrot", "broccoli", "spinach", "pepper", "onion", "potato", "tomato", "pea", "pumpkin"],
    "Animals": ["cat", "dog", "elephant", "tiger", "lion", "giraffe", "zebra", "rabbit", "bear", "wolf"],
    "Birds": ["eagle", "parrot", "sparrow", "penguin", "owl", "pigeon", "peacock", "flamingo"],
    "Insects": ["bee", "ant", "butterfly", "ladybug", "dragonfly", "grasshopper", "mosquito", "spider", "cockroach"],
    "Sports": ["football", "basketball", "tennis", "volleyball", "cricket", "hockey", "baseball", "archery", "swimming"],
    "Vehicles": ["car", "bus", "bicycle", "motorcycle", "train", "airplane", "ship", "helicopter", "scooter", "truck"]
}

# Define the path to the images folder
image_folder = "./images"

# Initialize session state variables
if 'name' not in st.session_state:
    st.session_state['name'] = ""
if 'category' not in st.session_state:
    st.session_state['category'] = list(word_categories.keys())[0]
if 'word' not in st.session_state:
    st.session_state['word'] = ""
if 'guesses' not in st.session_state:
    st.session_state['guesses'] = ""
if 'turns' not in st.session_state:
    st.session_state['turns'] = 5
if 'displayed_word' not in st.session_state:
    st.session_state['displayed_word'] = ""

# Start game logic
def start_game():
    st.session_state['name'] = st.text_input("Enter your name", value=st.session_state['name'])
    st.session_state['category'] = st.selectbox("Choose a category", options=list(word_categories.keys()), index=0)
    
    if st.button("Start Game"):
        st.session_state['word'] = random.choice(word_categories[st.session_state['category']])
        st.session_state['guesses'] = ""
        st.session_state['turns'] = 5
        st.session_state['displayed_word'] = "_ " * len(st.session_state['word'])

        # Show hint image if available
        show_image_hint()

# Function to display the hint image
def show_image_hint():
    image_path = os.path.join(image_folder, f"{st.session_state['word']}.jpg")
    if os.path.exists(image_path):
        st.image(image_path, caption="Hint", use_column_width=True)
    else:
        st.warning("No image hint available for this word.")

# Function to handle guesses
def make_guess():
    guess = st.text_input("Enter a letter to guess").lower()
    if st.button("Guess"):
        if len(guess) != 1 or not guess.isalpha():
            st.error("Please enter a single letter.")
            return
        if guess in st.session_state['guesses']:
            st.info("You already guessed that letter.")
            return

        st.session_state['guesses'] += guess
        if guess not in st.session_state['word']:
            st.session_state['turns'] -= 1
            st.info(f"'{guess}' is not in the word.")

        update_display()

# Function to update the word display
def update_display():
    displayed_word = " ".join(char if char in st.session_state['guesses'] else "_" for char in st.session_state['word'])
    st.session_state['displayed_word'] = displayed_word

    st.text(f"Word: {displayed_word}")
    st.text(f"Turns left: {st.session_state['turns']}")
    st.text(f"Guessed letters: {', '.join(st.session_state['guesses'])}")

    if "_" not in displayed_word:
        st.success(f"Congratulations, {st.session_state['name']}! You guessed the word '{st.session_state['word']}'!")
        reset_game()
    elif st.session_state['turns'] == 0:
        st.error(f"Game Over! The word was '{st.session_state['word']}'.")
        reset_game()

# Function to reset the game
def reset_game():
    st.session_state['word'] = ""
    st.session_state['guesses'] = ""
    st.session_state['turns'] = 5
    st.session_state['displayed_word'] = ""

# Main application
st.title("Word Guessing Game for Kids")
start_game()
if st.session_state['word']:
    make_guess()
    update_display()
