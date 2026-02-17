
import pandas as pd
import streamlit as st
import math
from help import *


DATA_DIR = "data/Lookup_Tables"
tables = {}

def zona_climatica(provincia, altitud):

    # row = Lookup$Row('zonas';31;provincia$)
    row = lookup_row('zonas', 'Provincia', provincia)

# Indice bruto es como interpolar la altitud en las columnas de la tabla
    if altitud < 8000:
        indice_bruto = 1 + (altitud - 50) * 26 / 1300

        if indice_bruto >= 27:
            indice = 27
        else:
            indice = math.trunc(indice_bruto) + 1

# Indice + 3 porque las primeras 3 columnas no son localizaciones (titulo, espacio, provincia)
        zona = lookup_value('zonas', row, indice + 3)
    else:
        zona = lookup_value('zonas', row, 3)

    return zona

def zonainv(provincia, altitud):
    # zonainv$ = Copy$(zona$;1;1)
    return zona_climatica(provincia, altitud)[0]  # letra

def zonaver(provincia, altitud):
    # zonaver$ = Copy$(zona$;2;1)
    return zona_climatica(provincia, altitud)[1]  # número

def zona_inv_localidad(provincia, altitud):

    row = lookup_row('zonas', 'Provincia', provincia)

    if altitud < 8000:
        indice_bruto = 1 + (altitud - 50) * 25 / 1250

        if indice_bruto >= 26:
            indice = 26
        else:
            indice = math.trunc(indice_bruto) + 1

    else:
        indice = 0
    
    zona = lookup_value('zonas', row, indice + 3)

    return zona

def demanda_referenciacalefaccion(provincia, altitud, tipo_vivienda):
    zonainvlocalidad = zona_inv_localidad(provincia, altitud)
    # para zona inv localidad, que tipo de referencias son a3c, a2c, b2c, c2c ?????????????????????
    row = lookup_row('sci_referencia', 0, zonainvlocalidad)
    # no entiendo que es el sci
    SCI = lookup_value('sci_referencia', row, 2)
    # calcula el sci pero no se usa para nada ???????????????????????????????
    # Por que nuevo ?????????????????????????????? si no se ha comprobado nada de fechas ???????????????
    if (tipo_vivienda == 'bloque'):
        demanda_referenciacalefaccion = lookup_value('sci_referencia', row, 'DR nuevo bloque')
    else:
        demanda_referenciacalefaccion = lookup_value('sci_referencia', row, 'DR nueva vivienda')
    
    return demanda_referenciacalefaccion

# que es scv ???????????????????????????????????????
def demanda_referenciarefrig(provincia, altitud, tipo_vivienda):
    zonaverlocalidad = zona_inv_localidad(provincia, altitud)
    row = lookup_row('scv_referencia', 0, zonaverlocalidad)
    SCV = lookup_value('scv_referencia', row, 2)
    # calcula el scv pero no se usa para nada ???????????????????????????????
    # Por que nuevo ?????????????????????????????? si no se ha comprobado nada de fechas ???????????????
    if (tipo_vivienda == 'bloque'):
        demanda_referenciarefrig = lookup_value('scv_referencia', row, 'DR nuevo bloque')
    else:
        demanda_referenciarefrig = lookup_value('scv_referencia', row, 'DR nuevo unif')
    
    return demanda_referenciarefrig

def elevacion(altitud, fila_capital):
    if altitud >= 8000:
        elevacion = 0
    else:
        # no estoy segura si empieza en 0 o en 1. si empieza en 1, hay que restar 1 a columna
        elevacion = altitud - lookup_value('Temp red ACS', fila_capital, 2)
    return elevacion

def referencia(tipo_vivienda):
    if tipo_vivienda == 'unifamiliar':
        referencia = 'cal uni'
    else:
        referencia = 'cal bloq'
    return referencia
# no tendría por que definir "referencia" pero lo hago por si acaso necesito el valor luego

