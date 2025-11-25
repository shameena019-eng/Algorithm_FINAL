# run_toy_mst.py
# Uses CLRS 4e library modules exactly as in your mst.py
# Place this file alongside the CLRS library modules or add the path to PYTHONPATH.

from Utility_functions.adjacency_list_graph import AdjacencyListGraph
from Chapter_21.mst import kruskal, prim, get_total_weight

import random
import time
import matplotlib.pyplot


labels = ['A', 'B', 'C', 'D', 'E']
index = {v: i for i, v in enumerate(labels)}

edges = [
    ('A', 'B', 4),
    ('A', 'C', 3),
    ('B', 'C', 1),
    ('B', 'D', 2),
    ('C', 'E', 5),
    ('D', 'E', 3),
]

G = AdjacencyListGraph(len(labels), False, True)
for u, v, w in edges:
    G.insert_edge(index[u], index[v], w)

mst_k = kruskal(G)
total_k = get_total_weight(mst_k)

mst_p = prim(G, index['A'])
total_p = get_total_weight(mst_p)


def undirected_edge_list(graph):
    out = []
    for u in range(graph.get_card_V()):
        for e in graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                out.append((labels[u], labels[v], e.get_weight()))
    out.sort(key=lambda t: (t[2], t[0], t[1]))
    return out


mst_edges = undirected_edge_list(mst_k)

mst_set = {(min(a, b), max(a, b)) for (a, b, _) in mst_edges}
closable = []
for (u, v, w) in edges:
    a, b = min(u, v), max(u, v)
    if (a, b) not in mst_set:
        closable.append((a, b, w))
closable.sort(key=lambda t: (t[2], t[0], t[1]))

print("Vertices:", labels)
print("All edges (toy):", sorted([(min(u, v), max(u, v), w) for (u, v, w) in edges], key=lambda t: (t[2], t[0], t[1])))
print("MST (Kruskal):", mst_edges)
print("MST total weight (Kruskal):", total_k)
print("MST total weight (Prim):", total_p)
print("Closable (non-MST) edges:", closable)


# ---------------------------------------------------------------------
# ------------------------------ TASK 4B -------------------------------
# ---------------------------------------------------------------------

# === Helper: build a random weighted undirected graph ===============
def generate_random_graph(n, edge_prob=0.15, max_w=20):
    """
    Generates a random weighted undirected graph using AdjacencyListGraph.
    CLRS-compatible.
    """
    G = AdjacencyListGraph(n, False, True)

    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_prob:
                w = random.randint(1, max_w)
                G.insert_edge(u, v, w)
    return G


# === Part 1: Empirical runtime measurements ==========================
def measure_mst_runtime():
    sizes = list(range(100, 1001, 100))
    runtimes = []

    for n in sizes:
        times = []
        for trial in range(3):  # average over 3 trials
            G = generate_random_graph(n)
            start = time.time()
            mst = kruskal(G)
            end = time.time()
            times.append(end - start)
        avg = sum(times) / len(times)
        runtimes.append(avg)
        print(f"n={n}, avg MST time={avg:.6f}s")

    # === Plot ===
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, runtimes, marker='o')
    plt.title("Task 4b — MST Runtime vs Number of Stations")
    plt.xlabel("Number of stations (n)")
    plt.ylabel("Average computation time (seconds)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return sizes, runtimes


# === Part 2: Real London Underground backbone analysis ===============
# Placeholder until you give me your data loader
def example_placeholder_loader():
    # TODO: replace with your real dataset loading function!
    # Should return: list_of_stations, list_of_edges_as_(u, v, w)
    return ["A", "B", "C"], [("A", "B", 5), ("B", "C", 2)]


def build_real_graph(stations, edges):
    index = {name: i for i, name in enumerate(stations)}
    G = AdjacencyListGraph(len(stations), False, True)

    # If duplicates exist between two stations, keep only min weight
    best = {}
    for u, v, w in edges:
        a, b = min(u, v), max(u, v)
        if (a, b) not in best or w < best[(a, b)]:
            best[(a, b)] = w

    for (u, v), w in best.items():
        G.insert_edge(index[u], index[v], w)
    return G, index


def extract_edge_list(graph, stations):
    out = []
    for u in range(graph.get_card_V()):
        for e in graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                out.append((stations[u], stations[v], e.get_weight()))
    return out


def task4b_real_network():
    print("\n--- Task 4b: Real London Underground Backbone ---\n")

    # === Load real data ===
    stations, edges = example_placeholder_loader()  # <<< replace later
    G, index_map = build_real_graph(stations, edges)

    # === Compute MST ===
    mst = kruskal(G)
    mst_total = get_total_weight(mst)

    # === List MST edges ===
    mst_edges = extract_edge_list(mst, stations)
    mst_set = {(min(a, b), max(a, b)) for (a, b, _) in mst_edges}

    # === Redundant (closable) edges ===
    redundant = []
    for (u, v, w) in edges:
        a, b = min(u, v), max(u, v)
        if (a, b) not in mst_set:
            redundant.append((a, b, w))

    redundant.sort(key=lambda t: (t[2], t[0], t[1]))

    print("Total MST backbone weight:", mst_total)
    print("\nFirst 10 redundant edges:")
    for r in redundant[:10]:
        print("  ", r)

    print("\n(For your report: take a screenshot of this output.)")

    return mst, mst_edges, redundant


# === Entry point for running Task 4b section =========================
if __name__ == "__main__":
    # 1) Experimental runtime graph
    measure_mst_runtime()

    # 2) Real network analysis
    task4b_real_network()
