from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "mysecretkey"

colores = {
    "Amarillo": "#ffff00",
    "Negro": "#000000",
    "Verde": "#00ff00",
    "Rojo": "#ff0000",
    "Cyan": "#00ffff",
    "Blanco": "#ffffff",
    "Morado": "#ff00ff",
    "Azul": "#0000ff"
}

def nuevo_secreto():
    return [random.choice(list(colores.values())) for _ in range(4)]

def random_colores():
    return [random.choice(list(colores.values())) for _ in range(4)]

def calcula_resultado(intento, secreto, historial):
    fallos = 0
    aciertos = 0
    for i in range(4):
        if intento[i] == secreto[i]:
            aciertos += 1
        elif intento[i] in secreto:
            fallos += 1
    historial.append({"intentos": intento, "aciertos": aciertos, "fallos": fallos})
    session["historial"] = historial
    return f"Aciertos [{aciertos}] - Fallos [{fallos}]"

@app.route("/", methods=["GET", "POST"])
def jugar():
    historial = session.get("historial", [])
    secreto = session.get("secreto", nuevosecreto)
    if request.method == "POST":
        intento = [request.form[f"intento[{i}]"] for i in range(4)]
        resultado_jugador = calcula_resultado(intento, secreto, historial)
        return render_template("juego.html", colores=colores, intento=intento, resultado_jugador=resultado_jugador, historial=historial, secreto=secreto)
    return render_template("juego.html", colores=colores, historial=historial, secreto=secreto)

@app.route("/reiniciar")
def reiniciar():
    session.pop("historial", None)
    session.pop("secreto", None)
    return redirect(url_for("jugar"))

if __name__ == "__main__":
    nuevosecreto = nuevo_secreto()
    app.run(debug=True)