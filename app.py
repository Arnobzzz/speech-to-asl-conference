import os
import cv2
import time
import speech_recognition as sr

# Folder containing images for each character
folder_path = "G:/D Drive/conference 2023/sign language/numbers/numbers"  # Replace with your actual folder path

# Function to display the image corresponding to a character
def display_image(character):
    image_path = os.path.join(folder_path, f"{character}.jpg")

    if not os.path.exists(image_path):
        print(f"Image for character '{character}' does not exist in the folder.")
        return None

    # Load and resize the image to a common size (e.g., 100x100 pixels)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (100, 100))  # Adjust the size as needed

    return image

# Initialize the recognizer
recognizer = sr.Recognizer()

# Main loop for capturing audio and displaying corresponding images
while True:
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 2.0  # Wait for 2 seconds of silence
        audio = recognizer.listen(source)
    
    # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        
        if text.lower() == "quit":
            break  # Exit the loop when "quit" is recognized
        
        images_to_display = []

        # Loop through each character in the recognized text
        for char in text.upper():  # Uppercase to match filenames
            image = display_image(char)
            if image is not None:
                images_to_display.append(image)

        # If there are images to display, concatenate and show them
        if images_to_display:
            row_image = cv2.hconcat(images_to_display)  # Concatenate images horizontally
            cv2.imshow("Characters", row_image)
            cv2.waitKey(3000)  # Display for 3 seconds (3000 milliseconds)
            cv2.destroyAllWindows()

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    # Pause for 1 second before restarting the loop
    time.sleep(1)

# Exit message
print("Goodbye!")
