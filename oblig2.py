
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
        return f"{self.title} ({self.tt_id}): {' | '.join([str(actor) for actor in self.actors])}"


class Actor:
    def __init__(self, nm_id, name, *movies):
        self.nm_id = nm_id
        self.name = name
        self.movies = movies

    def __str__(self):
        return f"{self.name}:{self.movies}"


def shortest_path(E, nmid1, nmid2):
    parents = {nmid1: none}
    queue = deque([nmid1])
    result = []

    while queue:
        v = deque.popleft(queue)
        result.append(v)
        for u in E[v]:
            if u not in parents:
                parents[u] = v
                queue.append(u)
    return parents





def main():
    # Problem 1
    movie_lines = read_data("movies.tsv") # Read lines in movies.tsv to list movie_lines containing [tt_id, title, rating, num. of voices]
    all_movies = {line[0]: Movie(*line[:-1]) for line in movie_lines} # Make a dictionary of all movies with keys tt_id and values is Movie-objects

    actor_lines = read_data("actors.tsv") # Read lines in actors.tsv to list actor_lines containing [nm_id, name, tt_id1, tt_id2, ... etc]
    all_actors = {line[0]: Actor(*line) for line in actor_lines} # Make a dictionary of all actors with keys nm_id and values is Actor-objects

    # Loop through all Actor-objects, and for each movie the actor contributes in,
    # first check that this movie is contained in movies.tsv,
    # then go to this movie object and add given actor to actors-list
    for actor in all_actors.values():
        for tt_id in actor.movies:
            if tt_id in all_movies:
                all_movies[tt_id].add_actor(actor)
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

    # Problem 2
    for movie in all_movies.values():
        for actor in movie.actors:
            movie.actors.remove(actor)
            adj_l = [actress.nm_id for actress in movie.actors]
            E = {actor.nm_id: adj_l}
            movie.actors.append(actor)

    print(E["nm0353790"])



if __name__ == '__main__':
    main()
