import random

def classify(data):
    classifications = ['Confirmed', 'Candidate', 'False Positive']
    return random.choice(classifications), random.random()