def litros_acs(tipo_vivienda):
    if tipo_vivienda == 'unifamiliar':
        litros_acs = 28
    else:
        litros_acs = 28*(22/30)
    return litros_acs

def hspf(tipo_calefaccion, inst_calefaccion, zona_invierno, califE):
    ## Esto teniendo en cuenta que junto las opciones
    if califE in ('Posterior a 2007', 'A', 'B', 'C'):
        tabla_HSPF = 'HSPF_nuevo'
    else:
        tabla_HSPF = 'HSPF_existente'
    fila_HSPF = lookup_row(tabla_HSPF, 'sistema', tipo_calefaccion)
    hspf = lookup_value(tabla_HSPF, fila_HSPF, inst_calefaccion)
    return hspf

def seer(zona_verano, califE):
    if (califE == 'Posterior a 2007') or (califE == 'A') or (califE == 'B') or (califE == 'C'):
        columna = 'nuevo'
    else:
        columna = 'existente'
    if zona_verano == '1':
        seer = -1
    else:
        fila = lookup_row('SEER', 'zona', zona_verano)
        seer = lookup_value('SEER', fila, columna)
    return seer

def tabla_acsspf(califE):
    if (califE == 'Posterior a 2007') or (califE == 'A') or (califE == 'B') or (califE == 'C'):
        tabla_acsspf = 'ACS_SPFnuevo'
    else:
        tabla_acsspf = 'ACS_SPFexistente'
    return tabla_acsspf

def alquiler_equipos(tipo_calefaccion):
    if tipo_calefaccion == 'gas natural':
        # en la tabla solo hay un valor para €/mes
        alquiler_equipos = lookup_value('alquiler equipos', 1, 'coste')  # €/mes, incluye canon IRC
    else:
        # no entiendo pq es 0
        alquiler_equipos = 0  # electricidad en luz
    return alquiler_equipos

def alquiler_equiposacs(tipo_acs, inst_acs):
    if (tipo_acs == 'gas natural') and (inst_acs == 'individual'):
        alquiler_equiposacs = lookup_value('alquiler equipos', 1, 'coste')  # €/mes, incluye canon IRC
    else:
        alquiler_equiposacs = 0  # electricidad en luz
    return alquiler_equiposacs

def impuesto_gas(suministro):
    if suministro == 'gas natural':
        impuesto_gas = lookup_value('impuestos', 1, 'impuesto')  # €/kWh de gas natural
    else:
        impuesto_gas = 0
    return impuesto_gas

def impuesto_electricidad(tipo):
    if (tipo == 'electricidad (radiadores)') or (tipo == 'electricidad (acumuladores)') or (tipo == 'bomba de calor'):
        impuesto_electricidad = lookup_value('impuestos', 2, 'impuesto') / 100  # porcentaje sobre gasto variable; en gastos de luz se pondrá el porcentaje sobre gasto fijo
    elif tipo == 'electricidad':
        impuesto_electricidad = lookup_value('impuestos', 2, 'impuesto') / 100  # porcentaje sobre gasto variable; en gastos de luz se pondrá el porcentaje sobre gasto fijo
    else:
        impuesto_electricidad = 0
    return impuesto_electricidad

def coste_fijocalreparto(tipo_calefaccion, inst_calefaccion, coste_fijoCAL):
    # de donde sale coste_fijoCAL??????????????????????????????
    if tipo_calefaccion == 'gas natural':
        if inst_calefaccion == 'central':
            coste_fijocalreparto = 0
        else:
            coste_fijocalreparto = coste_fijoCAL
    else:
        coste_fijocalreparto = 0
    return coste_fijocalreparto

def coste_fijoacsreparto(inst_acs, tipo_acs, inst_calefaccion, tipo_calefaccion, coste_fijoACS):
    if (tipo_acs == 'gas natural') and (inst_acs == 'individual'):
        if (tipo_calefaccion == 'gas natural') and (inst_calefaccion != 'central'):
            coste_fijoacsreparto = 0
        else:
            coste_fijoacsreparto = coste_fijoACS
    else:
        coste_fijoacsreparto = 0
    return coste_fijoacsreparto

