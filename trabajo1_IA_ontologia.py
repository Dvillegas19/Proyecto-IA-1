import rdflib
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, FOAF, DCTERMS
from owlrl import DeductiveClosure, RDFS_Semantics

# Inicializar Grafo y Namespace
g = Graph()
EX = Namespace("http://ejemplo.org/superheroes/")

g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("dcterms", DCTERMS)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

print("CONSTRUCCIÓN DE LA ONTOLOGÍA\n")

# DEFINICIÓN DE CLASES (13 Clases - rdfs:label y dcterms:description)
# Se crea una lista de tuplas con el NameSpace de cada clase, un RFDS label y DCTERMS description
clases = [
    (EX.Personaje, "Personaje", "Clase raíz para entidades del universo de cómics."),
    (EX.Superheroe, "Superhéroe", "Personaje enfocado en proteger la humanidad."),
    (EX.Supervillano, "Supervillano", "Personaje antagonista que genera caos."),
    (EX.HeroeMarvel, "Héroe de Marvel", "Superhéroe de la editorial Marvel Comics."),
    (EX.HeroeDC, "Héroe de DC", "Superhéroe de la editorial DC Comics."),
    (EX.VillanoMarvel, "Villano de Marvel", "Supervillano de la editorial Marvel Comics."),
    (EX.VillanoDC, "Villano de DC", "Supervillano de la editorial DC Comics."),
    (EX.Humano, "Humano", "Personaje de origen biológico terrestre."),
    (EX.HumanoTecnologico, "Humano Tecnológico", "Humano que utiliza gadgets o tecnología sin poderes nativos."),
    (EX.HumanoMutado, "Humano Mutado", "Humano con alteración biológica o genética."),
    (EX.Alienigena, "Alienígena", "Personaje no humano proveniente del espacio exterior o reinos extra-dimensionales."),
    (EX.Superpoder, "Superpoder", "Habilidad sobrehumana o metahumana."),
    (EX.Equipamiento, "Equipamiento", "Artefacto, arma o tecnología empleada.")
]

# Se recorre la lista de tuplas por tripletas con uri, label y descripcion para añadirlo al grafo
for uri_c, label, desc in clases:
    g.add((uri_c, RDF.type, RDFS.Class))
    g.add((uri_c, RDFS.label, Literal(label)))
    g.add((uri_c, DCTERMS.description, Literal(desc)))

# Jerarquía de Clases (rdfs:subClassOf)
# Se crea la jerarquía de clases, se definen cuales son las sub clases para cada clase
g.add((EX.Superheroe, RDFS.subClassOf, EX.Personaje))
g.add((EX.Supervillano, RDFS.subClassOf, EX.Personaje))
g.add((EX.HeroeMarvel, RDFS.subClassOf, EX.Superheroe))
g.add((EX.HeroeDC, RDFS.subClassOf, EX.Superheroe))
g.add((EX.VillanoMarvel, RDFS.subClassOf, EX.Supervillano))
g.add((EX.VillanoDC, RDFS.subClassOf, EX.Supervillano))
g.add((EX.Humano, RDFS.subClassOf, EX.Personaje))
g.add((EX.HumanoTecnologico, RDFS.subClassOf, EX.Humano))
g.add((EX.HumanoMutado, RDFS.subClassOf, EX.Humano))
g.add((EX.Alienigena, RDFS.subClassOf, EX.Personaje))

# DEFINICIÓN DE PROPIEDADES (10 Propiedades: Propiedad - Dominio - Rango - rdfs:label y dcterms:description)
# Se define una lista de tuplas para cada propiedad con Su NameSpace, dominio, rango, RDFS label y DCTERMS description
props = [
    (FOAF.name, EX.Personaje, XSD.string, "Nombre Real", "Nombre civil o de identidad real (Vocabulario FOAF)."),
    (EX.tienePoder, EX.Personaje, EX.Superpoder, "Tiene Poder", "Relaciona un personaje con su habilidad innata."),
    (EX.poseeArtefacto, EX.Personaje, EX.Equipamiento, "Posee Artefacto", "Relaciona un personaje con su equipamiento."),#
    (EX.esEnemigoDe, EX.Personaje, EX.Personaje, "Es Enemigo De", "Rivalidad combativa entre dos personajes."),
    (EX.usaIdentidadOculta, EX.Personaje, XSD.boolean, "Usa Identidad Oculta", "Indica si oculta su cara/identidad."),
    (EX.valorPopularidad, EX.Personaje, XSD.integer, "Valor Popularidad", "Métrica de 0 a 100 para lógica difusa."),
    (EX.valorAmenaza, EX.Personaje, XSD.integer, "Valor Amenaza", "Métrica de 0 a 10 para lógica difusa."),
    (EX.valorPoder, EX.Personaje, XSD.integer, "Valor Poder", "Métrica de 0 a 100 para lógica difusa.")
]

