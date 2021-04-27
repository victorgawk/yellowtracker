# Yellow Tracker

Yellow Tracker is a discord bot to track MVPs.

Instructions:

1. Add the bot to your server through this link: https://discordapp.com/oauth2/authorize?client_id=417462153528737792&permissions=8192&scope=bot

2. Define a channel from server to be used exclusively for MVP tracking (OBS: is strongly recommended that you use a new channel for this). This is done by using the **!setmvpchannel** command. The bot in this channel will keep a list of tracked MVPs and their respective respawn times. Only users with the "ADMINISTRATOR" permission can use this command.
  - **WARNING**: After you use this command, **ALL** messages from the channel (if there is any) will be erased and this will be irreversible!!! Be sure that you choose the right channel.

3. Use the **!track** command to track a MVP that has been defeated. OBS.: can only be used inside the MVP tracking channel.

OBS: In  addition to MVPs, the bot also can be used to track mining locations, where each location represents a group of maps (for instance, the mining location "Ice Dungeon (F1, F2, F3)" corresponds to the maps "ice_dun01", "ice_dun02" and "ice_dun03"). As well as MVPs, you need to define a channel to be used exclusively to track mining locations. To do this use the **!setminingchannel** command. This channel will keep the list of tracked mining locations.

Bot commands:

Command | Description
------- | ---------
**!track NAME TIME** or **!t NAME TIME** | Report that MVP **NAME** died **TIME** minutes ago. The **TIME** argument is optional. If you ommit this argument means the MVP has died just now. If **TIME** argument have the syntax HH:MM that means that MVP died at that time on TalonRO server time. In the mining channel, this command reports that the mining location **NAME** was visited **TIME** minutes ago.
**!woe** | Display the War of Emperium (WoE) times on TalonRO server.
**!gmc** | Display the Game Master Challenge (GMC) times on TalonRO server.
**!bghh** | Display the Battlegrounds Happy Hour times on TalonRO server.
**!help** | Lists all commands available for your user.
**!setmvpchannel** | Set the channel as MVP channel. Need "ADMINISTRATOR" permission.
**!unsetmvpchannel** | Disable the MVP channel. Need "ADMINISTRATOR" permission.
**!setminingchannel** | Set the channel as mining channel. Need "ADMINISTRATOR" permission.
**!unsetminingchannel** | Disable the mining channel. Need "ADMINISTRATOR" permission.
**!setmemberchannel** | Set a channel where the bot will send a message everytime a member join or left the server. Need "ADMINISTRATOR" permission.
**!unsetmemberchannel** | Disable the member channel. Need "ADMINISTRATOR" permission.
**!talonro** | Enable/disable TalonRO custom MVP respawn times (e.g. GTB respawn become 45 to 75 mins instead of 60 to 70 mins, Eddga become 105 to 135 instead of 120 to 130 mins, and so on). Need "ADMINISTRATOR" permission.
**!mobile** | Enable/disable track list mobile layout. Need "ADMINISTRATOR" permission.
**!settings** | Show bot settings. Need "ADMINISTRATOR" permission.
**!clean** | Remove all tracked MVPs from the list (useful after a server reboot). Need "ADMINISTRATOR" permission.

MVP List:

