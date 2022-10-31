import streamlit as st
import grammars.left_associative_grammar as lag
import grammars.right_associative_grammar as rag
import grammars.symbol_less_grammar as slg

DEFAULT_EXPR = "8 / 2 * (2 + 2)"


st.title("8 : 2(2 + 2)")
st.subheader("Un analisis desde el punto vista sintactico")

"""
En este pequeño articulo me gustaria agregar un poco de luz 
desde el punto de vista de programacion a la ambiguedad de la
expresion aritmetica `8 : 2(2 + 2)`.

Una de las bases en las que se han apoyado algunos detractores de
la ambiguedad de dicha expresion fue en el propio resultado que podian
dar los equipos de computo. Pero estos equipos de computo parecian tampoco
estar muy de acuerdo entre si, pues algunos daban como resultado 1 y otros daban
como resultado 16.

Lo primero es analizar desde el punto de vista computacional donde esta el error.
Para esto usaremos primero una version menos ambigua de la expresion original a 
la que llamaremos `s = 8 : 2 * (2 + 2)`. Con esto en mente uno pensaria que el 
error se encuentra en alguna parte mal programada del proceso de calculo de los 
propios de computo. Pero hay una parte mas superficial que sucede mucho antes de 
que un programa se convierta en 0s y 1s en un circuito logico. Y es el proceso de 
traducir una cadena de texto como la expresion `s` a puras instrucciones 
codificadas en 0s y 1s.

Algo que no se explica mucho en el mundo mas comun de la programacion es que las computadoras tienen
serios probremas para enteder lenguajes, de hecho, estan bien definidas las reglas que debe seguir uno para este ser comprendido
por las computadoras ¿Pero, como conseguimos analizar si un lenguaje puede o no cumplir estas reglas?
Bueno, aqui es donde la cosa se pone interesante, tenemos que "matematizar" el lenguaje, y esto se hace
escribiendo una gramatica que pueda generar todas las cadenas de texto de ese lenguaje.

Pero... ¿Qué es una gramática en el contexto de la programación? Una gramatica es formalmente definida
como la combinacion de un conjunto de terminales (el vocabulario), un conjunto de no terminales (simbolos generadores),
un simbolo no terminal inicial y un conjunto de producciones que transformen. Espera, no huyas aun. Para analizar un ejemplo,
creemos una gramatica para un lenguaje de operaciones aritmeticas que solo acepte sumas, restas, multiplicaciones,
divisiones y parentizacion, a la cual pertenece nuestra cadena de ejemplo `s`.

### Caso `s = 16`

#### Definimos los terminales
    { number, +, -, *, /, (, ) }

#### Definamos los no terminales:
    { expr, term, fact }

#### Definamos el simbolo inicial
    expr

Y ahora es donde comienza la parte que hara que nuestra cadena `s` sea evaluada como 16. Hagamos el ejemplo de 16 primero.

#### Definamos las producciones:
    # Una expresion se define como la suma o resta
    # entre una expresion y un termino o 
    # un termino en solitario de la siguiente forma
    expr -> expr + term
    expr -> expr - term
    expr -> term

    # Un termino se define como la multiplicacion o division
    # entre un termino y un factor o
    # un factor en solitario de la siguiente forma
    term -> term * fact
    term -> term / fact
    term -> fact

    # Un factor se define como un
    # numero o una expresion dentro de un parentesis
    # de la siguiente forma
    fact -> ( expr )
    fact -> number

Como podemos obervar nuestra gramatica asocia terminos hacia la izquierda porque definimos
el no terminal mas prioritario a la izquierda del operador, en este caso una expresion tiene
mayor nivel que un termino, y un termino tiene mayor nivel que un factor.

"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresion", value=DEFAULT_EXPR, key="left associative"
)

lag_result = lag.parser(lag.lexer(s))

if lag_result is not None:
    col2.caption("Resultado")
    col2.text(f"{lag_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramatica")

"""
### Caso `s = 1`

Para este caso mantendremos tanto los terminales, no terminales y simbolo inical de la gramatica anterior
pero haremos un ligero cambio en las producciones

#### Nuevas producciones:
    expr -> term + expr 
    expr -> term - expr
    expr -> term

    term -> fact * term
    term -> fact / term
    term -> fact

    fact -> ( expr )
    fact -> number