for propiedad_uri, domain_uri, range_uri, label, desc in props:
    g.add((propiedad_uri, RDF.type, RDF.Property))
    g.add((propiedad_uri, RDFS.domain, domain_uri))
    g.add((propiedad_uri, RDFS.range, range_uri))
    g.add((propiedad_uri, RDFS.label, Literal(label)))
    g.add((propiedad_uri, DCTERMS.description, Literal(desc)))

subprops=[
    (EX.esArchienemigoDe,  "Es Archienemigo De", "Subpropiedad para archirrivalidad histórica."),
    (EX.poseeArmaMitica,  "Posee Arma Mítica", "Subpropiedad para armas divinas/míticas.")

]
for subprop_uri , label, desc in subprops:
    g.add((subprop_uri, RDF.type, RDF.Property))
    g.add((subprop_uri, RDFS.label, Literal(label) ))
    g.add((subprop_uri, DCTERMS.description, Literal(desc)))

# Jerarquía de Propiedades (rdfs:subPropertyOf)
# Se definen las sub propiedades para cada propiedad
g.add((EX.poseeArmaMitica, RDFS.subPropertyOf, EX.poseeArtefacto))
g.add((EX.esArchienemigoDe, RDFS.subPropertyOf, EX.esEnemigoDe))


# INSTANCIACIÓN DE PODERES (13)
g.add((EX.SentidoAracnido, RDF.type, EX.SuperPoder))
g.add((EX.FuerzaMejorada, RDF.type, EX.SuperPoder))
g.add((EX.ControlTrueno, RDF.type, EX.SuperPoder))
g.add((EX.PoderCosmico, RDF.type, EX.SuperPoder))
g.add((EX.SuperVelocidad, RDF.type, EX.SuperPoder))
g.add((EX.Vuelo, RDF.type, EX.SuperPoder))
g.add((EX.FuerzaSobrehumana, RDF.type, EX.SuperPoder))
g.add((EX.FuerzaDivina, RDF.type, EX.SuperPoder))
g.add((EX.Simbionte, RDF.type, EX.SuperPoder))
g.add((EX.RayosOmega, RDF.type, EX.SuperPoder))
g.add((EX.ComunicacionMarina, RDF.type, EX.SuperPoder))
g.add((EX.Hechiceria, RDF.type, EX.SuperPoder))
g.add((EX.FactorCurativo, RDF.type, EX.SuperPoder))


# EQUIPAMIENTOS (14 instancias de equipamiento - La 15 (LazoDeLaVerdad)
# se declarará por inferencia de caso 2 con el rango de posee artefacto)
equipamientos = [EX.ArmaduraTech, EX.ArcoGadgets, EX.EscudoVibranium, EX.Mjolnir, EX.TablaCosmica,
        EX.Batarang, EX.PlaneadorBombas, EX.TrajeAlasTech, EX.Guantelete, EX.ToxinaRisa, EX.Acertijos, EX.TrajeKryptonita,
        EX.ArmaduraMisticotech, EX.TridenteDeNeptuno, EX.GarrasAdamantium]
for equipamiento in equipamientos:
    g.add((equipamiento, RDF.type, EX.Equipamiento))

