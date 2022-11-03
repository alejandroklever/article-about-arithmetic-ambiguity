import streamlit as st

import grammars.left_associative_grammar as lag
import grammars.right_associative_grammar as rag
import grammars.symbol_less_grammar as slg


E = "8 / 2 (2 + 2)"
S = "8 / 2 * (2 + 2)"

st.title("El ambiguo caso de `8/2(2+2)`")
st.subheader("Un análisis desde el punto vista sintáctico")
st.caption("""
Por Alejandro Klever Clemente
[![Twitter Follow](https://img.shields.io/twitter/follow/aklever4197?label=Follow%20on%20Twitter&color=blue&style=flat&logo=twitter)](https://twitter.com/aklever4197)
[![GitHub followers](https://img.shields.io/github/followers/alejandroklever?label=Follow%20on%20Github&style=flat&color=lightgray&logo=github)](https://github.com/alejandroklever)
"""
)

"""
#### Introducción

En este pequeño artículo me gustaría agregar un poco de luz 
desde el punto de vista de programación a la ambigüedad del resultado
de la expresión aritmética `e = 8 / 2 (2 + 2)`.

Una confusión bastante común dado que muchos equipos de cómputo darán
como resultado 1 al poner literalmente esta expresión en lugar de
poner una multiplicación explícita, contradiciendo el convenio de
resolución de operaciones de igual precedencia en el orden de aparición.
¿Pero, por qué es esto realmente un error?

Lo primero es analizar desde el punto de vista computacional donde esta el error.
Lo curioso es que este no es producto de una mala programación interna del circuito
lógico que realiza las operaciones a más bajo nivel, y tampoco a la hora de colocar
el orden de las instrucciones en el cpu, sino que es producto de un proceso
mucho mas superficial y es la traducción de la expresión `e`, que no es más que
una cadena de texto, a instrucciones que pueda entender un procesador.

Para este análisis usaremos primero una versión menos ambigua de la expresión original a 
la que llamaremos `s = 8 / 2 * (2 + 2)`.

Algo que no se explica mucho en el mundo mas común de la programación es que
las computadoras tienen serios probremas para enteder lenguajes, de hecho, 
están bien definidas las reglas que deben seguir estos para ser comprendido
por las computadoras. Pero, ¿cómo conseguimos analizar si un lenguaje puede o
no cumplir estas reglas? Bueno, aquí es donde la cosa se pone interesante,
tenemos que "matematizar" el lenguaje, y esto se hace escribiendo una gramática
que pueda generar y comprender todas las cadenas de texto de ese lenguaje.

Pero... ¿Qué es una gramática en el contexto de la programación? Una gramática
es formalmente definida como la combinación de un conjunto de terminales
(el vocabulario), un conjunto de no terminales (símbolos generadores),
un símbolo no terminal inicial y un conjunto de producciones que transformen. 
Espera, se que es mucho para procesar, pero no huyas aún, veamos un ejemplo.
Crearemos una gramática para un lenguaje de operaciones aritmeticas que
solo acepte sumas, restas, multiplicaciones, divisiones y parentización,
a la cual pertenece nuestra cadena de ejemplo `s`.

### Caso `s = 16`

##### Definimos los terminales
    { number, +, -, *, /, (, ) }

##### Definamos los no terminales:
    { expr, term, fact }

##### Definamos el símbolo inicial
    expr

Y ahora es donde comienza la parte que hara que nuestra cadena `s` sea evaluada
como 16.

##### Definamos las producciones:
    # Una expresión se define como la suma o resta
    # entre una expresión y un término o 
    # un término en solitario de la siguiente forma
    expr -> expr + term
    expr -> expr - term
    expr -> term

    # Un término se define como la multiplicacion o division
    # entre un término y un factor o
    # un factor en solitario de la siguiente forma
    term -> term * fact
    term -> term / fact
    term -> fact

    # Un factor se define como un
    # numero o una expresión dentro de un parentesis
    # de la siguiente forma
    fact -> ( expr )
    fact -> number

Como podemos obervar nuestra gramática asocia términos hacia la izquierda
porque definimos el no terminal más prioritario a la izquierda del operador,
en este caso una expresión tiene mayor prioridad que un término, y un término
tiene mayor prioridad que un factor.
"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresión", value=S, key="left associative"
)

lag_result = lag.parser(lag.lexer(s))

if lag_result is not None:
    col2.caption("Resultado")
    col2.text(f"{lag_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramática")

"""
### Caso `s = 1`

Para este caso mantendremos tanto los terminales, no terminales y símbolo inical
de la gramática anterior pero haremos un ligero cambio en las producciones 
(los terminales, los no terminales y el símbolo inicial seran los mismos)

##### Nuevas producciones:
    expr -> term + expr 
    expr -> term - expr
    expr -> term

    term -> fact * term
    term -> fact / term
    term -> fact

    fact -> ( expr )
    fact -> number

Como podemos observar el único cambio que hicimos fue intercambiar el orden de los no terminales en las 
operaciones, poniendo al de menor nivel a la izquierda del operador. 
"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresión", value=S, key="right associative"
)

rag_result = rag.parser(rag.lexer(s))

if rag_result is not None:
    col2.caption("Resultado")
    col2.text(f"{rag_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramática")

