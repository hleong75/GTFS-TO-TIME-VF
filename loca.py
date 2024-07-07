import csv
import numpy as np
from tqdm import tqdm

def read_gtfs_stops(file_path):
    """
    Lit le fichier GTFS stops.txt et crée un dictionnaire des coordonnées des arrêts.

    :param file_path: Chemin vers le fichier stops.txt
    :return: Dictionnaire avec stop_id comme clé et un tuple (stop_lat, stop_lon) comme valeur
    """
    stops_dict = {}
    
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in tqdm(reader, desc="Lecture des stops", unit=" arrêt"):
            stop_id = row['stop_id']
            stop_lat = float(row['stop_lat'])
            stop_lon = float(row['stop_lon'])
            
            stops_dict[stop_id] = (stop_lat, stop_lon)
    
    return stops_dict

def read_arrets(file_path):
    """
    Lit le fichier arrets.csv et crée un dictionnaire de correspondance entre stop_id et stop_name.

    :param file_path: Chemin vers le fichier arrets.csv
    :return: Dictionnaire avec stop_id comme clé et stop_name comme valeur
    """
    arrets_dict = {}
    
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in tqdm(reader, desc="Lecture des arrets", unit=" arrêt"):
            stop_id = row['stop_id']
            stop_name = row['stop_name']
            
            arrets_dict[stop_id] = stop_name
    
    return arrets_dict

def replace_stop_id_with_name(stops_dict, arrets_dict):
    """
    Remplace les stop_id dans stops_dict par les noms des arrêts correspondants.

    :param stops_dict: Dictionnaire avec stop_id comme clé et un tuple (stop_lat, stop_lon) comme valeur
    :param arrets_dict: Dictionnaire avec stop_id comme clé et stop_name comme valeur
    :return: Nouveau dictionnaire avec stop_name comme clé et un tuple (stop_lat, stop_lon) comme valeur
    """
    replaced_dict = {}
    
    for stop_id, coords in tqdm(stops_dict.items(), desc="Remplacement des stop_id", unit=" arrêt"):
        stop_name = arrets_dict.get(stop_id)
        replaced_dict[stop_name] = coords
    
    return replaced_dict

def save_localisations(file_path, localisations):
    """
    Sauvegarde le dictionnaire des localisations dans un fichier .npy.

    :param file_path: Chemin vers le fichier .npy
    :param localisations: Dictionnaire avec stop_name comme clé et un tuple (stop_lat, stop_lon) comme valeur
    """
    np.save(file_path, localisations)

def main():
    # Chemin vers vos fichiers stops.txt et arrets.csv dans le même dossier que le script
    stops_file_path = 'stops.txt'
    arrets_file_path = 'arrets.csv'
    localisations_file_path = 'localisations.npy'

    # Lire les fichiers
    stops_coordinates = read_gtfs_stops(stops_file_path)
    arrets_mapping = read_arrets(arrets_file_path)

    # Remplacer les stop_id par les noms des arrêts
    named_stops_coordinates = replace_stop_id_with_name(stops_coordinates, arrets_mapping)

    # Sauvegarder le dictionnaire des localisations dans un fichier .npy
    save_localisations(localisations_file_path, named_stops_coordinates)

    # Afficher un message de confirmation
    print(f"Les localisations ont été sauvegardées dans {localisations_file_path}")

if __name__=="__main__":
    main()
