import networkx as nx
import math
import random
import time
import matplotlib.pyplot as plt
from hopcroftkarp import *
from ford_fulkerson import *


def generate_graph(n, m, p, seed=None, directed=False):
    # return nx.generators.bipartite.bipartite_random_graph(n, m, p, seed=42, directed=False)
    G = nx.Graph()
    G = _add_nodes_with_bipartite_label(G, n, m)
    if directed:
        G = nx.DiGraph(G)
    G.name = "fast_gnp_random_graph(%s,%s,%s)" % (n, m, p)

    if not seed is None:
        random.seed(seed)

    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_bipartite_graph(n, m)

    lp = math.log(1.0 - p)

    v = 0
    w = -1
    while v < n:
        lr = math.log(1.0 - random.random())
        w = w + 1 + int(lr / lp)
        while w >= m and v < n:
            w = w - m
            v = v + 1
        if v < n:
            G.add_edge(v, n + w)

    if directed:
        # use the same algorithm to
        # add edges from the "m" to "n" set
        v = 0
        w = -1
        while v < n:
            lr = math.log(1.0 - random.random())
            w = w + 1 + int(lr / lp)
            while w >= m and v < n:
                w = w - m
                v = v + 1
            if v < n:
                G.add_edge(n + w, v)

    return G


def _add_nodes_with_bipartite_label(G, lena, lenb):
    G.add_nodes_from(range(0,lena+lenb))
    b=dict(zip(range(0,lena),[0]*lena))
    b.update(dict(zip(range(lena,lena+lenb),[1]*lenb)))
    nx.set_node_attributes(G, b, 'bipartite')
    return G


def generate_compare_plots():
    # size = 10000
    size_array = [100,200,300,400,500,600,700,800,900,1000]
    # size_array = [1000]
    prob = 0.5
    hopcroft_karp_time_lst = []
    ford_fulkerson_time_lst = []
    for size in size_array:
        print(size)
        graph = generate_graph(size, size, prob, seed=42)
        adj = {node: set(graph.adj[node].keys()) for node in dict(graph.adj).keys() if node < size}

        start = time.time()
        hopcroft_karp_matching = HopcroftKarp(adj).maximum_matching()
        end = time.time()
        hopcroft_karp_time = end - start
        hopcroft_karp_time_lst.append(hopcroft_karp_time)
        print("Time hopcroft_karp:", hopcroft_karp_time)

        start = time.time()
        ford_fulkerson_matching = GFG(adj, size=size).maximum_matching()
        end = time.time()
        ford_fulkerson_time = end - start
        ford_fulkerson_time_lst.append(ford_fulkerson_time)
        print("Time ford_fulkerson:", ford_fulkerson_time)

    plt.plot(size_array, hopcroft_karp_time_lst, 'r', label='Hopcroft Karp')
    plt.plot(size_array, ford_fulkerson_time_lst, 'b', label='Ford Fulkerson')
    plt.legend(loc='best')
    plt.grid()
    plt.xlabel("#Vertex")
    plt.ylabel("Time")
    plt.title("Running Time")
    plt.savefig("compare_algorithms.png")
    plt.show()


if __name__ == '__main__':
    # size = 10
    # prob = 0.5
    # # for size in range(10, 500, 20):
    # #     for prob in [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 0.5]:
    #
    # graph = generate_graph(size, size, prob, seed=42)
    # adj = {node: set(graph.adj[node].keys()) for node in dict(graph.adj).keys() if node < size}
    # # print("adj: ",adj)
    #
    # start = time.time()
    # hopcroft_karp_matching = HopcroftKarp(adj).maximum_matching()
    # # print("Hopcroft Karp:", hopcroft_karp_matching)
    # # print("Hopcroft Karp len =",len(hopcroft_karp_matching))
    # print("Time:",time.time() - start)
    #
    # start = time.time()
    # ford_fulkerson_matching = GFG(adj, size=size).maximum_matching()
    # # print("Ford Fulkerson:", ford_fulkerson_matching)
    # # print("Ford Fulkerson len =", len(ford_fulkerson_matching))
    # print("Time:", time.time() - start)
    # # print()
    # print("size:",size,"prob:",prob,"same:",len(hopcroft_karp_matching)==len(ford_fulkerson_matching))

    import sys
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(1500)

    generate_compare_plots()
