from datetime import datetime
from modules.movie_html_generator import generate_website
from modules import movie_storage_sql as storage
from dotenv import load_dotenv
import os
import statistics
import random
import requests


load_dotenv()


CURRENT_YEAR = datetime.now().year
API_KEY = os.getenv('API_KEY')


def print_program_title():
    """Prints the Title of the program when it starts"""
    print("********** My Movies Database **********")


def print_menu(menu_data):
    """Prints the Menu of the program"""
    for menu_number, menu_action in menu_data.items():
        print(f"{menu_number}: {menu_action['label']}")


def ask_user_to_enter_a_choice():
    """User can Enter a number to choose a menu action"""
    try:
        return int(input("Enter choice (1-10): "))
    except ValueError:
        return -1


def print_list_movies(movies_data):
    """Retrieve and display all movies from the database"""
    print(f"{len(movies_data)} movies in total")
    for movie, data in movies_data.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def add_movie(movies_data):
    """The User can add a movie title, year and rating to the database"""
    while True:
        search_title = input("Enter new movie name (or leave empty to cancel): ")
        if search_title == "":
            print("Action cancelled.")
            return

        exists = False # Prüft ob der Titel schon existiert in der database
        for movie_name in movies_data.keys():
            if movie_name.lower() == search_title.lower():
                exists = True
                break
        if exists:
            print(f"Movie '{search_title}' already exists! Use 'Update' to change the year or rating.")
            continue

        movie_info = search_movie_api(search_title)
        if movie_info is None:
            print('Data not found!')
            return
        else:
            title, year, rating, poster_image_url = movie_info
            storage.add_movie(title, year, rating, poster_image_url)
            return


def delete_movie(movies_data):
    """The user can delete a movie from the database by the title"""
    while True:
        movie_to_delete = input("Enter movie name to delete (leave empty to cancel): ")
        if movie_to_delete == "":
            print("Action cancelled.")
            return

        found_movie = None
        for movie_name in movies_data.keys():
            if movie_to_delete.lower() in movie_name.lower():
                found_movie = movie_name
                break

        if found_movie:
            delete_question = input(f'Are you sure you want to delete "{found_movie}"? (y/n): ').lower()
            if delete_question == "y":
                storage.delete_movie(found_movie)
                print(f"'{found_movie}' was deleted.")
                return
            else:
                print("Deletion cancelled.")
        else:
            print(f"Movie containing '{movie_to_delete}' not found. Try again.")



def update_movie(movies_data):
    """The user can update the year and rating from a movie"""
    while True:
        movie_to_update = input("Enter movie name (leave empty to cancel): ")
        if movie_to_update == "":
            print("Update cancelled.")
            return

        found_movie = None
        for movie_name in movies_data.keys():
            if movie_to_update.lower() in movie_name.lower():
                found_movie = movie_name
                break

        if found_movie:
            update_question = input(f"Do you want to update {found_movie} (y/n): ")
            if update_question == 'y':
                try:
                    rating_to_update = float(input("Enter new movie rating (0-10): "))
                    if 0 <= rating_to_update <= 10:
                        year_to_update = int(input("Enter new movie year: "))
                        if 1895 <= year_to_update < CURRENT_YEAR:
                            storage.update_movie(found_movie, rating_to_update, year_to_update)
                            break
                        else:
                            print(f"Rating {year_to_update} is invalid (must be between 1894 and {CURRENT_YEAR + 1}.)")
                    else:
                        print(f"Rating {rating_to_update} is invalid (must be between 0 and 10")
                except ValueError:
                    print(f"Invalid input: Not a number!")
            else:
                continue
        else:
            print(f"Movie {movie_to_update} doesn't exist!")


def stats(movies_data):
    """Shows overall stats from the movie database"""
    if not movies_data:
        print("No movies in database to calculate stats.")
        return

    ratings = [data['rating'] for data in movies_data.values()]

    avg_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)
    best_rating = max(ratings)
    worst_rating = min(ratings)

    best_movies = [name for name, data in movies_data.items() if data['rating'] == best_rating]
    worst_movies = [name for name, data in movies_data.items() if data['rating'] == worst_rating]

    print(f"Average rating: {avg_rating:.2f}")
    print(f"Median rating: {median_rating}")
    print(f"Best movie(s): {', '.join(best_movies)}, Rating: {best_rating}")
    print(f"Worst movie(s): {', '.join(worst_movies)}, Rating: {worst_rating}")


def print_random_movie(movies_data):
    """Shows a random movie from database"""
    random_movie = random.choice(list(movies_data.keys()))
    print(f"Your movie for tonight: {random_movie} ({movies_data[random_movie]['year']}), its rated {movies_data[random_movie]['rating']}")


def search_movie(movies_data):
    """Searches a movie from database"""
    movie_to_search = input("Enter part of movie name: ")
    for movie in movies_data.keys():
        if movie_to_search.lower() in movie.lower():
            print(f"{movie} ({movies_data[movie]['year']}): {movies_data[movie]['rating']}")


def search_movie_api(search_title):
    """Searche and get movie data from api by the title"""
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={search_title}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("Response") == "False":
            return None
        title = data['Title']
        year = data['Year']
        poster_image_url = data['Poster']
        rating_value = "0"  # Standardwert, falls nichts gefunden wird
        for rate in data.get('Ratings', []):
            if rate['Source'] == 'Internet Movie Database':
                # extracting the /10
                rating_value = rate['Value'].split('/')[0]
                break
        rating = float(rating_value)
        return title, year, rating, poster_image_url
    except requests.exceptions.RequestException as error:
        print(f"\n[!] Connection Error: API is not accessible. ({error})")
        return None


def print_movies_sorted_by_rating(movies_data):
    """Shows the movies from database sorted by rating"""
    if not movies_data:
        print("No movies in database.")
        return


    sorted_movies = sorted(movies_data.items(), key=lambda x: x[1]['rating'], reverse=True)

    for movie, data in sorted_movies:
        print(f"{movie} ({data['year']}): {data['rating']}")


def main():
    menu = {
        1: {"label": "List movies", "action": print_list_movies},
        2: {"label": "Add movie", "action": add_movie},
        3: {"label": "Delete movie", "action": delete_movie},
        4: {"label": "Update movie", "action": update_movie},
        5: {"label": "Stats", "action": stats},
        6: {"label": "Random movie", "action": print_random_movie},
        7: {"label": "Search movie", "action": search_movie},
        8: {"label": "Movies sorted by rating", "action": print_movies_sorted_by_rating},
        9: {"label": "Generate website", "action": generate_website},
        10: {"label": "Exit", "action": None},
    }

    print_program_title()

    while True:
        movies_db = storage.list_movies()
        print("")
        print_menu(menu)
        print("")
        user_choice = ask_user_to_enter_a_choice()
        print("")
        user_action = menu.get(user_choice)

        if user_action:
            if user_choice == 10:
                break
            if 1 <= user_choice <= 9:
                # Funktionen 1-9 brauchen die movies_db als Argument
                user_action["action"](movies_db)
        else:
            print(f"Invalid choice! '{user_choice}' is not on the menu.")

        print("")
        input("Press enter to continue")


if __name__ == "__main__":
    main()