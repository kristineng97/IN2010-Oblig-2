from queue import Queue
from heapq import heappush, heappop
from collections import defaultdict

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

def double_ended_breadth_first_search(from_actor, to_actor):
    """Searches for a path between two actors, by doing a BFS from both sides.

    Return:
        List of two-tuples
            (actor, movie they shared with the actor in the next tuple)
        The list is empty if there is no path between them
    """

    parents = {"from": {from_actor: None}, "to": {to_actor: None}}
    finished = False
    this_queue = {"from": None, "to": None}
    next_queue = {"from": Queue(), "to": Queue()}
    next_queue["from"].put(from_actor)
    next_queue["to"].put(to_actor)

    while not finished:
        for source in ["from", "to"]:
            this_queue[source] = next_queue[source]
            next_queue[source] = Queue()

            while this_queue[source].qsize():
                actor = this_queue[source].get()
                for other_actor in actor.neighbors:
                    if other_actor not in parents[source]:
                        parents[source][other_actor] = actor
                        next_queue[source].put(other_actor)

                        if source == "to" and other_actor in parents["from"]:
                            middle_actor = other_actor


                            path = build_path(parents["from"], from_actor, middle_actor) \
                                 + list(reversed(build_path(parents["to"], to_actor, middle_actor)))[1:]

                            return path

    return path


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
