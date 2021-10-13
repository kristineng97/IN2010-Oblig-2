from collections import defaultdict

class Actor:
    def __init__(self, all_movies, nm_id, name, *movies):
        self.nm_id = nm_id
        self.name = name
        self.movies = [all_movies[tt_id] for tt_id in movies if tt_id in all_movies]
        self.best_movie_neighbors = {}

    @property
    def neighbors(self):
        """Returns adjacency information, possibly after computing it

        `neighbors` is on the form
            {other_actor: [movies, they, have, played, together, in]}
        """
        if "_neighbors" in self.__dict__:
            return self._neighbors
        else:
            self._neighbors = defaultdict(lambda: set())
            self._build_adjacency()
            self._neighbors = dict(self._neighbors)
            return self._neighbors

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other_actor):
        return self.nm_id == other_actor.nm_id

    def __hash__(self):
        return self.nm_id.__hash__()

    def __lt__(self, other_actor):
        """Just for sorting in heap, when cost is the same.

        When stored in a heap like [(cost, actor)], we need some way of sorting
        tuples with the same cost. Since this order doesn't matter to us, we use
        this method to just pick an arbitrary element and put it first.
        """
        return True

    def _build_adjacency(self):
        """Finds neighbors of self by going through movies self has played in.

        The `Movie` objects stores a list of all actors playing in that movie.
        """
        for movie in self.movies:
            other_actors = (actor for actor in movie.actors if actor != self)
            for other_actor in other_actors:
                self._neighbors[other_actor].add(movie)

    def best_movie(self, other_actor):
        """Finds the best movie self and other_actor both star in"""

        if other_actor in self.best_movie_neighbors:
            return self.best_movie_neighbors[other_actor]
        else:
            assert other_actor in self.neighbors, \
                   f"{self.name} and {other.name} are not neighbors"
            
            prevcount = 10
            count = 10
            for movie in self.neighbors[other_actor]:
                count = min(movie.weight, count)
                if count < prevcount:
                    self.best_movie_neighbors[other_actor] = movie
                prevcount = count
            
            return self.best_movie_neighbors[other_actor]
