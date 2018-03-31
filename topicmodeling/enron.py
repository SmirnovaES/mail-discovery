import numpy as np
from topicmodeling.lib.visualization.visualizer import Visualizer


def main():
    a = np.ones((5, 4)) * np.arange(1, 5)
    b = (np.ones((2, 4)) / 4)
    dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
    l = [('a', 0.25), ('b', 0.25), ('c', 0.25), ('d', 0.25)]
    terms = [l for i in range(a.shape[0])]

    Visualizer(b, a, dict, terms)\
        .run('/home/geras-artem/Desktop', metrics='coherence')

if __name__ == '__main__':
    main()
