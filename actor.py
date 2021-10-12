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
