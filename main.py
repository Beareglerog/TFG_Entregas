from model import *
import numpy as np
#*********************************************************************************************
#                                   PROGRAMA PRINCIPAL 
# ********************************************************************************************* 

#### TNGO QUE AÑADIR LOS INPUTS DEL PROGRAMA


# CALEFACCIÓN
zona_invierno = zonainv(provincia, altitud) 
C1 = calcula_c1(califE, zona_invierno, tipo_vivienda) 
Io_Is = io_is(zona_invierno, tipo_vivienda, C1) 
demanda_RefCal = demanda_referenciacalefaccion(provincia, altitud, tipo_vivienda) 
demanda_CorregidaSigno = Io_Is * demanda_RefCal * superficie 
demanda_CorregidaCal = fdemanda_corregidacal(demanda_CorregidaSigno) 
HSPF = hspf(tipo_calefaccion, inst_calefaccion, zona_invierno, califE) 
consumo_calefaccion = demanda_CorregidaCal / HSPF 
consumo_gnCAL = consumo_gas(tipo_calefaccion, tipo_acs, consumo_calefaccion, consumo_acs, inst_calefaccion, inst_ACS, 'calefaccion') 
coste_fijoCAL = tarifa_suministro(inst_calefaccion, tipo_calefaccion, consumo_gnCAL, 'fijo', provincia, zona_invierno, pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
coste_fijoCALreparto = coste_fijocalreparto(tipo_calefaccion, inst_calefaccion, coste_fijoCAL) 
coste_variableCAL = tarifa_suministro(inst_calefaccion, tipo_calefaccion, consumo_gnCAL, 'variable', provincia, zona_invierno, pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
alquiler_equiposCAL = alquiler_equipos(tipo_calefaccion) 
impuesto_gas = impuesto_gas(tipo_calefaccion) 
impuesto_electricidad = impuesto_electricidad(tipo_calefaccion) 
gasto_CAL = (coste_fijoCALreparto*12 + coste_variableCAL*consumo_calefaccion + alquiler_equiposCAL*12 + impuesto_gas*consumo_calefaccion + impuesto_electricidad*coste_variableCAL*consumo_calefaccion)*(1+factor_ivacal(tipo_calefaccion, provincia)/100) 
gasto_CALsinimp = coste_fijoCALreparto*12 + coste_variableCAL*consumo_calefaccion 

# REFRIGERACIÓN
zona_verano = zonaver(provincia, altitud) 
C1_verano = calcula_c1_verano(califE, zona_verano, tipo_vivienda) 
Io_Is_verano = io_is_verano(zona_verano,tipo_vivienda, C1_verano) 
demanda_RefRef = demanda_referenciarefrig(provincia, altitud, tipo_vivienda) 
demanda_CorregidaSignoRef = Io_Is_verano * demanda_RefRef * superficie * ratio_supverano/100 
demanda_CorregidaRef = fdemanda_corregidacal(demanda_CorregidaSignoRef) 
SEER = seer(zona_verano, califE) 
consumo_refrigeracion = demanda_CorregidaRef / SEER 

# ACS

# NO ENTIENDO PQ SE HACE ESTO????????????????????????
B = np.zeros(13)  # creo el vector
B[4:10] = [0.0033] * 6 ## pongo 0.0033 desde la posicion 4, 6 veces (de 4 a 10)
B[1:4] = [0.0066] * 3 # de 1 a 3
B[10:13] = [0.0066] * 3

fila_capital = lookup_row('Temp red ACS',15,provincia) 
elevacion = elevacion(altitud, fila_capital) 

# Temperatura agua red
temperatura_AguaRed = np.zeros(13)

for i in range(1, 13):
    temperatura_AguaRed[i] = lookup_value('Temp red ACS',fila_capital,i+2) - B[i]*elevacion
    
litros_paxACS = litros_acs(tipo_vivienda) 
demanda_ACS = Npax*litros_paxACS*(365/12)*4,176*(12*60-np.sum(temperatura_AguaRed[1:12]))/(3600) 
tabla_ACSspf = tabla_acsspf(califE) 
fila_ACS_SPF = lookup_row(tabla_ACSspf,'sistema',tipo_ACS) 
ACS_SPF = lookup_value(tabla_ACSspf, fila_ACS_SPF, inst_ACS) 
consumo_ACS = demanda_ACS / ACS_SPF 
consumo_gnACS = consumo_gas(tipo_calefaccion, tipo_acs, consumo_calefaccion, consumo_acs, inst_calefaccion, inst_ACS, 'ACS') 
coste_fijoACS = tarifa_suministro(inst_acs, tipo_acs, consumo_gnACS, 'fijo', provincia, zona_invierno, pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
coste_fijoACSreparto = coste_fijoacsreparto(inst_acs, tipo_acs, inst_calefaccion, tipo_calefaccion, coste_fijoACS) 
coste_variableACS = tarifa_suministro(inst_acs, tipo_acs, consumo_gnACS, 'variable', provincia, zona_invierno, pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
alquiler_equiposACS = alquiler_equiposacs(tipo_acs, inst_acs) 
impuesto_gasACS = impuesto_gas(tipo_acs) 
impuesto_electricidadACS = impuesto_electricidad(tipo_acs) 
gasto_ACS = (coste_fijoACSreparto*12 + coste_variableACS*consumo_ACS + alquiler_equiposACS*12 + impuesto_gasACS*consumo_ACS + impuesto_electricidadACS*coste_variableACS*consumo_ACS)*(1+factor_ivaacs(tipo_acs, provincia)/100) 
gasto_ACSsinimp = coste_fijoACSreparto*12 + coste_variableACS*consumo_ACS 

# ELECTRICIDAD

pot_contratada_punta_sinREF = potencia_poromision(Npax, tipo_calefaccion, 'punta') 
pot_contratada_valle_sinREF = potencia_poromision(Npax, tipo_calefaccion, 'valle') 
pot_contratada_sinREF = pot_contratada_punta_sinREF 
#potencia normalizada para obtener el coste { energia_electrica = 3363} 

########## ratio supverano ???
if ratio_supverano < 30:
    pot_contratada_punta_conREF0 = 5.0
else:
    pot_contratada_punta_conREF0 = 6.9

pot_contratada_punta_conREF = max(
    pot_contratada_punta_conREF0,
    pot_contratada_punta_sinREF
)


miembros = miembro(Npax) 
energia_electrica = 1.07*(consumo_electrico(cocina, horno, lavadora, secadora, frigorifico, congelador, tv, ordenador, lavavajillas, movil, tablet, microondas, miembros, superficie, Npax, provincia) + factores(ocupado, parado, estudiante, jubilado, incapacitado, viudo, ama, otro, miembros)) 

coste_fijoELECTRICIDAD_sinREF = tarifa_electrica('fijo', pot_contratada_punta_sinREF, pot_contratada_valle_sinREF)*pot_contratada_sinREF 
coste_fijoELECTRICIDAD_conREF = tarifa_electrica('fijo', pot_contratada_punta_conREF, pot_contratada_valle_conREF)*pot_contratada_conREF 
coste_variableELECTRICIDAD = tarifa_electrica('variable', pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
impuesto_electricidadELEC = lookup_value('impuestos',2,'impuesto')/100 
alquiler_equiposELECTRICIDAD = lookup_value('alquiler equipos',2,'coste') #€/mes
gasto_ELEC_noTERMICO_sinREF = ( (coste_fijoELECTRICIDAD_sinREF*12 + coste_variableELECTRICIDAD*energia_electrica)*(1+impuesto_electricidadELEC))*(1+factor_ivaelectricidad_noconta(provincia)/100) + alquiler_equiposELECTRICIDAD*12*(1+factor_ivaelectricidad_conta(provincia)/100) 
gasto_ELEC_noTERMICO_conREF = (((coste_fijoELECTRICIDAD_conREF*12 + coste_variableELECTRICIDAD*energia_electrica)*(1+impuesto_electricidadELEC))*(1+factor_ivaelectricidad_noconta(provincia)/100) + alquiler_equiposELECTRICIDAD*12*(1+factor_ivaelectricidad_conta(provincia)/100))*corrige_zona1(zona_verano) + (1-corrige_zona1(zona_verano))*gasto_ELEC_noTERMICO_sinREF 
gasto_ELEC_TOTAL_sinREF = gasto_ELEC_noTERMICO_sinREF + factor_electricidadacs(tipo_ACS)*gasto_ACS + factor_electricidadcal(tipo_calefaccion)*gasto_CAL 
gasto_ELEC_TOTAL_conREF = gasto_ELEC_noTERMICO_conREF + factor_electricidadacs(tipo_ACS)*gasto_ACS + factor_electricidadcal(tipo_calefaccion)*gasto_CAL + gasto_REFRIGERACION 
coste_variableREFRIG = tarifa_suministroref(zona_verano) 
gasto_REFRIGERACION= coste_variableREFRIG*consumo_refrigeracion*(1+impuesto_electricidadELEC)*(1+factor_ivaelectricidad_noconta(provincia)/100) 
gasto_COMBUSTIBLE = (1 - factor_electricidadacs(tipo_ACS))*gasto_ACS + (1 - factor_electricidadcal(tipo_calefaccion))*gasto_CAL
