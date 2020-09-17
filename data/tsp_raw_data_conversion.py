import os
import numpy as np
import math
import pandas as pd

# Working directory should always be /lqubo/

data_path = 'data/tsp_raw_data'


def calculate_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


def parse_sln_file(sln_file):
    with open(os.path.join(data_path, sln_file), mode='r') as file:
        line_1 = file.readline()
        assert isinstance(line_1, str)
        v = [float(element) for element in line_1.split(' ') if element != '']
    return v


def parse_dat_file(dat_file):
    with open(os.path.join(data_path, dat_file).replace('\\', '/'), mode='r') as file:
        points = []
        num_points = int(dat_file.replace('tsp_', '').replace('.dat', ''))
        row_counter = 0
        while row_counter < num_points:
            line = file.readline()
            assert isinstance(line, str)
            if not line.isspace():
                row_counter += 1
                x_y_coordinates = [int(element) for element in line.split(' ') if element not in ['', '\n']]
                points.append(x_y_coordinates)
    return points


def form_distance_matrix(points):
    num_points = len(points)
    matrix = np.zeros((num_points, num_points))

    for i in range(num_points):
        for j in range(i+1, num_points):
            matrix[i][j] = calculate_distance(points[i][0], points[i][1], points[j][0], points[j][1])
            matrix[j][i] = matrix[i][j]

    return matrix


# domain = [i for i in range(4, 21)]
domain = list(range(4, 21))

for instance in domain:
    dat_file_path = 'tsp_' + str(instance) + '.dat'
    sln_file_path = 'tsp_' + str(instance) + '.sln'

    points_set = parse_dat_file(dat_file=dat_file_path)
    distance_matrix = form_distance_matrix(points_set)

    solution = [parse_sln_file(sln_file=sln_file_path)]
    n = [instance]

    distance_matrix_df = pd.DataFrame(data=distance_matrix)
    solution_df = pd.DataFrame({'solution': solution})

    distance_matrix_df.to_csv('./data/tsp_data/tsp_distance_' + str(instance) + '.csv')
    solution_df.to_csv('./data/tsp_data/tsp_solution_' + str(instance) + '.csv')