def factor_ivacal(tipo, provincia):
    if (tipo == 'electricidad (radiadores)') or (tipo == 'electricidad (acumuladores)') or (tipo == 'bomba de calor'):
        if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
            factor_ivacal = lookup_value('impuestos', 4, 2)
        elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
            factor_ivacal = lookup_value('impuestos', 6, 2)
        else:
            factor_ivacal = lookup_value('impuestos', 3, 2)
    elif tipo == 'gas natural':
        if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
            factor_ivacal = lookup_value('impuestos', 5, 2)
        elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
            factor_ivacal = lookup_value('impuestos', 7, 2)
        else:
            factor_ivacal = lookup_value('impuestos', 3, 2)
    else:
        factor_ivacal = 0
    return factor_ivacal

def factor_ivaacs(tipo, provincia):
    if tipo == 'electricidad':
        if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
            factor_ivaacs = lookup_value('impuestos', 4, 2)
        elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
            factor_ivaacs = lookup_value('impuestos', 6, 2)
        else:
            factor_ivaacs = lookup_value('impuestos', 3, 2)
    elif tipo == 'gas natural':
        if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
            factor_ivaacs = lookup_value('impuestos', 5, 2)
        elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
            factor_ivaacs = lookup_value('impuestos', 7, 2)
        else:
            factor_ivaacs = lookup_value('impuestos', 3, 2)
    else:
        factor_ivaacs = 0
    return factor_ivaacs

def factor_ivaelectricidad_conta(provincia):
    fila_IVAelectricidad = lookup_value('impuestos', 'tipo', 'IVA')
    if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
        factor_ivaelectricidad_conta = lookup_value('impuestos', 4, 2)
    elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
        factor_ivaelectricidad_conta = lookup_value('impuestos', 6, 2)
    else:
        factor_ivaelectricidad_conta = lookup_value('impuestos', fila_IVAelectricidad, 'impuesto')
    return factor_ivaelectricidad_conta

# no entiendo esta función??????????????????????
def factor_ivaelectricidad_noconta(provincia):
    fila_IVAelectricidad = lookup_value('impuestos', 'tipo', 'IVA')
    if (provincia == 'Palmas, Las') or (provincia == 'Santa Cruz de Tenerife'):
        factor_ivaelectricidad_noconta = 0
    elif (provincia == 'Ceuta') or (provincia == 'Melilla'):
        factor_ivaelectricidad_noconta = lookup_value('impuestos', 6, 2)
    else:
        factor_ivaelectricidad_noconta = lookup_value('impuestos', fila_IVAelectricidad, 'impuesto')
    return factor_ivaelectricidad_noconta

## QUE ES TRAMO????????????????
def potencia_poromision(Npax, tipo_calefaccion, tramo):
    potencia_minima = [2.4, 3.3, 3.8, 4.3, 4.9]
    potencia_maxima = [4.4, 6.0, 6.9, 7.8, 8.9]
    if Npax >= 5:
        N = 5
    else:
        N = Npax
    if (tipo_calefaccion == 'electricidad (radiadores)') or (tipo_calefaccion == 'electricidad (acumuladores)') or (tipo_calefaccion == 'bomba de calor'):
        if tipo_calefaccion == 'electricidad (acumuladores)':
            if tramo == 'Punta':
                potencia_poromision = potencia_minima[N]
            else:
                potencia_poromision = potencia_maxima[N]
        else:
            potencia_poromision = potencia_maxima[N] #el tramo valle es por la noche y findes, por lo que hay que poner la potencia máxima siempre
    else:
        potencia_poromision = potencia_minima[N]
    return potencia_poromision

