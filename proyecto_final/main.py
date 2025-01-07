import discord
from discord.ext import commands
from model import get_class
import os

DESASTRE_INFO = {
    0: {
        "name": "Huracán",
        "description": [
            "Un huracán es un sistema de tormentas de baja presión caracterizado por vientos intensos, lluvias torrenciales y marejadas ciclónicas"
            "Los huracanes se forman sobre aguas cálidas del océano cuando el aire húmedo asciende y el aire frío desciende, "
            "creando un sistema de baja presión que se intensifica por la rotación de la Tierra. Su impacto incluye inundaciones, "
            "destrucción de infraestructuras y pérdida de vidas humanas."
        ],
        "frequent_regions": [
            "Región del Caribe",
            "Costa Este de Estados Unidos",
            "Golfo de México",
            "Sureste de Asia"
        ],
        "safety_tips": [
            "Mantente informado mediante alertas meteorológicas.",
            "Prepárate con un plan de evacuación.",
            "Refuerza ventanas y puertas de tu vivienda.",
            "Almacena suficiente agua potable y alimentos no perecederos."
        ],
        "historical_event": (
            "El huracán Katrina (2005) fue uno de los más devastadores en la historia de Estados Unidos, "
            "causando más de 1800 muertes y daños estimados en $125 mil millones."
        ),
        "recommendation": [
            "Busca refugio en zonas altas.",
            "Evita áreas cercanas a ríos o playas.",
            "Ten listo un kit de emergencia."
        ],
        "video": "https://www.youtube.com/watch?v=xlDcT78g6zw"
    },
    1: {
        "name": "Incendio Forestal",
        "description":(
            "Un incendio forestal es un fuego incontrolado que se propaga en zonas boscosas o rurales.",
            "Los incendios forestales pueden ser causados por rayos, actividad humana o condiciones climáticas extremas como sequías y altas temperaturas. "
            "Pueden destruir ecosistemas, desplazar comunidades y afectar la calidad del aire en regiones enteras."
        ),
        "frequent_regions": [
            "California, Estados Unidos",
            "Amazonía, América del Sur",
            "Australia",
            "Mediterráneo, Europa"
        ],
        "safety_tips": [
            "Evacúa inmediatamente si las autoridades lo ordenan.",
            "Utiliza mascarillas para evitar inhalar humo.",
            "Ten un plan para evacuar con tus mascotas y documentos importantes."
        ],
        "historical_event": (
            "El incendio de Paradise en California (2018) destruyó más de 18,000 estructuras y causó la muerte de 85 personas."
        ),
        "recommendation": [
            "Aléjate de la zona afectada.",
            "Evita inhalar humo.",
            "Sigue las instrucciones de las autoridades locales."
        ],
        "video": "https://www.youtube.com/watch?v=VFoR-gw5Z-8"
    },
    2: {
        "name": "Inundación",
        "description":(
            "Una inundación ocurre cuando el agua cubre áreas normalmente secas, generalmente debido a lluvias intensas o desbordes de ríos.",
            "Las inundaciones pueden ser causadas por tormentas intensas, deshielos, tsunamis o rotura de represas. "
            "Pueden devastar comunidades, destruir cultivos y propagar enfermedades a través del agua contaminada."
        ),
        "frequent_regions": [
            "Sudeste Asiático",
            "Delta del Nilo, Egipto",
            "Ganges, India",
            "Bangladés"
        ],
        "safety_tips": [
            "Busca terreno elevado inmediatamente.",
            "Evita cruzar corrientes de agua incluso si parecen superficiales.",
            "Desconecta todos los aparatos eléctricos antes de evacuar."
        ],
        "historical_event": (
            "Las inundaciones del río Yangtsé en 1931, en China, son consideradas las más mortales, con más de 4 millones de víctimas."
        ),
        "recommendation": [
            "Busca terrenos altos.",
            "Evita caminar o conducir en agua estancada.",
            "Desconecta aparatos eléctricos."
        ],
        "video": "https://www.youtube.com/watch?v=wAaV8rV2bRw"
    },
    3: {
        "name": "Mega Sequía",
        "description":(
            "Una mega sequía es un periodo prolongado de escasez de agua que afecta ecosistemas y comunidades humanas.",
            "Las mega sequías son eventos climáticos extremos que pueden durar décadas, afectando gravemente la agricultura, "
            "el suministro de agua potable y los ecosistemas naturales."
        ),
        "frequent_regions": [
            "Oeste de Estados Unidos",
            "Australia",
            "Cuerno de África",
            "Región del Sahel, África"
        ],
        "safety_tips": [
            "Ahorra agua reutilizando para tareas domésticas.",
            "Planta vegetación resistente a la sequía.",
            "Evita el uso excesivo de agua en jardines y piscinas."
        ],
        "historical_event": (
            "La mega sequía del suroeste de Estados Unidos durante el siglo XII contribuyó al colapso de la civilización Ancestral Pueblo."
        ),
        "recommendation": [
            "Ahorra agua.",
            "Evita su uso innecesario.",
            "Sigue las medidas de racionamiento impuestas por las autoridades."
        ],
        "video": "https://www.youtube.com/watch?v=IhWRot4JXyI"
    },
    4: {
        "name": "Mega Tormenta",
        "description":(
            "Una mega tormenta combina fuertes vientos, lluvias intensas y granizo, causando daños masivos.",
            "Las mega tormentas son eventos meteorológicos extremos que pueden provocar inundaciones, cortes de energía y daños estructurales "
            "graves en comunidades urbanas y rurales."
        ),
        "frequent_regions": [
            "Costa Atlántica de Estados Unidos",
            "Sudeste Asiático",
            "Europa Occidental"
        ],
        "safety_tips": [
            "Mantente alejado de ventanas y puertas durante la tormenta.",
            "Evita usar aparatos eléctricos mientras haya tormentas eléctricas.",
            "Refúgiate en una habitación interior segura."
        ],
        "historical_event": (
            "El huracán Sandy (2012), aunque clasificado como tormenta post-tropical, afectó a 24 estados en Estados Unidos y causó daños por $68 mil millones."
        ),
        "recommendation": [
            "Permanece en un lugar seguro, lejos de ventanas y puertas.",
            "Ten listo un kit de emergencia.",
            "Mantente informado a través de los medios oficiales."
        ],
        "video": "https://www.youtube.com/watch?v=GynvrgoDNVM"
    },
    5: {
        "name": "Ola de Calor",
        "description":(
            "Una ola de calor es un periodo prolongado de temperaturas extremadamente altas.", 
            "Las olas de calor pueden causar problemas graves de salud como golpes de calor, deshidratación y enfermedades relacionadas con el calor. "
            "También pueden exacerbar sequías e incendios forestales."
        ),
        "frequent_regions": [
            "Sureste de Europa",
            "India y Pakistán",
            "Australia",
            "Estados del suroeste de Estados Unidos"
        ],
        "safety_tips": [
            "Mantente hidratado bebiendo agua constantemente.",
            "Evita actividades físicas al aire libre durante las horas más calurosas.",
            "Utiliza ventiladores o aire acondicionado para mantenerte fresco."
        ],
        "historical_event": (
            "La ola de calor en Europa en 2003 causó aproximadamente 70,000 muertes, afectando principalmente a personas mayores."
        ),
        "recommendation": [
            "Mantente hidratado.",
            "Evita la exposición al sol durante las horas más calurosas.",
            "Utiliza ropa ligera."
        ],
        "video": "https://www.youtube.com/watch?v=3FanX8WA2UA"
    }
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='*', intents=intents)