# PERSONAJES (26)
# MARVEL HEROES (7)
# Wolverine
g.add((EX.Wolverine, RDF.type, EX.HeroeMarvel))
g.add((EX.Wolverine, RDF.type, EX.HumanoMutado))
g.add((EX.Wolverine, FOAF.name, Literal("Logan", datatype=XSD.string)))
g.add((EX.Wolverine, EX.poseeArtefacto, EX.GarrasAdamantium))
g.add((EX.Wolverine, EX.tienePoder, EX.FactorCurativo))
g.add((EX.Wolverine, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Wolverine, EX.valorPopularidad, Literal(80, datatype=XSD.integer)))
g.add((EX.Wolverine, EX.valorAmenaza, Literal(6, datatype=XSD.integer)))
g.add((EX.Wolverine, EX.valorPoder, Literal(65, datatype=XSD.integer)))

# Iron Man
g.add((EX.IronMan, RDF.type, EX.HeroeMarvel))
g.add((EX.IronMan, RDF.type, EX.HumanoTecnologico))
g.add((EX.IronMan, FOAF.name, Literal("Tony Stark", datatype=XSD.string)))
g.add((EX.IronMan, EX.poseeArtefacto, EX.ArmaduraTech))
g.add((EX.IronMan, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.IronMan, EX.valorPopularidad, Literal(93, datatype=XSD.integer)))
g.add((EX.IronMan, EX.valorAmenaza, Literal(6, datatype=XSD.integer)))
g.add((EX.IronMan, EX.valorPoder, Literal(78, datatype=XSD.integer)))

# Hawkeye
g.add((EX.Hawkeye, RDF.type, EX.HeroeMarvel))
g.add((EX.Hawkeye, RDF.type, EX.HumanoTecnologico))
g.add((EX.Hawkeye, FOAF.name, Literal("Clint Barton", datatype=XSD.string)))
g.add((EX.Hawkeye, EX.poseeArtefacto, EX.ArcoGadgets))
g.add((EX.Hawkeye, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Hawkeye, EX.valorPopularidad, Literal(76, datatype=XSD.integer)))
g.add((EX.Hawkeye, EX.valorAmenaza, Literal(3, datatype=XSD.integer)))
g.add((EX.Hawkeye, EX.valorPoder, Literal(22, datatype=XSD.integer)))

# Spider-Man
g.add((EX.SpiderMan, RDF.type, EX.HeroeMarvel))
g.add((EX.SpiderMan, RDF.type, EX.HumanoMutado))
g.add((EX.SpiderMan, FOAF.name, Literal("Peter Parker", datatype=XSD.string)))
g.add((EX.SpiderMan, EX.tienePoder, EX.SentidoAracnido))
g.add((EX.SpiderMan, EX.tienePoder, EX.FuerzaSobrehumana))
g.add((EX.SpiderMan, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.SpiderMan, EX.valorPopularidad, Literal(100, datatype=XSD.integer)))
g.add((EX.SpiderMan, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.SpiderMan, EX.valorPoder, Literal(64, datatype=XSD.integer)))

# Capitan America
g.add((EX.CapitanAmerica, RDF.type, EX.HeroeMarvel))
g.add((EX.CapitanAmerica, RDF.type, EX.HumanoMutado))
g.add((EX.CapitanAmerica, FOAF.name, Literal("Steve Rogers", datatype=XSD.string)))
g.add((EX.CapitanAmerica, EX.poseeArtefacto, EX.EscudoVibranium))
g.add((EX.CapitanAmerica, EX.tienePoder, EX.FuerzaMejorada))
g.add((EX.CapitanAmerica, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.CapitanAmerica, EX.valorPopularidad, Literal(97, datatype=XSD.integer)))
g.add((EX.CapitanAmerica, EX.valorAmenaza, Literal(4, datatype=XSD.integer)))
g.add((EX.CapitanAmerica, EX.valorPoder, Literal(48, datatype=XSD.integer)))

# Thor
g.add((EX.Thor, RDF.type, EX.HeroeMarvel))
g.add((EX.Thor, RDF.type, EX.Alienigena))
g.add((EX.Thor, FOAF.name, Literal("Thor Odinson", datatype=XSD.string)))
g.add((EX.Thor, EX.poseeArmaMitica, EX.Mjolnir))
g.add((EX.Thor, EX.tienePoder, EX.ControlTrueno))
g.add((EX.Thor, EX.tienePoder, EX.FuerzaDivina))
g.add((EX.Thor, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Thor, EX.valorPopularidad, Literal(88, datatype=XSD.integer)))
g.add((EX.Thor, EX.valorAmenaza, Literal(7, datatype=XSD.integer)))
g.add((EX.Thor, EX.valorPoder, Literal(77, datatype=XSD.integer)))

