import requests

BASE_URL = "https://swapi.dev/api"

# a) ¿En cuántas películas aparecen planetas cuyo clima sea árido?
def peliculas_con_clima_arido():
    response = requests.get(f"{BASE_URL}/planets/")
    planetas_aridos = []
    while response.status_code == 200:
        data = response.json()
        planetas_aridos.extend([planet for planet in data['results'] if 'arid' in planet['climate']])
        if data['next']:
            response = requests.get(data['next'])
        else:
            break

    peliculas = set()
    for planeta in planetas_aridos:
        for film in planeta['films']:
            peliculas.add(film)
    return len(peliculas)

# b) ¿Cuántos Wookies aparecen en toda la saga?
def contar_wookies():
    response = requests.get(f"{BASE_URL}/species/")
    wookie_species_url = None
    while response.status_code == 200:
        data = response.json()
        for species in data['results']:
            if species['name'].lower() == 'wookiee':
                wookie_species_url = species['people']
                break
        if data['next'] and not wookie_species_url:
            response = requests.get(data['next'])
        else:
            break
    
    if not wookie_species_url:
        return 0

    return len(wookie_species_url)

# c) ¿Cuál es el nombre de la aeronave más pequeña en la primera película?
def aeronave_mas_pequena():
    response = requests.get(f"{BASE_URL}/films/1/")
    if response.status_code != 200:
        return None
    
    film_data = response.json()
    starships_urls = film_data.get('starships', [])
    smallest_starship = None
    smallest_length = float('inf')

    for starship_url in starships_urls:
        starship_response = requests.get(starship_url)
        if starship_response.status_code == 200:
            starship_data = starship_response.json()
            try:
                length = float(starship_data['length'].replace(',', ''))
                if length < smallest_length:
                    smallest_length = length
                    smallest_starship = starship_data['name']
            except ValueError:
                continue

    return smallest_starship

if __name__ == "__main__":
    print("a) Películas con planetas áridos:", peliculas_con_clima_arido())
    print("b) Número de Wookies:", contar_wookies())
    print("c) Aeronave más pequeña en la primera película:", aeronave_mas_pequena())
