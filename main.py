import random
import numpy as np


def divide_four(text: str):
    """Divides the input string into four-element list"""
    divided_list = []
    char_list = list(text)
    for i in range(0, len(char_list), 4):
        fragment = char_list[i:i + 4]
        divided_list.append(fragment)
    return divided_list


def create_possible_char_list():
    """Creates a list of all possible characters (numbers, upper/lower letters)"""
    possible_char_list = [chr(i) for i in range(48, 58)]
    possible_char_list.extend([chr(i) for i in range(65, 91)])
    possible_char_list.extend([chr(i) for i in range(97, 123)])
    possible_char_list.append(" ")
    return possible_char_list


def caesar_cipher(text: str, val: int, possible_char: list, rev: bool):
    """Implementation of the Caesar cipher or its reversed version for strings"""
    if not text:
        return text

    encrypted_text = ""
    for char in text:
        if char in possible_char:
            char_index = possible_char.index(char)
            if rev:
                # Move backwards
                new_index = (char_index - val) % len(possible_char)
            else:
                # Move forward
                new_index = (char_index + val) % len(possible_char)
            encrypted_text += possible_char[new_index]
        else:
            encrypted_text += char
    return encrypted_text


def generate_key(possible_char: list):
    """Generates a secret key for encryption/decryption"""
    # Secret key won't have 0 and a whitespace character
    secret_key = "".join(random.choice(possible_char[1:len(possible_char) - 1]) for _ in range(7))
    return secret_key


def create_adjacency_matrix():
    """Creates an adjacency matrix of the Perseus graph"""
    num_vertices = 14
    adjacency_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
    edges = [
        (1, 2), (2, 3), (3, 4), (4, 5), (4, 14),
        (5, 6), (6, 7), (8, 9), (8, 10), (8, 14),
        (9, 11), (10, 11), (12, 13), (12, 14)
    ]
    for start, end in edges:
        adjacency_matrix[start - 1, end - 1] = adjacency_matrix[end - 1, start - 1] = 1
    return adjacency_matrix


def set_graph_paths_weight(matrix: np.ndarray, secret_key: str, possible_char: list):
    """Sets weight value to every path connecting two vertices based on the secret key"""
    # Generates graph paths weights based on the secret key
    graph_weights = [(possible_char.index(char) % len(possible_char)) + 1 for char in secret_key]
    print(graph_weights)

    # Sets specific weights to certain graph path
    weight_index = 0
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                # Checks if wages to assign exist
                if weight_index < len(graph_weights):
                    weight = graph_weights[weight_index]
                    matrix[i, j] = matrix[j, i] = weight
                    weight_index += 1
                else:
                    # Repeats the process one more time
                    # 7-value key represents 14 graph paths weights
                    weight_index = 0
                    weight = graph_weights[weight_index]
                    matrix[i, j] = matrix[j, i] = weight
                    weight_index += 1
    return matrix