Carpeta_desastre = "C:/Users/Sebas/Desktop/proyecto_final/imagenes_desastres"
os.makedirs(Carpeta_desastre, exist_ok=True)

@bot.event
async def on_ready():
    channel_id = 1318773556150141015
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send("¡Hola! soy Clim-Bot y estoy listo para ayudar. 🚀, para poder responder tus preguntas sobre el cambio climatico usa el comando: *comandos")
    print(f'Te has logeado como {bot.user}')

@bot.command()
async def que_es(ctx):
    que_es = (
        "**Que es el cambio climatico** \n"
        "El cambio climático representa uno de los desafíos más críticos y urgentes de nuestra era.\n"
        "Se define como las alteraciones significativas y prolongadas en los patrones climáticos globales.\n"
        "Si bien algunos cambios climáticos pueden ocurrir de forma natural, \n"
        "la actividad humana desde la Revolución Industrial ha acelerado este proceso de manera sin precedentes, \n"
        "principalmente debido a la emisión descontrolada de gases de efecto invernadero."
    )
    await ctx.send(que_es)

@bot.command()
async def impactos(ctx):
    impactos = (
        "**Impactos odservables del cambio climatico** \n"
        "El cambio climático ya es una realidad visible en todo el planeta. La temperatura media global ha aumentado 1,1 °C desde finales del siglo XIX,\n"
        "con la última década registrada como la más cálida. Este aumento de temperaturas ha provocado efectos en cascada:\n"
        "•   **Eventos climáticos extremos:** Se observan sequías más intensas, inundaciones, tormentas más frecuentes y destructivas, así como olas de calor prolongadas.\n"
        "•   **Pérdida de biodiversidad:** Muchas especies enfrentan desajustes ecológicos y cambios en sus hábitats naturales.\n"
        "•   **Impacto en los sistemas humanos:** Cambios en la agricultura, la disponibilidad de agua y la salud pública, incluyendo nuevas enfermedades asociadas al aumento de temperaturas"
    )
    await ctx.send(impactos)

