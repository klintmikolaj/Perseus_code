# import random
# import numpy as np
#
# def divide_four(text: str):
#     """Divides the text into four-character lists"""
#
#     divided_list = []
#     char_list = list(text)
#
#     for i in range(0, len(char_list), 4):
#         fragment = char_list[i:i + 4]
#         divided_list.append(fragment)
#
#     return divided_list
#
#
# def create_possible_char_list():
#     """Creates a list for all the possible characters used by the cipher"""
#
#     possible_char_list = [chr(i) for i in range(48, 58)]
#     for i in range(65, 91):
#         possible_char_list.append(chr(i))
#     for i in range(97, 123):
#         possible_char_list.append(chr(i))
#     return possible_char_list
#
#
# def caesar_cipher(text: str, val: int, possible_char: list, rev: bool):
#     """Implementation of the Caesar cipher or its reversed version"""
#
#     char_index = possible_char.index(text)
#     val = val if rev else val * -1
#     final_char = possible_char[(char_index - val) % 62]
#     return final_char
#
# def generate_key(possible_char: list):
#     """Creates random key necessary for creating the graph"""
#
#     possible_char_no_zero = possible_char[1:]
#     secret_key = ""
#     while len(secret_key) < 8:
#         secret_key += possible_char_no_zero[random.randint(1, 61)]
#     return secret_key
#
# def create_adjacency_matrix():
#     """Creates matrix of vertices dependencies"""
#
#     num_vertices = 14
#
#     adjacency_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
#
#     edges = [
#         (1, 2), (2, 3), (3, 4), (4, 5), (4, 14),
#         (5, 6), (6, 7), (8, 9), (8, 10), (8, 14),
#         (9, 11), (10, 11), (12, 13), (12, 14)
#     ]
#
#     for edge in edges:
#         start, end = edge
#         adjacency_matrix[start - 1, end - 1] = 1
#         adjacency_matrix[end - 1, start - 1] = 1
#
#     return adjacency_matrix
#
# def set_graph_paths_weight(matrix: list, secret_key: str, possible_char: list):
#     """Sets weight value to every path connecting two vertices"""
#
#     possible_char_no_zero = possible_char[1:]
#     graph_weights = [(possible_char_no_zero.index(char) + random.randint(1, 61)) % 61 for char in secret_key] + [
#         (possible_char_no_zero.index(char) - random.randint(1, 61)) % 61 for char in secret_key]
#
#     weighted_matrix = np.copy(matrix)  # Utwórz kopię macierzy, aby zachować jej strukturę
#
#     weight_index = 0  # Deklaracja zmiennej weight_index przed jej użyciem
#
#     for i in range(matrix.shape[0]):
#         for j in range(i + 1,
#                        matrix.shape[1]):  # Iteruj tylko po górnotrójkątnej części macierzy, aby uniknąć duplikatów
#             if matrix[i, j] == 1:
#                 # Sprawdzanie, czy zostały jeszcze jakieś wagi do przypisania
#                 if weight_index < len(graph_weights):
#                     # Przypisanie wagi do obu kierunków krawędzi
#                     weight = graph_weights[weight_index]
#                     weighted_matrix[i, j] = weight
#                     weighted_matrix[j, i] = weight
#
#                     weight_index += 1  # Aktualizacja indeksu po przypisaniu wagi
#     return weighted_matrix
#
#
# def encryption(text: str, w_matrix: np.ndarray, possible_char: list):
#     # Dziel tekst na fragmenty po 4 znaki
#     div_list = divide_four(text)
#
#     # Tworzenie macierzy wag i listy możliwych znaków
#     secret_key = generate_key(possible_char)
#     print(secret_key)
#     weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
#     # print(weighted_matrix)
#
#     # Inicjowanie zmiennej na szyfrowany tekst
#     encrypted_text = ""
#
#     # Przetwarzanie każdego fragmentu
#     for fragment in div_list:
#         # Przypisanie początkowych wierzchołków dla każdego znaku w fragmencie
#         vertices = [1, 7, 11, 13]  # Przykładowe wierzchołki startowe
#
#         # Przechodzenie przez graf i tworzenie nowych fragmentów
#         new_fragment = ''
#         for char, vert in zip(fragment, vertices):
#             if vert == 11:
#                 # Znak z wierzchołka 11 jest podwajany
#                 new_char = caesar_cipher(char, weighted_matrix[vert - 1][vert], possible_char, False)
#                 new_fragment += new_char * 2
#             else:
#                 # Pozostałe znaki są przekształcane normalnie
#                 new_char = caesar_cipher(char, weighted_matrix[vert - 1][vert], possible_char, False)
#                 new_fragment += new_char
#
#         # Szyfrowanie stworzonego fragmentu
#         encrypted_text += new_fragment
#
#     return encrypted_text
#
#
# def decryption(encrypted_text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
#     # Używamy podanego klucza do ustawienia wag w macierzy
#     weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
#
#     # Reszta procesu deszyfrowania pozostaje taka sama, zakładając, że klucz jest poprawny
#     decrypted_text = ""
#     vertices = [1, 7, 11, 13]  # Wierzchołki startowe
#
#     for fragment in encrypted_text:
#         new_fragment = ''
#         vert_index = 0
#         for char in fragment:
#             # Deszyfrowanie znaku
#             new_char = caesar_cipher(char, weighted_matrix[vertices[vert_index] - 1][vertices[vert_index]],
#                                      possible_char, True)
#             new_fragment += new_char
#             vert_index += 1
#
#         # Dodanie deszyfrowanego fragmentu do pełnego tekstu
#         decrypted_text += new_fragment
#
#     return decrypted_text
#
# # possible_char = create_possible_char_list()
# # adjacency_matrix = create_adjacency_matrix()
# # text_to_encrypt = "A"
# # encrypted = encryption(text_to_encrypt, adjacency_matrix, possible_char)
# # print(encrypted)
# # encrypted = "8"
# # known_secret_key = "plHuEOQd"
# # decrypted = decryption(encrypted, adjacency_matrix, possible_char, known_secret_key)
# # print(decrypted)
#
# # Stwórz listę możliwych znaków i macierz sąsiedztwa
# possible_char = create_possible_char_list()
# adjacency_matrix = create_adjacency_matrix()
#
# # Pętla główna
# while True:
#     # Odbierz od użytkownika wybór akcji
#     action = input("Chcesz zaszyfrować czy odszyfrować tekst? (encrypt/decrypt): ").lower()
#
#     # Obsługa szyfrowania
#     if action == 'encrypt':
#         plaintext = input("Wprowadź tekst do zaszyfrowania: ")
#         secret_key = generate_key(possible_char)  # Generuj klucz tylko raz
#         print("Wygenerowany klucz:", secret_key)  # Wyświetl wygenerowany klucz
#         encrypted = encryption(plaintext, adjacency_matrix, possible_char,
#                                secret_key)  # Przekazanie klucza jako argument
#         print("Zaszyfrowany tekst:", encrypted)
#
#     # Obsługa deszyfrowania
#     elif action == 'decrypt':
#         secret_key = input("Wprowadź klucz do odszyfrowania: ")
#         ciphertext = input("Wprowadź tekst do odszyfrowania: ")
#         decrypted = decryption(ciphertext, adjacency_matrix, possible_char, secret_key)
#         print("Odszyfrowany tekst:", decrypted)
#
#     else:
#         print("Nieprawidłowa komenda.")
#
#     # Sprawdzenie, czy kontynuować
#     continue_prompt = input("Czy chcesz kontynuować? (tak/nie): ").lower()
#     if continue_prompt != 'tak':
#         break
#


import random
import numpy as np

def divide_four(text: str):
    divided_list = []
    char_list = list(text)
    for i in range(0, len(char_list), 4):
        fragment = char_list[i:i + 4]
        divided_list.append(fragment)
    return divided_list

def create_possible_char_list():
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
    secret_key = "".join(random.choice(possible_char[1:]) for _ in range(7))
    return secret_key

def create_adjacency_matrix():
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
    secret_key = generate_key(possible_char)
    print("Wygenerowany klucz:", secret_key)
    return _process_text(text, w_matrix, possible_char, secret_key, False), secret_key

def decryption(encrypted_text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str):
    return _process_text(encrypted_text, w_matrix, possible_char, secret_key, True)


def _process_text(text: str, w_matrix: np.ndarray, possible_char: list, secret_key: str, reverse: bool):
    div_list = divide_four(text)
    weighted_matrix = set_graph_paths_weight(w_matrix, secret_key, possible_char)
    processed_text = ""

    # Upewnij się, że używasz wagi z odpowiednich miejsc macierzy
    vertices = [0, 6, 10, 12]  # Indeksy wierzchołków startowych w macierzy są zerowo indeksowane

    for fragment in div_list:
        new_fragment = ''
        for char, vert in zip(fragment, vertices):
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
