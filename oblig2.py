import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import graphviz
import os
import string


def read_data(filename="movies.tsv"):
    l = []
    with open("movies.tsv", "r") as infile:
        for line in infile:
            l.append(line.strip().split("\t"))
    return l[:10]




class Movie:
    def __init__(self, tt_id, title, ranking):
        self.tt_id = tt_id
        self.title = title
        self.ranking = ranking
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)

class Actor:
    def __init__(self, nm_id, name, *movies):
        self.nm_id = nm_id
        self.name = name
        self.movies = movies




def main():
    movie_lines = read_data("movies.tsv")
    movies = [Movie(*line[:-1]) for line in movie_lines]

    actor_lines = read_data("actors.tsv")
    actors = [Actor(*line) for line in actor_lines]

    








if __name__ == '__main__':
    main()