@bot.command()
async def catastrofes(ctx):
    catastrofes = (
        "**Eventos catastroficos recientes** \n"
        "El cambio climático no es una amenaza futura; ya está causando devastación en todo el mundo: \n"
        "•	**Incendios en Australia (2019-2020):** Los incendios negros destruyeron más de 18 millones de hectáreas, mataron o desplazaron a casi 3 mil millones de animales y liberaron cantidades masivas de CO2 a la atmósfera. \n"
        "•	**Ola de Calor Europea (2022):** Temperaturas récord superiores a 40°C en países como Reino Unido, causando miles de muertes y graves sequías. \n"
        "•	**Inundaciones en Pakistán (2022):** Un tercio del país quedó bajo el agua, afectando a 33 millones de personas y causando pérdidas por más de 40 mil millones de dólares. \n"
        "•   **Sequía en el Cuerno de África (2020-2023):** La peor sequía en 40 años, poniendo a millones de personas en riesgo de hambruna. \n"
    )
    await ctx.send(catastrofes)

@bot.command()
async def causas(ctx):
    causas = (
        "**Causas del cambio climatico** \n"
        "•	**El uso de combustibles fósiles:** Carbón, petróleo y gas son los principales responsables del cambio climático. Representan más del 75 % de las emisiones mundiales de gases de efecto invernadero (GEI) y casi el 90 % de las emisiones de dióxido de carbono. Estos gases cubren la atmósfera y atrapan el calor solar, acelerando el calentamiento global.\n"
        "•	**Generación de energía:** La producción de electricidad y calor a partir de combustibles fósiles es una fuente clave de emisiones. Aunque las energías renovables, como la solar y la eólica, están creciendo, gran parte de la energía aún proviene del carbón y el gas.\n"
        "•	**Productos de fabricación:** La industria y la manufactura generan grandes cantidades de GEI al quemar combustibles fósiles y usar químicos derivados de estos. Sectores como el del cemento, el acero y la electrónica son altamente contaminantes.\n"
        "•	**Tala de bosques:** Cada año se pierden 12 millones de hectáreas de bosque, liberando el carbono almacenado en los árboles y reduciendo la capacidad de los ecosistemas para absorber dióxido de carbono.\n"
        "•	**Uso del transporte:** Automóviles, barcos y aviones funcionan principalmente con combustibles fósiles. El transporte es responsable de cerca del 25 % de las emisiones relacionadas con la energía.\n"
        "•	**Producción de alimentos:** Desde la deforestación hasta la emisión de metano por el ganado, la agricultura contribuye significativamente al cambio climático. Además, el transporte, envasado y distribución de alimentos incrementan las emisiones.\n"
        "•	**Energía en edificios:** Los sistemas de calefacción, climatización e iluminación en edificios residenciales y comerciales consumen grandes cantidades de energía fósil.\n"
        "•	**Consumo excesivo: Los** estilos de vida de las personas más ricas generan más emisiones que el 50 % más pobre de la población mundial. Desde el uso de plásticos hasta el derroche de energía, el consumo exacerbado aumenta la huella de carbono."
    )
    await ctx.send(causas)

