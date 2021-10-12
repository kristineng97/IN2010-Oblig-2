from queue import Queue
from heapq import heappush, heappop
import heapq
from collections import defaultdict

def read_data(filename="movies.tsv"):
    l = []
    with open(filename, "r") as infile:
        for line in infile:
            l.append(line.strip().split("\t"))
    return l


class Movie:
    def __init__(self, tt_id, title, ranking):
        self.tt_id = tt_id
        self.title = title
        self.ranking = float(ranking)
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def __str__(self):
        return f"{self.title}"

    def __lt__(self, other_movie):
        return self.weight < other_movie.weight

    @property
    def weight(self):
        return 10 - self.ranking

class Actor:
    def __init__(self, all_movies, nm_id, name, *movies):
        self.nm_id = nm_id
        self.name = name
        self.movies = [all_movies[tt_id] for tt_id in movies if tt_id in all_movies]
        self.best_movie_neighbors = {}

    @property
    def neighbors(self):
        if "_neighbors" in self.__dict__:
            return self._neighbors
        else:
            self._neighbors = {}
            self.build_adjacency()
            return self._neighbors

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other_actor):
        return self.nm_id == other_actor.nm_id

    def __hash__(self):
        return self.nm_id.__hash__()

    def __lt__(self, other_actor):
        """Just for sorting in heap, where order really doesn't matter when they have the same cost"""
        return True

    def build_adjacency(self):
        for movie in self.movies:
            other_actors = (o_actor for o_actor in movie.actors if o_actor != self)
            for other_actor in other_actors:
                if other_actor not in self._neighbors:
                    self._neighbors[other_actor] = {movie}
                else:
                    self._neighbors[other_actor].add(movie)

    def best_movie(self, other_actor):
        if other_actor in self.best_movie_neighbors:
            return self.best_movie_neighbors[other_actor]
        else:
            prevcount = 10
            count = 10
            if other_actor in self.neighbors:
                for movie in self.neighbors[other_actor]:
                    count = min(movie.weight, count)
                    if count < prevcount:
                        self.best_movie_neighbors[other_actor] = movie
                    prevcount = count
            else:
                raise AssertionError (f'Not neighbors {self.name} and {other_actor.name} are not neighbors')
            return self.best_movie_neighbors[other_actor]

def breadth_first_search(from_actor, to_actor):
    """BFS that starts at from_actor, and stops if to_actor is found.

    Return:
        Dictionary with actors as keys, parent actors as values.
    """
    parents = {from_actor: None}
    queue = Queue()
    queue.put(from_actor)

    while queue.qsize():
        actor = queue.get()
        for other_actor in actor.neighbors:
            if other_actor not in parents:
                parents[other_actor] = actor
                queue.put(other_actor)

                if other_actor == to_actor:
                    return parents

    return parents

# def double_ended_breadth_first_search(from_actor, to_actor):
#     """Searches for a path between two actors, by doing a BFS from both sides.

#     Return:
#         List of two-tuples
#             (actor, movie they shared with the actor in the next tuple)
#         The list is empty if there is no path between them
#     """

#     parents = {"from": {from_actor: None}, "to": {to_actor: None}}
#     finished = False
#     this_queue = {"from": None, "to": None}
#     next_queue = {"from": Queue(), "to": Queue()}
#     next_queue["from"].put(from_actor)
#     next_queue["to"].put(to_actor)

#     while not finished:
#         for source in ["from", "to"]:
#             this_queue[source] = next_queue[source]
#             next_queue[source] = Queue()

#             actor = this_queue[source].get()
#             for other_actor in actor.neighbors:
#                 if other_actor not in parents[source]:
#                     parents[source][other_actor] = actor
#                     next_queue[source].put(other_actor)

#                     if source == "to" and other_actor in parents["from"]:
#                         middle_actor = other_actor
#                         finished = True
#                         break


#     path = build_path(parents["from"], from_actor, middle_actor) \
#          + build_path(parents["to"], middle_actor, to_actor)

#     return path


def build_path(search_results, from_actor, to_actor):
    """Takes the result from breadth_first_search and makes a list of the path.

    Return:
        List of actors starting with from_actor and ending with to_actor
    """
    path = []
    this_actor = to_actor
    while this_actor is not None:
        path.append(this_actor)
        this_actor = search_results[this_actor]

    return list(reversed(path))


def dijkstra(from_actor, to_actor):
    """
    Function returning the shortest path for a
    weighted graph, using Dijkstra's algorithm.
    """
    heap = [(0, from_actor)]
    best_path = {from_actor: []}
    best_path_cost = defaultdict(lambda: float('inf'))
    best_path_cost[from_actor] = 0

    while heap:
        cost, actor = heappop(heap)
        if cost >= best_path_cost[to_actor]:
            break
        for other_actor in actor.neighbors:
            total_cost = cost + actor.best_movie(other_actor).weight
            if total_cost < best_path_cost[other_actor]:
                best_path_cost[other_actor] = total_cost
                heappush(heap, (total_cost, other_actor))
                best_path[other_actor] = best_path[actor] + [actor]

    return best_path[to_actor] + [to_actor], best_path_cost[to_actor]

def find_components(from_actor, not_visited):
    count_comp = 1
    queue = Queue()
    queue.put(from_actor)
    not_visited.remove(from_actor)

    while queue.qsize():
        actor = queue.get()
        for other_actor in actor.neighbors:
            if other_actor in not_visited:
                not_visited.remove(other_actor)
                queue.put(other_actor)
                count_comp += 1

    return count_comp

def find_all_components(all_actors):
    not_visited = set(all_actors.copy().values())
    all_components = defaultdict(lambda: 0)
    while not_visited:
        actor = next(iter(not_visited))
        count_comp = find_components(actor, not_visited)
        all_components[count_comp] += 1

    return all_components




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