Name | Alias | Map | Respawn Time | TalonRO Respawn
---- | ----- | --- | ------------ | ---------------
Amon Ra | - | moc_pryd06 | 60~70 mins | 45~75 mins |
Atroce | - | ra_fild02 | 240~250 mins | 210~280 mins |
Atroce | - | ra_fild03 | 180~190 mins | 150~220 mins |
Atroce | - | ra_fild04 | 300~310 mins | 270~340 mins |
Atroce | - | ve_fild01 | 180~190 mins | 150~220 mins |
Atroce | - | ve_fild02 | 360~370 mins | 330~400 mins |
Baphomet | - | prt_maze03 | 120~130 mins | 105~135 mins |
Beelzebub | - | abbey03 | 720~730 mins | 720~730 mins |
Bio3 MVP | - | lhz_dun03 | 100~130 mins | 100~130 mins |
Bio4 MVP | - | lhz_dun04 | 100~130 mins | 100~130 mins |
Boitata | - | bra_dun02 | 120~130 mins | 105~135 mins |
Dark Lord | DL | gl_chyard | 60~70 mins | 45~75 mins |
Detardeurus | Detale | abyss_03 | 180~190 mins | 180~190 mins |
Doppelganger | - | gef_dun02 | 120~130 mins | 105~135 mins |
Dracula | - | gef_dun01 | 60~70 mins | 45~75 mins |
Drake | - | treasure02 | 120~130 mins | 105~135 mins |
Eddga | - | pay_fild11 | 120~130 mins | 105~135 mins |
Egnigem Cenia | GEC | lhz_dun02 | 120~130 mins | 105~135 mins |
Evil Snake Lord | ESL | gon_dun03 | 94~104 mins | 94~104 mins |
Fallen Bishop | FBH | abbey02 | 120~130 mins | 105~135 mins |
Garm | Hatii | xmas_fild01 | 120~130 mins | 105~135 mins |
Gloom Under Night | - | ra_san05 | 300~310 mins | 270~340 mins |
Golden Thief Bug | GTB | prt_sewb4 | 60~70 mins | 45~75 mins |
Gold Queen Scaraba | GQS | dic_dun03 | 120~120 mins | 105~135 mins |
Gopinich | - | mosk_dun03 | 120~130 mins | 105~135 mins |
Hardrock Mammoth | Mammoth | man_fild03 | 240~241 mins | 210~270 mins |
Ifrit | - | thor_v03 | 660~670 mins | 660~670 mins |
Incantation Samurai | Samurai Specter | ama_dun03 | 91~101 mins | 76~116 mins |
Kiel D-01 | - | kh_dun02 | 120~180 mins | 120~180 mins |
Kraken | - | iz_dun05 | 120~130 mins | 105~135 mins |
Ktullanux | - | ice_dun03 | 120~120 mins | 120~120 mins |
Kublin Unres | - | arug_dun01 | 240~360 mins | 240~360 mins |
Kublin Vanilla | - | schg_dun01 | 240~360 mins | 240~360 mins |
Lady Tanee | Tanee; LT | ayo_dun02 | 420~430 mins | 360~490 mins |
Leak | - | dew_dun01 | 120~130 mins | 105~135 mins |
Lord of the Dead | LOD | niflheim | 133~133 mins | 133~133 mins |
Maya | - | anthell02 | 120~130 mins | 105~135 mins |
Maya Purple | MP | anthell01 | 120~180 mins | 120~180 mins |
Maya Purple | MP | gld_dun03 | 20~30 mins | 20~30 mins |
Mistress | - | mjolnir_04 | 120~130 mins | 105~135 mins |
Moonlight Flower | MF | pay_dun04 | 60~70 mins | 45~75 mins |
Nightmare Amon Ra | - | moc_prydn2 | 60~70 mins | 45~75 mins |
Orc Hero | OH | gef_fild02 | 1440~1450 mins | 1440~1450 mins |
Orc Hero | OH | gef_fild14 | 60~70 mins | 45~75 mins |
Orc Lord | OL | gef_fild10 | 120~130 mins | 105~135 mins |
Osiris | - | moc_pryd04 | 60~180 mins | 60~180 mins |
Pharaoh | - | in_sphinx5 | 60~70 mins | 45~75 mins |
Phreeoni | - | moc_fild17 | 120~130 mins | 105~135 mins |
Queen Scaraba | QS | dic_dun02 | 120~121 mins | 105~136 mins |
RSX-0806 | - | ein_dun02 | 125~135 mins | 110~140 mins |
Stormy Knight | SK | xmas_dun02 | 60~70 mins | 45~75 mins |
Tao Gunka | Tao1 | beach_dun | 300~310 mins | 270~340 mins |
Tao Gunka | Tao2 | beach_dun2 | 300~310 mins | 270~340 mins |
Tao Gunka | Tao3 | beach_dun3 | 300~310 mins | 270~340 mins |
Tendrilion | - | spl_fild03 | 60~60 mins | 45~75 mins |
Thanatos | - | thana_boss | 120~120 mins | 120~120 mins |
Turtle General | TG | tur_dun04 | 60~70 mins | 45~75 mins |
Valkyrie Randgris | VR | odin_tem03 | 480~840 mins | 480~840 mins |
Vesper | - | jupe_core | 120~130 mins | 105~135 mins |
White Lady | Bacsojin | lou_dun03 | 116~126 mins | 116~126 mins |
Wounded Morroc | WM | moc_fild22 | 720~900 mins | 720~900 mins |

Mining locations:

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