def encrypt(text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
    """Encrypts the given string by the Perseus graph rules"""
    div_list = divide_four(text)
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    encrypted_text = ""

    for fragment in div_list:
        # Fill the list with None object if the string cannot be devided by 4
        fragment_padded = fragment + [None] * (4 - len(fragment))

        encrypted_char_from_1_to_4 = ''
        encrypted_char_from_7_to_4 = ''
        sum8 = ''
        sum13 = ''

        if fragment_padded[0] is not None:
            encrypted_char1 = caesar_cipher(fragment_padded[0], weighted_matrix[0][1], possible_char, False)
            encrypted_char2 = caesar_cipher(encrypted_char1, weighted_matrix[1][2], possible_char, False)
            encrypted_char_from_1_to_4 = caesar_cipher(encrypted_char2, weighted_matrix[2][3], possible_char, False)

        if fragment_padded[1] is not None:
            encrypted_char7 = caesar_cipher(fragment_padded[1], weighted_matrix[6][5], possible_char, False)
            encrypted_char6 = caesar_cipher(encrypted_char7, weighted_matrix[5][4], possible_char, False)
            encrypted_char_from_7_to_4 = caesar_cipher(encrypted_char6, weighted_matrix[4][3], possible_char, False)

        sum4 = encrypted_char_from_1_to_4 + encrypted_char_from_7_to_4
        sum4 = caesar_cipher(sum4, weighted_matrix[3][13], possible_char, False)

        if fragment_padded[2] is not None:
            encrypted_char11a = caesar_cipher(fragment_padded[2], weighted_matrix[10][8], possible_char, False)
            encrypted_char11b = caesar_cipher(fragment_padded[2], weighted_matrix[10][9], possible_char, False)
            encrypted_char9 = caesar_cipher(encrypted_char11a, weighted_matrix[8][7], possible_char, False)
            encrypted_char10 = caesar_cipher(encrypted_char11b, weighted_matrix[9][7], possible_char, False)
            sum8 = encrypted_char9 + encrypted_char10
            sum8 = caesar_cipher(sum8, weighted_matrix[7][13], possible_char, False)

        if fragment_padded[3] is not None:
            encrypted_char_13 = caesar_cipher(fragment_padded[3], weighted_matrix[12][11], possible_char, False)
            sum13 = caesar_cipher(encrypted_char_13, weighted_matrix[11][13], possible_char, False)

        encrypted_text += sum4 + sum8 + sum13

    return encrypted_text


def decrypt(encrypted_text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
    """Decrypts the given string by the Perseus graph rules"""
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    decrypted_text = ""
    segment_length = 5  # Maximum size of a segment

    for i in range(0, len(encrypted_text), segment_length):
        fragment = encrypted_text[i:i + segment_length]
        fragment_length = len(fragment)

        # Decoding sum4 (4th vert)
        if fragment_length > 1:
            sum4 = caesar_cipher(fragment[:2], weighted_matrix[3][13], possible_char, True)
            decrypted_char_from_1_to_4 = caesar_cipher(sum4[0], weighted_matrix[2][3], possible_char, True)
            decrypted_char_from_1_to_4 = caesar_cipher(decrypted_char_from_1_to_4, weighted_matrix[1][2], possible_char,
                                                       True)
            decrypted_char_from_1_to_4 = caesar_cipher(decrypted_char_from_1_to_4, weighted_matrix[0][1], possible_char,
                                                       True)
            decrypted_char_from_7_to_4 = caesar_cipher(sum4[1], weighted_matrix[4][3], possible_char, True)
            decrypted_char_from_7_to_4 = caesar_cipher(decrypted_char_from_7_to_4, weighted_matrix[5][4], possible_char,
                                                       True)
            decrypted_char_from_7_to_4 = caesar_cipher(decrypted_char_from_7_to_4, weighted_matrix[6][5], possible_char,
                                                       True)
            decrypted_text += decrypted_char_from_1_to_4 + decrypted_char_from_7_to_4
        elif fragment_length == 1:
            sum4 = caesar_cipher(fragment[0], weighted_matrix[3][13], possible_char, True)
            decrypted_char_from_1_to_4 = caesar_cipher(sum4, weighted_matrix[2][3], possible_char, True)
            decrypted_char_from_1_to_4 = caesar_cipher(decrypted_char_from_1_to_4, weighted_matrix[1][2], possible_char,
                                                       True)
            decrypted_char_from_1_to_4 = caesar_cipher(decrypted_char_from_1_to_4, weighted_matrix[0][1], possible_char,
                                                       True)
            decrypted_text += decrypted_char_from_1_to_4

        # Decoding sum8
        if fragment_length > 3:
            sum8 = caesar_cipher(fragment[2:4], weighted_matrix[7][13], possible_char, True)
            decrypted_char_from_11 = caesar_cipher(sum8[0], weighted_matrix[8][7], possible_char, True)
            decrypted_char_from_11 = caesar_cipher(decrypted_char_from_11, weighted_matrix[10][8], possible_char, True)
            decrypted_text += decrypted_char_from_11

        # Decoding sum13
        if fragment_length == 5:
            sum13 = caesar_cipher(fragment[4], weighted_matrix[11][13], possible_char, True)
            decrypted_char_13 = caesar_cipher(sum13, weighted_matrix[12][11], possible_char, True)
            decrypted_text += decrypted_char_13

    return decrypted_text


# Main loop for testing encryption and decryption
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
BLUE = "\033[34m"

print("\nSzyfr Orfeusza")
while True:
    possible_char = create_possible_char_list()
    adjacency_matrix = create_adjacency_matrix()
    action = input("\nChcesz zaszyfrować czy odszyfrować tekst? (wpisz: 'z' - zaszyfruj, 'o' - odszyfruj): ").lower()
    action.strip()
    if action == 'z':
        plaintext = input("Wprowadź tekst do zaszyfrowania: ")
        secret_key = generate_key(possible_char)  # Generates a random key
        encrypted_text = encrypt(plaintext, adjacency_matrix, possible_char, secret_key)
        print(f"Zaszyfrowany tekst: >>{BLUE}{encrypted_text}{RESET}<<")
        print(f"Użyj tego klucza do deszyfrowania: >>{RED}{secret_key}{RESET}<<")
    elif action == 'o':
        secret_key = ""
        while len(secret_key) != 7:
            secret_key = input("Wprowadź klucz do odszyfrowania (Poprawny klucz składa się z 7 znaków): ")
        ciphertext = input("Wprowadź tekst do odszyfrowania: ")
        decrypted_text = decrypt(ciphertext, adjacency_matrix, possible_char, secret_key)
        print(f"Odszyfrowany tekst: >>{GREEN}{decrypted_text}{RESET}<<")
    else:
        print("Nieznana akcja.")
    if input("\nCzy chcesz kontynuować? (wpisz: 'tak'): ").lower() != 'tak':
        break
