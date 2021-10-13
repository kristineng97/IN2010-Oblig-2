from queue import Queue
from heapq import heappush, heappop
from collections import defaultdict
import time

from actor import Actor
from movie import Movie
from traverse import dijkstra, breadth_first_search, double_ended_breadth_first_search
from components import find_all_components

def read_data(filename="movies.tsv"):
    l = []
    with open(filename, "r") as infile:
        for line in infile:
            l.append(line.strip().split("\t"))
    return l

def main():
    BOLD = '\033[1m'
    END = '\033[0m'

    # Problem 1
    start = time.time()
    timings = []

    # Read lines in movies.tsv to list movie_lines containing
    # [tt_id, title, rating, num. of voices]
    movie_lines = read_data("movies.tsv")
    # Make a dict of all movies with keys tt_id and values is Movie-objects
    all_movies = {line[0]: Movie(*line[:-1]) for line in movie_lines}

    # Read lines in actors.tsv to list actor_lines containing
    # [nm_id, name, tt_id1, tt_id2, ... etc]
    actor_lines = read_data("actors.tsv")
    # Make a dict of all actors with keys nm_id and values is Actor-objects
    all_actors = {line[0]: Actor(all_movies, *line) for line in actor_lines}

    # Loop through all Actor-objects, and for each movie the actor contributes
    # in, go to this movie object and add given actor to actors-list
    for actor in all_actors.values():
        for movie in actor.movies:
            movie.add_actor(actor)

    # We want the actors to be the nodes in our graph, so numbers of nodes is
    # the length of all_actors-dict. The edges are the movies they play together
    # in, so we count these by summing the number of edges in each movies fully
    # connected graph of actors
    count_edges = 0
    for movie in all_movies.values():
        count_edges += len(movie.actors)*(len(movie.actors) - 1)/2

    print(f"\n\n{BOLD}Oppgave 1{END}\n\nNodes: {len(all_actors)}\nEdges: {int(count_edges)}\n")
    timings.append(time.time() - start)

    # Problem 2
    # We then want to verify that our graph works correctly by checking that it
    # can find the shortest path between specific actors
    print(f"\n{BOLD}Oppgave 2{END}\n")
    start = time.time()
    
    actor_pair_ids = [("nm2255973", "nm0000460"),
                      ("nm0424060", "nm0000243"),
                      ("nm4689420", "nm0000365"),
                      ("nm0000288", "nm0001401"),
                      ("nm0031483", "nm0931324")]
    for from_actor_id, to_actor_id in actor_pair_ids:
        from_actor = all_actors[from_actor_id]
        to_actor = all_actors[to_actor_id]

        # Here, we have two implementations of breadth first search to find
        # the path between two actors. The first is a simple implementation,
        # while the second one searches from both sides and thus saves time
        # if each actor has many neighbors. The simple implementation is:
        # path = breadth_first_search(from_actor, to_actor)
        # While the double ended implementation is:
        path = double_ended_breadth_first_search(from_actor, to_actor)

        for actor, next_actor in zip(path[:-1], path[1:]):
            movie = next(iter(actor.neighbors[next_actor]))
            print(f"{actor.name}\n==[ {movie.title} ({movie.ranking}) ] ==> ",
                  end="")
        print(path[-1].name, "\n")
    timings.append(time.time() - start)


    # Problem 3
    print(f"\n{BOLD}Oppgave 3{END}\n")
    start = time.time()
    
    # Go through the same actors as in problem 2, but this time finding the path
    # through a weighted graph, with 10 - rating being the weight of each movie
    for from_actor_id, to_actor_id in actor_pair_ids:
        from_actor = all_actors[from_actor_id]
        to_actor = all_actors[to_actor_id]

        path, total_weight = dijkstra(from_actor, to_actor)

        for actor, next_actor in zip(path[:-1], path[1:]):
            movie = actor.best_movie(next_actor)
            print(f"{actor.name}\n==[ {movie.title} ({movie.ranking}) ] ==> ",
                  end="")
        print(path[-1].name)
        print(f"Total weight: {total_weight:.1f}\n")
    timings.append(time.time() - start)

    # Problem 4
    print(f"\n{BOLD}Oppgave 4{END}\n")
    start = time.time()
    
    # We here want to find how many components of different sizes there are
    all_components = find_all_components(all_actors)

    for key, value in reversed(sorted(dict(all_components).items())):
        print(f"There are {value} components of size {key}")
    timings.append(time.time() - start)
    
    print(f"\n{BOLD}Timinger{END}\n")
    for i, timing in enumerate(timings):
        print(f"Oppgave {i+1} tok {timing:.5f} sekunder.")
    print(f"Totalt tok det altså {sum(timings):.2f} sekunder.")

if __name__ == '__main__':
    main()