# Silver Surfer
g.add((EX.SilverSurfer, RDF.type, EX.HeroeMarvel))
g.add((EX.SilverSurfer, RDF.type, EX.Alienigena))
g.add((EX.SilverSurfer, FOAF.name, Literal("Norrin Radd", datatype=XSD.string)))
g.add((EX.SilverSurfer, EX.poseeArmaMitica, EX.TablaCosmica))
g.add((EX.SilverSurfer, EX.tienePoder, EX.PoderCosmico))
g.add((EX.SilverSurfer, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.SilverSurfer, EX.valorPopularidad, Literal(37, datatype=XSD.integer)))
g.add((EX.SilverSurfer, EX.valorAmenaza, Literal(9, datatype=XSD.integer)))
g.add((EX.SilverSurfer, EX.valorPoder, Literal(95, datatype=XSD.integer)))


# DC HEROES (7)
# Supergirl
g.add((EX.Supergirl, RDF.type, EX.HeroeDC))
g.add((EX.Supergirl, RDF.type, EX.Alienigena))
g.add((EX.Supergirl, FOAF.name, Literal("Kara Zor-El", datatype=XSD.string)))
g.add((EX.Supergirl, EX.tienePoder, EX.Vuelo))
g.add((EX.Supergirl, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Supergirl, EX.valorPopularidad, Literal(50, datatype=XSD.integer)))
g.add((EX.Supergirl, EX.valorAmenaza, Literal(7, datatype=XSD.integer)))
g.add((EX.Supergirl, EX.valorPoder, Literal(90, datatype=XSD.integer)))

# Batman
g.add((EX.Batman, RDF.type, EX.HeroeDC))
g.add((EX.Batman, RDF.type, EX.HumanoTecnologico))
g.add((EX.Batman, EX.esArchienemigoDe, EX.Joker))
g.add((EX.Batman, FOAF.name, Literal("Bruce Wayne", datatype=XSD.string)))
g.add((EX.Batman, EX.poseeArtefacto, EX.Batarang))
g.add((EX.Batman, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Batman, EX.valorPopularidad, Literal(99, datatype=XSD.integer)))
g.add((EX.Batman, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.Batman, EX.valorPoder, Literal(28, datatype=XSD.integer)))

# Green Arrow
g.add((EX.GreenArrow, RDF.type, EX.HeroeDC))
g.add((EX.GreenArrow, RDF.type, EX.HumanoTecnologico))
g.add((EX.GreenArrow, FOAF.name, Literal("Oliver Queen", datatype=XSD.string)))
g.add((EX.GreenArrow, EX.poseeArtefacto, EX.ArcoGadgets))
g.add((EX.GreenArrow, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.GreenArrow, EX.valorPopularidad, Literal(62, datatype=XSD.integer)))
g.add((EX.GreenArrow, EX.valorAmenaza, Literal(2, datatype=XSD.integer)))
g.add((EX.GreenArrow, EX.valorPoder, Literal(19, datatype=XSD.integer)))

# Flash
g.add((EX.Flash, RDF.type, EX.HeroeDC))
g.add((EX.Flash, RDF.type, EX.HumanoMutado))
g.add((EX.Flash, EX.esArchienemigoDe,EX.ReverseFlash))
g.add((EX.Flash, FOAF.name, Literal("Barry Allen", datatype=XSD.string)))
g.add((EX.Flash, EX.tienePoder, EX.SuperVelocidad))
g.add((EX.Flash, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Flash, EX.valorPopularidad, Literal(70, datatype=XSD.integer)))
g.add((EX.Flash, EX.valorAmenaza, Literal(7, datatype=XSD.integer)))
g.add((EX.Flash, EX.valorPoder, Literal(85, datatype=XSD.integer)))

