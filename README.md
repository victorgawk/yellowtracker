# Yellow Tracker

Yellow Tracker is a discord bot to track MVPs.

Instructions:

1. Add the bot to your server through this link: https://discordapp.com/oauth2/authorize?client_id=417462153528737792&permissions=8192&scope=bot

2. Define a channel from server to be used exclusively for MVP tracking (OBS: is strongly recommended that you use a new channel for this). This is done by using the **!setmvpchannel** command. The bot in this channel will keep a list of tracked MVPs and their respective respawn times. Only users with the "Manage Server" permission can use this command.
  - **WARNING**: After you use this command, **ALL** messages from channel (if there is any) will be erased and this will be irreversible!!! Be sure that you are choosing the right channel.

3. Use the **!track** commad to track a MVP that has been defeated. OBS.: can only be used inside MVP channel.

4. The bot also can be configured to speak the MVP name in a voice channel everytime a tracked MVP reachs the minimun respawn time. Use the **!setvoicechannel** command to define a voice channel that bot will enter and speak. OBS.: if you don't want the bot entering voice channel anymore, use the **!unsetvoicechannel** command.

5. In  addition to MVPs, the bot also can be used to track mining zones, where each zone represents one or more mining maps with characteristics in common (for instance, the mining zone "Ice Dungeon" corresponds to the "ice_dun01", "ice_dun02" and "ice_dun03" maps). As well as MVPs, you need to define a channel to be used exclusively to track mining zones. Use the **!setminingchannel** command. This channel will keep the list of tracked mining zones.

Command list:

Command | Description
------- | ---------
**!setmvpchannel NAME** | Set the **NAME** channel as MVP channel. 
**!setminingchannel NAME** | Set the **NAME** channel as mining channel. 
**!setvoicechannel NAME** | Set the **NAME** channel as voice channel. 
**!unsetmvpchannel** | Disable the MVP channel.
**!unsetminingchannel** | Disable the mining channel.
**!unsetvoicechannel** | Disables the voice channel.
**!settings** | Display the bot settings on the server.
**!track NAME TIME** or **!t NAME TIME** | Report that MVP **NAME** died **TIME** minutes ago. The **TIME** argument is optional. If you ommit this argument means the MVP has died just now. In the mining channel, this command reports that the mining zone **NAME** was visited **TIME** minutes ago.
**!track all PERCENTAGE** or **!t all PERCENTAGE** | Track all MVPs at once. The optional parameter PERCENTAGE is used to modify the time that are mvps being tracked. "!t all 0.5" means that GTB will respawn in ~30min and Mistress will respawn in ~1 hour and "!t all 1" means that all MVP are respawning right now. This command can be used also to clear the mvp list, just type a high value for PERCENTAGE like "!t all 99". Only users with the "Manage Server" permission can use this command.
**!talonro** | Enable TalonRO custom MVP respawn times (e.g. GTB respawn become 45 to 75 mins instead of 60 to 70 mins, Eddga become 105 to 135 instead of 120 to 130 mins, and so on)

MVP List:

Name | Alias | Map | Respawn Time
---- | ----- | --- | -------
Amon Ra | - | moc_pryd06 | 60~70 mins |    
Atroce | - | ra_fild02 | 240~250 mins |    
Atroce | - | ra_fild03 | 180~190 mins |    
Atroce | - | ra_fild04 | 300~310 mins |    
Atroce | - | ve_fild01 | 180~190 mins |    
Atroce | - | ve_fild02 | 360~370 mins |    
Baphomet | - | prt_maze03 | 120~130 mins |    
Beelzebub | - | abbey03 | 720~730 mins |    
Bio3 MVP | - | lhz_dun03 | 100~130 mins |    
Bio4 MVP | - | lhz_dun04 | 100~130 mins |    
Boitata | - | bra_dun02 | 120~130 mins |    
Dark Lord | DL | gl_chyard | 60~70 mins |    
Detardeurus | Detale | abyss_03 | 180~190 mins |    
Doppelganger | - | gef_dun02 | 120~130 mins |    
Dracula | - | gef_dun01 | 60~70 mins |    
Drake | - | treasure02 | 120~130 mins |    
Eddga | - | pay_fild11 | 120~130 mins |    
Egnigem Cenia | GEC | lhz_dun02 | 120~130 mins |    
Evil Snake Lord | ESL | gon_dun03 | 94~104 mins |    
Fallen Bishop | FBH | abbey02 | 120~130 mins |    
Garm | Hatii | xmas_fild01 | 120~130 mins |    
Gloom Under Night | - | ra_san05 | 300~310 mins |    
Golden Thief Bug | GTB | prt_sewb4 | 60~70 mins |    
Gold Queen Scaraba | GQS | dic_dun03 | 120~120 mins |    
Gopinich | - | mosk_dun03 | 120~130 mins |    
Hardrock Mammoth | Mammoth | man_fild03 | 240~241 mins |    
Ifrit | - | thor_v03 | 660~670 mins |    
Kiel D-01 | - | kh_dun02 | 120~180 mins |    
Kraken | - | iz_dun05 | 120~130 mins |    
Ktullanux | - | ice_dun03 | 120~120 mins |    
Kublin Unres | - | schg_dun01 | 240~360 mins |    
Kublin Vanilla | - | arug_dun01 | 240~360 mins |    
Lady Tanee | LT; Tanee | ayo_dun02 | 420~430 mins |    
Leak | - | dew_dun01 | 120~130 mins |    
Lord of the Dead | LOD | niflheim | 133~133 mins |    
Maya | - | anthell02 | 120~130 mins |    
Maya Purple | MP | anthell01 | 120~180 mins |    
Maya Purple | MP | gld_dun03 | 20~30 mins |    
Mistress | - | mjolnir_04 | 120~130 mins |    
Moonlight Flower | MF | pay_dun04 | 60~70 mins |    
Nightmare Amon Ra | - | moc_prydn2 | 60~70 mins |    
Orc Hero | OH | gef_fild02 | 1440~1450 mins |    
Orc Hero | OH | gef_fild14 | 60~70 mins |    
Orc Lord | OL | gef_fild10 | 120~130 mins |    
Osiris | - | moc_pryd04 | 60~180 mins |    
Pharaoh | - | in_sphinx5 | 60~70 mins |    
Phreeoni | - | moc_fild17 | 120~130 mins |    
Queen Scaraba | QS | dic_dun02 | 120~121 mins |    
RSX-0806 | - | ein_dun02 | 125~135 mins |    
Samurai Specter | Incantation Samurai | ama_dun03 | 91~101 mins |    
Stormy Knight | SK | xmas_dun02 | 60~70 mins |    
Tao Gunka | - | beach_dun | 300~310 mins |    
Tao Gunka | - | beach_dun2 | 300~310 mins |    
Tao Gunka | - | beach_dun3 | 300~310 mins |    
Tendrilion | - | spl_fild03 | 60~60 mins |    
Thanatos | - | thana_boss | 120~120 mins |    
Turtle General | TG | tur_dun04 | 60~70 mins |    
Valkyrie Randgris | VR | odin_tem03 | 480~840 mins |    
Vesper | - | jupe_core | 120~130 mins |    
White Lady | Bacsojin | lou_dun03 | 116~126 mins |    
Wounded Morroc | WM | moc_fild22 | 720~900 mins |    

Mining zones:

Name|
----|
Coal Mine|
Comodo East|
Comodo North|
Comodo West|
Einbech|
Geffen|
Ice Dungeon|
Izlude|
Louyang|
Magma|
Mistress|
Payon|
Thor|
Umbala|
