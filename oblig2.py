
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


def main():
    movie_lines = read_data("movies.tsv")
    all_movies = {line[0]: Movie(*line[:-1]) for line in movie_lines}

    actor_lines = read_data("actors.tsv")
    all_actors = {line[0]: Actor(*line) for line in actor_lines}

    for actor in all_actors.values():
        for tt_id in actor.movies:
            if tt_id in all_movies:
                all_movies[tt_id].add_actor(actor)

    count_edges = 0
    for movie in all_movies.values():
        count_edges += len(movie.actors)*(len(movie.actors) - 1)/2

    for i,movie in enumerate(all_movies.values()):
        if i > 10:
            break
        print(movie)

    print(len(all_actors))
    print(count_edges)

if __name__ == '__main__':
    main()
