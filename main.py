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
                # Deszyfrowanie: przesuń wstecz
                new_index = (char_index - val) % len(possible_char)
            else:
                # Szyfrowanie: przesuń do przodu
                new_index = (char_index + val) % len(possible_char)
            encrypted_text += possible_char[new_index]
        else:
            encrypted_text += char  # Zostawia znak niezmieniony, jeśli nie ma go w possible_char
    return encrypted_text



def generate_key(possible_char: list):
    """Generates a secret key for encryption/decryption"""
    # Secret key won't have 0 and a whitespace character
    secret_key = "".join(random.choice(possible_char[1:len(possible_char)-1]) for _ in range(7))
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
    div_list = divide_four(text)
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    encrypted_text = ""

    for fragment in div_list:
        # Wypełniamy brakujące znaki None zamiast spacji
        fragment_padded = fragment + [None] * (4 - len(fragment))

        # Inicjalizacja zmiennych do przechowywania zaszyfrowanych fragmentów
        encrypted_char_from_1_to_4 = ''
        encrypted_char_from_7_to_4 = ''
        sum8 = ''
        sum13 = ''

        # Szyfrowanie znaków z wierzchołka 1 do wierzchołka 4
        if fragment_padded[0] is not None:
            encrypted_char1 = caesar_cipher(fragment_padded[0], weighted_matrix[0][1], possible_char, False)
            encrypted_char2 = caesar_cipher(encrypted_char1, weighted_matrix[1][2], possible_char, False)
            encrypted_char_from_1_to_4 = caesar_cipher(encrypted_char2, weighted_matrix[2][3], possible_char, False)
            print(f"3-4 {encrypted_char_from_1_to_4}")

        # Szyfrowanie znaków z wierzchołka 7 do wierzchołka 4
        if fragment_padded[1] is not None:
            encrypted_char7 = caesar_cipher(fragment_padded[1], weighted_matrix[6][5], possible_char, False)
            encrypted_char6 = caesar_cipher(encrypted_char7, weighted_matrix[5][4], possible_char, False)
            encrypted_char_from_7_to_4 = caesar_cipher(encrypted_char6, weighted_matrix[4][3], possible_char, False)
            print(f"6-4 {encrypted_char_from_7_to_4}")

        # Sumowanie i szyfrowanie znaków z wierzchołka 4 do 14
        sum4 = encrypted_char_from_1_to_4 + encrypted_char_from_7_to_4
        print(f"4 przed szyfr {sum4}")
        sum4 = caesar_cipher(sum4, weighted_matrix[3][13], possible_char, False)
        print(f"4 po szyfr {sum4}")

        # Szyfrowanie i duplikacja znaków z wierzchołka 11 do wierzchołka 8
        if fragment_padded[2] is not None:
            encrypted_char11a = caesar_cipher(fragment_padded[2], weighted_matrix[10][8], possible_char, False)
            encrypted_char11b = caesar_cipher(fragment_padded[2], weighted_matrix[10][9], possible_char, False)
            encrypted_char9 = caesar_cipher(encrypted_char11a, weighted_matrix[8][7], possible_char, False)
            encrypted_char10 = caesar_cipher(encrypted_char11b, weighted_matrix[9][7], possible_char, False)
            sum8 = encrypted_char9 + encrypted_char10
            print(f"8 przed szyfr {sum8}")
            sum8 = caesar_cipher(sum8, weighted_matrix[7][13], possible_char, False)
            print(f"8 po szyfr {sum8}")

        # Szyfrowanie znaków z wierzchołka 13 do wierzchołka 14
        if fragment_padded[3] is not None:
            encrypted_char_13 = caesar_cipher(fragment_padded[3], weighted_matrix[12][11], possible_char, False)
            print(f"12 przed szyfr {encrypted_char_13}")
            sum13 = caesar_cipher(encrypted_char_13, weighted_matrix[11][13], possible_char, False)
            print(f"12 po szyfr {sum13}")

        # Połączenie zaszyfrowanych fragmentów i dodanie do zaszyfrowanego tekstu
        encrypted_text += sum4 + sum8 + sum13

    return encrypted_text


def decrypt(encrypted_text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    decrypted_text = ""

    # Przypisujemy długości zaszyfrowanych fragmentów dla każdego z wierzchołków
    segment_length = 5  # Fragment pochodzący z wierzchołka 14, przyjmujemy 5 znaków jako przykład

    for i in range(0, len(encrypted_text), segment_length):
        fragment = encrypted_text[i:i + segment_length]

        # Odszyfrowywanie znaków z wierzchołka 14 do wierzchołka 4
        sum4 = caesar_cipher(fragment[:2], weighted_matrix[3][13], possible_char, True)
        sum8 = caesar_cipher(fragment[2:4], weighted_matrix[7][13], possible_char, True)
        sum13 = caesar_cipher(fragment[4], weighted_matrix[11][13], possible_char, True)

        # Odszyfrowywanie z wierzchołka 4 do wierzchołka 1 i 7
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

        # Odszyfrowywanie z wierzchołka 11
        decrypted_char_from_11 = caesar_cipher(sum8, weighted_matrix[8][7], possible_char, True)
        decrypted_char_from_11 = caesar_cipher(decrypted_char_from_11, weighted_matrix[9][7], possible_char, True)
        decrypted_char_from_11 = caesar_cipher(decrypted_char_from_11, weighted_matrix[10][8], possible_char,
                                               True)  # Zakładamy że oba znaki są takie same, więc wystarczy jeden

        # Łączenie odszyfrowanych znaków
        decrypted_text += decrypted_char_from_1_to_4 + decrypted_char_from_7_to_4 + decrypted_char_from_11 + sum13

    return decrypted_text


# Main loop for testing encryption and decryption
possible_char = create_possible_char_list()
adjacency_matrix = create_adjacency_matrix()
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

print("Witaj w programie kodującym Perseusz!")
while True:
    action = input("Chcesz zaszyfrować czy odszyfrować tekst? (wpisz: 'z' - zaszyfruj, 'o' - odszyfruj): ").lower()
    action.strip()
    if action == 'z':
        plaintext = input("Wprowadź tekst do zaszyfrowania: ")
        secret_key = generate_key(possible_char)  # Generowanie klucza
        encrypted_text = encrypt(plaintext, adjacency_matrix, possible_char, secret_key)
        print(f"Zaszyfrowany tekst: >>{encrypted_text}<<")
        print(f"Użyj tego klucza do deszyfrowania: {secret_key}")
    elif action == 'o':
        secret_key = input("Wprowadź klucz do odszyfrowania: ")
        ciphertext = input("Wprowadź tekst do odszyfrowania: ")
        decrypted_text = decrypt(ciphertext, adjacency_matrix, possible_char, secret_key)
        print("Odszyfrowany tekst:", decrypted_text)
    else:
        print("Nieznana akcja.")
    if input("Czy chcesz kontynuować? (tak/nie): ").lower() != 'tak':
        break
