import csv
import os
import shutil
from tqdm import tqdm

def load_gtfs_files(gtfs_path):
    """
    Charge les fichiers GTFS nécessaires.

    Args:
        gtfs_path (str): Le chemin vers le dossier contenant les fichiers GTFS.

    Returns:
        tuple: Cinq listes de dictionnaires contenant les données des fichiers routes, trips, stop_times, stops, et transfers.
    """
    routes = []
    trips = []
    stop_times = []
    stops = []
    transfers = []

    print("Chargement des fichiers GTFS...")

    with open(f'{gtfs_path}/routes.txt', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Chargement routes"):
            routes.append(row)

    with open(f'{gtfs_path}/trips.txt', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Chargement trips"):
            trips.append(row)

    with open(f'{gtfs_path}/stop_times.txt', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Chargement stop_times"):
            stop_times.append(row)

    with open(f'{gtfs_path}/stops.txt', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Chargement stops"):
            stops.append(row)

    with open(f'{gtfs_path}/transfers.txt', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in tqdm(reader, desc="Chargement transfers"):
            transfers.append(row)

    return routes, trips, stop_times, stops, transfers

def display_menu():
    """
    Affiche un menu interactif pour sélectionner le mode de transport.
    """
    print("Menu des modes de transport :")
    print("1. Tramway")
    print("2. Métro")
    print("3. Train")
    print("4. Bus")
    print("5. Ferry")
    print("6. Téléphérique")
    print("7. Funiculaire")
    print("8. Quitter")

def filter_data(routes, trips, stop_times, stops, transfers, transport_type):
    """
    Filtre les données GTFS pour ne conserver que celles correspondant au type de transport sélectionné.

    Args:
        routes (list): Liste des routes.
        trips (list): Liste des voyages.
        stop_times (list): Liste des horaires d'arrêt.
        stops (list): Liste des arrêts.
        transfers (list): Liste des transferts.
        transport_type (str): Type de transport sélectionné.

    Returns:
        tuple: Cinq listes de dictionnaires contenant les données filtrées pour les fichiers routes, trips, stop_times, stops, et transfers.
    """
    transport_type_map = {
        '1': '0',  # Tramway
        '2': '1',  # Métro
        '3': '2',  # Train
        '4': '3',  # Bus
        '5': '4',  # Ferry
        '6': '5',  # Téléphérique
        '7': '6',  # Funiculaire
    }
    route_ids = {route['route_id'] for route in routes if route['route_type'] == transport_type_map[transport_type]}

    filtered_routes = [route for route in routes if route['route_id'] in route_ids]
    filtered_trips = [trip for trip in trips if trip['route_id'] in route_ids]
    trip_ids = {trip['trip_id'] for trip in filtered_trips}
    filtered_stop_times = [stop_time for stop_time in stop_times if stop_time['trip_id'] in trip_ids]
    stop_ids = {stop_time['stop_id'] for stop_time in filtered_stop_times}
    filtered_stops = [stop for stop in stops if stop['stop_id'] in stop_ids]
    filtered_transfers = [transfer for transfer in transfers if transfer['from_stop_id'] in stop_ids and transfer['to_stop_id'] in stop_ids]

    return filtered_routes, filtered_trips, filtered_stop_times, filtered_stops, filtered_transfers

def save_filtered_data(gtfs_path, filtered_routes, filtered_trips, filtered_stop_times, filtered_stops, filtered_transfers):
    """
    Sauvegarde les données filtrées dans un nouveau dossier.

    Args:
        gtfs_path (str): Le chemin vers le dossier contenant les fichiers GTFS d'origine.
        filtered_routes (list): Liste des routes filtrées.
        filtered_trips (list): Liste des voyages filtrés.
        filtered_stop_times (list): Liste des horaires d'arrêt filtrés.
        filtered_stops (list): Liste des arrêts filtrés.
        filtered_transfers (list): Liste des transferts filtrés.
    """
    output_path = f"{gtfs_path}_filtered"
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    print(f"Sauvegarde des données filtrées dans le dossier {output_path}...")

    with open(f'{output_path}/routes.txt', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_routes[0].keys())
        writer.writeheader()
        for row in tqdm(filtered_routes, desc="Sauvegarde routes"):
            writer.writerow(row)

    with open(f'{output_path}/trips.txt', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_trips[0].keys())
        writer.writeheader()
        for row in tqdm(filtered_trips, desc="Sauvegarde trips"):
            writer.writerow(row)

    with open(f'{output_path}/stop_times.txt', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_stop_times[0].keys())
        writer.writeheader()
        for row in tqdm(filtered_stop_times, desc="Sauvegarde stop_times"):
            writer.writerow(row)

    with open(f'{output_path}/stops.txt', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_stops[0].keys())
        writer.writeheader()
        for row in tqdm(filtered_stops, desc="Sauvegarde stops"):
            writer.writerow(row)

    with open(f'{output_path}/transfers.txt', mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=filtered_transfers[0].keys())
        writer.writeheader()
        for row in tqdm(filtered_transfers, desc="Sauvegarde transfers"):
            writer.writerow(row)

def main():
    """
    Fonction principale du programme. Affiche un menu interactif, charge les fichiers GTFS, filtre les données et sauvegarde les résultats.
    """
    gtfs_path = os.path.dirname(__file__)
    routes, trips, stop_times, stops, transfers = load_gtfs_files(gtfs_path)

    while True:
        display_menu()
        choice = input("Choisissez un mode de transport (1-8) : ")
        if choice == '8':
            print("Au revoir!")
            break
        elif choice in [str(i) for i in range(1, 8)]:
            filtered_routes, filtered_trips, filtered_stop_times, filtered_stops, filtered_transfers = filter_data(routes, trips, stop_times, stops, transfers, choice)
            save_filtered_data(gtfs_path, filtered_routes, filtered_trips, filtered_stop_times, filtered_stops, filtered_transfers)
            print(f"Données filtrées et sauvegardées dans le dossier {gtfs_path}_filtered.")
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
