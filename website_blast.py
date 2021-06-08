from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route('/')
def database():
    """Home pagina met connectie aan de database

    :return: HTML pagina met resultaten
    """
    # Connectie met de database
    mydb = mysql.connector.connect(host="mysql.dehoogjes.nl",
                                   user="dehoogjesnl",
                                   password="Maritdh@2000",
                                   auth_plugin='mysql_native_password',
                                   database="dehoogjesnl")
    cursor = mydb.cursor()
    # Dingen invoeren en knopje aan de database linken
    invoer = request.args.get("invoer", "")
    knopje = request.args.get("knopje", "")
    cursor.execute(
        "select * from blast_resultaten where description like"
        " '%" + invoer + "%'")
    # Alle resultaten eruit halen
    resultaat = cursor.fetchall()
    # Cursor en database closen
    cursor.close()
    mydb.close()
    # Returnen HTML pagina en resultaat
    return render_template("website_project.html", len=len(resultaat),
                           invoer=resultaat)


@app.route('/tabel')
def web_box():
    """Tabel pagina met connectie aan de database

    :return: HTML pagina met de 10 meest voorkomende organismen uit
    de database
    """
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
        "select scientific_name, count(*) from blast_resultaten"
        " group by scientific_name order by count(*) desc limit 10;")
    # Alle resultaten eruit halen
    resultaat = cursor.fetchall()
    # Cursor en database closen
    cursor.close()
    mydb.close()
    # Returnen HTML pagina en resultaat
    return render_template("website_plot.html", invoer=resultaat)


if __name__ == '__main__':
    app.run()