@bot.command()
async def consecuencias(ctx):
    consecuencias = (
        "**Consecuencias del cambio climatico** \n"
        "•	 **Elevación de temperaturas:** Desde los años 80, cada década ha sido más cálida que la anterior. Esto provoca olas de calor más frecuentes, incendios forestales y enfermedades relacionadas con el calor.\n"
        "•	 **Tormentas más potentes:** El aumento de la humedad por la evaporación intensifica las tormentas tropicales, que destruyen comunidades y causan pérdidas económicas y humanas.\n"
        "•	 **Sequías y escasez de agua:** Regiones secas enfrentan una disponibilidad de agua más limitada, afectando cultivos y aumentando el riesgo de tormentas de arena.\n"
        "•	 **Aumento del nivel del mar:** El calentamiento de los océanos y el deshielo polar amenazan a las comunidades costeras e insulares.\n"
        "•	 **Pérdida de biodiversidad:** Muchas especies no logran adaptarse al rápido cambio climático, enfrentando extinción.\n"
        "•	 **Escasez de alimentos:** Las alteraciones en el clima reducen la productividad agrícola, poniendo en riesgo la seguridad alimentaria.\n"
        "•	 **Impactos en la salud humana:** El cambio climático exacerba enfermedades, contamina el aire y genera estrés mental por desplazamientos forzados.\n"
        "•	 **Pobreza y migración:** Las catástrofes relacionadas con el clima obligan a millones de personas a abandonar sus hogares, aumentando la pobreza.\n"
    )
    await ctx.send(consecuencias)

@bot.command()
async def respuestas_humanas(ctx):
    respuestas_humanas = (
        "**Respuestas humanas del cambio climatico** \n"
        "•	 **Mitigación:** Reducción de emisiones de gases de efecto invernadero mediante el cambio a fuentes de energía renovables, como la solar y la eólica, y la disminución del uso de combustibles fósiles. Esto incluye compromisos internacionales como el Acuerdo de París, que busca limitar el aumento de la temperatura global a menos de 2 °C, preferiblemente 1,5 °C.\n"
        "•	 **Adaptación:** Ajuste a las nuevas condiciones climáticas para proteger a las personas y los ecosistemas. Ejemplos incluyen sistemas de alerta temprana para desastres y la planificación urbana resiliente al clima.\n"
    )
    await ctx.send(respuestas_humanas)

@bot.command()
async def reaccion_internacional(ctx):
    reaccion_internacional = (
        "**La reaccion internacional al cambio climatico** \n"
        "El cambio climático requiere una acción concertada a nivel global. La Convención Marco de las Naciones Unidas sobre el Cambio Climático (CMNUCC), adoptada en 1992, marcó un primer paso importante. Las Conferencias de las Partes (COP),"
        "como la COP21 celebrada en París en 2015, han establecido objetivos ambiciosos para reducir emisiones y promover economías bajas en carbono. A pesar de estos esfuerzos, las políticas actuales apuntan a un aumento de la temperatura global de 2,8 °C para finales de siglo, lejos de los objetivos establecidos."
    )
    await ctx.send(reaccion_internacional)

