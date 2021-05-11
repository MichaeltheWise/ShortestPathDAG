# -*- coding: utf-8 -*-
"""
Created on Mon May 10 2021

@author: Michael Lin
"""
import collections
import functools


# Decorator
def store(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.edge_list = collections.defaultdict(list)

    def add_edge(self, start, end, weight):
        """
        Add in edges to internal edge default dictionary
        :param start: starting point
        :param end: ending point
        :param weight: edge weight
        :return: None
        """
        self.edge_list[start].append((end, weight))

    def topological_sort(self, val, visited, stack):
        """
        DFS Topological sort
        :param val: starting node
        :param visited: visited tracker
        :param stack: stack
        :return: None
        """
        visited[val] = True
        if val in self.edge_list.keys():
            for node, weight in self.edge_list[val]:
                if not visited[node]:
                    self.topological_sort(node, visited, stack)
        stack.append(val)

    def shortest_path(self, start, end):
        """
        Calculate the shortest path
        :param start: starting point
        :param end: ending point
        :return: The shortest distance to the ending point and the corresponding shortest path
        """
        # If not in range, raise exception
        if end > self.nodes or start < 0:
            raise KeyError("Can't find the starting point or ending point")

        # dist_map records the shortest distance
        # visited records whether the node has been visited or not for topological sort
        # topsort_order collects topological sorted order
        # shortest_path collects the index that has the lowest distance to end point
        dist_map = [float('inf')] * self.nodes
        dist_map[start] = 0
        visited = [False] * self.nodes
        topsort_order = []
        shortest_path = collections.defaultdict(int)

        # Get the topological sorted order
        for i in range(self.nodes):
            if not visited[i]:
                self.topological_sort(start, visited, topsort_order)

        # Having the topological order, find the shortest path
        while topsort_order:
            # Original topological sort algorithm has the order reversed
            # Here we don't need to reverse since we are popping from the back anyway
            curr = topsort_order.pop()
            for node, weight in self.edge_list[curr]:
                # dist_map[node] = min(dist_map[node], dist_map[curr] + weight)
                if dist_map[node] > dist_map[curr] + weight:
                    dist_map[node] = dist_map[curr] + weight
                    # To find the path, store the index that gives us the shortest distance
                    shortest_path[node] = curr

        # Print out the path going backwards
        curr = shortest_path[end]
        res = [end, curr]
        while curr != start:
            res.append(shortest_path[curr])
            curr = shortest_path[curr]
        res.reverse()

        return dist_map[end], res

    def recurse_shortest_path(self, start, end):
        # Use decorator to store the value to speed up top-down recursion result
        @store
        def dist(node):
            if node == end:
                return 0
            # Straight forward implementation, use recursion to check the sum of weight and distance at v
            return min(w + dist(v) for v, w in self.edge_list[node])
        return dist(start)


def main():
    # Test 1
    test_graph = Graph(6)
    test_graph.add_edge(0, 1, 5)
    test_graph.add_edge(0, 2, 3)
    test_graph.add_edge(1, 3, 6)
    test_graph.add_edge(1, 2, 2)
    test_graph.add_edge(2, 4, 4)
    test_graph.add_edge(2, 5, 2)
    test_graph.add_edge(2, 3, 7)
    test_graph.add_edge(3, 4, -1)
    test_graph.add_edge(4, 5, -2)
    d1, path1 = test_graph.shortest_path(1, 5)
    dist_recursion1 = test_graph.recurse_shortest_path(1, 5)
    print("Shortest distance: {}".format(d1))
    print("Shortest path: {}".format(path1))
    print("Shortest distance using recursion: {}".format(dist_recursion1))

    # Test 2
    test_graph2 = Graph(6)
    test_graph2.add_edge(0, 1, 2)
    test_graph2.add_edge(0, 5, 9)
    test_graph2.add_edge(1, 2, 1)
    test_graph2.add_edge(1, 3, 2)
    test_graph2.add_edge(1, 5, 6)
    test_graph2.add_edge(2, 3, 7)
    test_graph2.add_edge(3, 4, 2)
    test_graph2.add_edge(3, 5, 3)
    test_graph2.add_edge(4, 5, 4)
    d2, path2 = test_graph2.shortest_path(0, 5)
    dist_recursion2 = test_graph2.recurse_shortest_path(0, 5)
    print("\nShortest distance: {}".format(d2))
    print("Shortest path: {}".format(path2))
    print("Shortest distance using recursion: {}".format(dist_recursion2))


if __name__ == '__main__':
    main()
