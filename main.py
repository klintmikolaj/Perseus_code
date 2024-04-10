import random
import numpy as np

def divide_four(text: str):
    """Divides the text into four-character lists"""

    divided_list = []
    char_list = list(text)

    for i in range(0, len(char_list), 4):
        fragment = char_list[i:i + 4]
        divided_list.append(fragment)

    return divided_list


def create_possible_char_list():
    """Creates a list for all the possible characters used by the cipher"""

    possible_char_list = [chr(i) for i in range(48, 58)]
    for i in range(65, 91):
        possible_char_list.append(chr(i))
    for i in range(97, 123):
        possible_char_list.append(chr(i))
    return possible_char_list


def caesar_cipher(text: str, val: int, possible_char: list, rev: bool):
    """Implementation of the Caesar cipher or its reversed version"""

    char_index = possible_char.index(text)
    val = val if rev else val * -1
    final_char = possible_char[(char_index - val) % 62]
    return final_char

def generate_key(possible_char: list):
    """Creates random key necessary for creating the graph"""
    possible_char_no_zero = possible_char[1:]
    secret_key = ""
    while len(secret_key) < 8:
        secret_key += possible_char_no_zero[random.randint(1, 61)]
    return secret_key

def create_adjacency_matrix():
    """Creates matrix of vertices dependencies"""

    num_vertices = 14

    adjacency_matrix = np.zeros((num_vertices, num_vertices), dtype=int)

    edges = [
        (1, 2), (2, 3), (3, 4), (4, 5), (4, 14),
        (5, 6), (6, 7), (8, 9), (8, 10), (8, 14),
        (9, 11), (10, 11), (12, 13), (12, 14)
    ]

    for edge in edges:
        start, end = edge
        adjacency_matrix[start - 1, end - 1] = 1
        adjacency_matrix[end - 1, start - 1] = 1

    return adjacency_matrix

def set_graph_paths_weight(matrix: list, secret_key: str, possible_char: list):
    """Sets weight value to every path connecting two vertices"""
    possible_char_no_zero = possible_char[1:]
    graph_weights = [(possible_char_no_zero.index(char) + random.randint(1, 61)) % 61 for char in secret_key]
    graph_weights += [(possible_char_no_zero.index(char) - random.randint(1, 61)) % 61 for char in secret_key]

    weighted_matrix = np.zeros(matrix.shape, dtype=int)
    weight_index = 0

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] == 1 and weight_index < len(graph_weights):
                weighted_matrix[i, j] = graph_weights[weight_index]
                weight_index += 1

    return weighted_matrix

def set_values(values_list: list):
    """Sets values to certain vertices on the graph"""
    for val in values_list:
        ...

def encryption(div_list: list, w_matrix: list):
    starting_vert = [1, 7, 11, 13]
    for packet in div_list:
        for val in packet:







lista = create_possible_char_list()
matrix = create_adjacency_matrix()
key = generate_key(lista)
print(set_graph_paths_weight(matrix, key, lista))