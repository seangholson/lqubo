import numpy as np
import os

# Working directory should always be /QAP-Quantum-Computing/
# DAT files should always be in /qap-qc/data
dat_path = 'data/'


def parse_dat_file(dat_file):
    with open(os.path.join(dat_path, dat_file).replace('\\', '/'), mode='r') as file:
        n = int(file.readline())
        dist = read_square_matrix(file, n)
        flow = read_square_matrix(file, n)

    return n, dist, flow


def read_square_matrix(matrix_file, matrix_size):
    matrix = []
    row_counter = 0
    while row_counter < matrix_size:
        line = matrix_file.readline()
        assert isinstance(line, str)
        if not line.isspace():
            row_counter += 1
            matrix_row = [int(element) for element in line.split(' ') if element != '']
            matrix.append(matrix_row)
    return np.array(matrix)
