import os
import sys
import csv
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
        if parent == current:   # reached filesystem root
            break
        current = parent

    raise FileNotFoundError(
        f"Could not find directory '{target_name}' within {max_levels} levels above {start_dir}"
    )

#look for the clrs folder above the folder the code is stored in
CLRS_DIR = find_directory_upwards(BASE_DIR, "clrsPython", max_levels=10)

for subfolder in ["Utility functions", "Chapter 20", "Chapter 22", "Chapter 10", "Chapter 6"]:
    sys.path.append(os.path.join(CLRS_DIR, subfolder))

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from print_path import print_path

def load_london_graph(csv_path):
    edges = []           # (station1_name, station2_name, time)
    station_set = set()  #to gather unique station names only (minimise repeats)

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)   # skip header: Station1, Station2, Time

        for row in reader:
            s1, s2, t = row[0].strip(), row[1].strip(), float(row[2])
            edges.append((s1, s2, t))
            station_set.add(s1)
            station_set.add(s2)

    #map the station name to an index, in alphabetical order
    stations = sorted(list(station_set))
    name_to_index = {name: idx for idx, name in enumerate(stations)}

    #initialise the graph
    n = len(stations)
    graph = AdjacencyListGraph(card_V=n, directed=False, weighted=True)

    #insert edges in to the graph
    for s1, s2, t in edges:
        u = name_to_index[s1]
        v = name_to_index[s2]
        graph.insert_edge(u, v, weight=t)

    return graph, stations, name_to_index

def run_dijkstra():
    csv_path = os.path.join(BASE_DIR, "london_underground_data.csv")

    graph, stations, name_to_index = load_london_graph(csv_path)

    #start and end station to be calculated
    start_station = "Finsbury Park"
    dest_station  = "Cockfosters"

    if start_station not in name_to_index or dest_station not in name_to_index:
        print("One of the station names does not exist in the CSV.")
        return

    s = name_to_index[start_station]
    t = name_to_index[dest_station]

    #call and run dijkstra
    t0 = perf_counter()
    d, pi = dijkstra(graph, s)
    t1 = perf_counter()

    #Extract travel time
    total_time = d[t]

    # Convert index path into the station name path
    route = print_path(pi, s, t, lambda i: stations[i])

    print("\nLondon Underground Shortest Path")
    print(f"Start:       {start_station}")
    print(f"Destination: {dest_station}")
    print(f"Total time:  {total_time} minutes")
    print(f"Route:       {' -> '.join(route)}")
    print(f"Runtime:     {(t1 - t0):.7f} seconds\n")

if __name__ == "__main__":
    run_dijkstra()
