from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesario para sesiones

# Bancos de preguntas
preguntas = {
    1: [
        {"info": "Los carros eléctricos ayudan a reducir la contaminación porque no emiten CO₂ directamente.",
        "pregunta": "¿Qué gas contaminante reducen los autos eléctricos?",
        "respuestas": ["CO₂", "Oxígeno", "Nitrógeno"],
        "correcta": "CO₂"}
    ],
    2: [
        {"info": "Las fábricas generan desechos que contaminan el aire y el agua.",
        "pregunta": "¿Qué producen muchas fábricas y daña la atmósfera?",
        "respuestas": ["CO₂", "Agua potable", "Vitaminas"],
        "correcta": "CO₂"}
    ],
    3: [
        {"info": "La capa de ozono nos protege de la radiación ultravioleta.",
        "pregunta": "¿Qué pasaría si la capa de ozono desapareciera?",
        "respuestas": ["Aumenta la radiación UV", "Más oxígeno", "Menos calor"],
        "correcta": "Aumenta la radiación UV"}
    ],
    4: [
        {"pregunta": "¿Qué país es el mayor emisor de CO₂ en la actualidad?",
        "respuestas": ["China", "Brasil", "Noruega"],
        "correcta": "China"},
        {"pregunta": "¿Qué gas liberan los combustibles fósiles principalmente?",
        "respuestas": ["CO₂", "Oxígeno", "Hidrógeno"],
        "correcta": "CO₂"},
        {"pregunta": "¿Qué capa protege la Tierra de la radiación solar?",
        "respuestas": ["Ozono", "Nitrógeno", "Helio"],
        "correcta": "Ozono"},
        {"pregunta": "¿Cuál es una fuente de energía renovable?",
        "respuestas": ["Solar", "Carbón", "Gasolina"],
        "correcta": "Solar"},
        {"pregunta": "¿Qué ocurre con el hielo polar por el cambio climático?",
        "respuestas": ["Se derrite", "Aumenta", "Se mantiene igual"],
        "correcta": "Se derrite"},
    ]
}

@app.route("/")
def inicio():
    session.clear()
    session["nivel"] = 1
    session["desbloqueados"] = [1]  # boton 1 desbloqueado al inicio
    return render_template("index.html", desbloqueados=session["desbloqueados"])

@app.route("/nivel/<int:n>")
def nivel(n):
    desbloqueados = session.get("desbloqueados", [])
    if n not in desbloqueados:
        return redirect(url_for("inicio"))

    if n == 4:
        # preguntas aleatorias
        preguntas_seleccionadas = random.sample(preguntas[4], 5)
        session["preguntas4"] = preguntas_seleccionadas
        session["respuestas4"] = []
        return render_template("nivel.html", nivel=n, preguntas=preguntas_seleccionadas, modo="final")
    else:
        pregunta = random.choice(preguntas[n])
        return render_template("nivel.html", nivel=n, pregunta=pregunta, modo="normal")

@app.route("/responder/<int:n>", methods=["POST"])
def responder(n):
    if n == 4:
        # respuestas
        respuestas = session.get("respuestas4", [])
        respuestas.append(request.form.get("respuesta"))
        session["respuestas4"] = respuestas

        if len(respuestas) >= 5:
            # revisar
            preguntas4 = session["preguntas4"]
            correctas = sum(1 for i, p in enumerate(preguntas4) if respuestas[i] == p["correcta"])
            if correctas == 5:
                return render_template("final.html", resultado="ganaste", correctas=correctas)
            else:
                return render_template("game_over.html", correctas=correctas)
        else:
            return redirect(url_for("nivel", n=4))

    else:
        respuesta = request.form.get("respuesta")
        for p in preguntas[n]:
            if respuesta == p["correcta"]:
                desbloqueados = session.get("desbloqueados", [])
                if (n+1) not in desbloqueados:
                    desbloqueados.append(n+1)
                session["desbloqueados"] = desbloqueados
                return redirect(url_for("inicio"))
        return render_template("nivel.html", nivel=n, pregunta=random.choice(preguntas[n]), modo="normal", error="Incorrecto ❌")

if __name__ == "__main__":
    app.run(debug=True)
