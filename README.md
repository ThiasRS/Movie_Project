# 🎥 Movie Database

A sleek, modern movie database application. This project uses a Python backend to manage movie data and generates a high-fidelity static HTML frontend.

## ✨ Features

* **Pure CSS Dark Mode:** A native Dark Mode toggle using the "Checkbox Hack".
* **Dynamic Grid:** Responsive movie gallery that adapts to any screen size.
* **Interactive UI:** Smooth cubic-bezier transitions, hover scales, and tooltips for long movie titles.
* **Python-Powered:** Automatically generates the production `index.html` from your data source.

## 🚀 Getting Started

### Prerequisites
* Python 3.x installed on your machine.

### Installation
1.  **Clone the repository:**

2.  **Generate the Website:**
    Run your Python script to process the database and build the frontend:
    ```bash
    python movies.py
    ```

3.  **View the Result:**
    Open `_static/index.html` in any modern web browser (Chrome, Safari, Edge).

## 🛠 Tech Stack

* **Backend:** Python 3 (Data processing & HTML generation)
* **Frontend:** HTML5, CSS3 (Custom Variables, Flexbox, & Grid)

## 📂 Project Structure

* `movies.py` — The core logic for data management and HTML generation.
* `_static/`
    * `index_template.html` — The base structure for the generated site.
    * `style.css` — The complete styling suite including the Dark Mode logic.
    * `index.html` — The final generated output (auto-created).

## 📝 License

This project is open source and available under the MIT License.