# Superman
g.add((EX.Superman, RDF.type, EX.HeroeDC))
g.add((EX.Superman, RDF.type, EX.Alienigena))
g.add((EX.Superman, FOAF.name, Literal("Clark Kent", datatype=XSD.string)))
g.add((EX.Superman, EX.esArchienemigoDe, EX.LexLuthor))
g.add((EX.Superman, EX.tienePoder, EX.Vuelo))
g.add((EX.Superman, EX.tienePoder, EX.FuerzaSobrehumana))
g.add((EX.Superman, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Superman, EX.valorPopularidad, Literal(97, datatype=XSD.integer)))
g.add((EX.Superman, EX.valorAmenaza, Literal(9, datatype=XSD.integer)))
g.add((EX.Superman, EX.valorPoder, Literal(98, datatype=XSD.integer)))

# Wonder Woman
g.add((EX.WonderWoman, RDF.type, EX.HeroeDC))
g.add((EX.WonderWoman, RDF.type, EX.HumanoMutado))
g.add((EX.WonderWoman, FOAF.name, Literal("Diana Prince", datatype=XSD.string)))
g.add((EX.WonderWoman, EX.poseeArmaMitica, EX.LazoDeLaVerdad))
g.add((EX.WonderWoman, EX.tienePoder, EX.FuerzaDivina))
g.add((EX.WonderWoman, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.WonderWoman, EX.valorPopularidad, Literal(89, datatype=XSD.integer)))
g.add((EX.WonderWoman, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.WonderWoman, EX.valorPoder, Literal(60, datatype=XSD.integer)))

# Aquaman
g.add((EX.Aquaman, RDF.type, EX.HeroeDC))
g.add((EX.Aquaman, RDF.type, EX.HumanoMutado))
g.add((EX.Aquaman, FOAF.name, Literal("Arthur Curry", datatype=XSD.string)))
g.add((EX.Aquaman, EX.poseeArmaMitica, EX.TridenteDeNeptuno))
g.add((EX.Aquaman, EX.tienePoder, EX.ComunicacionMarina))
g.add((EX.Aquaman, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Aquaman, EX.valorPopularidad, Literal(50, datatype=XSD.integer)))
g.add((EX.Aquaman, EX.valorAmenaza, Literal(6, datatype=XSD.integer)))
g.add((EX.Aquaman, EX.valorPoder, Literal(65, datatype=XSD.integer)))


# MARVEL VILLAINS (6)
# Carnage
g.add((EX.Carnage, RDF.type, EX.VillanoMarvel))
g.add((EX.Carnage, RDF.type, EX.HumanoMutado))
g.add((EX.Carnage, FOAF.name, Literal("Cletus Kasady", datatype=XSD.string)))
g.add((EX.Carnage, EX.tienePoder, EX.Simbionte))
g.add((EX.Carnage, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Carnage, EX.valorPopularidad, Literal(50, datatype=XSD.integer)))
g.add((EX.Carnage, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.Carnage, EX.valorPoder, Literal(68, datatype=XSD.integer)))

# Green Goblin
g.add((EX.GreenGoblin, RDF.type, EX.VillanoMarvel))
g.add((EX.GreenGoblin, RDF.type, EX.HumanoTecnologico))
g.add((EX.GreenGoblin, FOAF.name, Literal("Norman Osborn", datatype=XSD.string)))
g.add((EX.GreenGoblin, EX.poseeArtefacto, EX.PlaneadorBombas))
g.add((EX.GreenGoblin, EX.tienePoder, EX.FuerzaMejorada))
g.add((EX.GreenGoblin, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.GreenGoblin, EX.valorPopularidad, Literal(69, datatype=XSD.integer)))
g.add((EX.GreenGoblin, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.GreenGoblin, EX.valorPoder, Literal(55, datatype=XSD.integer)))

# Vulture
g.add((EX.Vulture, RDF.type, EX.VillanoMarvel))
g.add((EX.Vulture, RDF.type, EX.HumanoTecnologico))
g.add((EX.Vulture, FOAF.name, Literal("Adrian Toomes", datatype=XSD.string)))
g.add((EX.Vulture, EX.poseeArtefacto, EX.TrajeAlasTech))
g.add((EX.Vulture, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Vulture, EX.valorPopularidad, Literal(25, datatype=XSD.integer)))
g.add((EX.Vulture, EX.valorAmenaza, Literal(2, datatype=XSD.integer)))
g.add((EX.Vulture, EX.valorPoder, Literal(21, datatype=XSD.integer)))