@bot.command()
async def soluciones(ctx):
    soluciones = (
        "**Soluciobes para el cambio climatico** \n"
        "•	 **Compromiso político:** Es crucial que los países más contaminantes lideren el cambio hacia modelos sostenibles mediante políticas y acuerdos internacionales, como el Acuerdo de París.\n"
        "•	 **Educación ambiental:** Concienciar a la población sobre los efectos del cambio climático y fomentar prácticas sostenibles puede generar un cambio a nivel comunitario.\n"
        "•	 **Transición energética:** Sustituir los combustibles fósiles por energías renovables como la solar y la eólica es fundamental para reducir las emisiones.\n"
        "•	 **Movilidad sostenible:** Promover el uso de bicicletas, transporte público y vehículos eléctricos reduce significativamente la huella de carbono.\n"
        "•	 **Reducción de residuos:** Implementar prácticas de reciclaje y reutilización, así como combatir la obsolescencia programada, ayuda a disminuir la contaminación.\n"
        "•	 **Consumo local:** Favorecer la compra de productos locales reduce las emisiones asociadas al transporte.\n"
        "•	 **Nuevos modelos económicos:** Fomentar negocios enfocados en la economía circular y sostenible puede mitigar el impacto ambiental.\n"
        "•	 **Proyectos de reforestación:** Recuperar bosques y proteger áreas naturales ayuda a absorber el dióxido de carbono y a preservar la biodiversidad.\n"
    )
    await ctx.send(soluciones)

@bot.command()
async def comandos(ctx):
    comandos = (
        "**Comandos para operar a Clim-Bot** \n"
        "Clim-Bot es un bot de discord que te va a enseñar sobre el cambio climatico, que es, causas consecuencias y como nos esta perjudicando \n"
        "•	   *que_es\n"
        "•	   *impactos\n"
        "•	   *catastrofes\n"
        "•	   *causas\n"
        "•	   *consecuencias\n"
        "•	   *respuestas_humanas\n"
        "•	   *reaccion_internacional\n"
        "•	   *soluciones\n"
        "•	   *comandos\n"
        "•	   *desastres\n"
    )
    await ctx.send(comandos)


@bot.command()
async def desastres(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_path = os.path.join(Carpeta_desastre, attachment.filename)
            await attachment.save(file_path)

            result = get_class(model_path="./keras_model.h5", labels_path="./labels.txt", image_path=file_path)
            
            try:
                disaster_name, confidence = result  
                disaster_name = disaster_name.strip()  
                confidence = f"{int(float(confidence) * 100)}%"  

                name_to_id = {
                    "Huracanes": 0,
                    "Incendios Forestales": 1,
                    "Inundaciones": 2,
                    "Mega Sequías": 3,
                    "Mega Tormentas": 4,
                    "Olas de Calor": 5
                }
                
                disaster_id = name_to_id.get(disaster_name, None)
                
                if disaster_id is not None and disaster_id in DESASTRE_INFO:
                    info = DESASTRE_INFO[disaster_id]
                    recommendations = "\n".join([f"- {rec}" for rec in info['recommendation']])
                    safety_tips = "\n".join([f"- {tip}" for tip in info['safety_tips']])
                    frequentsregions = "\n".join([f"- {tip}" for tip in info['frequent_regions']])
                    descripcion = ", ".join(info['description'])
                    video_link = info['video']
                    response = (
                        f"**{info['name']}**\n"
                        f"**Descripción**:{descripcion}\n"
                        f"**Regiones frecuentes**:\n{frequentsregions}\n"
                        f"**Recomendaciones**:\n{recommendations}\n"
                        f"**Tips de seguridad**:\n{safety_tips}\n"
                        f"**Acontecimiento histórico**: {info['historical_event']}\n"
                        f"**Porcentaje de identificación**: {confidence}\n"
                        f"**Video relacionado**: {video_link}"
                    )
                else:
                    response = "No se pudo identificar correctamente el desastre natural."

                await ctx.send(response)
            except (ValueError, KeyError, TypeError) as e:
                await ctx.send("Hubo un error procesando la información del desastre natural.")
                print(f"Error al procesar el resultado del modelo: {e}")
    else:
        await ctx.send("Ups, no has cargado ninguna imagen.")


bot.run("pon tu token aca")