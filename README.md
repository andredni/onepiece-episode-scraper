# One Piece Episode Data Scraper with Flask API

This Python script scrapes episode data from the One Piece anime Wikipedia page and provides a simple Flask API to access the data.

## Prerequisites

- Python 3.x
- Flask
- Beautiful Soup
- Requests

You can install the required libraries using the following command:

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python index.py

```


## Usage

1. Clone or download this repository.

2. Open a terminal and navigate to the project directory.

3. Run the Flask application:

The API server will start and listen on `http://127.0.0.1:5000/`.

## Endpoints

- **GET /api/episodes**: Returns a list of all episodes.

Query Parameters:
- `chapter=false`: Exclude chapters and only list episodes.
- `number=<episode_number>`: Get details of a specific episode by number.
- `title=<episode_title>`: Search for episodes containing a specific title.

- **GET /api/chapters**: Returns a list of all chapters.

Test URL: [https://onepiece.r2dlan.me/api/episodes](https://onepiece.r2dlan.me/api/episodes)
