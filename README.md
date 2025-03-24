# Go2Web CLI Tool

Go2Web is a simple command-line web scraping and search tool that allows you to fetch web pages, search for information online, and navigate through search results.

## Features

- Fetch and display content from any URL
- Search the web using DuckDuckGo
- Format and display HTML or JSON content
- Navigate through search results
- Intelligent caching for faster response times

## Installation

```bash
git clone https://github.com/yourusername/go2web.git
cd go2web
```

## Usage

### Basic Commands

```bash
# Fetch a web page
python go2web.py -u https://example.com

# Search for a term
python go2web.py -s "python web scraping"

# Open a specific search result (by number)
python go2web.py -link 2

# Request specific content format
python go2web.py -u https://api.example.com --json
python go2web.py -u https://example.com --html
```

### Examples

Search for a term:
```bash
python go2web.py -s "climate change"
```

Open the third search result:
```bash
python go2web.py -link 3
```

Fetch a specific URL with JSON formatting:
```bash
python go2web.py -u https://api.github.com/users/octocat --json
```

## How It Works
![ScreenRecording-Mar242025-VEED-ezgif com-optimize](https://github.com/user-attachments/assets/b928ed9c-21ad-4879-a17c-0d22e2270696)



## Project Structure

- `go2web.py`: Main application entry point
- `src/http_client.py`: Handles HTTP requests with caching
- `src/formatters.py`: Formats HTML and JSON content
- `src/search.py`: Performs web searches via DuckDuckGo
- `src/cache.py`: Manages response caching

## Dependencies

- BeautifulSoup4: For HTML parsing
- Socket: For network communication
- SSL: For secure connections
- JSON: For handling JSON data