def tarifa_suministro(inst_termica, tipo_instalacion, consumo_gn, termino,
                      provincia, zona_invierno, potencia_punta, potencia_valle):

    sistema = None
    #sistema me ayuda a definir que fila de la tabla tarifas tengo que usar

    # --- Combustibles no eléctricos ---
    if tipo_instalacion == "gas natural":
        if inst_termica == "individual":
            sistema = "gas natural" if consumo_gn > 5000 else "gas natural (bajo consumo)"
        else:
            sistema = "gas natural central"

    elif tipo_instalacion in ("glp", "gasóleo"):
        if provincia == "Ceuta":
            sistema = f"{tipo_instalacion}_ceuta"
        elif provincia == "Melilla":
            sistema = f"{tipo_instalacion}_melilla"
        elif provincia in ("Palmas, Las", "Santa Cruz de Tenerife"):
            sistema = f"{tipo_instalacion}_canarias"
        else:
            sistema = tipo_instalacion

    elif tipo_instalacion in ("carbón", "biomasa"):
        sistema = tipo_instalacion

    if sistema is not None:
        fila = lookup_row("tarifas", "sistema", sistema)
        return lookup_value("tarifas", fila, termino)

    # --- Eléctrico ---
    # que es lo de fijo y variable y punta y valle?????????????
    if termino == "fijo":
        fijo_punta = lookup_value("pvpc", 1, "fijo")
        fijo_valle = lookup_value("pvpc", 2, "fijo")
        return (fijo_punta * potencia_punta + fijo_valle * potencia_valle) / potencia_punta

    variable_punta = lookup_value("pvpc", 1, "variable")
    variable_valle = lookup_value("pvpc", 2, "variable")
    variable_llano = lookup_value("pvpc", 3, "variable")

    fila_pesos = lookup_row("pesos tarifa electrica", 1, zona_invierno)
    peso_punta = lookup_value("pesos tarifa electrica", fila_pesos, "peso_punta")
    peso_valle = lookup_value("pesos tarifa electrica", fila_pesos, "peso_valle")
    peso_llano = lookup_value("pesos tarifa electrica", fila_pesos, "peso_llano")

    if tipo_instalacion == "electricidad (acumuladores)":
        return variable_valle
    if tipo_instalacion == "electricidad":
        return variable_llano

    return (variable_punta * peso_punta
            + variable_llano * peso_llano
            + variable_valle * peso_valle)

def tarifa_suministroref(zona_verano): 
    variable_punta = lookup_value('pvpc', 1, 'variable') 
    variable_valle = lookup_value('pvpc', 2, 'variable') 
    variable_llano = lookup_value('pvpc', 3, 'variable') 
    if zona_verano == '1': 
        tarifa_suministroref = 0 
    else: 
        fila_pesos = lookup_row('pesos tarifa electrica verano', 1, zona_verano) 
        peso_punta = lookup_value('pesos tarifa electrica verano', fila_pesos, 'peso_punta') 
        peso_valle = lookup_value('pesos tarifa electrica verano', fila_pesos, 'peso_valle') 
        peso_llano = lookup_value('pesos tarifa electrica verano', fila_pesos, 'peso_llano') 
        tarifa_suministroref = variable_punta*peso_punta + variable_llano*peso_llano + variable_valle*peso_valle 
    return tarifa_suministroref

def tarifa_electrica(termino, potencia_punta, potencia_valle): 
    if termino == 'fijo': 
        fijo_punta = lookup_value('pvpc', 1, 'fijo') 
        fijo_valle = lookup_value('pvpc', 2, 'fijo') 
        tarifa_electrica = (fijo_punta*potencia_punta + fijo_valle*potencia_valle)/potencia_punta 
    else: 
        variable_punta = lookup_value('pvpc', 1, 'variable') 
        variable_valle = lookup_value('pvpc', 2, 'variable') 
        variable_llano = lookup_value('pvpc', 3, 'variable') 
        fila_pesos = lookup_row('pesos tarifa electrica', 1, 'usos domesticos')
        peso_punta = lookup_value('pesos tarifa electrica', fila_pesos, 'peso_punta')
        peso_valle = lookup_value('pesos tarifa electrica', fila_pesos, 'peso_valle')
        peso_llano = lookup_value('pesos tarifa electrica', fila_pesos, 'peso_llano')
        tarifa_electrica = variable_punta*peso_punta + variable_llano*peso_llano + variable_valle*peso_valle 
    return tarifa_electrica

