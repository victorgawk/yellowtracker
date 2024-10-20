# Yellow Tracker

Yellow Tracker is a discord bot to track MVPs.

## Run local

Prerequisites to run this application:

- Python 3.10 or above
- A discord bot token
- A PostgreSQL database

1. In the PostgreSQL database, use the content from the file `sql/yellowtracker.sql` to create the initial database structure.
2. In the `src` folder, create a file named `.env` with the following variables:
```properties
# REQUIRED (bot will raise an error if it's not defined)

BOT_USER_TOKEN=your discord bot token
DATABASE_URL=your PostgresSQL URL with the syntax postgres://username:password@host:port/database

# OPTIONAL (bot will use the default value if it's not defined)

DEL_MSG_AFTER_SECS=time to delete a message in a track channel after message last update (default = 10 seconds)
TABLE_ENTRY_EXPIRATION_MINS=time to remove an entry from the track table after entry max respawn was reached (default = 20 minutes)
TIMER_DELAY_SECS=bot timer delay in seconds (default = 5 seconds)
TIMEZONE=timezone used for datetimes in HH:MM format (default = PST8PDT)
GUILD_ID=a single server ID to sync the slash commands (default = None)
```
3. Inside a terminal/command prompt, go to the `src` folder.
4. Execute the command `pip install -r requirements.txt` to install the application dependencies.
5. Execute the command `python app.py` to start the application.

## Usage

- Define a channel from your discord server to be used exclusively for MVP tracking (OBS: is strongly recommended that you use a new channel for this). This is done by using the **/setmvpchannel** command. The bot in this channel will keep a table with the tracked MVPs and their respective remaining times to respawn.
  - **WARNING**: After you use this command, **ALL** messages from the channel (if there is any) will be erased and this will be irreversible!!! Be sure that you choose the right channel.

- Use the **/track** command to track a MVP that has been defeated. OBS.: can only be used inside a MVP track channel.

OBS: In addition to MVPs, Yellow Tracker can also be used to track mining locations, where each location represents a collection with one or more maps (for instance, the mining location "Ice Dungeon (F1, F2, F3)" corresponds to the maps "ice_dun01", "ice_dun02" and "ice_dun03"). As well as MVPs, you need to define a track channel to be used exclusively for mining locations. To do this use the **/setminingchannel** command.

### Bot commands:

Command | Description
------- | ---------
**/track** `name` `time` | Report that MVP `name` died. The optional `time` argument can be used to determine the exact time the MVP died. Ommit this argument to report that the MVP died just now. The `time` argument must have the syntax `HHMM` telling that the MVP died at `time` relative to the `TIMEZONE` environment variable or a custom timezone defined with `/timezone` command.
**/setmvpchannel** | Define the current channel as the MVP track channel.
**/unsetmvpchannel** | Undo the MVP channel definition in the discord server.
**/setminingchannel** | Define the current channel as the mining location track channel.
**/unsetminingchannel** | Undo the mining location channel definition in the discord server.
**/custom** | Enable/disable custom MVP respawn times (e.g. GTB respawn become 45 to 75 mins instead of 60 to 70 mins, Eddga become 105 to 135 instead of 120 to 130 mins, and so on).
**/timezone** | Set a custom timezone for MVP tracking when the time is set in `HH:MM` syntax.
**/mobile** | Enable/disable track table mobile layout.
**/settings** | Show current bot settings.
**/clean** | Remove all tracked MVPs/mining locations from the table (useful after a server reboot).
**/woe** | Display War of Emperium (WoE) times.
**/gmc** | Display Game Master Challenge (GMC) times.
**/hh** | Display Battleground Happy Hour times.

### MVP List:

Name | Alias | Map | Respawn Time | Custom Respawn
---- | ----- | --- | ------------ | ---------------
Amon Ra | - | moc_pryd06 | 60~70 mins | 55~75 mins |
Atroce | - | ra_fild02 | 240~250 mins | 210~270 mins |
Atroce | - | ra_fild03 | 180~190 mins | 150~210 mins |
Atroce | - | ra_fild04 | 300~310 mins | 270~330 mins |
Atroce | - | ve_fild01 | 180~190 mins | 150~210 mins |
Atroce | - | ve_fild02 | 360~370 mins | 330~390 mins |
Baphomet | - | prt_maze03 | 120~130 mins | 105~135 mins |
Beelzebub | - | abbey03 | 720~730 mins | 540~840 mins |
Bio3 MVP | - | lhz_dun03 | 100~130 mins | 100~130 mins |
Bio4 MVP | - | lhz_dun04 | 100~130 mins | 100~130 mins |
Boitata | - | bra_dun02 | 120~130 mins | 105~135 mins |
Dark Lord | DL | gl_chyard | 60~70 mins | 55~75 mins |
Detardeurus | Detale | abyss_03 | 180~190 mins | 150~210 mins |
Doppelganger | - | gef_dun02 | 120~130 mins | 105~135 mins |
Dracula | - | gef_dun01 | 60~70 mins | 55~70 mins |
Drake | - | treasure02 | 120~130 mins | 105~135 mins |
Eddga | - | pay_fild11 | 120~130 mins | 105~135 mins |
Egnigem Cenia | GEC | lhz_dun02 | 120~130 mins | 120~130 mins |
Evil Snake Lord | ESL | gon_dun03 | 94~104 mins | 84~114 mins |
Fallen Bishop | FBH | abbey02 | 120~130 mins | 105~135 mins |
Garm | Hatii | xmas_fild01 | 120~130 mins | 105~135 mins |
Gloom Under Night | - | ra_san05 | 300~310 mins | 270~330 mins |
Golden Thief Bug | GTB | prt_sewb4 | 60~70 mins | 55~75 mins |
Gold Queen Scaraba | GQS | dic_dun03 | 120~120 mins | 105~135 mins |
Gopinich | - | mosk_dun03 | 120~130 mins | 105~135 mins |
Hardrock Mammoth | Mammoth | man_fild03 | 240~241 mins | 210~270 mins |
Ifrit | - | thor_v03 | 660~670 mins | 540~780 mins |
Incantation Samurai | Samurai Specter | ama_dun03 | 91~101 mins | 75~120 mins |
Kiel D-01 | - | kh_dun02 | 120~180 mins | 120~180 mins |
Kraken | - | iz_dun05 | 120~130 mins | 105~135 mins |
Ktullanux | - | ice_dun03 | 120~120 mins | 120~120 mins |
Kublin | - | arug_dun01 | 240~360 mins | 240~360 mins |
Kublin | - | mocg_dun | 240~360 mins | 240~360 mins |
Kublin | - | schg_dun01 | 240~360 mins | 240~360 mins |
Lady Tanee | LT; Tanee | ayo_dun02 | 420~430 mins | 360~385 mins |
Leak | - | dew_dun01 | 120~130 mins | 75~105 mins |
Lord of the Dead | LOD | niflheim | 133~133 mins | 133~133 mins |
Maya | - | anthell02 | 120~130 mins | 105~135 mins |
Maya Purple | MP | anthell01 | 120~180 mins | 120~180 mins |
Maya Purple | MP | gld_dun03 | 20~30 mins | 20~30 mins |
Mistress | - | mjolnir_04 | 120~130 mins | 105~135 mins |
Moonlight Flower | MF | pay_dun04 | 60~70 mins | 55~75 mins |
Nightmare Amon Ra | - | moc_prydn2 | 60~70 mins | 55~75 mins |
Orc Hero | OH | gef_fild02 | 1440~1450 mins | 1440~1450 mins |
Orc Hero | OH | gef_fild14 | 60~70 mins | 55~75 mins |
Orc Lord | OL | gef_fild10 | 120~130 mins | 105~135 mins |
Osiris | - | moc_pryd04 | 60~180 mins | 60~180 mins |
Pharaoh | - | in_sphinx5 | 60~70 mins | 55~75 mins |
Phreeoni | - | moc_fild17 | 120~130 mins | 105~135 mins |
Queen Scaraba | QS | dic_dun02 | 120~121 mins | 105~136 mins |
RSX-0806 | - | ein_dun02 | 125~135 mins | 110~140 mins |
Stormy Knight | SK | xmas_dun02 | 60~70 mins | 55~75 mins |
Tao Gunka | Tao1 | beach_dun | 300~310 mins | 270~330 mins |
Tao Gunka | Tao2 | beach_dun2 | 300~310 mins | 270~330 mins |
Tao Gunka | Tao3 | beach_dun3 | 300~310 mins | 270~330 mins |
Tendrilion | - | spl_fild03 | 60~60 mins | 60~75 mins |
Thanatos | - | thana_boss | 120~120 mins | 120~120 mins |
Turtle General | TG | tur_dun04 | 60~70 mins | 55~75 mins |
Valkyrie Randgris | VR | odin_tem03 | 480~840 mins | 480~840 mins |
Vesper | - | jupe_core | 120~130 mins | 105~135 mins |
White Lady | Bacsojin | lou_dun03 | 116~126 mins | 105~135 mins |
Wounded Morroc | WM | moc_fild22 | 720~900 mins | 720~900 mins |

### Mining locations:

Name|
----|
Byalan Dungeon (F1, F2, F3, F4, F5)|
Coal Mine (Entrance, F1, F2, F3)|
Comodo (West, North, East)|
Einbech Dungeon (Entrance, F1, F2)|
Geffen Dungeon (F1, F2, F3)|
Ice Dungeon (F1, F2, F3)|
Louyang (F1, F2)|
Magma Dungeon (F1, F2)|
Mistress Map|
Payon Dungeon (F1, F2)|
Thor Volcano (F1, F2, F3)|
Umbala Dungeon (F1, F2)|
