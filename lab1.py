import random

grammar = {
    'S': ['aS', 'bS', 'cA'],
    'A': ['aB'],
    'B': ['aB', 'bB', 'c']
}


def generate_random_string(start_symbol):
    if start_symbol not in grammar:
        return start_symbol
    production = random.choice(grammar[start_symbol])
    generated_string = ''
    for symbol in production:
        generated_string += generate_random_string(symbol)
    return generated_string


if __name__ == "__main__":
    start_symbol = 'S'

    for _ in range(5):
        random_string = generate_random_string(start_symbol)
        print(random_string)
