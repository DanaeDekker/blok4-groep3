from Bio.Blast import NCBIWWW, NCBIXML
import re
import mysql.connector

# Connecten aan de database
mydb = mysql.connector.connect(
    host="mysql.dehoogjes.nl",
    user="dehoogjesnl",
    password="Maritdh@2000",
    auth_plugin='mysql_native_password',
    database="dehoogjesnl"))
cursor = mydb.cursor()


def lees_inhoud(bestandnaam):
    """Inlezen van het bestand

    @return: lijst_header en lijst_seq - sequenties en headers in een
    lijst
    """
    # lege lijsten aanmaken
    lijst_header = []
    lijst_seq = []
    try:
        # bestand openen
        with open(bestandnaam, "r") as bestand:
            # Door het bestand lopen
            for line in bestand:
                # Regel splitten op tab
                regel = line.split("\t")
                # Juiste kolommen toevoegen aan de lijst
                lijst_seq.append(regel[1])
                lijst_header.append(regel[0])
                lijst_seq.append(regel[4])
                lijst_header.append(regel[3])
                # Returnen van de lijsten
        return lijst_seq, lijst_header
    except FileNotFoundError:
        print('Bestand %s niet aanwezig' % bestand)
    except IOError:
        print('Bestand %s niet leesbaar' % bestand)
    except NameError:
        print("Kan variabele niet vinden")
    except ValueError:
        print("Deze opgegeven waarden kloppen niet")
    except IndexError:
        print("Je zoekt buiten bereik van de lijst")


def header_seq(lijst_header, lijst_seq):
    """Headers en sequenties in de database zetten

    @param lijst_header: alle headers in een lijst
    @param lijst_seq: alle sequenties in een lijst
    @return: -
    """
    try:
        # Door het bestand lopen
        for i in range(0, len(lijst_header)):
            # Alle headers en sequenties toevoegen aan de database
            cursor.execute(
                "insert into sequenties (header, sequentie)"
                " values ('" + lijst_header[i] +
                "','" + lijst_seq[i] + "')")
            # Naar de database sturen
            mydb.commit()
    except NameError:
        print("Kan variabele niet vinden")
    except ValueError:
        print("Deze opgegeven waarden kloppen niet")
    except SyntaxError:
        print("Er klopt iets niet in de code")
    except IndexError:
        print("Je zoekt buiten bereik van de lijst")


def fasta_invoer(lijst_seq):
    """Blast uitvoeren en wegschrijven in een XML file

    @param lijst_seq: lijst met alle sequenties
    @return: XML-file met blast resultaten erin
    """
    count = 0
    try:
        # Door het hele bestand lopen
        for sequentie in lijst_seq[0:len(lijst_seq)]:
            # Teller meegeven
            print("Start BLAST....", count)
            # Filters en instellingen van BLAST toevoegen
            result_handle = NCBIWWW.qblast("blastx", "nr", sequentie,
                                           expect=0.01, hitlist_size=10)
            print("BLAST resultaat in variabele")
            # Een nieuw bestand aanmaken
            with open("my_blast.xml", "a") as out_handle:
                blast_results = result_handle.read()
                # Wegschrijven resultaten BLAST
                out_handle.write(blast_results)
            print("Klaar", count)
            # Na elke sequentie die geblast is +1
            count += 1
    except NameError:
        print("Kan variabele niet vinden")
    except ValueError:
        print("Deze opgegeven waarden kloppen niet")
    except IndexError:
        print("Je zoekt buiten bereik van de lijst")


def parsing_xml():
    """Parsen van het bestand en De BLAST resultaten in
     de database zetten

    @return: -
    """
    teller = 0
    count_index = 0
    try:
        # Door het bestand lopen
        with open("my_blast.xml", "r") as out_handle:
            # Parsen BLAST output
            blast_records = NCBIXML.parse(out_handle)
            # Selecteren van eerste query
            next(blast_records)
            # Door elk alignment heen lopen die bij een sequentie hoort
            for blast_record in blast_records:
                # Getal meegeven per alignment
                count_index += 1
                # Over alle alignments heen lopen
                for alignment in blast_record.alignments:
                    # Over alle informaties binnen de alignment lopen
                    for hsp in alignment.hsps:
                        teller += 1
                        # Description uit bestand halen
                        description = alignment.title
                        # Accession code uit bestand halen
                        accession = alignment.accession
                        # Bitscore uit bestand halen
                        bit_score = hsp.score
                        # E-value uit bestand halen
                        e_value = hsp.expect
                        # Scientific name uit description halen met
                        # een regex
                        scientific_name = re.findall("\[[^\]]*\]", description)
                        if scientific_name[0] != "":
                            sc_name = scientific_name[0]
                            sc_name = str(sc_name).strip("[]")
                        # Alles toevoegen aan de database
                            cursor.execute(
                                "insert into blast_resultaten (result_id,"
                                " accession, description, scientific_name,"
                                " e_value, bitscore, seq_id) values"
                                " ('" + str(teller) + "','" + accession +
                                "','" + description + "','" +
                                scientific_name + "','"
                                + str(e_value) + "','" + str(bit_score) +
                                "','" + str(count_index) + "')")
                        # Naar de database sturen
                            mydb.commit()
    except NameError:
        print("Kan variabele niet vinden")
    except ValueError:
        print("Deze opgegeven waarden kloppen niet")
    except SyntaxError:
        print("Er klopt iets niet in de code")
    except IndexError:
        print("Je zoekt buiten bereik van de lijst")
    except TypeError:
        print("Kan van integer geen string maken")


if __name__ == '__main__':
    bestand = "dataset_groep_3.txt"
    # lijst_seq, lijst_header = lees_inhoud(bestand)
    # fasta_invoer(lijst_seq)
    # header_seq(lijst_header, lijst_seq)
    parsing_xml()
