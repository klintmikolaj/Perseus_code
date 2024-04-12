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
    return possible_char_list


def caesar_cipher(text: str, val: int, possible_char: list, rev: bool):
    """Implementation of the Caesar cipher or its reversed version"""
    if not text:
        return text  # Zwraca pusty tekst, jeśli nie ma co szyfrować

    encrypted_text = ""
    for char in text:  # Zmodyfikowano, aby obsługiwała cały tekst, a nie pojedynczy znak
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
    secret_key = "".join(random.choice(possible_char[1:]) for _ in range(7))
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
    # Generowanie wag na podstawie klucza
    graph_weights = [(possible_char.index(char) % len(possible_char)) + 1 for char in secret_key]

    # Ustawienie wag dla krawędzi zgodnie z kolejnością określoną w graph_weights
    weight_index = 0
    for i in range(matrix.shape[0]):
        for j in range(i + 1, matrix.shape[1]):
            if matrix[i, j] == 1:
                # Sprawdzenie, czy nie wyczerpaliśmy jeszcze wag
                if weight_index < len(graph_weights):
                    weight = graph_weights[weight_index]
                    matrix[i, j] = matrix[j, i] = weight
                    weight_index += 1
                else:
                    # Jeśli są więcej połączeń niż długość klucza, zacznij od nowa z listą wag
                    weight_index = 0
                    weight = graph_weights[weight_index]
                    matrix[i, j] = matrix[j, i] = weight
                    weight_index += 1
    return matrix


def encryption(text: str, w_matrix: np.ndarray, possible_char: list):
    """Encrypts the data"""
    secret_key = generate_key(possible_char)
    print("Wygenerowany klucz:", secret_key)
    return move_between_vertices(text, w_matrix, possible_char, secret_key, False), secret_key


def decryption(encrypted_text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
    """Decrypts the data"""
    return move_between_vertices(encrypted_text, w_matrix, possible_char, secret_key, True)


def move_between_vertices(text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str, reverse: bool):
    """Processes the text with the algorithm based on the graph """
    div_list = divide_four(text)
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    processed_text = ""

    # Upewnij się, że używasz wagi z odpowiednich miejsc macierzy
    vertices_index = [0, 6, 10, 12]  # Indeksy wierzchołków startowych w macierzy są zerowo indeksowane

    for fragment in div_list:
        new_fragment = ''
        for char, vert in zip(fragment, vertices_index):
            if char:
                # Użycie wagi z macierzy - ważne jest, aby waga była odpowiednia dla danego znaku
                weight = weighted_matrix[vert][np.where(weighted_matrix[vert] > 0)][
                    0]  # Pobierz pierwszą niezerową wagę dla wierzchołka
                new_char = caesar_cipher(char, weight, possible_char, reverse)
                new_fragment += new_char
        processed_text += new_fragment
    return processed_text


# Main loop for testing encryption and decryption
possible_char = create_possible_char_list()
adjacency_matrix = create_adjacency_matrix()

while True:
    action = input("Chcesz zaszyfrować czy odszyfrować tekst? (encrypt/decrypt): ").lower()
    if action == 'encrypt':
        plaintext = input("Wprowadź tekst do zaszyfrowania: ")
        encrypted_text, secret_key = encryption(plaintext, adjacency_matrix, possible_char)
        print("Zaszyfrowany tekst:", encrypted_text)
        print("Użyj tego klucza do deszyfrowania:", secret_key)
    elif action == 'decrypt':
        secret_key = input("Wprowadź klucz do odszyfrowania: ")
        ciphertext = input("Wprowadź tekst do odszyfrowania: ")
        decrypted_text = decryption(ciphertext, adjacency_matrix, possible_char, secret_key)
        print("Odszyfrowany tekst:", decrypted_text)
    else:
        print("Nieznana akcja.")
    if input("Czy chcesz kontynuować? (tak/nie): ").lower() != 'tak':
        break
