/*
DROP TABLE IF EXISTS mining_guild_log;
DROP TABLE IF EXISTS mvp_guild_log;
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
    CONSTRAINT mvp_guild_pk PRIMARY KEY (id_mvp, id_guild)
);

CREATE TABLE mining_guild (
    id_mining integer NOT NULL,
    id_guild bigint NOT NULL,
    track_time timestamp without time zone NOT NULL,
    CONSTRAINT mining_guild_pk PRIMARY KEY (id_mining, id_guild)
);

CREATE TABLE mvp_guild_log (
    id_mvp integer NOT NULL,
    id_guild bigint NOT NULL,
    log_date timestamp without time zone NOT NULL,
    log_user text NOT NULL,
    CONSTRAINT mvp_guild_log_pk PRIMARY KEY (id_mvp, id_guild, log_date, log_user)
);

CREATE TABLE mining_guild_log (
    id_mining integer NOT NULL,
    id_guild bigint NOT NULL,
    log_date timestamp without time zone NOT NULL,
    log_user text NOT NULL,
    CONSTRAINT mining_guild_log_pk PRIMARY KEY (id_mining, id_guild, log_date, log_user)
);

INSERT INTO global_parameter(id)VALUES(1);

INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Amon Ra','moc_pryd06',60,70,45,75);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Atroce','ra_fild02',240,250,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Atroce','ra_fild03',180,190,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Atroce','ra_fild04',300,310,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Atroce','ve_fild01',180,190,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Atroce','ve_fild02',360,370,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Baphomet','prt_maze03',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Beelzebub','abbey03',720,730,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Bio3 MVP','lhz_dun03',100,130,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Bio4 MVP','lhz_dun04',100,130,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Boitata','bra_dun02',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Dark Lord','gl_chyard',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'DL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Detardeurus','abyss_03',180,190,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Detale');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Doppelganger','gef_dun02',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Dracula','gef_dun01',60,70,45,75);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Drake','treasure02',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Eddga','pay_fild11',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Egnigem Cenia','lhz_dun02',120,130,105,135);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GEC');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Evil Snake Lord','gon_dun03',94,104,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'ESL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Fallen Bishop','abbey02',120,130,105,135);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'FBH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Garm','xmas_fild01',120,130,105,135);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Hatii');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Gloom Under Night','ra_san05',300,310,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Gold Queen Scaraba','dic_dun03',120,120,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GQS');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Golden Thief Bug','prt_sewb4',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'GTB');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Gopinich','mosk_dun03',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Hardrock Mammoth','man_fild03',240,241,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Mammoth');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Ifrit','thor_v03',660,670,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Kiel D-01','kh_dun02',120,180,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Kraken','iz_dun05',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Ktullanux','ice_dun03',120,120,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Kublin Unres','schg_dun01',240,360,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Kublin Vanilla','arug_dun01',240,360,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Lady Tanee','ayo_dun02',420,430,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'LT');
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tanee');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Leak','dew_dun01',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Lord of the Dead','niflheim',133,133,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'LOD');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Maya','anthell02',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Maya Purple','anthell01',120,180,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MP');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Maya Purple','gld_dun03',20,30,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MP');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Mistress','mjolnir_04',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Moonlight Flower','pay_dun04',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'MF');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Nightmare Amon Ra','moc_prydn2',60,70,45,75);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Orc Hero','gef_fild02',1440,1450,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Orc Hero','gef_fild14',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OH');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Orc Lord','gef_fild10',120,130,105,135);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'OL');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Osiris','moc_pryd04',60,180,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Pharaoh','in_sphinx5',60,70,45,75);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Phreeoni','moc_fild17',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Queen Scaraba','dic_dun02',120,121,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'QS');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('RSX-0806','ein_dun02',125,135,110,140);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Samurai Specter','ama_dun03',91,101,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Incantation Samurai');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Stormy Knight','xmas_dun02',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'SK');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Tao Gunka','beach_dun',300,310,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao1');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Tao Gunka','beach_dun2',300,310,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao2');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Tao Gunka','beach_dun3',300,310,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Tao3');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Tendrilion','spl_fild03',60,60,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Thanatos','thana_boss',120,120,NULL,NULL);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Turtle General','tur_dun04',60,70,45,75);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'TG');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Valkyrie Randgris','odin_tem03',480,840,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'VR');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Vesper','jupe_core',120,130,105,135);
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('White Lady','lou_dun03',116,126,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'Bacsojin');
INSERT INTO mvp(name,map,t1,t2,t1talonro,t2talonro)VALUES('Wounded Morroc','moc_fild22',720,900,NULL,NULL);
INSERT INTO mvp_alias(id_mvp,alias)VALUES(currval('mvp_seq'),'WM');

INSERT INTO mining(name)VALUES('Coal Mine');
INSERT INTO mining(name)VALUES('Payon');
INSERT INTO mining(name)VALUES('Einbech');
INSERT INTO mining(name)VALUES('Geffen');
INSERT INTO mining(name)VALUES('Thor');
INSERT INTO mining(name)VALUES('Magma');
INSERT INTO mining(name)VALUES('Ice Dungeon');
INSERT INTO mining(name)VALUES('Izlude');
INSERT INTO mining(name)VALUES('Louyang');
INSERT INTO mining(name)VALUES('Comodo North');
INSERT INTO mining(name)VALUES('Comodo East');
INSERT INTO mining(name)VALUES('Comodo West');
INSERT INTO mining(name)VALUES('Umbala');
INSERT INTO mining(name)VALUES('Mistress');