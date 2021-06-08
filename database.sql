-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2021-05-18 10:37:53.906

-- tables
-- Table: blast_resultaten
CREATE TABLE blast_resultaten (
    result_id int NOT NULL,
    accession varchar(50) NOT NULL,
    description varchar(1000) NOT NULL,
    scientific_name varchar(200) NOT NULL,
    e_value float NOT NULL,
    identity int NOT NULL,
    bitscore int NOT NULL,
    seq_id int NOT NULL,
    CONSTRAINT blast_resultaten_pk PRIMARY KEY (result_id)
);

-- Table: sequenties
CREATE TABLE sequenties (
    seq_id int AUTO_INCREMENT NOT NULL,
    header varchar(100) NOT NULL,
    sequentie varchar(500) NOT NULL,
    CONSTRAINT sequenties_pk PRIMARY KEY (seq_id)
);



-- foreign keys
-- Reference: blast_resultaten_sequenties (table: blast_resultaten)
ALTER TABLE blast_resultaten ADD CONSTRAINT blast_resultaten_sequenties FOREIGN KEY blast_resultaten_sequenties (seq_id)
    REFERENCES sequenties (seq_id);



-- End of file.

