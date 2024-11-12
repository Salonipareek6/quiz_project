import random
import streamlit as st
from PIL import Image
import os
import time

# Word categories for guessing
word_categories = {
    "Fruits": [
        "apple", "banana", "kiwi", "strawberry", "mango",
        "lemon", "dragonfruit", "grapes", "watermelon", "cherry"
    ],
    "Colors": [
        "red", "blue", "green", "yellow", "purple",
        "orange", "pink", "black", "white", "gray"
    ],
    "Vegetables": [
        "carrot", "broccoli", "spinach", "pepper", "onion",
        "potato", "tomato", "pea", "pumpkin"
    ],
    "Animals": [
        "cat", "dog", "elephant", "tiger", "lion",
        "giraffe", "zebra", "rabbit", "bear", "wolf"
    ],
    "Birds": [
        "eagle", "parrot", "sparrow", "penguin", "owl",
        "pigeon", "peacock", "flamingo",
    ],
    "Insects": [
        "bee", "ant", "butterfly", "ladybug", "dragonfly",
        "grasshopper", "mosquito", "spider", "cockroach", "grasshopper"
    ],
    "Sports": [
        "football", "basketball", "tennis", "volleyball", "cricket",
        "hockey", "baseball", "archery", "swimming"
    ],
    "Vehicles": [
        "car", "bus", "bicycle", "motorcycle", "train",
        "airplane", "ship", "helicopter", "scooter", "truck"
    ]
}

# Path for images (adjust this with your actual path)
image_folder = "path/to/your/images/folder"  # Modify this with your image folder path

# Initialize the session state variables
if 'turns' not in st.session_state:
    st.session_state.turns = 5
if 'guesses' not in st.session_state:
    st.session_state.guesses = ""
if 'word' not in st.session_state:
    st.session_state.word = ""
if 'displayed_word' not in st.session_state:
    st.session_state.displayed_word = ""

# Function to start the game
def start_game():
    # Get the player's name and category
    if 'name' not in st.session_state:
        st.session_state.name = st.text_input("Enter your name:")

    if st.button("Start Game") and st.session_state.name:
        # Select random word from chosen category
        category = st.selectbox("Choose a category:", list(word_categories.keys()))
        st.session_state.word = random.choice(word_categories[category])
        st.session_state.displayed_word = "_ " * len(st.session_state.word)
        st.session_state.turns = 5
        st.session_state.guesses = ""

        # Display the word to guess
        st.text_area("Word to guess:", value=st.session_state.displayed_word, height=50)

        # Display guessed letters
        st.text("Guessed letters: " + ", ".join(st.session_state.guesses))

        # Show hint image for 4 seconds
        show_image_hint(st.session_state.word)

# Function to show the hint image for 4 seconds
def show_image_hint(word):
    try:
        image_path = os.path.join(image_folder, f"{word}.jpg")
        if os.path.exists(image_path):
            img = Image.open(image_path)
            # Display the image
            st.image(img, caption="Hint Image", use_column_width=True)

            # Wait for 4 seconds before clearing the image
            time.sleep(4)

            # Clear the image after 4 seconds
            st.empty()
        else:
            st.warning(f"No image found for the word '{word}'")
    except Exception as e:
        st.error(f"Error loading image: {e}")

# Function to make a guess
def make_guess():
    # Check if the game has started and session state is initialized
    if st.session_state.word != "" and st.session_state.turns > 0:
        guess = st.text_input("Enter your guess:", max_chars=1)
        if guess and len(guess) == 1 and guess.isalpha():
            if guess in st.session_state.guesses:
                st.warning("You already guessed that letter!")
            else:
                st.session_state.guesses += guess
                if guess not in st.session_state.word:
                    st.session_state.turns -= 1
                    st.warning(f"Wrong guess! Turns left: {st.session_state.turns}")
                else:
                    update_displayed_word()

                # Update displayed word
                update_displayed_word()

                if st.session_state.turns == 0:
                    st.error(f"You lost! The word was '{st.session_state.word}'.")
                    reset_game()

# Function to update the displayed word
def update_displayed_word():
    if 'word' in st.session_state and 'guesses' in st.session_state:
        displayed_word = " ".join([char if char in st.session_state.guesses else "_" for char in st.session_state.word])
        st.session_state.displayed_word = displayed_word
        st.text_area("Word to guess:", value=st.session_state.displayed_word, height=50)

# Reset game
def reset_game():
    st.session_state.turns = 5
    st.session_state.guesses = ""
    st.session_state.word = ""
    st.session_state.displayed_word = ""

# Main section for running the Streamlit app
if __name__ == "__main__":
    st.title("Word Guessing Game")
    start_game()
    make_guess()
