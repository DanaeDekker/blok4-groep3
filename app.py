import jinja2.exceptions
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route('/')
def web_home():
    """De homepagina van de website

    :return: HTML pagina met een overzicht van de website
    """
    # Returnen van HTML pagina
    return render_template("website_home.html")

@app.route('/database')
def database():
    """Database pagina met connectie aan de database

    :return: HTML pagina met resultaten uit de database
    """
    try:
        lijst = []
        # Connectie met de database
        mydb = mysql.connector.connect(
            host="mysql.dehoogjes.nl",
            user="dehoogjesnl",
            password="Maritdh@2000",
            auth_plugin='mysql_native_password',
            database="dehoogjesnl",
            buffered=True)

        cursor = mydb.cursor()
        # Dingen invoeren en knopje aan de database linken
        invoer = request.args.get("invoer", "")
        # deze regel kon niet in pep8 want dan doet de query het niet meer
        cursor.execute("select accession ,description, scientific_name, e_value, bitscore from blast_resultaten inner join organisme on blast_resultaten.organisme_id = organisme.organisme_id where description like '%" + invoer + "%'")
        # Alle resultaten eruit halen
        resultaat = cursor.fetchall()

        # Cursor en database closen
        cursor.close()
        mydb.close()

            # Returnen HTML pagina en resultaat
        return render_template("website_project.html",
                               len=len(resultaat), invoer=resultaat)
    except SyntaxError:
        print("Er klopt iets niet in de code")
    except TypeError:
        print("Object type klopt niet")
    except NameError:
        print("Kan variabele niet vinden")
    except mysql.connector.errors.ProgrammingError:
        print("Dit bestaat niet in de database")
    except jinja2.exceptions.TemplateNotFound:
        print("Er klopt iets niet bij het aanroepen van de"
              " HTML template")



@app.route('/pie')
def web_box():
    """Overzicht pagina met connectie aan de database

    :return: HTML pagina met de 10 meest voorkomende organismen uit
    de database
    """
    try:
        # Connectie met de database
        mydb = mysql.connector.connect(host="mysql.dehoogjes.nl",
                                    user="dehoogjesnl",
                                    password="Maritdh@2000",
                                    auth_plugin='mysql_native_password',
                                    database="dehoogjesnl")
        cursor = mydb.cursor()
        # Dingen invoeren aan de database linken
        invoer = request.args.get("invoer", "")
        cursor.execute(
            "select scientific_name, count(*) from organisme"
            " group by scientific_name order by count(*) desc limit 10;")
        # Alle resultaten eruit halen
        resultaat = cursor.fetchall()
        # Cursor en database closen
        cursor.close()
        mydb.close()
        # Returnen HTML pagina en resultaat
        return render_template("website_plot.html", invoer=resultaat)

    except SyntaxError:
        print("Er klopt iets niet in de code")
    except TypeError:
        print("Object type klopt niet")
    except NameError:
        print("Kan variabele niet vinden")
    except mysql.connector.errors.ProgrammingError:
        print("Dit bestaat niet in de database")
    except jinja2.exceptions.TemplateNotFound:
        print("Er klopt iets niet bij het aanroepen van de"
              " HTML template")





if __name__ == '__main__':
    app.run()