def consumo_gas(tipo_calefaccion, tipo_acs, consumo_calefaccion, consumo_acs, inst_calefaccion, inst_ACS, llamada): 
    if tipo_calefaccion == 'gas natural': 
        cal = 1 
        if llamada == 'calefaccion': 
            peso_cal = 1 
        elif inst_calefaccion == inst_ACS: 
            peso_cal = 1 
        else: 
            peso_cal = 0 
    else: 
        cal = 0
        peso_cal = 0 

    if tipo_acs == 'gas natural': 
        acs = 1 
        if llamada == 'ACS': 
            peso_acs = 1 
        elif inst_calefaccion == inst_ACS: 
            peso_acs = 1 
        else: 
            peso_acs = 0
    else: 
        acs = 0
        peso_acs = 0

    return consumo_calefaccion*cal*peso_cal + consumo_acs*acs*peso_acs

def fdemanda_corregidacal(demanda_CorregidaSigno):
    if demanda_CorregidaSigno < 0:
        fdemanda_corregidacal = 0
    else:
        fdemanda_corregidacal = demanda_CorregidaSigno
    return fdemanda_corregidacal

def io_is(zona_invierno, tipo_vivienda, C1):
    row = lookup_row('Dispersion R', 'Zona', zona_invierno)
    R = float(str(lookup_value('Dispersion R', row, tipo_vivienda)).replace(",", "."))
    C1 = float(str(C1).replace(",", "."))
    io_is = (1 + (C1 - 0.6) * 2 * (R - 1)) / R
    return io_is

def io_is_verano(zona_verano, tipo_vivienda, C1):
    if zona_verano == '1':
        io_is_verano = -1
    else:
        row = lookup_row('Dispersion R verano', 'Zona', zona_verano)
        R = lookup_value('Dispersion R verano', row, tipo_vivienda)
        io_is_verano = (1 + (C1 - 0.6) * 2 * (R - 1)) / R
    return io_is_verano

def calcula_c1(califE, zona_invierno, tipo_vivienda):
    if tipo_vivienda == 'bloque':
        row = lookup_row('C1_bloque', 'zona', zona_invierno)
        calcula_c1 = lookup_value('C1_bloque', row, califE)
    else:
        row = lookup_row('C1_unifamiliar', 'zona', zona_invierno)
        calcula_c1 = lookup_value('C1_unifamiliar', row, califE)
    return calcula_c1

def calcula_c1_verano(califE, zona_verano, tipo_vivienda):
    if zona_verano == '1':
        calcula_c1_verano = -1
    elif tipo_vivienda == 'bloque':
        row = lookup_row('C1_bloque_verano', 'zona', zona_verano)
        calcula_c1_verano = lookup_value('C1_bloque_verano', row, califE)
    else:
        row = lookup_row('C1_unifamiliar_verano', 'zona', zona_verano)
        calcula_c1_verano = lookup_value('C1_unifamiliar_verano', row, califE)
    return calcula_c1_verano

def corrige_zona1(zona_verano):
    if zona_verano==1:
        corrige_zona1 = 0
    else:
        corrige_zona1 = 1

    return corrige_zona1

def factor_electricidadacs(tipo_ACS):
    if tipo_ACS=='electricidad':
        factor_electricidadacs = 1
    else:
        factor_electricidadacs = 0
        
    return factor_electricidadacs

def factor_electricidadcal(tipo_calefaccion):
    if tipo_calefaccion in ('electricidad(radiadores)', 'electricidad(acumuladores)', 'bomba de calor'):
        factor_electricidadcal = 1
    else:
        factor_electricidadcal = 0
        
    return factor_electricidadcal

