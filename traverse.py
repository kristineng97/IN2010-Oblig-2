from queue import Queue
from heapq import heappush, heappop
from collections import defaultdict

def breadth_first_search(from_actor, to_actor):
    """BFS that starts at from_actor, and stops if to_actor is found.

    Return:
        List of actors starting with from_actor and ending with to_actor
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

    return build_path(parents, from_actor, to_actor)

def double_ended_breadth_first_search(from_actor, to_actor):
    """Searches for a path between two actors, by doing a BFS from both sides.

    Loops around the from_actor and to_actor interchangingly until a middle 
    actor, some actor that can be reached from both initial actors is found. To
    do this we have to keep track of some extra queues, and it gets a bit more
    complicated, but works quite a lot faster than the single ended approach.

    Return:
        List of actors starting with from_actor and ending with to_actor
    """
    parents = {"from": {from_actor: None}, "to": {to_actor: None}}
    this_queue = {"from": None, "to": None}
    next_queue = {"from": Queue(), "to": Queue()}
    next_queue["from"].put(from_actor)
    next_queue["to"].put(to_actor)

    while next_queue["from"].qsize() or next_queue["to"].qsize():
        for source, other_source in zip(["from", "to"], ["to", "from"]):
            this_queue[source] = next_queue[source]
            next_queue[source] = Queue()

            while this_queue[source].qsize():
                actor = this_queue[source].get()
                for other_actor in actor.neighbors:
                    if other_actor not in parents[source]:
                        parents[source][other_actor] = actor
                        next_queue[source].put(other_actor)

                        if other_actor in parents[other_source]:
                            from_path = build_path(parents["from"], from_actor,
                                                   other_actor)
                            to_path = build_path(parents["to"], to_actor,
                                                 other_actor)
                            return from_path + list(reversed(to_path))[1:]


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
    """Finds shortest path for a weighted graph, using Dijkstra's algorithm.

    Stops when the currently found path to the to_actor is the path with the
    lowest cost.

    Return:
        Two-tuple with:
            List of actors starting with from_actor and ending with to_actor
            The associated cost of the path
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
