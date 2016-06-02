


def fecha_parser(fecha):
    fecha_hora = str(fecha).split()
    fechas = fecha_hora[0].split("-")

    cadena = str(fechas[2]) + " de " + numbers_to_strings(int(fechas[1])) + " del " + str(fechas[0])

    return cadena

def numbers_to_strings(argument):
    switcher = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "setiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre",
    }
    return switcher.get(argument, "nothing")
