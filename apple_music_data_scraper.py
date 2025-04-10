import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = "https://music.apple.com/us/playlist/week-85/pl.u-mJy83ZPtNVLP7kq"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find the JSON data in the script tag
script_tag = soup.find('script', type='application/json')
json_data_line = script_tag.string.strip()

# Find the start and end of the JSON data within the line
start_index = json_data_line.find('[')
end_index = json_data_line.rfind(']') + 1

# Extract the JSON substring
json_substring = json_data_line[start_index:end_index]

# Parse the JSON data
json_data = json.loads(json_substring)

# List to store song details
song_details = []

# Extract title, artist, album, and play length entries from the JSON data
for section in json_data[0]['data']['sections']:
    if section['itemKind'] == 'trackLockup':
        for item in section['items']:
            title = item['title']
            artist = item['subtitleLinks'][0]['title']
            album = item['tertiaryLinks'][0]['title'] if item['tertiaryLinks'] else 'N/A'
            play_length_ms = item['duration']
            play_length_min = play_length_ms // 60000
            play_length_sec = (play_length_ms % 60000) // 1000
            play_length = f"{play_length_min}:{play_length_sec:02d}"
            song_details.append({
                'title': title,
                'artist': artist,
                'album': album,
                'play_length': play_length
            })

# Print the extracted song details
for detail in song_details:
    print(f"{detail['title']} - {detail['artist']} ({detail['album']}): {detail['play_length']}")
