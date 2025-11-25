import csv
import heapq
import time
import os
from collections import defaultdict

DATA_FILEPATH = "London_Underground_data.csv"
DELIMITER = ','

def load_underground_graph(filepath):
    """
    Reads the London Underground data CSV and builds the graph using a
    'dictionary of dictionaries' (Adjacency List structure).
    """
    print(f"Attempting to load data from: {os.path.abspath(filepath)}")

    graph = defaultdict(dict)
    encodings_to_try = ['utf-8', 'latin-1']
    connection_count = 0

    # Loop through encodings until one succeeds
    for encoding in encodings_to_try:
        try:
            # 1. Open the file: 'with' ensures the file is closed automatically
            with open(filepath, mode='r', newline='', encoding=encoding) as file:

                # 2. Initialize the CSV reader using the explicit DELIMITER setting
                reader = csv.reader(file, delimiter=DELIMITER)

                # 3. Skip the header row and get the actual data
                try:
                    next(reader)
                except StopIteration:
                    print("Warning: CSV file appears empty or has no header.")
                    return defaultdict(dict)

                print(f"Successfully opened and reading with encoding: {encoding}")

                # 4. PROCESS THE DATA
                for row in reader:
                    # We expect a row structure: [Line, Station A, Station B, Time, ...]
                    if len(row) < 4:
                        continue

                    # Access the correct columns (indices 1, 2, and 3)
                    station_a = row[1].strip()
                    station_b = row[2].strip()
                    time_str = row[3].strip()

                    if station_a and station_b and time_str:
                        try:

                            time_cost = int(time_str)

                            graph[station_a][station_b] = time_cost
                            graph[station_b][station_a] = time_cost
                            connection_count += 1

                        except ValueError:
                            continue


                break

        except FileNotFoundError:
            print(
                f"ERROR: File not found at '{os.path.abspath(filepath)}'. Please ensure the file is named '{DATA_FILEPATH}'.")
            return defaultdict(dict)

        except UnicodeDecodeError as e:
            if encoding == encodings_to_try[-1]:
                raise e
            print(
                f"Warning: Failed to decode with {encoding}. Retrying with {encodings_to_try[encodings_to_try.index(encoding) + 1]}...")
            continue
        except Exception as e:
            # Catch any remaining unexpected errors, like the binary data issue
            print(
                f"An unexpected error occurred during data loading: {e}. Check if the file is a true CSV (plain text).")
            return defaultdict(dict)

    if not graph:
        print("Error: Graph is empty after processing data. Check CSV format.")
        return defaultdict(dict)

    print(f"Graph built successfully. Total unique stations: {len(graph)}. Total connections: {connection_count}")
    return graph


def dijkstra_shortest_path(graph, start_station):
    """
    Implements Dijkstra's algorithm to find the shortest time path from a start station.
    """
    if start_station not in graph:
        raise ValueError(f"Start station '{start_station}' not found in the graph.")

    distances = {station: float('inf') for station in graph}
    distances[start_station] = 0
    predecessors = {}
    priority_queue = [(0, start_station)]

    while priority_queue:
        current_distance, current_station = heapq.heappop(priority_queue)

        if current_distance > distances[current_station]:
            continue

        for neighbor, weight in graph[current_station].items():
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_station
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, predecessors


def find_shortest_path(graph, start_station, end_station):
    """
    Executes Dijkstra's and reconstructs the path.
    """
    if start_station not in graph or end_station not in graph:
        return [], 0

    distances, predecessors = dijkstra_shortest_path(graph, start_station)
    total_time = distances.get(end_station, float('inf'))
    if total_time == float('inf'):
        return [], 0

    path = []
    current = end_station

    while current != start_station:
        if current not in predecessors:
            return [], 0
        path.insert(0, current)
        current = predecessors[current]

    path.insert(0, start_station)

    return path, total_time


def main():
    """
    Main execution block for demonstrating the journey planner.
    This runs multiple tests for the Task 3b report.
    """
    print("--- COMP 1828 Journey Planner (Task 3 Solution) ---")

    underground_graph = load_underground_graph(DATA_FILEPATH)

    if not underground_graph:
        print("Failed to load graph. Exiting.")
        return

    test_journeys = [
        ("Harrow & Wealdstone", "Elephant & Castle"),  # Long journey test
        ("King's Cross St. Pancras", "Oxford Circus"),  # Central short journey test
        ("Cockfosters", "Brixton"),  # Complex, multi-line journey
    ]

    print("\n" + "=" * 50)
    print("Beginning Empirical Performance Testing")
    print("=" * 50)

    for start, end in test_journeys:
        print(f"\nPLANNING JOURNEY: {start} -> {end}")

        start_time = time.perf_counter()
        path, total_time = find_shortest_path(underground_graph, start, end)
        end_time = time.perf_counter()
        runtime = (end_time - start_time) * 1000  # Time in milliseconds

        if path:
            print("-" * 25)
            print(f"Path Found ({len(path)} stops):")
            print(" -> ".join(path))
            print(f"Total Travel Time: {total_time} minutes")
            print(f"Execution Time (Dijkstra's + Reconstruction): {runtime:.4f} ms")
            print("-" * 25)
        else:
            print(f"Result: Path not found from {start} to {end}.")
            print("-" * 25)


if __name__ == "__main__":
    main()
