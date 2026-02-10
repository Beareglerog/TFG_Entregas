from model import *
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
coste_fijoCAL = tarifa_suministro(inst_calefaccion$; tipo_calefaccion$; consumo_gnCAL; 'fijo'; provincia$; zona_invierno$; pot_contratada_punta_sinREF; pot_contratada_valle_sinREF) 
coste_fijoCALreparto = coste_fijocalreparto(tipo_calefaccion, inst_calefaccion, coste_fijoCAL) 
coste_variableCAL = tarifa_suministro(inst_calefaccion, tipo_calefaccion, consumo_gnCAL; 'variable', provincia, zona_invierno, pot_contratada_punta_sinREF, pot_contratada_valle_sinREF) 
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
