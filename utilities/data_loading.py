import os
import numpy as np


# Working directory should always be /qap-qc/

dat_path = 'data/dat'
sln_path = 'data/sln'


def parse_dat_file(dat_file):
    with open(os.path.join(dat_path, dat_file).replace('\\', '/'), mode='r') as file:
        n = int(file.readline())
        dist = read_square_matrix(file, n)
        flow = read_square_matrix(file, n)

    return n, dist, flow


def parse_sln_file(sln_file):
    with open(os.path.join(sln_path, sln_file), mode='r') as file:
        line_1 = file.readline()
        assert isinstance(line_1, str)
        n, v = [int(element) for element in line_1.split(' ') if element != '']
        line_2 = file.readline()
        assert isinstance(line_2, str)
        p = [int(element) for element in line_2.split(' ') if element != '']
    return n, v, p


def read_square_matrix(matrix_file, matrix_size):
    matrix = []
    row_counter = 0
    while row_counter < matrix_size:
        line = matrix_file.readline()
        assert isinstance(line, str)
        if not line.isspace():
            row_counter += 1
            matrix_row = [int(element) for element in line.split(' ') if element not in ['', '\n']]
            matrix.append(matrix_row)
    return np.array(matrix)
