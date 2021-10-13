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

    @property
    def weight(self):
        return 10 - self.ranking