"""
Lo mas impresionante de esto que hemos encontrado 2 gramaticas diferentes que analizan sintactica y lexicograficamente
el lenguaje de las expresiones aritmeticas, pero producen arboles de ejecucion diferentes.
"""

col1, col2 = st.columns(2)

_, graph = lag_result.to_graph()
col1.markdown("##### Arbol de ejecucion `s = 16`")
col1.graphviz_chart(graph)

_, graph = rag_result.to_graph()
col2.markdown("##### Arbol de ejecucion `s = 1`")
col2.graphviz_chart(graph)


"""
Y aunque estos casos nos lleven a inclinarnos a asociar a la izquierda por una cuestion de naturalidad,
ambas gramaticas son consideradas correctas porque ambas generan y entienden todas las cadenas 
del lenguaje de expresiones aritmeticas.
"""

"""
### Caso `e = 8 / 2 (2 + 2)`

Una vez analizado como un simple cambio en la gramática puede afectar a como se ejecutan
a la resolucion de la misma, quiero dejar una cosa en clara: Si eres porgramador, por favor, usa la primera gramática.
Por otro lado no podemos olvidar que aquí estabamos trabajando con una expresión que usa todos los símbolos aritmeticos,
¿Que pasaría si a nuestro lenguaje le damos la posibilidad de operar omitiendo el símbolo `*`?
Primeramente debemos cambiar la gramática con la que venimos para poder analizar expresiones del tipo `2(2 + 2)`, puesto a que nuestro lenguaje cambió...

Para interpretar el nuevo lenguaje agregaremos el no terminal `conj` y haremos los siguientes cambios en las
producciones.

##### Nuevas producciones:
    expr -> expr + term
    expr -> expr - term
    expr -> term

    term -> term * conj
    term -> term / conj
    term -> conj

    conj -> fact ( expr )
    conj -> fact

    fact -> ( expr )
    fact -> number

Como puede comprobar a continuación, esta gramática ya nos permite enteder expresiones 
mas fáciles de escribir. Aún así el resultado de la expresión `e` es 1, y el de `s` es 16 
"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresión",
    value=E,
    key="symboless grammar operation 1",
)

slg_result = slg.parser(slg.lexer(s))

if slg_result is not None:
    col2.caption("Resultado")
    col2.text(f"{slg_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramática")


col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresión",
    value=S,
    key="symboless grammar operation 2",
)

slg.lexer.column = 0
slg.lexer.position = 0
slg_result = slg.parser(slg.lexer(s))

if slg_result is not None:
    col2.caption("Resultado")
    col2.text(f"{slg_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramática")

"""
¿Y esto por qué? ¿No estamos asociando a la izquierda como Dios manda? Bueno, como
pueden comprobar en la gramática la prioridad de operacion hace que un `conj` sea
más prioritario de resolver que un `term` ¿Y por qué no le damos la misma prioridad?
Pues, realmente es un tema mas complejo de explicar, pero está relacionado con
conflictos en prefijos de la parte derecha de las producciones, por lo que no es
viable resolverlo de esta forma. No obstante invito a todo el que quiera a generar
una gramática slr que logre mantener a las operaciones al mismo nivel.

En vista de que no pueden tener el mismo nivel de prioridad, solo queda escoger cual
de los dos tendrá la mayor prioridad. Y la razon por la que escogemos que el conj tendrá 
mayor prioridad operacional es porque en el caso contrario sencillamente tendríamos
una gramática que no es capaz de entender ni generar todas las cadenas del lenguaje
de expresiones aritmeticas con omisión de símbolos.

Esto no es algo raro. Lenguajes de programación de propósito cientifico como Julia aceptan esta
notación y lo resuelven dándole más prioridad al no expresiones con coeficientes que a la división o
multiplicación literal. Para más info sobre como Julia hace esto puede ir a la [Documentación Oficial](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/#man-numeric-literal-coefficients). 
"""

"""
### Conclusiones

He intentado resumir en este artículo todo una introducción muy breve y algo informal sobre es
el análisis de los lenguajes computables con el fin de arrojar luz a los 2 planteamientos que incitaron
este texto:

- Lo que a priori parece ser un error quizas sea el resultado de un convenio acordado porque es la mejor forma de hacer algo o bien porque es la unica forma.

- Los convenios son normas comunicativas para omitir información y así hacer mas fluida la comunicación, por lo cual usarlos y aceptarlos esta bien siempre y cuando entendamos que los convenios están atados a las reglas de las matemáticas, pero las estas no están atadas a los convenios.

Espero que esto les haya ayudado a entender que como un equipo de cómputo resuelve este tipo
de ambigüedades.
"""

"""
### Links

Este artículo fue escrito y publicado gracias a [Streamlit](https://streamlit.io/),
una herramienta que nos permite escribir aplicaciones webs con Python y desplegarlas en la nube.

El código fuente de este artículo puede ser encontrado en [![Star the Repo](https://img.shields.io/github/stars/alejandroklever/article-about-arithmetic-ambiguity?label=Star%20the%20Repo&style=flat&color=gray&logo=github)](https://github.com/alejandroklever/article-about-arithmetic-ambiguity)

Para la creación de las gramáticas fue usada la biblioteca de Python [![PyJapt Repo](https://img.shields.io/github/stars/alejandroklever/PyJapt?label=pyjapt&style=flat&color=blue&logo=python)](https://github.com/alejandroklever/PyJapt)
"""
