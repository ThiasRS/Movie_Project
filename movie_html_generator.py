import os


def generate_website(movies_data):
    """Generates a static HTML website from the database data"""

    # Pfade definieren (relativ zum Hauptverzeichnis)
    template_path = os.path.join('_static', 'index_template.html')
    output_path = os.path.join('_static', 'index.html')

    # 1. Generate HTML Content
    movie_html_items = ""
    for title, data in movies_data.items():
        # Wir greifen auf die Daten zu, die aus deiner SQL DB kommen
        poster_url = data.get('poster_image_url', '')
        year = data.get('year', 'N/A')
        rating = data.get('rating', 'N/A')

        display_year = str(year)[:4]

        movie_html_items += f"""
        <li>
            <div class="movie-item">
                <img class="movie-poster" src="{poster_url}" alt="{title} Poster"/>
                <div class="movie-title" title="{title}">{title}</div>  
                <div class="movie-year">{display_year}</div>
                <div class="movie-rating">Rating: {rating}</div>
            </div>
        </li>
        """

    # 2. Read template and replace placeholder
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template_content = file.read()

        new_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_html_items)

        # 3. Write Index.html
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(new_content)

        print(f"Website successfully generated.")

    except FileNotFoundError:
        print(f"Error: Could not find {template_path}. Please check the folder structure.")