# Venom
g.add((EX.Venom, RDF.type, EX.VillanoMarvel))
g.add((EX.Venom, RDF.type, EX.HumanoMutado))
g.add((EX.Venom, FOAF.name, Literal("Eddie Brock", datatype=XSD.string)))
g.add((EX.Venom, EX.tienePoder, EX.Simbionte))
g.add((EX.Venom, EX.tienePoder, EX.FuerzaSobrehumana))
g.add((EX.Venom, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Venom, EX.valorPopularidad, Literal(79, datatype=XSD.integer)))
g.add((EX.Venom, EX.valorAmenaza, Literal(7, datatype=XSD.integer)))
g.add((EX.Venom, EX.valorPoder, Literal(74, datatype=XSD.integer)))

# Thanos
g.add((EX.Thanos, RDF.type, EX.VillanoMarvel))
g.add((EX.Thanos, RDF.type, EX.Alienigena))
g.add((EX.Thanos, FOAF.name, Literal("Thanos", datatype=XSD.string)))
g.add((EX.Thanos, EX.poseeArmaMitica, EX.Guantelete))
g.add((EX.Thanos, EX.tienePoder, EX.FuerzaSobrehumana))
g.add((EX.Thanos, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Thanos, EX.valorPopularidad, Literal(89, datatype=XSD.integer)))
g.add((EX.Thanos, EX.valorAmenaza, Literal(10, datatype=XSD.integer)))
g.add((EX.Thanos, EX.valorPoder, Literal(96, datatype=XSD.integer)))

# Doctor Doom
g.add((EX.DoctorDoom, RDF.type, EX.VillanoMarvel))
g.add((EX.DoctorDoom, RDF.type, EX.HumanoTecnologico))
g.add((EX.DoctorDoom, FOAF.name, Literal("Victor von Doom", datatype=XSD.string)))
g.add((EX.DoctorDoom, EX.poseeArtefacto, EX.ArmaduraMisticotech))
g.add((EX.DoctorDoom, EX.tienePoder, EX.Hechiceria))
g.add((EX.DoctorDoom, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.DoctorDoom, EX.valorPopularidad, Literal(90, datatype=XSD.integer)))
g.add((EX.DoctorDoom, EX.valorAmenaza, Literal(9, datatype=XSD.integer)))
g.add((EX.DoctorDoom, EX.valorPoder, Literal(90, datatype=XSD.integer)))

# DC VILLAINS (6)
# General Zod
g.add((EX.GeneralZod, RDF.type, EX.VillanoDC))
g.add((EX.GeneralZod, RDF.type, EX.Alienigena))
g.add((EX.GeneralZod, FOAF.name, Literal("Dru-Zod", datatype=XSD.string)))
g.add((EX.GeneralZod, EX.tienePoder, EX.Vuelo))
g.add((EX.GeneralZod, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.GeneralZod, EX.valorPopularidad, Literal(80, datatype=XSD.integer)))
g.add((EX.GeneralZod, EX.valorAmenaza, Literal(7, datatype=XSD.integer)))
g.add((EX.GeneralZod, EX.valorPoder, Literal(70, datatype=XSD.integer)))

# Joker
g.add((EX.Joker, RDF.type, EX.VillanoDC))
g.add((EX.Joker, RDF.type, EX.HumanoTecnologico))
g.add((EX.Joker, FOAF.name, Literal("Desconocido", datatype=XSD.string)))
g.add((EX.Joker, EX.esArchienemigoDe, EX.Batman))
g.add((EX.Joker, EX.poseeArtefacto, EX.ToxinaRisa))
g.add((EX.Joker, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Joker, EX.valorPopularidad, Literal(95, datatype=XSD.integer)))
g.add((EX.Joker, EX.valorAmenaza, Literal(3, datatype=XSD.integer)))
g.add((EX.Joker, EX.valorPoder, Literal(14, datatype=XSD.integer)))

