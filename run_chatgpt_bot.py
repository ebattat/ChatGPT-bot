import openai
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)

# Create a logger object
logger = logging.getLogger()

# Set up your OpenAI API credentials
openai.api_key = ''


class ChatGPTBot:
    """
    This class makes ChatGPT as a real Bot
    """

    @staticmethod
    def speak(text: str):
        """
        This method speak the text
        :param text:
        :return:
        """
        tts = gTTS(text=text, lang='en')
        tts.save('output.mp3')  # Save the speech as an MP3 file
        pygame.mixer.init()
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        time.sleep(len(text)/10)  # Add a small delay after speaking

    @staticmethod
    def recognize_speech():
        """
        This method initializes the speech recognizer
        :return:
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            logger.info("Listening...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            logger.info("Sorry, I couldn't understand your speech.")
            return ""
        except sr.RequestError:
            logger.info("Sorry, I'm having trouble accessing the speech recognition service.")
            return ""

    @staticmethod
    def get_answer(question: str):
        """
        This method get the answer from openai API - interact with ChatGPT
        :param question:
        :return:
        """
        prompt = f"Question: {question}\nAnswer:"
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=50,
            temperature=0.7
        )

        if 'choices' in response and len(response['choices']) > 0:
            answer = response['choices'][0]['text']
            return answer.split('\n')[0]  # Return the generated answer without leading/trailing spaces
        else:
            return "Sorry, I don't have an answer for that question."

    @staticmethod
    def cleanup():
        """
        This method cleans up resources after speaking
        :return:
        """
        pygame.mixer.music.stop()


# Initialize ChatGPTBot class
chatgpt_bot = ChatGPTBot()

# Example conversation loop
# Example question: what is the capital of France ?
# Important ask question only after see Listening...
while True:
    # Bot asks a question
    question = "What can I help you with?"
    chatgpt_bot.speak(question)
    # User provides a spoken response
    user_response = chatgpt_bot.recognize_speech()
    # for exit
    if not user_response:
        continue
    elif user_response == 'goodbye':
        chatgpt_bot.speak('goodbye')
        logger.info('Shut down ChatGPT Bot')
        break
    # User response is converted to text
    logger.info(f'User: {user_response}')
    # Adding short answer to get short response
    user_question = f'{user_response}'
    bot_response = chatgpt_bot.get_answer(user_question)
    logger.info(f'ChatGPT Bot: {bot_response}')
    # ChatGPT Bot response is spoken
    chatgpt_bot.speak(bot_response)
    time.sleep(len(bot_response)/10)

# Clean up resources after speaking
chatgpt_bot.cleanup()
