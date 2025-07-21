import random
from string import ascii_letters

def generate_random_name(count: int):
    random_name: str = ""
    for i in range(count):
        random_name += random.choice(ascii_letters)
    
    return random_name
