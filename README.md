
# twitch-farmer

Simple python 3.7+ based tool that allows you to farm gift subs, emotes and other stuff.
## About
This small application allows you to connect to a large number of streams to get some drops such as gift subs, channel bonuses (**not** channel points, see screenshot below) and emotes during special Twitch events.

![Gifts](https://i.imgur.com/LKV5xRg.png)
![Bonuses](https://i.imgur.com/ATEqoaF.png)

## Installation

1. Check out twitch-farmer into your desired directory
```
$ git clone https://github.com/ROFLailXGOD/twitch-farmer your_directory
```
2. Install all dependencies
```
$ pip install -r requirements.txt
```
## Usage
### Prerequisites
First of all, you need to get your OAUTH token and client ID. The former is needed to connect to the Twitch IRC server and, therefore, to chats. You can get it [here](https://twitchapps.com/tmi/).  
The latter is used to send requests to the [New Twitch API](https://dev.twitch.tv/docs/api/) for gathering data about active streams. To get the ID follow Step 1 from the link above.  
After getting both token and ID rename `settings/local.py.skeleton` to `settings/local.py` and replace default values:
```
OAUTH = 'password'
CLIENT_ID = 'client_id'
```
Also, do not forget to change `NICK` to your Twitch username (login name) in **lowercase** in `settings/base.py`:
```
NICK = 'zazaza691'
```
### (Optional) Configuration
There are several options you can tweak in the `settings/base.py` file:
* `MAX_CONNECTIONS`: maximum amount of streams you can connect to simultaneously
* `MIN_VIEWERS`: minimum amount of viewers on the stream the application will connect to
* `MAX_VIEWERS`: maximum amount of viewers on the stream the application will connect to
* `GAMES`: list of games the application will connect to. By default it is empty which means that the application connects to streams of any games. Specify game IDs, if you want to change this behaviour.  

Example:
```
GAMES = [21779, 32982]
```
will force the application to connect only to League of Legends and Grand Theft Auto V streams. Here's the list of the most popular games' IDs:
```
21779 - League of Legends
32982 - Grand Theft Auto V
509658 - Just Chatting
491931 - Escape From Tarkov
33214 - Fortnite
29595 - Dota 2
138585 - Hearthstone
493057 - PLAYERUNKNOWN'S BATTLEGROUNDS
18122 - World of Warcraft
32399 - Counter-Strike: Global Offensive
498566 - Slots
29307 - Path of Exile
488552 - Overwatch
511224 - Apex Legends
514790 - Legends of Runeterra
491487 - Dead by Daylight
```
If your desired game is not listed, leave a request in issues. I might update this guide to show how to find game IDs by yourself.  
**Note:** do not specify a big number for MAX_VIEWERS and/or MAX_CONNECTIONS. It might break the application. How to determine whether the application is still working or not read in the next paragraph.

### Running the application
To run the application simply execute:
```
python app.py
```
If everything works, you should start seeing channels that you're connecting to. Also, roughly every 5 minutes you should see `Sent PONG` message. That indicates that everything is still good.  
Application updates the streams list every 20 minutes: disconnects from channels that went offline and connects to new ones.
## DISCLAIMER
Twitch-farmer was made for personal use only, but I don't mind sharing it. If you find any flows in the code feel free to let me know. If you have any problems with running this app, then I'm afraid I can't help you since I've provided all relevant information above.  

There's also no "connection lost" situations handling. I might look into that in the future.

Happy farming!
