import jinja2.exceptions
from flask import Flask, render_template, request
import mysql.connector
import re

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
        sc_lijst = []
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
        cursor.execute("select * from blast_resultaten where description like '%" + invoer + "%'")


        # Alle resultaten eruit halen
        resultaat = cursor.fetchall()
        # Cursor en database closen
        cursor.close()
        mydb.close()

        for i in resultaat:
            print(i[2])
            scientific_name = re.findall("\[[^\]]*\]",i[2])
            print(scientific_name)
            if scientific_name != []:
                sc_name = scientific_name[0]
                print(sc_name)
                sc = str(sc_name).strip("[]")
                print(sc)
                sc_lijst.append(sc)
            # Returnen HTML pagina en resultaat
        return render_template("website_project.html",
                               len=len(resultaat), invoer=resultaat, sclijst=sc_lijst)
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