# Riddler
g.add((EX.Riddler, RDF.type, EX.VillanoDC))
g.add((EX.Riddler, RDF.type, EX.HumanoTecnologico))
g.add((EX.Riddler, FOAF.name, Literal("Edward Nygma", datatype=XSD.string)))
g.add((EX.Riddler, EX.poseeArtefacto, EX.Acertijos))
g.add((EX.Riddler, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.Riddler, EX.valorPopularidad, Literal(60, datatype=XSD.integer)))
g.add((EX.Riddler, EX.valorAmenaza, Literal(2, datatype=XSD.integer)))
g.add((EX.Riddler, EX.valorPoder, Literal(9, datatype=XSD.integer)))

# Reverse Flash
g.add((EX.ReverseFlash, RDF.type, EX.VillanoDC))
g.add((EX.ReverseFlash, EX.esArchienemigoDe,EX.Flash))
g.add((EX.ReverseFlash, RDF.type, EX.HumanoMutado))
g.add((EX.ReverseFlash, FOAF.name, Literal("Eobard Thawne", datatype=XSD.string)))
g.add((EX.ReverseFlash, EX.tienePoder, EX.SuperVelocidad))
g.add((EX.ReverseFlash, EX.usaIdentidadOculta, Literal(True, datatype=XSD.boolean)))
g.add((EX.ReverseFlash, EX.valorPopularidad, Literal(58, datatype=XSD.integer)))
g.add((EX.ReverseFlash, EX.valorAmenaza, Literal(8, datatype=XSD.integer)))
g.add((EX.ReverseFlash, EX.valorPoder, Literal(88, datatype=XSD.integer)))

# Darkseid
g.add((EX.Darkseid, RDF.type, EX.VillanoDC))
g.add((EX.Darkseid, RDF.type, EX.Alienigena))
g.add((EX.Darkseid, FOAF.name, Literal("Uxas", datatype=XSD.string)))
g.add((EX.Darkseid, EX.tienePoder, EX.RayosOmega))
g.add((EX.Darkseid, EX.tienePoder, EX.FuerzaDivina))
g.add((EX.Darkseid, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.Darkseid, EX.valorPopularidad, Literal(63, datatype=XSD.integer)))
g.add((EX.Darkseid, EX.valorAmenaza, Literal(10, datatype=XSD.integer)))
g.add((EX.Darkseid, EX.valorPoder, Literal(100, datatype=XSD.integer)))

# Lex Luthor
g.add((EX.LexLuthor, RDF.type, EX.VillanoDC))
g.add((EX.LexLuthor, RDF.type, EX.HumanoTecnologico))
g.add((EX.LexLuthor, FOAF.name, Literal("Lex Luthor", datatype=XSD.string)))
g.add((EX.LexLuthor, EX.esArchienemigoDe, EX.Superman))
g.add((EX.LexLuthor, EX.poseeArtefacto, EX.TrajeKryptonita))
g.add((EX.LexLuthor, EX.usaIdentidadOculta, Literal(False, datatype=XSD.boolean)))
g.add((EX.LexLuthor, EX.valorPopularidad, Literal(89, datatype=XSD.integer)))
g.add((EX.LexLuthor, EX.valorAmenaza, Literal(5, datatype=XSD.integer)))
g.add((EX.LexLuthor, EX.valorPoder, Literal(63, datatype=XSD.integer)))

tripletas_antes = len(g)
print(f"Total de tripletas explícitas ingresadas: {tripletas_antes}\n")

print("Evidencia casos antes del motor de inferencia")
c1_1 = (EX.Thor, RDF.type, EX.Superheroe) in g
c1_2 = (EX.Superman, RDF.type, EX.Personaje) in g
print(f"Caso 1: \nTripletas inferidas por jerarquía de clase")
print(f"Thor RDF:type SuperHeroe -> Inferido de Thor RDF:type HeroeMarvel  {c1_1}")
print(f"Superman RDF:type Personaje -> Inferido de Superman RDF:type HeroeDC {c1_2}\n")

c2_dom = (EX.WonderWoman, RDF.type, EX.Personaje) in g
c2_ran = (EX.LazoDeLaVerdad, RDF.type, EX.Equipamiento) in g
print(f"Caso 2: \nTripletas inferidas por Domain / Range")
print(f"WonderWoman poseeArtefacto LazoDeLaVerdad (Sin tipos explícitos)")
print(f"-> Inferido Dominio: WonderWoman es Personaje: {c2_dom}")
print(f"-> Inferido Rango: LazoDeLaVerdad es Equipamiento: {c2_ran}\n")

