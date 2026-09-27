from experta import *
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF
import random
import re

# Traducción de la ontología para traer los datos al sistema experto
g = Graph()
g.parse("ontologia_generada.ttl", format="turtle")
EX = Namespace("http://ejemplo.org/superheroes/")

# La función extraer_nombre toma un uri completo, a traves de un regex 
# y la función split toma el nombre local y lo retorna 
def extraer_nombre(uri_o_literal):
    if isinstance(uri_o_literal, URIRef):
        return re.split(r'[/#]', str(uri_o_literal))[-1]
    return str(uri_o_literal)

clase=set()
propiedad=set()
for s,p,o in g.triples((None,RDF.type,RDFS.Class)):
    clase.add(s.split("/")[-1])



for s,p,o in g.triples((None,RDF.type,RDF.Property)) :
    s_literal=s.split("/")[-1]
    print(s)
    if "#" not in s_literal and ("dc/" not in s):
        propiedad.add(s_literal)





# Diccionario donde estarán guardados los personajes con keys igual a sus atributos y propiedades, ambas previamentes definidas en la ontología. 
# Así como values con valores booleanos que validarán si poseen o no esta característica 
personajes_dict = {}
# Lista para imprimirle los personajes al usuario que quiera jugar Akinator
# con los personajes disponibles
nombre_personajes=[]



# Clases de Hechos
class Personaje(Fact):
    """Candidato a ser el personaje a adivinar en la base de conocimientos"""
    pass

class Respuesta(Fact):
    """La respuesta actual dada por el usuario"""
    pass

class AtributoEvaluado(Fact):
    """Historial para no hacer las mismas preguntas"""
    pass

class EstadoJuego(Fact):
    """Control de fase de inferencia"""
    pass

class PerfilDifuso(Fact):
    """Almacena las métricas de desempate y dispara la regla difusas"""
    pass

class Clase(Fact):
    """Declara las clases de cada personaje"""

class Propiedad(Fact):
    """Declara las propiedades de cada personaje"""
# Sistema experto

