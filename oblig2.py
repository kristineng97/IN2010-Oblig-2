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
    parents = {from_actor: None}
    queue = Queue()
    queue.put(from_actor)
    result = []

    while queue:
        actor = queue.get()
        result.append(actor)
        for other_actor, common_movies in actor.neighbors.items():
            if other_actor == to_actor:
                parents[other_actor] = (actor, next(iter(common_movies)))
                
                return parents

            elif other_actor not in parents:
                parents[other_actor] = (actor, next(iter(common_movies)))
                queue.put(other_actor)

    return parents

def build_path_from_search_results(search_results, from_actor, to_actor):
    """

    Return: List of two-tuples (actor, movie they shared with the actor in the next tuple)
    """
    path = []
    this = (to_actor, None)
    while this is not None:
        path.append(this)
        this = search_results[this[0]]
    
    return path

def find_shortest_path(from_actor, to_actor):
    search_results = breadth_first_search(from_actor, to_actor)
    path = build_path_from_search_results(search_results, from_actor, to_actor)

    return path

def main():
    # Problem 1
    movie_lines = read_data("movies.tsv") # Read lines in movies.tsv to list movie_lines containing [tt_id, title, rating, num. of voices]
    all_movies = {line[0]: Movie(*line[:-1]) for line in movie_lines} # Make a dictionary of all movies with keys tt_id and values is Movie-objects

    actor_lines = read_data("actors.tsv") # Read lines in actors.tsv to list actor_lines containing [nm_id, name, tt_id1, tt_id2, ... etc]
    all_actors = {line[0]: Actor(all_movies, *line) for line in actor_lines} # Make a dictionary of all actors with keys nm_id and values is Actor-objects

    # Loop through all Actor-objects, and for each movie the actor contributes in,
    # first check that this movie is contained in movies.tsv,
    # then go to this movie object and add given actor to actors-list
    for actor in all_actors.values():
        for movie in actor.movies:
            movie.add_actor(actor)

    # Testing:
    #for i,movie in enumerate(all_movies.values()):
    #    if i > 3:
    #        break
    #    print(movie)


    # This gives us a nice way to access all the necessary adjacency relations

    # We want the actors to be the nodes in our graph, so numbers of nodes is the length of all_actors-dict
    # Now we want to count the number of edges in the graph:
    count_edges = 0
    for movie in all_movies.values():
        count_edges += len(movie.actors)*(len(movie.actors) - 1)/2

    # This gives the result:
    print(f"Oppgave 1\n\nNodes: {len(all_actors)}\nEdges: {int(count_edges)}\n")

    actor_pair_ids = [("nm2255973", "nm0000460")
                    , ("nm0424060", "nm0000243")
                    , ("nm4689420", "nm0000365")
                    , ("nm0000288", "nm0001401")
                    , ("nm0031483", "nm0931324")]
    for from_actor_id, to_actor_id in actor_pair_ids:
        from_actor = all_actors[from_actor_id]
        to_actor = all_actors[to_actor_id]

        path = find_shortest_path(from_actor, to_actor)
        for actor, movie in reversed(path):
            if movie is not None:
                print(f"{actor.name}\n==[ {movie.title} ({movie.ranking}) ] ==> ", end="")
            else:
                print(actor.name, "\n")


if __name__ == '__main__':
    main()