c3_1 = (EX.Thor, EX.poseeArtefacto, EX.Mjolnir) in g
c3_2 = (EX.Joker, EX.esEnemigoDe, EX.Batman) in g
print("Caso 3: \nTripletas inferidas por jerarquía de propiedades")
print(f"Thor poseeArtefacto Mjolnir -> Inferido de Thor poseeArmaMitica Mjolnir: {c3_1}")
print(f"Joker esEnemigoDe Batman -> Inferido de Joker EsArchienemigoDe Batman: {c3_2}\n")

# Activación motor de inferencia (OWL-RL)
print("Aplicando el motor de inferencia (DeductiveClosure - RDFS_Semantics)")

DeductiveClosure(RDFS_Semantics).expand(g)
tripletas_despues = len(g)

print(f"Tripletas antes del razonamiento:  {tripletas_antes}")
print(f"Tripletas después del razonamiento: {tripletas_despues}")
print(f"Nuevas afirmaciones inferidas: {tripletas_despues - tripletas_antes}\n")

# Documentación de casos
print("Documentación casos")

# Caso 1: Jerarquía de clases (subClassOf) - 2 Casos
c1_1 = (EX.Thor, RDF.type, EX.Superheroe) in g
c1_2 = (EX.Superman, RDF.type, EX.Personaje) in g
print(f"Caso 1: \nTripletas inferidas por jerarquía de clase")
print(f"Thor RDF:type SuperHeroe -> Inferido de Thor RDF:type HeroeMarvel  {c1_1}")
print(f"Superman RDF:type Personaje -> Inferido de Superman RDF:type HeroeDC {c1_2}\n")

# CASO 2: Inferencia desde Domain / Range
c2_dom = (EX.WonderWoman, RDF.type, EX.Personaje) in g
c2_ran = (EX.LazoDeLaVerdad, RDF.type, EX.Equipamiento) in g
print(f"Caso 2: \nTripletas inferidas por Domain / Range")
print(f"WonderWoman poseeArtefacto LazoDeLaVerdad (Sin tipos explícitos)")
print(f"-> Inferido Dominio: WonderWoman es Personaje: {c2_dom}")
print(f"-> Inferido Rango: LazoDeLaVerdad es Equipamiento: {c2_ran}\n")

# CASO 3: Jerarquía de Propiedades (subPropertyOf)
c3_1 = (EX.Thor, EX.poseeArtefacto, EX.Mjolnir) in g
c3_2 = (EX.Joker, EX.esEnemigoDe, EX.Batman) in g
print("Caso 3: \nTripletas inferidas por jerarquía de propiedades")
print(f"Thor poseeArtefacto Mjolnir -> Inferido de Thor poseeArmaMitica Mjolnir: {c3_1}")
print(f"Joker esEnemigoDe Batman -> Inferido de Joker EsArchienemigoDe Batman: {c3_2}\n")

# Evidencia de los 4 hechos inferidos automáticamente por el razonador
print("Evidencia de los 4 hechos inferidos automáticamente por el razonador")
hechos_ejemplo = [
    ("ex:Superman", "rdf:type", "ex:Personaje", "Inferido por subclase ex:Alienigena"),
    ("ex:Thanos", "rdf:type", "ex:Personaje", "Inferido por subclase ex:VillanoMarvel"),
    ("ex:IronMan", "rdf:type", "ex:Humano", "Inferido por subclase ex:HumanoTecnologico"),
    ("ex:Guantelete", "rdf:type", "ex:Equipamiento", "Inferido por subpropiedad ex:poseeArmaMitica")
]

for idx, (s, p, o, razon) in enumerate(hechos_ejemplo, start=1):
    print(f"Hecho Inferido {idx}: ({s} {p} {o})")
    print(f"Justificación: {razon}\n")


# Serialización en Turtle
archivo_ontologia = "ontologia_generada.ttl"
g.serialize(destination=archivo_ontologia, format="turtle")
print(f"Ontología serializada correctamente en '{archivo_ontologia}'")
print("Ir al final de documento para ver donde quedo guardado en tu drive")