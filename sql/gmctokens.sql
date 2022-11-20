/*
DROP TABLE IF EXISTS gmc_token_box_req_token;
DROP TABLE IF EXISTS gmc_token_box_req;
DROP TABLE IF EXISTS gmc_token_acc_amount;
DROP TABLE IF EXISTS gmc_token_acc;
DROP SEQUENCE IF EXISTS gmc_token_acc_seq;
DROP SEQUENCE IF EXISTS gmc_token_box_req_seq;
*/

CREATE SEQUENCE gmc_token_acc_seq;
CREATE SEQUENCE gmc_token_box_req_seq;

CREATE TABLE gmc_token_acc (
    id integer NOT NULL,
    id_user bigint NOT NULL,
    CONSTRAINT gmc_token_acc_pk PRIMARY KEY (id)
);

CREATE TABLE gmc_token_acc_amount (
    id_gmc_token_acc integer NOT NULL,
    token_name text NOT NULL,
    amount integer NOT NULL,
    CONSTRAINT gmc_token_acc_amount_pk PRIMARY KEY (id_gmc_token_acc, token_name),
    CONSTRAINT gmc_token_acc_amount_acc_fk FOREIGN KEY (id_gmc_token_acc) REFERENCES gmc_token_acc(id)
);

CREATE TABLE gmc_token_box_req (
    id integer NOT NULL,
    id_gmc_token_acc integer NOT NULL,
    box_name text NOT NULL,
    CONSTRAINT gmc_token_box_req_pk PRIMARY KEY (id),
    CONSTRAINT gmc_token_box_req_un UNIQUE (id_gmc_token_acc, box_name),
    CONSTRAINT gmc_token_box_req_acc_fk FOREIGN KEY (id_gmc_token_acc) REFERENCES gmc_token_acc(id)
);

CREATE TABLE gmc_token_box_req_token (
    id_gmc_token_box_req integer NOT NULL,
    token_name text NOT NULL,
    CONSTRAINT gmc_token_box_req_token_pk PRIMARY KEY (id_gmc_token_box_req, token_name),
    CONSTRAINT gmc_token_box_req_token_req_fk FOREIGN KEY (id_gmc_token_box_req) REFERENCES gmc_token_box_req(id)
);