Como podemos observar el unico cambio que hicimos fue intercambiar el orden de los no terminales en las 
operaciones, poniendo al de menor nivel a la izquierda del operador. 
"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresion", value=DEFAULT_EXPR, key="right associative"
)

rag_result = rag.parser(rag.lexer(s))

if rag_result is not None:
    col2.caption("Resultado")
    col2.text(f"{rag_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramatica")

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
Una vez analizado como un simple cambio en la gramatica puede afectar a como se ejecutan
a la resolucion de la misma, quiero dejar una cosa en clara: Si eres porgramador, por favor, usa la primera gramatica.
Por otro lado no podemos olvidar que aqui estabamos trabajando con una expresion que usa todos los simbolos aritmeticos,
¿Que pasaria si a nuestro lenguaje le damos la posibilidad de operar omitiendo el simbolo `*`?
Primeramente debemos cambiar la gramatica con la que venimos para poder analizar expresiones del tipo `2(2 + 2)`, puesto a que nuestro lenguaje cambió...

Para interpretar el nuevo lenguaje agregaremos el no terminal conj y haremos los siguientes cambios en las
producciones.

#### Nuevas producciones:
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

Como puede comprobar a continuacion, esta gramatica ya nos permite enteder expresiones 
mas fáciles de escribir, el resultado de la expresion `r` es 1, y el de `s` es 16 
"""

col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresion", value="8 / 2 (2 + 2)", key="symboless grammar operation 1"
)

slg_result = slg.parser(slg.lexer(s))

if slg_result is not None:
    col2.caption("Resultado")
    col2.text(f"{slg_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramatica")


col1, col2 = st.columns(2)
s = col1.text_input(
    "Introduce una expresion", value="8 / 2 * (2 + 2)", key="symboless grammar operation 2"
)

slg.lexer.column = 0
slg.lexer.position = 0
slg_result = slg.parser(slg.lexer(s))

if slg_result is not None:
    col2.caption("Resultado")
    col2.text(f"{slg_result.evaluate()}")
else:
    col2.caption("Error")
    col2.text(f"Expresion invalida para esta gramatica")

"""
¿Y esto por qué? ¿No estamos asociando a la izquierda como Dios manda? Bueno, como pueden comprobar
en la gramatica la prioridad de operacion hace que un `conj` sea mas prioritario de resolver que un `term`
¿Y por qué no le damos la misma prioridad? Pues, realmente es un tema mas complejo de explicar, pero está
relacionado con conflictos en prefijos de la parte derecha de las producciones, por lo que no es viable resolverlo
de esta forma. No obstante insto a que todo el que quiera a generar una gramatica slr que logre mantener
mantenter a las operaciones al mismo nivel.

En vista de que no pueden tener el mismo nivel de prioridad, solo queda escoger cual
de los dos tendrá la mayor prioridad. Y la razon por la que escogemos que el conj tendrá 
mayor prioridad operacional es porque en el caso contrario sencillamente tendriamos una gramatica
que no es capaz de entender ni generar todas las cadenas del lenguaje de expresiones aritmeticas con omision
de simbolos.

Esto no es algo raro. Lenguajes de programacion de proposito cientifico como Julia aceptan esta
notacion y lo resuelven dandole mas prioridad al no expresiones con coeficientes que a la division o
multiplicacion literal. Para mas info sobre como Julia hace esto puede ir a la [Documentación Oficial](https://docs.julialang.org/en/v1/manual/integers-and-floating-point-numbers/#man-numeric-literal-coefficients). 
"""

"""
#### Conclusiones
He intentado resumir en este artículo todo una introducción muy breve y algo informal sobre es
el analisis de los lenguajes computables con el fin de arrojar luz a los 2 planteamientos que insitaron
este texto:

- Lo que a priori parece ser un error quizas sea el resultado de un convenio acordado porque es la mejor forma
de hacer algo o bien porque es la unica forma.

- Los convenios son normas comunicativas para omitir información y así hacer mas fluida la comunicación, por lo cual
usarlos y aceptarlos esta bien siempre y cuando entendamos que los convenios estan atados a las reglas de
las matematicas, pero las estas no estan atadas a los convenios.
"""

