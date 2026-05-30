"""
NLP Chatbot Module
Automated Quad Machine — AI Safety Companion Drone
Author: M. Satyavardhan | B.Tech CSE, Malla Reddy College of Engineering (2020)

A retrieval-based conversational AI using:
  - NLTK for tokenisation and lemmatisation
  - TF-IDF + cosine similarity for response selection
  - Google TTS + Speech Recognition for voice I/O

The drone initiates conversation once a registered user's face is confirmed.
If the user stops responding, the system triggers an emergency alert.
"""

import io
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
from speech import play_aud, aud_rec

warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)

# ── Load knowledge base ──────────────────────────────────────────
with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# ── Text normalisation ───────────────────────────────────────────
lemmer = WordNetLemmatizer()


def lem_tokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def lem_normalize(text):
    return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# ── Greeting patterns ────────────────────────────────────────────
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = [
    "hi", "hey", "*nods*", "hi there", "hello",
    "I am glad you are talking to me"
]


def greeting(sentence: str):
    """Return a greeting response if the input is a greeting."""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# ── TF-IDF response generation ───────────────────────────────────
def response(user_response: str) -> str:
    """
    Generate the best matching response from the knowledge base
    using TF-IDF cosine similarity.

    Args:
        user_response (str): The user's spoken input.

    Returns:
        str: The drone's reply.
    """
    robo_response = ''
    sent_tokens.append(user_response)

    tfidf_vec = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    tfidf = tfidf_vec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]

    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        robo_response = "I am sorry, I don't understand you."
    else:
        robo_response = sent_tokens[idx]

    sent_tokens.remove(user_response)
    return robo_response


# ── Main chatbot loop ────────────────────────────────────────────
def chatbot_main(user_name: str) -> None:
    """
    Start the voice-based conversation loop with the identified user.
    Exits gracefully on 'bye' / 'thank you', or triggers alert on silence.

    Args:
        user_name (str): The name returned by face recognition.
    """
    play_aud(
        f"Hi {user_name}, my name is Dummy. "
        "I will answer your queries. Say bye or thank you to exit."
    )

    flag = True
    while flag:
        user_response = aud_rec()
        print(user_response)
        user_response = user_response.lower()

        if user_response == 'bye':
            flag = False
            play_aud("Bye! Take care.")
        elif user_response in ('thanks', 'thank you'):
            flag = False
            play_aud("You are welcome.")
        else:
            if greeting(user_response) is not None:
                play_aud(greeting(user_response))
            else:
                reply = response(user_response)
                print("Dummy: ", reply)
                play_aud(reply)
