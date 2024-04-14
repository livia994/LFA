def generate_combinations(regex):
    char_sets = {
        'M': ['N', ''],
        'N': ['N'],
        'O': ['O', ''],
        'P': ['P', ''],
        'Q': ['Q', ''],
        'R': ['R'],
        'x': ['x', 'y', 'z'],
        'y': ['x', 'y', 'z'],
        'z': ['x', 'y', 'z'],
        '8': ['8'],
        '9': ['9'],
        '0': ['0'],
        'H': ['H', 'I'],
        'I': ['L'],
        'J': ['J', 'K'],
        'K': ['L']
    }

    combinations = ['']

    processed_parts = []

    for part in regex.split():
        part_combinations = ['']
        processed_part = ''

        for char in part:
            if char in char_sets:
                part_combinations = [combo + new_char for combo in part_combinations for new_char in char_sets[char]]
                processed_part += f"({char} → {'|'.join(char_sets[char])}) "
            elif char.isdigit():
                part_combinations = [combo * int(char) for combo in part_combinations]
                processed_part += f"(repeat {char} times) "
            elif char.startswith("pow"):
                repeat_part = ['']
                for sub_char in char.split("(")[1].split(")")[0].split(",")[1:]:
                    repeat_part = [combo + new_char for combo in repeat_part for new_char in char_sets[sub_char]]
                part_combinations = [combo1 + combo2 for combo1 in part_combinations for combo2 in repeat_part]

        combinations = [combo1 + combo2 for combo1 in combinations for combo2 in part_combinations]
        processed_parts.append(processed_part)

    return combinations, processed_parts

def generate_valid_combinations(regexes):
    for regex in regexes:u
        combinations, processed_parts = generate_combinations(regex)
        if len(combinations) > 5:
            combinations = combinations[:5]
        print(f"For regex {regex}: {', '.join(combinations)}")
        print(f"Sequence of processing: {' → '.join(processed_parts)}\n")

regexes = [
    "M? N^2 (O|P)^3 Q* pow(R,+)",
    "(x|y|z)^3  pow(8,+) (9|0)^2",
    "(H|i) (J|k) pow(L,*)  N"
]

generate_valid_combinations(regexes)
