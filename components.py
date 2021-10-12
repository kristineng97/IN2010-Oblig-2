from queue import Queue
from collections import defaultdict

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
