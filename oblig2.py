from queue import Queue
from heapq import heappush, heappop
from collections import defaultdict

from actor import Actor
from movie import Movie
from traverse import dijkstra, breadth_first_search, build_path
from components import find_all_components

def read_data(filename="movies.tsv"):
    l = []
    with open(filename, "r") as infile:
        for line in infile:
            l.append(line.strip().split("\t"))
    return l


def main():
    # Problem 1

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

    print(f"Oppgave 1\n\nNodes: {len(all_actors)}\nEdges: {int(count_edges)}\n")

    # Problem 2
    # We then want to verify that our graph works correctly by checking that it
    # can find the shortest path between specific actors
    print("Oppgave 2\n")
    actor_pair_ids = [("nm2255973", "nm0000460")
                    , ("nm0424060", "nm0000243")
                    , ("nm4689420", "nm0000365")
                    , ("nm0000288", "nm0001401")
                    , ("nm0031483", "nm0931324")]
    for from_actor_id, to_actor_id in actor_pair_ids:
        from_actor = all_actors[from_actor_id]
        to_actor = all_actors[to_actor_id]

        search_results = breadth_first_search(from_actor, to_actor)
        path = build_path(search_results, from_actor, to_actor)
        # path = double_ended_breadth_first_search(from_actor, to_actor)

        for actor, next_actor in zip(path[:-1], path[1:]):
            movie = next(iter(actor.neighbors[next_actor]))
            print(f"{actor.name}\n==[ {movie.title} ({movie.ranking}) ] ==> ",
                  end="")
        print(path[-1].name)
        print()

    # Problem 3

    print("\nOppgave 3\n")
    for from_actor_id, to_actor_id in actor_pair_ids:
        from_actor = all_actors[from_actor_id]
        to_actor = all_actors[to_actor_id]

        path = dijkstra(from_actor, to_actor)[0]
        total_weight = dijkstra(from_actor, to_actor)[1]

        for actor, next_actor in zip(path[:-1], path[1:]):
            movie = actor.best_movie(next_actor)
            print(f"{actor.name}\n==[ {movie.title} ({movie.ranking}) ] ==> ",
                end="")
        print(path[-1].name)
        print(f"Total weight: {total_weight:.1f}\n")


    # Problem 4
    print("\nOppgave 4\n")
    from_actor = all_actors["nm0031483"]
    all_components = find_all_components(all_actors)

    for key, value in reversed(sorted(dict(all_components).items())):
        print(f"There are {value} components of size {key}")


if __name__ == '__main__':
    main()