##################################################################################################
#                        FUNCIONES CONSUMO ELÉCTRICO NO TÉRMICO                                  #
##################################################################################################

"Función para devolver el número de miembros para el consumo eléctrico (no térmico)"
def miembro(Npax):
    match Npax:
        case 1:
            miembro = '1'
        case 2:
            miembro = '2'
        case 3:
            miembro = '3'
        case 4:
            miembro = '4'
        case _:
            miembro = 'Mas de 4'
    return miembro

#Función para saber columna en la que posicionarse en las Lookup Tables
# (Si se le resta uno obtenemos el nº de miembros numéricamente)
def columna(Npax):
    match Npax:
        case 1:
            columna = 2
        case 2:
            columna = 3
        case 3:
            columna = 4
        case 4:
            columna = 5
        case _: #default
            columna = 6
    return columna

#Funcion para calculo de gasto electrico de cada aparato
def gesin(nombre_aparato, miembros):
    Col = columna(miembros)
    if nombre_aparato in('Lavavajillas','Secadora','Congelador', 'Ordenador'):
        gesin= lookup_value('CMECon', lookup_row('CMECon', 1, nombre_aparato),Col)/(lookup_value('Penetracion', lookup_row('Penetracion',1,nombre_aparato),2))
    else:
        gesin=lookup_value('CMESin',lookup_row('CMESin',1,nombre_aparato),Col)
    return gesin
 
def gecon(nombre_aparato, miembros):
    Col=columna(miembros)
    if nombre_aparato=='Tablet':
        gecon= lookup_value('CMESin',lookup_row('CMESin', 1,nombre_aparato),Col)*lookup_value('Penetracion', lookup_row('Penetracion',1,nombre_aparato),2)
    else:
        gecon=lookup_value('CMECon',lookup_row('CMECon',1,nombre_aparato),Col)
    return gecon

def gei(provincia, Npax, superficie):
    zona_ilu = lookup_value('zonas', lookup_row('zonas', 31, provincia), 32)
    if Npax<5:
        miembros = Npax
    else:
        miembros = 5
    if(superficie<70):
        catalogar_sup = 2
    elif superficie<=110:
        catalogar_sup = 3
    else:
        catalogar_sup = 4
    gei = lookup_value(zona_ilu,miembros,catalogar_sup)
    
    return gei

#Funcion para determinar si aplicacamos el consumo con o sin penetracion y si hay dicho aparato
def consumo_aparato(aparato, nombre_aparato, miembros):
    match aparato:
        case 'True':
            consumo_aparato = gesin(nombre_aparato, miembros)
        case 'False':
            consumo_aparato = 0
        #### dudoso
        case 'NS/NC':
            consumo_aparato = gecon(nombre_aparato, miembros)
        case _:
             raise ValueError(f"Valor de aparato no válido: {aparato}")
    
    return consumo_aparato

#Consumo electrico total de todos los electrodomésticos
def consumo_electrico(cocina, horno, lavadora, secadora, frigorifico, congelador, tv, ordenador, lavavajillas, movil, tablet, microondas, miembros, superficie, Npax, provincia):
    consumo_electrico = consumo_aparato(cocina,'Cocina',miembros) +  consumo_aparato(horno,'Horno', miembros) + consumo_aparato(lavadora,'Lavadora',miembros) +  consumo_aparato(secadora,'Secadora',miembros) + consumo_aparato(frigorifico,'Frigorifico',miembros)+consumo_aparato(congelador,'Congelador',miembros)+consumo_aparato(tv,'TV',miembros) + consumo_aparato(ordenador,'Ordenador',miembros)+consumo_aparato(lavavajillas,'Lavavajillas',miembros)+consumo_aparato(movil,'Movil',miembros)+consumo_aparato(tablet,'Tablet',miembros)+ consumo_aparato(microondas,'Microondas',miembros)+ gei(provincia, Npax, superficie)
    return consumo_electrico

