import random
import streamlit as st
import os
from PIL import Image
import time

# Word categories for the guessing game
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
        "grasshopper", "mosquito", "spider", "cockroach", "grasshoper"
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

# Folder path for the images
image_folder = "images"  # Path to the image folder

# Function to display the hint image for only 4 seconds
def show_image_hint():
    # Check if hint should be shown
    if 'show_hint' not in st.session_state or not st.session_state['show_hint']:
        st.session_state['show_hint'] = True  # Set the hint to show initially
        st.session_state['hint_start_time'] = time.time()  # Save the start time

    image_path = os.path.join(image_folder, f"{st.session_state['word']}.jpg")

    # Display image if it's within 4 seconds of start time
    if st.session_state['show_hint'] and time.time() - st.session_state['hint_start_time'] < 4:
        if os.path.exists(image_path):
            st.image(image_path, caption="Hint (4 seconds)", use_column_width=True)
        else:
            st.warning("No image hint available for this word.")
    else:
        st.session_state['show_hint'] = False  # Hide hint after 4 seconds

# Streamlit app layout
st.title("Word Guessing Game for Kids")

# Create dropdown for category selection
category = st.selectbox("Choose a category:", list(word_categories.keys()))

# User's name input
name = st.text_input("Enter your name")

if st.button("Start Game"):
    if not name:
        st.warning("Please enter your name to start the game!")
    else:
        st.session_state['name'] = name
        st.session_state['category'] = category
        st.session_state['word'] = random.choice(word_categories[category])
        st.session_state['guesses'] = ""
        st.session_state['turns'] = 5

        st.session_state['displayed_word'] = "_ " * len(st.session_state['word'])
        st.session_state['guesses_label'] = "Guessed letters: "
        st.session_state['turns_label'] = f"Turns left: {st.session_state['turns']}"

        # Show hint image for 4 seconds
        show_image_hint()

        st.session_state['name_input_disabled'] = True
        st.session_state['category_disabled'] = True

        st.text_area("Word to guess:", value=st.session_state['displayed_word'], height=50)

        # Input field for guesses
        guess = st.text_input("Enter a letter to guess:")

        if guess:
            guess = guess.lower()
            if len(guess) != 1 or not guess.isalpha():
                st.error("Please enter a single valid letter!")
            elif guess in st.session_state['guesses']:
                st.info("You've already guessed that letter!")
            else:
                st.session_state['guesses'] += guess

                if guess not in st.session_state['word']:
                    st.session_state['turns'] -= 1
                    st.info(f"'{guess}' is not in the word!")

                # Update the displayed word with guessed letters
                displayed_word = " ".join(char if char in st.session_state['guesses'] else "_" for char in st.session_state['word'])
                st.session_state['displayed_word'] = displayed_word
                st.session_state['turns_label'] = f"Turns left: {st.session_state['turns']}"
                st.session_state['guesses_label'] = "Guessed letters: " + ", ".join(st.session_state['guesses'])

                st.text_area("Word to guess:", value=st.session_state['displayed_word'], height=50)

                # Check for win or loss
                if "_" not in displayed_word:
                    st.success(f"Congratulations, {st.session_state['name']}! You win! The word was '{st.session_state['word']}'")
                    st.session_state['game_over'] = True
                elif st.session_state['turns'] == 0:
                    st.error(f"Game Over! The word was '{st.session_state['word']}'")
                    st.session_state['game_over'] = True

        if 'game_over' in st.session_state and st.session_state['game_over']:
            if st.button("Play Again"):
                st.session_state.clear()
                st.experimental_rerun()
