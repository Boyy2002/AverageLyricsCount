import musicbrainzngs
import sys
import requests
import json


musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

print("please insert the name of the artist")

inputArtist = input() 

artists = musicbrainzngs.search_artists(artist=inputArtist)
if (artists['artist-count'] == 0):
    print('artist not found')
    sys.exit()

artist = artists['artist-list'][0]
print(u"artist found {name}".format(name=artist["name"]))

allSongs = set()

currentOffset = 0
recordings = musicbrainzngs.browse_recordings(artist=artist['id'], limit=100, offset=0)
while(len(recordings["recording-list"]) > 0):
    for recording in recordings["recording-list"]:
        allSongs.add(recording["title"])
               
    currentOffset = currentOffset + 100
    recordings = musicbrainzngs.browse_recordings(artist=artist['id'], limit=100, offset=currentOffset)

print('songs for the artist')
totalvalidsong = 0
totalvalidlyrics = 0
for song in sorted(allSongs): 
    print(song)

    address = ('https://api.lyrics.ovh/v1/' + inputArtist +'/' + song)
    
    response = requests.get(address) 
    if response.status_code == 200:
        lyrics = response.json() ["lyrics"]
        lyricsCount = len(lyrics.split())
        print(lyricsCount) 
        if lyricsCount > 0:
            totalvalidsong += 1
            totalvalidlyrics += lyricsCount
    else  :
        print("Failed")

average = totalvalidlyrics / totalvalidsong
Message = ("The average number of lyrics for " + artist["name"] +" is " + str(average)) 

with open('Message.txt', 'w') as outfile:
    json.dump(Message, outfile)