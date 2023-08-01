import pyttsx3
import speech_recognition as sr
import os

def speak(text, voice_gender='female'):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')
    if voice_gender == 'female':
        # Set the voice as female (assuming a female voice is available)
        engine.setProperty('voice', voices[1].id)
    else:
        # Set the voice as male (assuming a male voice is available)
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

def listen_for_activation_phrase():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    activation_phrase = "sky"  # The activation phrase to trigger the assistant
    sensitivity = 0.5  # Adjust the sensitivity for activation phrase detection (0 to 1)

    try:
        with microphone as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=2)  # Set a shorter timeout of 2 seconds

        recognized_text = recognizer.recognize_google(audio).lower()

        # Check if the activation phrase is recognized and repeated at least 'sensitivity' times
        if activation_phrase in recognized_text and recognized_text.count(activation_phrase) > sensitivity:
            return True

    except sr.UnknownValueError:
        pass

    return False

def process_command():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)  # Set a timeout of 5 seconds for command recognition

        recognized_command = recognizer.recognize_google(audio).lower()
        return recognized_command

    except sr.UnknownValueError:
        pass

    return None

def open_application(application_name):
    try:
        os.system(f"start {application_name}")  # Use 'start' command to open applications on Windows
    except Exception as e:
        print(f"Error while opening the application: {e}")

def main():
    print("Waiting for 'sky'...")

    while True:
        if listen_for_activation_phrase():
            print("Activated!")
            speak("Hello boss! How can I assist you?", voice_gender='female')  # Respond with a female voice
            # Add your custom logic to handle user commands and interactions

            # Example: Command the AI to open applications based on voice commands
            while True:
                command = process_command()
                if command is None:
                    continue
                elif "exit" in command:
                    break
                elif "open " in command:
                    app_name = command.replace("open ", "").strip()
                    open_application(app_name)

if __name__ == "__main__":
    main()
