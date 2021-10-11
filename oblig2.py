from queue import Queue

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
        self.ranking = ranking
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def __str__(self):
        return f"{self.title}"


class Actor:
    def __init__(self, all_movies, nm_id, name, *movies):
        self.nm_id = nm_id
        self.name = name
        self.movies = [all_movies[tt_id] for tt_id in movies if tt_id in all_movies]

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

    def build_adjacency(self):
        for movie in self.movies:
            other_actors = (o_actor for o_actor in movie.actors if o_actor != self)
            for other_actor in other_actors:
                if other_actor not in self._neighbors:
                    self._neighbors[other_actor] = {movie}
                else:
                    self._neighbors[other_actor].add(movie)


def breadth_first_search(from_actor, to_actor):
    """BFS that starts at from_actor, and stops if to_actor is found.

    Return:
        Dictionary with actors as keys, parent actors as values.
    """
    parents = {from_actor: None}
    queue = Queue()
    queue.put(from_actor)

    while queue:
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

    # We then want to verify that our graph works correctly by checking that it
    # can find the shortest path between specific actors
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


if __name__ == '__main__':
    main()