#Funciones para determinar miembros con el mismo trabajo
def ocupado(ocupacion, Col):
    match ocupacion:

        case 0:
            ocupado = 0
        case 1:
            ocupado = lookup_value('Factores', lookup_row('Factores', 1, '01'), Col)
        case 2:
            ocupado = lookup_value('Factores', lookup_row('Factores', 1, '02'), Col)
        case 3:
            ocupado = lookup_value('Factores', lookup_row('Factores', 1, '03'), Col)
        case _: #default
            raise ValueError(f"Valor no válido: {ocupacion}")
    
    return ocupado

def parado(ocupacion, Col):
    match ocupacion:
        case 0:
            parado = 0
        case 1:
            parado = lookup_value('Factores', lookup_row('Factores', 1, 'P1'), Col)
        case _:
            parado = lookup_value('Factores', lookup_row('Factores', 1, 'P2'), Col)
 
    return parado


def estudiante(ocupacion, Col):
    match ocupacion:
        case 0:
            estudiante = 0
        case 1:
            estudiante = lookup_value('Factores', lookup_row('Factores', 1, 'E1'), Col)
        case _:
            estudiante = lookup_value('Factores', lookup_row('Factores', 1, 'E2'), Col)
 
    return estudiante

def jubilado(ocupacion, Col):
    match ocupacion:
        case 0:
            jubilado = 0
        case 1:
            jubilado = lookup_value('Factores', lookup_row('Factores', 1, 'J1'), Col)
        case _:
            jubilado = lookup_value('Factores', lookup_row('Factores', 1, 'J2'), Col)
 
    return jubilado


def incapacitado(ocupacion, Col):
    match ocupacion:
        case 0:
            incapacitado = 0
        case _:
            incapacitado = lookup_value('Factores', lookup_row('Factores', 1, 'Pe1'), Col)
 
    return incapacitado

def viudo(ocupacion, Col):
    match ocupacion:
        case 0:
            viudo = 0
        case _:
            viudo = lookup_value('Factores', lookup_row('Factores', 1, 'Pe2'), Col)
 
    return viudo

def ama(ocupacion, Col):
    match ocupacion:
        case 0:
            ama = 0
        case _:
            ama = lookup_value('Factores', lookup_row('Factores', 1, 'C'), Col)
 
    return ama

def otro(ocupacion, Col):
    match ocupacion:
        case 0:
            otro = 0
        case _:
            otro = lookup_value('Factores', lookup_row('Factores', 1, 'X'), Col)
 
    return otro

# Funcion para determinar cada factor de cada tipo de trabajo

def factor(ocupacion, nombre_ocupacion, Col): 
    match nombre_ocupacion:
        case'Ocupado': 
            factor = ocupado(ocupacion,Col) 
        case'Parado':
            factor = parado(ocupacion, Col) 
        case 'Estudiante':
            factor = estudiante(ocupacion,Col) 
        case 'Jubilado':
            factor = jubilado(ocupacion,Col) 
        case'Incapacitado':
            factor = incapacitado(ocupacion,Col) 
        case'Viudo':
            factor = viudo(ocupacion,Col) 
        case'Ama':
            factor = ama(ocupacion, Col) 
        case _:
            factor = otro(ocupacion,Col) 
    return factor

# Funcion para determinar la suma de todos los factores

def factores(ocupado, parado, estudiante, jubilado, incapacitado, viudo, ama, otro, miembros):
    Col = columna(miembros) 
    factores = factor(ocupado, 'Ocupado', Col) +factor(parado,'Parado', Col) + factor(estudiante, 'Estudiante', Col) + factor(jubilado, 'Jubilado', Col) + factor(incapacitado, 'Incapacitado', Col) + factor(viudo, 'Viudo', Col) + factor(ama, 'Ama', Col) + factor(otro, 'Otro', Col) 
    return factores
 



            


