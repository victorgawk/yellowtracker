/*
DROP TABLE IF EXISTS mining_guild;
DROP TABLE IF EXISTS mining;
DROP TABLE IF EXISTS mvp_guild;
DROP TABLE IF EXISTS mvp_alias;
DROP TABLE IF EXISTS mvp;
DROP TABLE IF EXISTS channel_guild;
DROP TABLE IF EXISTS guild;
DROP TABLE IF EXISTS global_parameter;
DROP SEQUENCE IF EXISTS mvp_seq;
DROP SEQUENCE IF EXISTS mining_seq;
*/

CREATE SEQUENCE mvp_seq;
CREATE SEQUENCE mining_seq;

CREATE TABLE global_parameter (
    id bigint NOT NULL,
    race_time timestamp without time zone,
    CONSTRAINT global_parameter_pk PRIMARY KEY (id)
);

CREATE TABLE guild (
    id bigint NOT NULL,
    talonro boolean NOT NULL DEFAULT TRUE,
    mobile boolean NOT NULL DEFAULT FALSE,
    id_mvp_channel bigint,
    id_mining_channel bigint,
    id_member_channel bigint,
    CONSTRAINT guild_pk PRIMARY KEY (id)
);

CREATE TABLE mvp (
    id integer NOT NULL DEFAULT nextval('mvp_seq'::regclass),
    name text NOT NULL,
    map text NOT NULL,
    t1 integer NOT NULL,
    t2 integer NOT NULL,
    t1talonro integer,
    t2talonro integer,
    CONSTRAINT mvp_pk PRIMARY KEY (id)
);

CREATE TABLE mining (
    id integer NOT NULL DEFAULT nextval('mining_seq'::regclass),
    name text NOT NULL,
    CONSTRAINT mining_pk PRIMARY KEY (id)
);

CREATE TABLE mvp_alias (
    id_mvp integer NOT NULL,
    alias text NOT NULL,
    CONSTRAINT mvp_alias_pk PRIMARY KEY (id_mvp, alias)
);


CREATE TABLE mvp_guild (
    id_mvp integer NOT NULL,
    id_guild bigint NOT NULL,
    track_time timestamp without time zone NOT NULL,
    entry_time timestamp without time zone NOT NULL,
    id_user bigint NOT NULL,
    CONSTRAINT mvp_guild_pk PRIMARY KEY (id_mvp, id_guild)
);

CREATE TABLE mining_guild (
    id_mining integer NOT NULL,
    id_guild bigint NOT NULL,
    track_time timestamp without time zone NOT NULL,
    entry_time timestamp without time zone NOT NULL,
    id_user bigint NOT NULL,
    CONSTRAINT mining_guild_pk PRIMARY KEY (id_mining, id_guild)
);

INSERT INTO global_parameter(id)VALUES(1);

INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Amon Ra','moc_pryd06',60,70,45,75,1511);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Atroce','ra_fild02',240,250,210,280,1785);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Atroce','ra_fild03',180,190,150,220,1785);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Atroce','ra_fild04',300,310,270,340,1785);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Atroce','ve_fild01',180,190,150,220,1785);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Atroce','ve_fild02',360,370,330,400,1785);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Baphomet','prt_maze03',120,130,105,135,1039);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Beelzebub','abbey03',720,730,NULL,NULL,1873);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Bio3 MVP','lhz_dun03',100,130,NULL,NULL,1646);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Bio4 MVP','lhz_dun04',100,130,NULL,NULL,2237);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Boitata','bra_dun02',120,130,105,135,2068);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Dark Lord','gl_chyard',60,70,45,75,1272);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'DL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Detardeurus','abyss_03',180,190,NULL,NULL,1719);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Detale');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Doppelganger','gef_dun02',120,130,105,135,1046);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Dracula','gef_dun01',60,70,45,75,1389);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Drake','treasure02',120,130,105,135,1112);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Eddga','pay_fild11',120,130,105,135,1115);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Egnigem Cenia','lhz_dun02',120,130,105,135,1658);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GEC');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Evil Snake Lord','gon_dun03',94,104,NULL,NULL,1418);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'ESL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Fallen Bishop','abbey02',120,130,105,135,1871);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'FBH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Garm','xmas_fild01',120,130,105,135,1252);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Hatii');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Gloom Under Night','ra_san05',300,310,270,340,1768);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Gold Queen Scaraba','dic_dun03',120,120,105,135,2165);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GQS');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Golden Thief Bug','prt_sewb4',60,70,45,75,1086);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GTB');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Gopinich','mosk_dun03',120,130,105,135,1885);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Hardrock Mammoth','man_fild03',240,241,210,270,1990);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Mammoth');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Ifrit','thor_v03',660,670,NULL,NULL,1832);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Kiel D-01','kh_dun02',120,180,NULL,NULL,1734);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Kraken','iz_dun05',120,130,105,135,2202);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Ktullanux','ice_dun03',120,120,NULL,NULL,1779);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Kublin Unres','arug_dun01',240,360,NULL,NULL,1980);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Kublin Vanilla','schg_dun01',240,360,NULL,NULL,1980);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Lady Tanee','ayo_dun02',420,430,360,490,1688);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'LT');
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tanee');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Leak','dew_dun01',120,130,105,135,2156);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Lord of the Dead','niflheim',133,133,NULL,NULL,1373);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'LOD');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Maya','anthell02',120,130,105,135,1147);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Maya Purple','anthell01',120,180,NULL,NULL,1289);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MP');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Maya Purple','gld_dun03',20,30,NULL,NULL,1289);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MP');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Mistress','mjolnir_04',120,130,105,135,1059);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Moonlight Flower','pay_dun04',60,70,45,75,1150);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MF');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Nightmare Amon Ra','moc_prydn2',60,70,45,75,2362);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Orc Hero','gef_fild02',1440,1450,NULL,NULL,1087);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Orc Hero','gef_fild14',60,70,45,75,1087);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Orc Lord','gef_fild10',120,130,105,135,1190);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Osiris','moc_pryd04',60,180,NULL,NULL,1038);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Pharaoh','in_sphinx5',60,70,45,75,1157);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Phreeoni','moc_fild17',120,130,105,135,1159);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Queen Scaraba','dic_dun02',120,121,105,136,2087);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'QS');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('RSX-0806','ein_dun02',125,135,110,140,1623);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Incantation Samurai','ama_dun03',91,101,76,116,1542);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Samurai Specter');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Stormy Knight','xmas_dun02',60,70,45,75,1251);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'SK');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Tao Gunka','beach_dun',300,310,270,340,1583);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao1');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Tao Gunka','beach_dun2',300,310,270,340,1583);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao2');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Tao Gunka','beach_dun3',300,310,270,340,1583);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao3');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Tendrilion','spl_fild03',60,60,45,75,1991);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Thanatos','thana_boss',120,120,NULL,NULL,1708);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Turtle General','tur_dun04',60,70,45,75,1312);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'TG');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Valkyrie Randgris','odin_tem03',480,840,NULL,NULL,1765);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'VR');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Vesper','jupe_core',120,130,105,135,1685);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('White Lady','lou_dun03',116,126,NULL,NULL,1630);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Bacsojin');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro,id_mob)VALUES('Wounded Morroc','moc_fild22',720,900,NULL,NULL,1917);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'WM');

INSERT INTO mining(name)VALUES('Payon Dungeon F1, F2');
INSERT INTO mining(name)VALUES('Coal Mine Entrance, F1, F2, F3');
INSERT INTO mining(name)VALUES('Einbech Dungeon Entrance, F1, F2');
INSERT INTO mining(name)VALUES('Geffen Dungeon F1, F2, F3');
INSERT INTO mining(name)VALUES('Thor Volcano F1, F2, F3');
INSERT INTO mining(name)VALUES('Magma Dungeon F1, F2');
INSERT INTO mining(name)VALUES('Ice Dungeon F1, F2, F3');
INSERT INTO mining(name)VALUES('Byalan Dungeon F1, F2, F3, F4, F5');
INSERT INTO mining(name)VALUES('Louyang F1, F2');
INSERT INTO mining(name)VALUES('Comodo West, North, East');
INSERT INTO mining(name)VALUES('Mistress Map');
INSERT INTO mining(name)VALUES('Umbala Dungeon F1, F2');
