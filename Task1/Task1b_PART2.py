import os
import sys
import csv

# Point Python at the CLRS folders
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

# Add CLRS chapter folders to path
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 10"))

# Import CLRS chained hash table
from chained_hashtable import ChainedHashTable


# Simple hash function (doesn't require miller_rabin)
def simple_hash(key):
    hash_val = 0
    for char in str(key):
        hash_val = (hash_val * 31 + ord(char))
    return abs(hash_val)


class LondonUndergroundStatusSystem:

    def __init__(self, table_size):
        self.operational_stations = ChainedHashTable(table_size, hash_func=simple_hash)
        self.table_size = table_size
        self.station_count = 0

    def mark_operational(self, station_name):
        normalised_name = station_name.strip()
        self.operational_stations.insert(normalised_name)
        self.station_count += 1

    def check_status(self, station_name):
        normalised_name = station_name.strip()
        result = self.operational_stations.search(normalised_name)

        if result is not None:
            return f"Operational"
        else:
            return f"Not Found"


def find_next_prime(n):
    """Find the next prime number >= n."""

    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n


def extract_stations_from_csv(filename):
    """Extract unique station names from CSV file."""
    unique_stations = set()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Extract station from column 2
                if len(row) >= 2:
                    station1 = row[1].strip()
                    if station1:
                        unique_stations.add(station1)

                # Extract station from column 3
                if len(row) >= 3:
                    station2 = row[2].strip()
                    if station2:
                        unique_stations.add(station2)

        return sorted(list(unique_stations))

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
        return []


def main():
    print("LONDON UNDERGROUND STATION STATUS SYSTEM")
    print("Using CLRS Chained Hash Table (Chapter 11)")
    print()

    # STEP 1: DATA ACQUISITION
    print("STEP 1: DATA ACQUISITION")
    print("Method: Python CSV parsing script")
    print("Description: Extracts station names from CSV columns 2 and 3,")
    print("             uses Python set to eliminate duplicates, then sorts.")
    print()

    csv_filename = os.path.join(PROJECT_ROOT, "data", "London_Underground_data.csv")
    stations = extract_stations_from_csv(csv_filename)

    if not stations:
        print("Failed to load data. Exiting.\n")
        return

    print(f"✓ Extracted {len(stations)} unique stations\n")

    print("Sample stations (first 15):")
    for i, station in enumerate(stations[:15], 1):
        print(f"  {i:2d}. {station}")
    print(f"  ... and {len(stations) - 15} more\n")

    # STEP 2: POPULATE HASH TABLE
    print("STEP 2: POPULATING CLRS HASH TABLE")


    table_size = find_next_prime(len(stations))
    system = LondonUndergroundStatusSystem(table_size)

    print(f"Hash table size (prime): {table_size}")
    print(f"Loading {len(stations)} stations into CLRS chained hash table...")

    for station in stations:
        system.mark_operational(station)

    load_factor = system.station_count / system.table_size
    print(f"✓ System populated!")
    print(f"  Total stations loaded: {system.station_count}")
    print(f"  Load factor (α): {load_factor:.3f}\n")

    # STEP 3: TEST QUERIES
    print("STEP 3: TESTING STATION STATUS QUERIES")
    print()

    test_queries = [
        ("King's Cross St. Pancras", "Valid station"),
        ("Paddingtn", "MISSPELLED (should be Paddington)"),
        ("Narnia", "FICTIONAL station"),
    ]

    for i, (query, description) in enumerate(test_queries, 1):
        print(f"Query {i}: {description}")
        print(f"  Input:  '{query}'")
        status = system.check_status(query)
        print(f"  Output: {status}")
        print()


    print("TESTING COMPLETE")



if __name__ == "__main__":
    main()

