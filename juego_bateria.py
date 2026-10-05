from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "ranking.db"


# =========================================================
# BASE DE DATOS
# =========================================================

def crear_base_datos():
    conexion = sqlite3.connect(DATABASE)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            puntos INTEGER NOT NULL,
            fecha TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def obtener_ranking():
    conexion = sqlite3.connect(DATABASE)

    jugadores = conexion.execute("""
        SELECT id, nombre, puntos, fecha
        FROM jugadores
        ORDER BY puntos DESC, id ASC
    """).fetchall()

    conexion.close()

    return jugadores


# =========================================================
# HTML
# =========================================================

HTML = """

<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>⚡ Batería Natural</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    font-family: Arial, sans-serif;

    color: white;

    background:
    linear-gradient(
        135deg,
        #061b2b,
        #064e4e,
        #102b4c
    );

    overflow-x: hidden;
}


/* FONDO */

.burbuja {

    position: fixed;

    bottom: -120px;

    border-radius: 50%;

    background:
    rgba(255,255,255,0.12);

    z-index: -1;

    animation:
    subir 10s linear infinite;
}

.b1 {
    width: 70px;
    height: 70px;
    left: 10%;
}

.b2 {
    width: 110px;
    height: 110px;
    left: 40%;
    animation-duration: 13s;
}

.b3 {
    width: 45px;
    height: 45px;
    left: 75%;
    animation-duration: 8s;
}

.b4 {
    width: 90px;
    height: 90px;
    left: 90%;
    animation-duration: 11s;
}

@keyframes subir {

    from {
        transform: translateY(0);
        opacity: 0;
    }

    30% {
        opacity: 1;
    }

    to {
        transform: translateY(-120vh);
        opacity: 0;
    }
}


/* CONTENEDOR */

.contenedor {

    width: 92%;

    max-width: 900px;

    margin: auto;

    padding: 30px 0;
}


.tarjeta {

    background:
    rgba(0,0,0,0.60);

    backdrop-filter:
    blur(10px);

    border-radius: 25px;

    padding: 35px;

    text-align: center;

    box-shadow:
    0 20px 60px
    rgba(0,0,0,0.5);

    animation:
    aparecer 0.6s ease;
}


@keyframes aparecer {

    from {

        opacity: 0;

        transform:
        translateY(30px)
        scale(0.95);

    }

    to {

        opacity: 1;

        transform:
        translateY(0)
        scale(1);

    }
}


/* TITULOS */

h1 {
    font-size: 42px;
    margin: 15px 0;
}

h2 {
    font-size: 28px;
}

p {
    font-size: 18px;
    line-height: 1.5;
}

.emoji {

    font-size: 80px;

    animation:
    flotar 2s infinite ease-in-out;
}


@keyframes flotar {

    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-15px);
    }
}


/* REGISTRO */

.registro {
    color: #55efc4;
}


input {

    width: 80%;

    max-width: 450px;

    padding: 16px;

    margin: 20px 0;

    border: none;

    border-radius: 12px;

    font-size: 18px;

    text-align: center;
}


input:focus {

    outline:
    3px solid #00cec9;
}


/* BOTONES */

button {

    border: none;

    border-radius: 12px;

    padding: 15px 25px;

    margin: 8px;

    font-size: 17px;

    font-weight: bold;

    color: white;

    background:
    linear-gradient(
        135deg,
        #00b894,
        #00cec9
    );

    cursor: pointer;

    transition: 0.3s;
}


button:hover {

    transform: scale(1.07);

    box-shadow:
    0 0 25px
    rgba(0,255,210,0.6);
}


.secundario {

    background:
    linear-gradient(
        135deg,
        #6c5ce7,
        #a29bfe
    );
}


/* PREGUNTAS */

.informacion {

    display: flex;

    justify-content:
    space-between;

    margin-bottom: 15px;

    font-weight: bold;
}


.puntos {
    color: #55efc4;
}


.progreso {

    width: 100%;

    height: 14px;

    background:
    rgba(255,255,255,0.15);

    border-radius: 20px;

    overflow: hidden;

    margin-bottom: 25px;
}


.barra {

    height: 100%;

    background:
    linear-gradient(
        90deg,
        #00cec9,
        #55efc4
    );

    transition:
    width 0.5s;
}


.opciones {

    display: grid;

    gap: 15px;

    margin-top: 25px;
}


.opcion {

    padding: 18px;

    border-radius: 15px;

    background:
    rgba(255,255,255,0.10);

    border:
    2px solid
    rgba(255,255,255,0.15);

    cursor: pointer;

    font-size: 18px;

    transition: 0.3s;
}


.opcion:hover {

    transform:
    translateX(8px);

    background:
    rgba(0,255,200,0.15);

    border-color:
    #00ffd5;
}


.correcta {

    background:
    #00b894 !important;

    border-color:
    #55efc4 !important;
}


.incorrecta {

    background:
    #d63031 !important;

    border-color:
    #ff7675 !important;
}


.mensaje {

    min-height: 30px;

    margin-top: 20px;

    font-weight: bold;
}


/* RESULTADO */

.puntuacion {

    font-size: 70px;

    color:
    #55efc4;

    font-weight: bold;

    animation:
    pulso 1.5s infinite;
}


@keyframes pulso {

    50% {
        transform: scale(1.1);
    }
}


.posicion {

    font-size: 34px;

    color:
    #ffeaa7;

    margin: 20px;
}


/* RANKING */

.tabla {

    width: 100%;

    margin-top: 25px;

    border-collapse:
    collapse;
}


.tabla th,
.tabla td {

    padding: 15px;

    border-bottom:
    1px solid
    rgba(255,255,255,0.15);
}


.tabla th {

    background:
    rgba(0,206,201,0.25);
}


.tabla tr:hover {

    background:
    rgba(255,255,255,0.08);
}


.medalla {
    font-size: 25px;
}


/* CONFETI */

.confeti {

    position: fixed;

    width: 10px;

    height: 18px;

    top: -30px;

    z-index: 100;

    animation:
    caer 3s linear forwards;
}


@keyframes caer {

    to {

        transform:
        translateY(110vh)
        rotate(720deg);

        opacity: 0;

    }
}


/* CELULAR */

@media(max-width:600px) {

    h1 {
        font-size: 30px;
    }

    h2 {
        font-size: 23px;
    }

    .tarjeta {
        padding: 20px;
    }

    .emoji {
        font-size: 60px;
    }

    .informacion {
        font-size: 14px;
    }

    .opcion {
        font-size: 16px;
    }

}

</style>

</head>


<body>

<div class="burbuja b1"></div>
<div class="burbuja b2"></div>
<div class="burbuja b3"></div>
<div class="burbuja b4"></div>


<div class="contenedor">

<div id="app"></div>

</div>


<script>


/* =====================================================
   VARIABLES
===================================================== */

let nombreJugador = "";

let preguntaActual = 0;

let puntos = 0;


/* =====================================================
   PREGUNTAS
===================================================== */

const preguntas = [

{
    pregunta:
    "¿Cuál puede producir electricidad mediante una reacción química?",

    opciones: [
        "🪨 Una piedra",
        "🍋🥔 Un limón y una papa",
        "🥛 Un vaso de agua"
    ],

    correcta: 1
},

{
    pregunta:
    "¿Qué metales necesitamos para construir una batería natural?",

    opciones: [
        "🔶 Cobre y zinc",
        "📄 Papel y agua",
        "🪵 Madera y plástico"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué produce la reacción química?",

    opciones: [
        "☀️ Luz solar",
        "⚡ Corriente eléctrica",
        "🔥 Fuego"
    ],

    correcta: 1
},

{
    pregunta:
    "¿Cuál funciona como electrodo positivo?",

    opciones: [
        "🔶 Cobre",
        "🪵 Madera",
        "📄 Papel"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Cuál funciona como electrodo negativo?",

    opciones: [
        "🔩 Zinc",
        "📄 Papel",
        "🪵 Madera"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué función cumple el limón o la papa?",

    opciones: [
        "🍋 Actuar como electrolito",
        "💡 Producir luz",
        "🔊 Producir sonido"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Para qué sirven los electrodos?",

    opciones: [
        "⚡ Permiten la transferencia de electrones",
        "🎨 Dan color a la batería",
        "❄️ Enfrían el limón"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué ocurre al conectar varias celdas en serie?",

    opciones: [
        "⚡ Puede aumentar el voltaje",
        "💧 Aparece más agua",
        "🔥 Se produce fuego"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Puede una batería de limón producir energía para dispositivos pequeños?",

    opciones: [
        "✅ Sí, dependiendo del número de celdas",
        "❌ Nunca",
        "🌞 Solo durante el día"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué tipo de energía obtenemos?",

    opciones: [
        "⚡ Energía eléctrica",
        "🌪️ Energía eólica",
        "☀️ Energía solar"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué ocurre con los electrones durante la reacción?",

    opciones: [
        "⚡ Se mueven a través del circuito",
        "❄️ Se congelan",
        "💨 Desaparecen"
    ],

    correcta: 0
},

{
    pregunta:
    "¿Qué ayuda a completar el circuito?",

    opciones: [
        "🔌 Un cable",
        "🪨 Una piedra",
        "📄 Una hoja"
    ],

    correcta: 0
}

];


/* =====================================================
   REGISTRO
===================================================== */

function mostrarRegistro() {

    document.getElementById("app").innerHTML = `

    <div class="tarjeta">

        <div class="emoji">
            🍋🥔⚡
        </div>

        <h1 class="registro">
            DESAFÍO: LA BATERÍA NATURAL
        </h1>

        <h2>
            👤 REGISTRO DEL JUGADOR
        </h2>

        <p>
            Escribe tu nombre para comenzar.
        </p>

        <input
            id="nombre"
            type="text"
            maxlength="25"
            placeholder="Escribe tu nombre..."
            onkeydown="presionarEnter(event)"
        >

        <br>

        <button onclick="comenzarJuego()">
            🚀 COMENZAR
        </button>

        <button
            class="secundario"
            onclick="mostrarRanking()">

            🏆 VER RANKING

        </button>

    </div>

    `;
}


/* =====================================================
   ENTER
===================================================== */

function presionarEnter(event) {

    if(event.key === "Enter") {

        comenzarJuego();

    }

}


/* =====================================================
   COMENZAR
===================================================== */

function comenzarJuego() {

    const input =
    document.getElementById("nombre");

    const nombre =
    input.value.trim();


    if(nombre === "") {

        alert(
            "⚠️ Escribe tu nombre antes de comenzar."
        );

        input.focus();

        return;
    }


    nombreJugador = nombre;

    preguntaActual = 0;

    puntos = 0;


    mostrarPregunta();

}


/* =====================================================
   PREGUNTA
===================================================== */

function mostrarPregunta() {

    const pregunta =
    preguntas[preguntaActual];


    const progreso =
    (preguntaActual /
    preguntas.length) * 100;


    document.getElementById("app")
    .innerHTML = `

    <div class="tarjeta">

        <div class="informacion">

            <span>
                👤 ${escapar(nombreJugador)}
            </span>

            <span class="puntos">
                ⚡ ${puntos} puntos
            </span>

        </div>


        <div class="progreso">

            <div
                class="barra"
                style="width:${progreso}%">
            </div>

        </div>


        <p>
            Pregunta
            ${preguntaActual + 1}
            de
            ${preguntas.length}
        </p>


        <h2>
            ${pregunta.pregunta}
        </h2>


        <div class="opciones">

            ${pregunta.opciones.map(

                (opcion, indice) => `

                <div
                    class="opcion"
                    onclick="
                    responder(
                        ${indice},
                        this
                    )">

                    ${opcion}

                </div>

                `

            ).join("")}

        </div>


        <div
            id="mensaje"
            class="mensaje">

        </div>

    </div>

    `;
}


/* =====================================================
   RESPONDER
===================================================== */

function responder(indice, elemento) {

    const opciones =
    document.querySelectorAll(".opcion");


    opciones.forEach(opcion => {

        opcion.style.pointerEvents =
        "none";

    });


    const pregunta =
    preguntas[preguntaActual];


    const mensaje =
    document.getElementById(
        "mensaje"
    );


    if(indice === pregunta.correcta) {

        elemento.classList.add(
            "correcta"
        );


        puntos += 10;


        mensaje.innerHTML =
        "✅ ¡CORRECTO! +10 puntos";


        mensaje.style.color =
        "#55efc4";


    } else {

        elemento.classList.add(
            "incorrecta"
        );


        /*
        Si tiene 0 puntos,
        no pierde nada.

        Si tiene más de 0,
        pierde 2 puntos.
        */

        if(puntos > 0) {

            puntos -= 2;

        }


        opciones[
            pregunta.correcta
        ].classList.add(
            "correcta"
        );


        mensaje.innerHTML =
        "❌ Incorrecto. -2 puntos";


        mensaje.style.color =
        "#ff7675";

    }


    setTimeout(() => {

        preguntaActual++;


        if(
            preguntaActual <
            preguntas.length
        ) {

            mostrarPregunta();

        } else {

            terminarJuego();

        }

    }, 1300);

}


/* =====================================================
   TERMINAR JUEGO
===================================================== */

async function terminarJuego() {

    crearConfeti();


    try {

        const respuesta =
        await fetch(
            "/guardar",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({

                    nombre:
                    nombreJugador,

                    puntos:
                    puntos

                })

            }
        );


        const datos =
        await respuesta.json();


        if(!respuesta.ok) {

            throw new Error(
                datos.error ||
                "Error al guardar"
            );

        }


        mostrarResultado(
            datos.posicion
        );


    } catch(error) {

        alert(
            "No se pudo guardar el resultado."
        );

        console.error(error);

    }

}


/* =====================================================
   RESULTADO
===================================================== */

function mostrarResultado(posicion) {

    let mensaje = "";


    if(puntos >= 100) {

        mensaje =
        "🏆 ¡INCREÍBLE!";

    } else if(puntos >= 70) {

        mensaje =
        "🔥 ¡Excelente trabajo!";

    } else if(puntos >= 40) {

        mensaje =
        "👏 ¡Muy bien!";

    } else {

        mensaje =
        "💪 ¡Buen intento!";

    }


    document.getElementById("app")
    .innerHTML = `

    <div class="tarjeta">

        <div class="emoji">
            🎉🏆⚡
        </div>


        <h1>
            ¡JUEGO TERMINADO!
        </h1>


        <h2>
            👤 ${escapar(nombreJugador)}
        </h2>


        <p>
            Tu puntuación:
        </p>


        <div class="puntuacion">
            ${puntos}
        </div>


        <p>
            PUNTOS
        </p>


        <div class="posicion">

            🏆 POSICIÓN #${posicion}

        </div>


        <h2>
            ${mensaje}
        </h2>


        <button
            onclick="mostrarRanking()">

            📊 VER RANKING

        </button>


        <button
            class="secundario"
            onclick="mostrarRegistro()">

            🔄 JUGAR DE NUEVO

        </button>

    </div>

    `;
}


/* =====================================================
   RANKING
===================================================== */

async function mostrarRanking() {

    try {

        const respuesta =
        await fetch("/ranking");


        const jugadores =
        await respuesta.json();


        let filas = "";


        jugadores.forEach(
            (jugador, index) => {

            let posicion =
            index + 1;


            let medalla =
            posicion;


            if(posicion === 1) {

                medalla = "🥇";

            }

            else if(posicion === 2) {

                medalla = "🥈";

            }

            else if(posicion === 3) {

                medalla = "🥉";

            }


            filas += `

            <tr>

                <td class="medalla">
                    ${medalla}
                </td>

                <td>
                    ${escapar(jugador.nombre)}
                </td>

                <td>
                    <strong>
                        ${jugador.puntos}
                    </strong>
                </td>

            </tr>

            `;

        });


        if(jugadores.length === 0) {

            filas = `

            <tr>

                <td colspan="3">

                    Todavía no hay jugadores.

                </td>

            </tr>

            `;

        }


        document.getElementById("app")
        .innerHTML = `

        <div class="tarjeta">

            <div class="emoji">
                🏆
            </div>


            <h1>
                RANKING
            </h1>


            <p>
                Clasificación de todos
                los jugadores.
            </p>


            <table class="tabla">

                <thead>

                    <tr>

                        <th>
                            Posición
                        </th>

                        <th>
                            Jugador
                        </th>

                        <th>
                            Puntos
                        </th>

                    </tr>

                </thead>


                <tbody>

                    ${filas}

                </tbody>

            </table>


            <br>


            <button
                onclick="mostrarRegistro()">

                👤 NUEVO JUGADOR

            </button>

        </div>

        `;


    } catch(error) {

        alert(
            "No se pudo cargar el ranking."
        );

        console.error(error);

    }

}


/* =====================================================
   SEGURIDAD PARA NOMBRES
===================================================== */

function escapar(texto) {

    const div =
    document.createElement("div");

    div.textContent =
    texto;

    return div.innerHTML;

}


/* =====================================================
   CONFETI
===================================================== */

function crearConfeti() {

    const colores = [

        "#00cec9",
        "#55efc4",
        "#ffeaa7",
        "#fdcb6e",
        "#ff7675",
        "#a29bfe",
        "#74b9ff"

    ];


    for(
        let i = 0;
        i < 80;
        i++
    ) {

        const confeti =
        document.createElement(
            "div"
        );


        confeti.className =
        "confeti";


        confeti.style.left =
        Math.random() *
        100 +
        "vw";


        confeti.style.background =
        colores[
            Math.floor(
                Math.random() *
                colores.length
            )
        ];


        confeti.style.animationDelay =
        Math.random() *
        1.5 +
        "s";


        document.body.appendChild(
            confeti
        );


        setTimeout(() => {

            confeti.remove();

        }, 3500);

    }

}


/* =====================================================
   INICIAR PÁGINA
===================================================== */

mostrarRegistro();

</script>

</body>

</html>

"""


