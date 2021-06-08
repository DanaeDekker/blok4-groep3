-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2021-06-08 11:47:12.102

-- tables
-- Table: blast_resultaten
CREATE TABLE blast_resultaten (
    result_id int NOT NULL,
    accession varchar(25) NOT NULL,
    description varchar(100) NOT NULL,
    e_value Float NOT NULL,
    bitscore int NOT NULL,
    seq_id int NOT NULL,
    organisme_id int NOT NULL,
    CONSTRAINT blast_resultaten_pk PRIMARY KEY (result_id)
);

-- Table: organisme
CREATE TABLE organisme (
    organisme_id int NOT NULL,
    scientific_name varchar(100) NOT NULL,
    CONSTRAINT organisme_pk PRIMARY KEY (organisme_id)
);

-- Table: sequenties
CREATE TABLE sequenties (
    seq_id int NOT NULL,
    header varchar(60) NOT NULL,
    sequentie varchar(301) NOT NULL,
    CONSTRAINT sequenties_pk PRIMARY KEY (seq_id)
);

-- foreign keys
-- Reference: blast_resultaten_organisme (table: blast_resultaten)
ALTER TABLE blast_resultaten ADD CONSTRAINT blast_resultaten_organisme FOREIGN KEY blast_resultaten_organisme (organisme_id)
    REFERENCES organisme (organisme_id);

-- Reference: blast_resultaten_sequenties (table: blast_resultaten)
ALTER TABLE blast_resultaten ADD CONSTRAINT blast_resultaten_sequenties FOREIGN KEY blast_resultaten_sequenties (seq_id)
    REFERENCES sequenties (seq_id);

-- End of file.