class Akinator(KnowledgeEngine):
    """ NO-LOOP MEDIANTE NEGACIÓN (NOT) 
        # Esta regla exige como requisito que NO exista ya el AtributoEvaluado.
        # Al declararlo dentro de la regla, la condición NOT se vuelve falsa y evita el ciclo infinito.
        
    @Rule(
            AS.r << Respuesta(atributo=MATCH.attr),
            NOT(AtributoEvaluado(nombre=MATCH.attr)),
            salience=1
        )
        def registrar_historial_y_limpiar(self, r, attr):
            self.declare(AtributoEvaluado(nombre=attr))
            self.retract(r) # Limpiamos la respuesta de la memoria
            """
    
    
    @Rule(EstadoJuego(fase="descarte"),
        NOT(AtributoEvaluado(nombre=MATCH.attr)), #no-loop
        OR(
            Clase(clase=MATCH.attr, pregunta=MATCH.p1), Propiedad(prop=MATCH.attr, pregunta=MATCH.p1)
            ),
            salience=5) 
    
    def registrar_historial(self, attr, p1)
        respuesta=input(p1,"si o no")
        self.declare(Respuesta(atributo=c,valor=respuesta))

        print(dicts[p])

    
    @Rule(EstadoJuego(fase="desempate"), PerfilDifuso(poder=MATCH.p, amenaza=MATCH.a))
    def notificar_desempate(self, p, a):
        print(f"\nSe detectó un empate. Aplicando perfil difuso para desempatar a los candidatos")


    @Rule(AS.r << Respuesta(atributo=MATCH.r), salience=7)
    def eliminiar_respuesta(self,r):
        self.retract(r)
        candidatos_restantes = [fact for fact in self.facts.values() if isinstance(fact, Personaje)]
        if len(candidatos_restantes) <= 2:
            self.declare(EstadoJuego(fase="final", candidatos=candidatos_restantes))
        
    @Rule(EstadoJuego(fase="final", candidatos=MATCH.candidatos_restantes)
          NOT(EstadoJuego(fase="desempate")))#no-loop
    def decision_final(self,candidatos_restantes):
        if len(candidatos_restantes) == 1:
            cand = candidatos_restantes[0]
            print(f"\nEl motor determinó que es: {cand['uri'].upper()}")

        elif len(candidatos_restantes) == 0:
            print("\nNo se encontró un personaje con estos atributos ")

        elif len(candidatos_restantes) == 2:
            print(f"\nQuedan {len(candidatos_restantes)} candidatos. Activando lógica difusa...")
            self.declare(EstadoJuego(fase="desempate", candidatos= candidatos_restantes))

    @Rule(EstadoJuego(fase="desempate",candidatos=MATCH.candidatos_restantes))   
    def desempate(self):
        pass 

    
    # REGLAS DE DESCARTE (Salience 10 - Se ejecutan antes de limpiar) 
    @Rule(AS.r << Respuesta(atributo="esSuperheroe", valor=True), AS.c << Personaje(esSuperheroe=False), salience=10)
    def desc_no_superheroe(self, c): 
        self.retract(c)
        self.declare(AtributoEvaluado(nombre="esSuperheroe"))
        self.declare(AtributoEvaluado(nombre="esVillano"))
        self.declare(AtributoEvaluado(nombre="VillanoDC"))

    @Rule(Respuesta(atributo="esSuperheroe", valor=False), AS.c << Personaje(esSuperheroe=True), salience=10)
    def desc_si_superheroe(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esSupervillano", valor=True), AS.c << Personaje(esSupervillano=False), salience=10)
    def desc_no_supervillano(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esSupervillano", valor=False), AS.c << Personaje(esSupervillano=True), salience=10)
    def desc_si_supervillano(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esHeroeMarvel", valor=True), AS.c << Personaje(esHeroeMarvel=False), salience=10)
    def desc_no_hm(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esHeroeMarvel", valor=False), AS.c << Personaje(esHeroeMarvel=True), salience=10)
    def desc_si_hm(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esHeroeDC", valor=True), AS.c << Personaje(esHeroeDC=False), salience=10)
    def desc_no_hdc(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esHeroeDC", valor=False), AS.c << Personaje(esHeroeDC=True), salience=10)
    def desc_si_hdc(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esHumano", valor=True), AS.c << Personaje(esHumano=False), salience=10)
    def desc_no_humano(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esHumano", valor=False), AS.c << Personaje(esHumano=True), salience=10)
    def desc_si_humano(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esHumanoTecnologico", valor=True), AS.c << Personaje(esHumanoTecnologico=False), salience=10)
    def desc_no_htec(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esHumanoTecnologico", valor=False), AS.c << Personaje(esHumanoTecnologico=True), salience=10)
    def desc_si_htec(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esAlienigena", valor=True), AS.c << Personaje(esAlienigena=False), salience=10)
    def desc_no_alien(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esAlienigena", valor=False), AS.c << Personaje(esAlienigena=True), salience=10)
    def desc_si_alien(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="tienePoder", valor=True), AS.c << Personaje(tienePoder=False), salience=10)
    def desc_no_poder(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="tienePoder", valor=False), AS.c << Personaje(tienePoder=True), salience=10)
    def desc_si_poder(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="poseeArtefacto", valor=True), AS.c << Personaje(poseeArtefacto=False), salience=10)
    def desc_no_art(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="poseeArtefacto", valor=False), AS.c << Personaje(poseeArtefacto=True), salience=10)
    def desc_si_art(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esArchienemigoDe", valor=True), AS.c << Personaje(esArchienemigoDe=False), salience=10)
    def desc_no_archi(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esArchienemigoDe", valor=False), AS.c << Personaje(esArchienemigoDe=True), salience=10)
    def desc_si_archi(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esVillanoMarvel", valor=True), AS.c << Personaje(esVillanoMarvel=False), salience=10)
    def desc_no_villanomarvel(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esVillanoMarvel", valor=False), AS.c << Personaje(esVillanoMarvel=True), salience=10)
    def desc_si_villanomarvel(self, c): 
        self.retract(c)

    @Rule(Respuesta(atributo="esVillanoDC", valor=True), AS.c << Personaje(esVillanoDC=False), salience=10)
    def desc_no_villanodc(self, c): 
        self.retract(c)
    @Rule(Respuesta(atributo="esVillanoDC", valor=False), AS.c << Personaje(esVillanoDC=True), salience=10)
    def desc_si_villanodc(self, c): 
        self.retract(c)


# Ciclo de preguntas
engine = Akinator()
engine.reset()
engine.declare(EstadoJuego(fase="descarte"))

for personaje in random.shuffle(personajes_dict.values()):
    engine.declare(Personaje(**personaje))


banco_preguntas = {
    "esArchienemigoDe" : ["¿Tú personaje tiene algún archienemigo (de los que están en la lista)?", True,[]],
    "esVillanoMarvel" : ["¿Tú personaje es un villano de Marvel?", True,["esVillanoDC", "esSuperVillano","esHeroeMarvel","esHeroeDC","esSuperHeroe"]],
    "esVillanoDC" : ["¿Tú personaje es un villano de DC?", True,["esVillanoMarvel","esSuperheroe","esHeroeMarvel","esHeroeDC","esSupervillano"]],
    "esHumanoMutado" : ["¿Tú personaje es un humano Mutado?", True,["esHumano","esAlienigena","esHumanoTecnologico"]],
    "esSuperheroe": ["¿Tu personaje es un Superhéroe?", True, ["esSupervillano", "esVillanoMarvel", "esVillanoDC"]],
    "esSupervillano": ["¿Tu personaje es un Supervillano?", True, ["esSuperheroe", "esHeroeMarvel", "esHeroeDC"]],
    "esHeroeMarvel": ["¿Es un Héroe de Marvel?", True, ["esHeroeDC", "esVillanoMarvel", "esVillanoDC"]],
    "esHeroeDC": ["¿Es un Héroe de DC?", True, ["esHeroeMarvel", "esVillanoMarvel", "esVillanoDC"]] ,
    "esHumano": ["¿Tu personaje es de especie Humana?", True, ["esAlienigena"]],
    "esHumanoTecnologico": ["¿Es un humano con tecnología?", True, ["esHumanoMutado", "esAlienigena", "esHumano"]],
    "esAlienigena": ["¿Tu personaje es Alienígena?", True, ["esHumano", "esHumanoTecnologico", "esHumanoMutado"]],
    "tienePoder": ["¿Posee algún Superpoder (Superfuerza, Supervelocidad, etc..)?", True, []],
    "poseeArtefacto": ["¿Posee algún artefacto o equipamiento (traje, arco, martillo, lazo, etc..)?", True, []],
    "usaIdentidadOculta": ["Tú personaje tiene una identidad oculta?", True, []]
}

keys_preguntas = list(banco_preguntas.keys())
random.shuffle(keys_preguntas)

candidatos_restantes = []

idx = 1
print("Elija un personaje para adivinarlo\n")
for i in nombre_personajes:
  print(f"{idx}. {i}")
  idx+=1

for prop in keys_preguntas:
    if banco_preguntas[prop][1]:
        print(f"\nPregunta: {banco_preguntas[prop][0]}")
        respuesta = input("Responde (1 para Sí, 2 para No): ").strip()
        valor_booleano = (respuesta == "1")

        # Desactivamos preguntas opuestas si la respuesta es Sí
        if valor_booleano and len(banco_preguntas[prop][2]) > 0:
            for opuesto in banco_preguntas[prop][2]:
                if opuesto in banco_preguntas:
                    banco_preguntas[opuesto][1] = False

        # Declaramos solo la respuesta. La negación en las reglas controlará el ciclo.
        engine.declare(Respuesta(atributo=prop, valor=valor_booleano))
        engine.run()

        candidatos_restantes = [fact for fact in engine.facts.values() if isinstance(fact, Personaje)]
        if len(candidatos_restantes) <= 2:
            break


# Dependiendo de la cantidad de los personajes restantes despues de la ronda de preguntas el sistema tomara distintos caminos:
# -Si solo queda un personaje el sistema lo imprimirá en pantalla automáticamente y el juego se dará por terminado 
# -Si no queda ningún personaje en la lista se imprimirá en pantalla que no pudo adivinar el personaje
# -Si quedan 2 personajes entrar en fase de desempate utilizando el sistema difuso para desempatar 
if len(candidatos_restantes) == 1:
    cand = candidatos_restantes[0]
    print(f"\nEl motor determinó que es: {cand['uri'].upper()}")

elif len(candidatos_restantes) == 0:
    print("\nNo se encontró un personaje con estos atributos ")

elif len(candidatos_restantes) == 2:
    print(f"\nQuedan {len(candidatos_restantes)} candidatos. Activando lógica difusa...")

    try:
        print("0-35: Débil (Humanos un poquito más poderosos)\n25-70: Medio poderoso (Armas avanzadas y sobrehumanos) \n60-100: Poderoso (Universal)")
        v_pod = float(input("¿Nivel de PODER (0 a 100)?: \n"))

        print("\nPiense en amenaza como, si el personaje fuera(o es) malo , que tanta magnitud destruiría")
        print("0-3: Baja (Amenaza ciudades)\n3-7: Media (Amenaza el mundo)\n7-10: Alta (Amenaza el universo)")
        v_ame = float(input("¿Nivel de AMENAZA (0 a 10)?: \n"))


        print("\n0-30: Poco Popular \n30-70: Medio conocido \n70-100: ícono, muy conocido")
        v_pop = float(input("¿Nivel de POPULARIDAD (0 a 100)?: \n"))


        # Disparamos los hechos en el motor para cumplir con el uso de PerfilDifuso
        engine.declare(EstadoJuego(fase="desempate"))
        engine.declare(PerfilDifuso(poder=v_pod, amenaza=v_ame, popularidad=v_pop))
        engine.run()

        # Se llama a la función evaluar_perfil_difuso y toma como parametros los valores ingresados por el usuario
        impacto_esperado = evaluar_perfil_difuso(v_pod, v_ame, v_pop)
        mejor_candidato = None
        menor_dif = float('inf')

        for cand in candidatos_restantes:
            # Extraemos los valores del Fact de Experta
            impacto_cand = evaluar_perfil_difuso(
                cand['valorPoder'],
                cand['valorAmenaza'],
                cand['valorPopularidad']
            )

            # El personaje que tenga la menor diferencia de impacto es el ganador
            if abs(impacto_esperado - impacto_cand) < menor_dif:
                menor_dif = abs(impacto_esperado - impacto_cand)
                mejor_candidato = cand

        if mejor_candidato:
            print(f"\nLa Lógica Difusa desempató a favor de: {mejor_candidato['uri'].upper()}\n")

    except ValueError:
        print("\nEntrada inválida. Ingresa solo números.")