# =========================================================
# PÁGINA PRINCIPAL
# =========================================================

@app.route("/")
def inicio():

    return render_template_string(HTML)


# =========================================================
# GUARDAR RESULTADO
# =========================================================

@app.route("/guardar", methods=["POST"])
def guardar():

    datos = request.get_json()

    nombre = datos.get(
        "nombre",
        ""
    ).strip()

    puntos = int(
        datos.get(
            "puntos",
            0
        )
    )


    if not nombre:

        return jsonify({
            "error":
            "Nombre vacío"
        }), 400


    # Evita puntuaciones negativas

    if puntos < 0:

        puntos = 0


    fecha = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )


    conexion = sqlite3.connect(
        DATABASE
    )

    cursor = conexion.cursor()


    cursor.execute("""
        INSERT INTO jugadores
        (nombre, puntos, fecha)
        VALUES (?, ?, ?)
    """, (
        nombre,
        puntos,
        fecha
    ))


    conexion.commit()


    # ID del jugador recién guardado

    nuevo_id = cursor.lastrowid


    conexion.close()


    # Obtener ranking actualizado

    ranking = obtener_ranking()


    # Buscar posición

    posicion = 1


    for indice, jugador in enumerate(
        ranking
    ):

        if jugador[0] == nuevo_id:

            posicion = indice + 1

            break


    return jsonify({

        "posicion":
        posicion

    })


# =========================================================
# RANKING
# =========================================================

@app.route("/ranking")
def ranking():

    jugadores = obtener_ranking()


    datos = []


    for jugador in jugadores:

        datos.append({

            "id":
            jugador[0],

            "nombre":
            jugador[1],

            "puntos":
            jugador[2],

            "fecha":
            jugador[3]

        })


    return jsonify(datos)


# =========================================================
# INICIAR SERVIDOR
# =========================================================

if __name__ == "__main__":

    crear_base_datos()


    print("")
    print("==========================================")
    print("       ⚡ BATERÍA NATURAL ⚡")
    print("==========================================")
    print("")
    print("Servidor iniciado.")
    print("")
    print("En esta computadora:")
    print("http://127.0.0.1:5000")
    print("")
    print("Para otros dispositivos:")
    print("Usa la dirección IPv4 de esta computadora.")
    print("")


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )