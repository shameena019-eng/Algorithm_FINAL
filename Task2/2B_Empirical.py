import os
import sys
import random
from time import perf_counter

#Erald Jonuzi 001380316-6

# Same import as 2a
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def find_directory_upwards(start_dir, target_name, max_levels=10):
    #search through the filesystem until it finds the clrs folder
    current = start_dir

    for _ in range(max_levels + 1):
        candidate = os.path.join(current, target_name)
        if os.path.isdir(candidate):
            return candidate

        parent = os.path.dirname(current)
        if parent == current: # reached filesystem root
            break
        current = parent

    raise FileNotFoundError(
        f"Could not find directory '{target_name}' within {max_levels} levels above {start_dir}"
    )

#look for the clrs folder above the folder the code is stored in
CLRS_DIR = find_directory_upwards(BASE_DIR, "clrsPython", max_levels=10)

for subfolder in ["Utility functions", "Chapter 20", "Chapter 22", "Chapter 10", "Chapter 6"]:
    sys.path.append(os.path.join(CLRS_DIR, subfolder))

from generate_random_graph import generate_random_graph
from dijkstra import dijkstra


def empirical_performance():
    #test run sizes of graph
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    #How many Dijkstra runs per graph size
    runs_per_size = 20

    #Probability that an edge exists between any pair of vertices
    edge_probability = 0.05

    #Edge weights
    min_weight = 1
    max_weight = 20

    random.seed(1337) #fixed seed for reproducibility

    print("Empirical Performance of Dijkstra on Random Graphs")
    print("N_vertices, average_time_per_dijkstra_seconds")

    for n in sizes:
        # Generate a random graph with n amount of vertices
        graph = generate_random_graph(
            card_V=n,
            edge_probability=edge_probability,
            by_adjacency_lists=True,
            directed=False,
            weighted=True,
            min_weight=min_weight,
            max_weight=max_weight,
        )

        total_time = 0.0

        for i in range(runs_per_size):
            #Choose a random source vertex
            s = random.randrange(n)

            #measure the time dijkstra needs to run
            t0 = perf_counter()
            d, pi = dijkstra(graph, s)
            t1 = perf_counter()

            total_time += (t1 - t0)

        avg_time = total_time / runs_per_size
        print(f"{n}, {avg_time:.9f}")


if __name__ == "__main__":
    empirical_performance()
