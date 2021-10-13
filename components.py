from queue import Queue
from collections import defaultdict

def find_components(actor, not_visited):
    """Count the number of nodes in the same component as actor
    
    As a side effect, all actors in the same node as actor is removed from
    `not_visited`.
    """
    count_comp = 1
    queue = Queue()
    queue.put(actor)
    not_visited.remove(actor)

    while queue.qsize():
        actor = queue.get()
        for other_actor in actor.neighbors:
            if other_actor in not_visited:
                not_visited.remove(other_actor)
                queue.put(other_actor)
                count_comp += 1

    return count_comp

def find_all_components(all_actors):
    """Find all components, and count nodes in all of them"""
    not_visited = set(all_actors.copy().values())
    all_components = defaultdict(lambda: 0)
    while not_visited:
        actor = next(iter(not_visited))
        count_comp = find_components(actor, not_visited)
        all_components[count_comp] += 1

    return all_components
