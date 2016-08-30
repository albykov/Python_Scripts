#todo: add intermediate folder to all functions
import mergeDatasetsSimple as ms
import arcpy
import percentOfIntersection, myhelpers


perc_buildings_2be_OS = 50
is_overlapping = True

def_output_folder = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160704\res0837'
myhelpers.createNewFolder(r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160704')
myhelpers.createNewFolder(def_output_folder)

rooflines = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\rooflinesDiss.shp'
edm_parkland = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\GED_Parkland_o2upd.shp'
edm_vacantcityland = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\VacantCityLand_o2upd.shp'
edm_turf = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\TURF_o2upd.shp'
edm_jointuseareas = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\JointUseAreas_o2upd.shp'
edm_naturalareas = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\GED_NaturalAreas_o2upd.shp'
edm_yards = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\yards_o2fix.shp'
#downtown OS
edm_dtos = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\dt_OS_o2upd.shp'

#non parks facility areas
edm_npfa = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\nonParksCityFacArea_o2upd.shp'
edm_cityHoldings = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\cityHoldings_o2upd.shp'
edm_pmaint = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\parks_maint_sites_o2upd.shp'
edm_pparks = r'\\10.100.1.135\d$\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\prov_parks.shp'

#drainage stormwater mf
edm_dswm = r'\\10.100.1.135\d$\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\drainageStormwaterManagements_o2.shp'
edm_pulrow = r'\\10.100.1.135\d$\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\PUL_and_ROW_o2.shp'

e_picnic = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\picnicsites_o2upd.shp'
e_campuses = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\campuses_o2upd.shp'
e_sportfields = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\sfields_o2upd.shp'
e_pgrounds = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\playgrounds_o2upd.shp'
#dog offleash areas
e_dofa = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\e_dogofareas_o2upd.shp'
e_ssites = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\schoolS_o2upd.shp'

###PARKLAND
fields_schema_parkland = {}
fields_schema_parkland['NAME'] = ''
fields_schema_parkland['OWNERSHIP'] = 'OWNERSHIP2'
fields_schema_parkland['CLASS'] = 'CLASS'
fields_schema_parkland['TYPE'] = 'TYPE'
# fields_schema_parkland['P_BUILD'] = 'P_BUILD'
fields_schema_parkland['MAINTAINER'] = ''
fields_schema_parkland['PACCESS'] = 'PACCESS'

edm_parkland_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_parkland, def_output_folder)
arcpy.Copy_management(edm_parkland, edm_parkland_copy)

myhelpers.addNewField(edm_parkland_copy, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
fromds = myhelpers.getFileNameWithNoExtentionAndPath(edm_parkland)
arcpy.CalculateField_management(edm_parkland_copy, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")

myhelpers.addNewField(edm_parkland_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_parkland_copy, 'PACCESS', "'YES'", "PYTHON_9.3")



###CHOLDINGS
#edm_cityHoldings
fields_schema_ch = {}
fields_schema_ch['OWNERSHIP'] = 'OWNERSHIP2'
fields_schema_ch['TYPE'] = 'TYPE'
fields_schema_ch['NAME'] = 'HOLDING_SU'
# fields_schema_ch['P_BUILD'] = 'P_BUILD'
fields_schema_ch['PACCESS'] = 'PACCESS'

edm_cityHoldings_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_cityHoldings, def_output_folder)
arcpy.Copy_management(edm_cityHoldings, edm_cityHoldings_copy)

myhelpers.addNewField(edm_cityHoldings_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
myhelpers.addNewField(edm_cityHoldings_copy,
                      "TEXT"
                      , "PACCESS"
                      , 10
                      , field_precision = None
                      , field_alias = None
                      , field_scale = None
                      , field_is_nullable = None
                      , field_is_required = None
                      , toOverwrite = True)

myhelpers.addNewField(edm_cityHoldings_copy,
                      "TEXT"
                      , "holdsu_c"
                      , 50
                      , field_precision = None
                      , field_alias = None
                      , field_scale = None
                      , field_is_nullable = None
                      , field_is_required = None
                      , toOverwrite = True)

myhelpers.addNewField(edm_cityHoldings_copy,
                      "TEXT"
                      , "rec_p_cap"
                      , 50
                      , field_precision = None
                      , field_alias = None
                      , field_scale = None
                      , field_is_nullable = None
                      , field_is_required = None
                      , toOverwrite = True)

myhelpers.addNewField(edm_cityHoldings_copy,
                      "TEXT"
                      , "aq_p_cap"
                      , 50
                      , field_precision = None
                      , field_alias = None
                      , field_scale = None
                      , field_is_nullable = None
                      , field_is_required = None
                      , toOverwrite = True)

arcpy.CalculateField_management(in_table=edm_cityHoldings_copy
                                , field="holdsu_c"
                                , expression="!HOLDING_SU!.upper()"
                                , expression_type="PYTHON_9.3"
                                , code_block="")

arcpy.CalculateField_management(in_table=edm_cityHoldings_copy
                                , field="rec_p_cap"
                                , expression="!REQUIRED_P!.upper()"
                                , expression_type="PYTHON_9.3"
                                , code_block="")

arcpy.CalculateField_management(in_table=edm_cityHoldings_copy
                                , field="aq_p_cap"
                                , expression="!ACQUIRED_P!.upper()"
                                , expression_type="PYTHON_9.3"
                                , code_block="")

arcpy.MakeFeatureLayer_management (edm_cityHoldings_copy, "edm_cityHoldings_copy")
arcpy.CalculateField_management("edm_cityHoldings_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
search_q = ''
search_q = "\"holdsu_c\" like '%PARK%' or \"rec_p_cap\" like '%PARK%' or \"aq_p_cap\" like '%PARK%'"
print search_q
arcpy.SelectLayerByAttribute_management ("edm_cityHoldings_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_cityHoldings_copy", 'TYPE', "'PARK'", "PYTHON_9.3")


search_q = "\"holdsu_c\" not like '%PARK%' and \"rec_p_cap\" not like '%PARK%' and \"aq_p_cap\" not like '%PARK%' "
print search_q
arcpy.SelectLayerByAttribute_management ("edm_cityHoldings_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_cityHoldings_copy", 'TYPE', "'POTENTIAL OS'", "PYTHON_9.3")
#im not sure how to define ownership of this layer rather than YES coz it is a city's land
#arcpy.CalculateField_management("edm_cityHoldings_copy", 'PACCESS', "'UNKNOWN'", "PYTHON_9.3")

result = ms.mergeDS(edm_parkland, edm_cityHoldings_copy
                    , def_output_folder + "\\" + "p_ch.shp"
                    , fields_schema_parkland, fields_schema_ch, False)



#DRAINAGE STORM WATER FEATURES
fields_schema_dswm = {}
fields_schema_dswm['NAME'] = 'NAME'
fields_schema_dswm['OWNERSHIP'] = 'OWNERSHIP'
fields_schema_dswm['TYPE'] = 'TYPE'
# fields_schema_parkland['P_BUILD'] = 'P_BUILD'
fields_schema_dswm['PACCESS'] = 'PACCESS'

edm_dswm_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_dswm, def_output_folder)
arcpy.Copy_management(edm_dswm, edm_dswm_copy)

myhelpers.addNewField(edm_dswm_copy, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
fromds = myhelpers.getFileNameWithNoExtentionAndPath(edm_dswm)
arcpy.CalculateField_management(edm_dswm_copy, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")

myhelpers.addNewField(edm_dswm_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_dswm_copy, 'PACCESS', "'YES'", "PYTHON_9.3")

myhelpers.addNewField(edm_dswm_copy, 'TEXT', 'TYPE', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_dswm_copy, 'TYPE', "'OS'", "PYTHON_9.3")
result = ms.mergeDS(result, edm_dswm_copy
                    , def_output_folder + "\\" + 'p_ch_pp_dswm.shp'
                    , {}, fields_schema_dswm, False)



#PUBLIC UTILITY LOTS and RIGHT OF WAYS
fields_schema_pulrow = {}
fields_schema_pulrow['NAME'] = 'NAME'
fields_schema_pulrow['OWNERSHIP'] = 'OWNERSHIP'
fields_schema_pulrow['TYPE'] = 'TYPE'
# fields_schema_pulrow['P_BUILD'] = 'P_BUILD'
fields_schema_pulrow['PACCESS'] = 'PACCESS'

edm_pulrow_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_pulrow, def_output_folder)
arcpy.Copy_management(edm_pulrow, edm_pulrow_copy)

myhelpers.addNewField(edm_pulrow_copy, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
fromds = myhelpers.getFileNameWithNoExtentionAndPath(edm_pulrow_copy)
arcpy.CalculateField_management(edm_dswm_copy, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")

myhelpers.addNewField(edm_dswm_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_dswm_copy, 'PACCESS', "'YES'", "PYTHON_9.3")

myhelpers.addNewField(edm_pulrow_copy, 'TEXT', 'TYPE', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_pulrow_copy, 'TYPE', "'OS'", "PYTHON_9.3")
result = ms.mergeDS(result, edm_dswm_copy
                    , def_output_folder + "\\" + 'p_ch_pp_pulrow.shp'
                    , {}, fields_schema_dswm, False)

###PROVINCIAL PARKS
fields_schema_pparks = {}
fields_schema_pparks['NAME'] = 'PARK_NAME'
fields_schema_pparks['OWNERSHIP'] = 'OWNERSHIP'
fields_schema_pparks['TYPE'] = 'TYPE'
# fields_schema_parkland['P_BUILD'] = 'P_BUILD'
fields_schema_pparks['PACCESS'] = 'PACCESS'

edm_pparks_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_pparks, def_output_folder)
arcpy.Copy_management(edm_pparks, edm_pparks_copy)

myhelpers.addNewField(edm_pparks_copy, 'TEXT', 'FROMDS', '50', None, None, None, None, None, True)
fromds = myhelpers.getFileNameWithNoExtentionAndPath(edm_pparks)
arcpy.CalculateField_management(edm_pparks_copy, 'FROMDS', "'"+fromds+"'", "PYTHON_9.3")

myhelpers.addNewField(edm_pparks_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_pparks_copy, 'PACCESS', "'YES'", "PYTHON_9.3")

myhelpers.addNewField(edm_pparks_copy, 'TEXT', 'OWNERSHIP', '50', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_pparks_copy, 'OWNERSHIP', "'Province of Alberta'", "PYTHON_9.3")

myhelpers.addNewField(edm_pparks_copy, 'TEXT', 'TYPE', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_pparks_copy, 'TYPE', "'PARK'", "PYTHON_9.3")
result = ms.mergeDS(result, edm_pparks_copy
                    , def_output_folder + "\\" + 'p_ch_pp.shp'
                    , {}, fields_schema_pparks, False)



###JU AREAS
#JOINTUSEAREAS
fields_schema_juareas = {}
fields_schema_juareas['NAME'] = 'OFFICIAL_N'
fields_schema_juareas['NAME2'] = 'COMMON_NAM'
fields_schema_juareas['OWNERSHIP'] = 'OWNER'
fields_schema_juareas['MAINTAINER'] = 'MAINTAINER'
fields_schema_juareas['CLASS'] = ''
fields_schema_juareas['TYPE'] = 'TYPE'
fields_schema_juareas['PACCESS'] = 'PACCESS'
# fields_schema_juareas['P_BUILD'] = 'P_BUILD'

edm_jointuseareas_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_jointuseareas, def_output_folder)
arcpy.Copy_management(edm_jointuseareas, edm_jointuseareas_copy)

myhelpers.addNewField(edm_jointuseareas_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_jointuseareas_copy, 'PACCESS', "'YES'", "PYTHON_9.3")

myhelpers.addNewField(edm_jointuseareas_copy, 'TEXT', 'MAINTAINER', '50', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_jointuseareas_copy, 'MAINTAINER', "'PARKS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_jointuseareas_copy
                    , def_output_folder + "\\" + 'p_ch_jua.shp'
                    , {}, fields_schema_juareas, False)



###PARKS MAINT
#edm_pmaint
fields_schema_pmaint = {}
fields_schema_pmaint['OWNERSHIP'] = 'OWNER'
fields_schema_pmaint['MAINTAINER'] = 'MAINTAINER'
fields_schema_pmaint['TYPE'] = 'TYPE2'
fields_schema_pmaint['NAME'] = 'NAME'
# fields_schema_pmaint['P_BUILD'] = 'P_BUILD'
fields_schema_pmaint['PACCESS'] = 'PACCESS'

edm_pmaint_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_pmaint, def_output_folder)
arcpy.Copy_management(edm_pmaint, edm_pmaint_copy)

myhelpers.addNewField(edm_pmaint_copy, 'TEXT', 'NAME_CAP', '100', None, None, None, None, None, True)

arcpy.CalculateField_management(in_table=edm_pmaint_copy
                                , field="NAME_CAP"
                                , expression="!NAME!.upper()"
                                , expression_type="PYTHON_9.3"
                                , code_block="")

myhelpers.addNewField(edm_pmaint_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (edm_pmaint_copy, "edm_pmaint_copy")

search_q = "\"OWNER\" NOT IN ('Developer' , 'Fire Department' , 'Homeowners Association' , 'Police' , 'Private' , 'Unknown' , 'Waste Management')" #+ ' AND "P_BUILD" < '+str(perc_buildings_2be_OS)
arcpy.SelectLayerByAttribute_management ("edm_pmaint_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_pmaint_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

search_q = "\"OWNER\" IN ('Developer' , 'Fire Department' , 'Homeowners Association' , 'Police' , 'Private' , 'Unknown' , 'Waste Management')"
arcpy.SelectLayerByAttribute_management ("edm_pmaint_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_pmaint_copy", 'PACCESS', "'NO'", "PYTHON_9.3")

myhelpers.addNewField(edm_pmaint_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)

search_q = "\"NAME_CAP\" NOT LIKE '%PARK%' AND \"PACCESS\" = 'YES'"# AND \"P_BUILD\" " #+" < "+str(perc_buildings_2be_OS)
arcpy.SelectLayerByAttribute_management ("edm_pmaint_copy", "NEW_SELECTION", search_q)
print search_q
arcpy.CalculateField_management("edm_pmaint_copy", 'TYPE2', "'POTENTIAL OS'", "PYTHON_9.3")

search_q = "\"name_CAP\" LIKE '%PARK%' AND \"name_CAP\" NOT LIKE '%PARKING%'"
arcpy.SelectLayerByAttribute_management ("edm_pmaint_copy", "NEW_SELECTION", search_q)
print search_q
arcpy.CalculateField_management("edm_pmaint_copy", 'TYPE2', "'PARK'", "PYTHON_9.3")

search_q = "\"NAME_CAP\" NOT LIKE '%PARK%' AND \"PACCESS\" <> 'YES'"# OR \"P_BUILD\" " #+" >= "+str(perc_buildings_2be_OS) + ")"
arcpy.SelectLayerByAttribute_management ("edm_pmaint_copy", "NEW_SELECTION", search_q)
print search_q
arcpy.CalculateField_management("edm_pmaint_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_pmaint_copy
                    , def_output_folder + "\\" + 'p_ch_jua_pm.shp'
                    , {}, fields_schema_pmaint, False)



###DT OS
fields_schema_dtos = {}
fields_schema_dtos['OWNERSHIP'] = 'OWNER'
fields_schema_dtos['MAINTAINER'] = 'MAINTAINER'
fields_schema_dtos['TYPE'] = 'TYPE2'
fields_schema_dtos['NAME'] = 'NAME'
#fields_schema_dtos['P_BUILD'] = 'P_BUILD'
fields_schema_dtos['PACCESS'] = 'PACCESS'

edm_dtos_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_dtos, def_output_folder)
arcpy.Copy_management(edm_dtos, edm_dtos_copy)

myhelpers.addNewField(edm_dtos_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.CalculateField_management(edm_dtos_copy, 'PACCESS', "'YES'", "PYTHON_9.3")

arcpy.MakeFeatureLayer_management (edm_dtos_copy, "edm_dtos_copy")
myhelpers.addNewField("edm_dtos_copy", 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)
search_q = "\"NAME\" LIKE '%PARK%'"
arcpy.SelectLayerByAttribute_management ("edm_dtos_copy", "NEW_SELECTION", search_q)
print search_q
arcpy.CalculateField_management("edm_dtos_copy", 'TYPE2', "'PARK'", "PYTHON_9.3")

search_q = "\"NAME\" NOT LIKE '%PARK%'"
arcpy.SelectLayerByAttribute_management ("edm_dtos_copy", "NEW_SELECTION", search_q)
print search_q
arcpy.CalculateField_management("edm_dtos_copy", 'TYPE2', "'OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_dtos_copy
                    , def_output_folder + "\\" + 'p_ch_jua_pm_dtos.shp'
                    , {}, fields_schema_dtos, False)



#VACANTCITYLAND
fields_schema_vacantcityland = {}
fields_schema_vacantcityland['NAME'] = 'NAME'
fields_schema_vacantcityland['OWNERSHIP'] = 'OWNER'
fields_schema_vacantcityland['MAINTAINER'] = 'MAINTAINER'
fields_schema_vacantcityland['CLASS'] = ''
fields_schema_vacantcityland['TYPE'] = 'TYPE'
#fields_schema_vacantcityland['P_BUILD'] = 'P_BUILD'
fields_schema_vacantcityland['PACCESS'] = 'PACCESS'

edm_vacantcityland_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_vacantcityland, def_output_folder)
arcpy.Copy_management(edm_vacantcityland, edm_vacantcityland_copy)

myhelpers.addNewField(edm_vacantcityland_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)

if not myhelpers.fieldExist(edm_vacantcityland_copy, 'TYPE'):
    myhelpers.addNewField(edm_vacantcityland_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
    arcpy.MakeFeatureLayer_management (edm_vacantcityland_copy, "edm_vacantcityland_copy")
    arcpy.CalculateField_management("edm_vacantcityland_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
    arcpy.CalculateField_management("edm_vacantcityland_copy", 'TYPE', "'POTENTIAL OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_vacantcityland_copy
                    , def_output_folder + "\\" + 'p_ch_jua_pm_dtos_vcl.shp'
                    , {}, fields_schema_vacantcityland, False)#, True)



###TURF
fields_schema_turf = {}
fields_schema_turf['NAME'] = ''
fields_schema_turf['OWNERSHIP'] = 'OWNER'
fields_schema_turf['MAINTAINER'] = 'MAINTAINER'
fields_schema_turf['CLASS'] = 'SERVICE_LE'
fields_schema_turf['TYPE'] = 'TYPE2'
#fields_schema_turf['P_BUILD'] = 'P_BUILD'
fields_schema_turf['PACCESS'] = 'PACCESS'

edm_turf_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_turf, def_output_folder)
arcpy.Copy_management(edm_turf, edm_turf_copy)
if not myhelpers.fieldExist(edm_turf_copy, 'P_BUILD'):
    percentOfIntersection.getPercentOf2FCIntersections(edm_turf_copy, rooflines, False, '', 'A_BUILD', 'P_BUILD')

myhelpers.addNewField(edm_turf_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)
myhelpers.addNewField(edm_turf_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (edm_turf_copy, "edm_turf_copy")
search_q = "\"OWNER\" IN( 'Homeowners Association')"
arcpy.SelectLayerByAttribute_management ("edm_turf_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_turf_copy", 'PACCESS', "'NO'", "PYTHON_9.3")

search_q = "\"OWNER\" NOT IN( 'Homeowners Association')"
arcpy.SelectLayerByAttribute_management ("edm_turf_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_turf_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

arcpy.SelectLayerByAttribute_management ("edm_turf_copy", "NEW_SELECTION", "\"PACCESS\" <> 'YES' OR \"P_BUILD\" >= "+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_turf_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")
arcpy.SelectLayerByAttribute_management ("edm_turf_copy", "NEW_SELECTION", "\"PACCESS\" = 'YES' AND \"P_BUILD\" < "+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_turf_copy", 'TYPE2', "'POTENTIAL OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_turf_copy
                    , def_output_folder + "\\" + 'p_ch_jua_pm_dtos_vcl_t.shp'
                    , {}, fields_schema_turf, False)



#NATURAL AREAS
fields_schema_naturalareas = {}
fields_schema_naturalareas['NAME'] = 'NAME'
fields_schema_naturalareas['OWNERSHIP'] = 'OWNER'
fields_schema_naturalareas['MAINTAINER'] = 'MAINTAINER'
fields_schema_naturalareas['CLASS'] = ''
fields_schema_naturalareas['TYPE'] = 'TYPE2'
#fields_schema_naturalareas['NA_TYPE'] = 'TYPE'
fields_schema_naturalareas['P_BUILD'] = 'P_BUILD'
fields_schema_naturalareas['PACCESS'] = 'PACCESS'

edm_naturalareas_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_naturalareas, def_output_folder)
arcpy.Copy_management(edm_naturalareas, edm_naturalareas_copy)

myhelpers.addNewField(edm_naturalareas_copy, 'TEXT', 'PACCESS', '10', None, None, None, None, None, True)
arcpy.MakeFeatureLayer_management (edm_naturalareas_copy, "edm_naturalareas_copy")

search_q = "\"OWNER\" IN('Private' , 'Unknown')"
arcpy.SelectLayerByAttribute_management ("edm_naturalareas_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_naturalareas_copy", 'PACCESS', "'NO'", "PYTHON_9.3")
search_q = "\"OWNER\" NOT IN( 'Private' , 'Unknown' )"
arcpy.SelectLayerByAttribute_management ("edm_naturalareas_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_naturalareas_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

myhelpers.addNewField(edm_naturalareas_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)
arcpy.SelectLayerByAttribute_management ("edm_naturalareas_copy", "NEW_SELECTION", "\"PACCESS\" <> 'YES' ") #+" OR \"P_BUILD\" >="+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_naturalareas_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")
arcpy.SelectLayerByAttribute_management ("edm_naturalareas_copy", "NEW_SELECTION", "\"PACCESS\" = 'YES' ") #+" AND \"P_BUILD\" <"+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_naturalareas_copy", 'TYPE2', "'POTENTIAL OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_naturalareas_copy
                    , def_output_folder + "\\" + 'p_ch_jua_pm_dtos_vcl_t_na.shp'
                    , {}, fields_schema_naturalareas, False)




###NONPARKSFA
fields_schema_npfa = {}
fields_schema_npfa['OWNERSHIP'] = 'OWNER'
fields_schema_npfa['MAINTAINER'] = 'MAINTAINER'
fields_schema_npfa['TYPE'] = 'TYPE2'
fields_schema_npfa['NAME'] = 'NAME'
fields_schema_npfa['P_BUILD'] = 'P_BUILD'
fields_schema_npfa['PACCESS'] = 'PACCESS'

edm_npfa_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_npfa, def_output_folder)
arcpy.Copy_management(edm_npfa, edm_npfa_copy)
percentOfIntersection.getPercentOf2FCIntersections(edm_npfa_copy, rooflines, False, '', 'A_BUILD', 'P_BUILD')

myhelpers.addNewField(edm_npfa_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)
myhelpers.addNewField(edm_npfa_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (edm_npfa_copy, "edm_npfa_copy")
search_q = "\"OWNER\" IN( 'Fire Department')"
arcpy.SelectLayerByAttribute_management ("edm_npfa_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_npfa_copy", 'PACCESS', "'NO'", "PYTHON_9.3")
search_q = "\"OWNER\" NOT IN( 'Fire Department')"
arcpy.SelectLayerByAttribute_management ("edm_npfa_copy", "NEW_SELECTION", search_q)
arcpy.CalculateField_management("edm_npfa_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

arcpy.SelectLayerByAttribute_management ("edm_npfa_copy", "NEW_SELECTION", "\"PACCESS\" <> 'YES' OR \"P_BUILD\" >="+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_npfa_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")
arcpy.SelectLayerByAttribute_management ("edm_npfa_copy", "NEW_SELECTION", "\"PACCESS\" = 'YES' AND \"P_BUILD\" <"+str(perc_buildings_2be_OS))
arcpy.CalculateField_management("edm_npfa_copy", 'TYPE2', "'POTENTIAL OS'", "PYTHON_9.3")

result = ms.mergeDS(result, edm_npfa_copy
                     , def_output_folder + "\\" + 'p_ch_jua_pm_dtos_vcl_t_na_npfa.shp'
                    , {}, fields_schema_npfa, False)


###YARDS - No Access!!!!!!!!!!!
#todo# here
#YARDS
# fields_schema_yards = {}
# fields_schema_yards['OWNERSHIP'] = 'OWNER'
# fields_schema_yards['MAINTAINER'] = 'MAINTAINER'
# fields_schema_yards['TYPE'] = 'TYPE2'
# fields_schema_yards['P_BUILD'] = 'P_BUILD'
# fields_schema_npfa['PACCESS'] = 'PACCESS'
#
# edm_yards_copy = myhelpers.getNewFilePathWithDateNoSpaces(edm_yards, def_output_folder)
# arcpy.Copy_management(edm_yards, edm_yards_copy)
# if not myhelpers.fieldExist(edm_yards_copy, 'P_BUILD'):
#     percentOfIntersection.getPercentOf2FCIntersections(edm_yards_copy, rooflines, False, '', 'A_BUILD', 'P_BUILD')
#
# #adding TYPE TO YARdS
# if not myhelpers.fieldExist(edm_yards_copy, 'TYPE2'):
#     myhelpers.addNewField(edm_yards_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)
#     arcpy.MakeFeatureLayer_management (edm_yards_copy, "edm_yards_copy")
#     arcpy.SelectLayerByAttribute_management ("edm_yards_copy", "NEW_SELECTION", '"P_BUILD" >= '+str(perc_buildings_2be_OS))
#     arcpy.CalculateField_management("edm_yards_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")
#     arcpy.SelectLayerByAttribute_management ("edm_yards_copy", "NEW_SELECTION", '"P_BUILD" < '+str(perc_buildings_2be_OS))
#     arcpy.CalculateField_management("edm_yards_copy", 'TYPE2', "'POTENTIAL OS'", "PYTHON_9.3")
#
# result = ms.mergeDS(result, edm_yards_copy
#                      , r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_161617\res160624\m5.shp'
#                      # myhelpers.getNewFilePathWithDateNoSpacesWithFixes
#                      #    (edm_yards_copy
#                      #    ,myhelpers.getFileNameWithNoExtentionAndPath(result)+"_m_"
#                      #    ,None)
#                     , {}, fields_schema_yards, False)
#print 'parkland+vacantland+turf+natareas+jointuse+yards', result



###PICNIC
fields_schema_picnic = {}
fields_schema_pmaint['OWNERSHIP'] = 'OWNER'
fields_schema_picnic['MAINTAINER'] = 'MAINTAINER'
fields_schema_picnic['TYPE'] = 'TYPE'
fields_schema_picnic['NAME'] = 'NAME'
fields_schema_picnic['PACCESS'] = 'PACCESS'
#fields_schema_picnic['P_BUILD'] = 'P_BUILD'

e_picnic_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_picnic, def_output_folder)
arcpy.Copy_management(e_picnic, e_picnic_copy)

myhelpers.addNewField(e_picnic_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)

if not myhelpers.fieldExist(e_picnic_copy, 'TYPE'):
    myhelpers.addNewField(e_picnic_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
if not myhelpers.fieldExist(e_picnic_copy, 'NAME'):
    myhelpers.addNewField(e_picnic_copy, 'TEXT', 'NAME', 50, None, None, None, None, None, True)
arcpy.MakeFeatureLayer_management (e_picnic_copy, "e_picnic_copy")
arcpy.CalculateField_management("e_picnic_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
arcpy.CalculateField_management("e_picnic_copy", 'NAME', "'PICNIC SITE'", "PYTHON_9.3")
arcpy.CalculateField_management("e_picnic_copy", 'TYPE', "'OS'", "PYTHON_9.3")

result = ms.mergeDS(result, e_picnic_copy
                     , def_output_folder + "\\" + 'picnic.shp'
                    , {}, fields_schema_picnic, False)
print 'e1', result



#e_campuses = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160614\ds\campuses_o2upd.shp'
fields_schema_campus = {}
fields_schema_campus['OWNERSHIP'] = 'OWNER'
fields_schema_campus['TYPE'] = 'TYPE'
fields_schema_campus['NAME'] = 'Desc_'
fields_schema_campus['P_BUILD'] = 'P_BUILD'
fields_schema_campus['PACCESS'] = 'PACCESS'

e_campuses_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_campuses, def_output_folder)
arcpy.Copy_management(e_campuses, e_campuses_copy)

myhelpers.addNewField(e_campuses_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)
if not myhelpers.fieldExist(e_campuses_copy, 'P_BUILD'):
    percentOfIntersection.getPercentOf2FCIntersections(e_campuses_copy, rooflines, False, '', 'A_BUILD', 'P_BUILD')

if not myhelpers.fieldExist(e_campuses_copy, 'TYPE'):
    myhelpers.addNewField(e_campuses_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
arcpy.MakeFeatureLayer_management (e_campuses_copy, "e_campuses_copy")
arcpy.CalculateField_management("e_campuses_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

arcpy.CalculateField_management("e_campuses_copy", 'TYPE', "'POTENTIAL OS'", "PYTHON_9.3")

result = ms.mergeDS(result, e_campuses_copy
                     , def_output_folder + "\\" + 'campuses.shp'
                    , {}, fields_schema_campus, False)
print 'e2', result



#e_pgrounds = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160614\ds\playgrounds_o2upd.shp'
fields_schema_pg = {}
fields_schema_pg['TYPE'] = 'TYPE'
fields_schema_pg['NAME'] = 'NAME'
fields_schema_pg['PACCESS'] = 'PACCESS'
#fields_schema_pg['P_BUILD'] = 'P_BUILD'

e_pgrounds_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_pgrounds, def_output_folder)
arcpy.Copy_management(e_pgrounds, e_pgrounds_copy)

myhelpers.addNewField(e_pgrounds_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_pgrounds_copy, 'TEXT', 'NAME', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_pgrounds_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (e_pgrounds_copy, "e_pgrounds_copy")
arcpy.CalculateField_management("e_pgrounds_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
arcpy.CalculateField_management("e_pgrounds_copy", 'NAME', "'PLAY GROUND'", "PYTHON_9.3")
arcpy.CalculateField_management("e_pgrounds_copy", 'TYPE', "'OS'", "PYTHON_9.3")

result = ms.mergeDS(result, e_pgrounds_copy
                     , def_output_folder + "\\" + 'playgrounds.shp'
                    , {}, fields_schema_pg, False)
print 'e3', result


#DOG OFFLEASH AREAS
#e_dofa = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160614\ds\e_dogofareas_o2upd.shp'
fields_schema_dofa = {}
fields_schema_dofa['TYPE'] = 'TYPE'
fields_schema_dofa['NAME'] = 'NAME'
fields_schema_dofa['PACCESS'] = 'PACCESS'
#fields_schema_dofa['P_BUILD'] = 'P_BUILD'

e_dofa_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_dofa, def_output_folder)
arcpy.Copy_management(e_dofa, e_dofa_copy)

myhelpers.addNewField(e_dofa_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_dofa_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
arcpy.MakeFeatureLayer_management (e_dofa_copy, "e_dofa_copy")
arcpy.CalculateField_management("e_dofa_copy", 'TYPE', "'OS'", "PYTHON_9.3")
arcpy.CalculateField_management("e_dofa_copy", 'PACCESS', "'YES'", "PYTHON_9.3")

result = ms.mergeDS(result, e_dofa_copy
                     , def_output_folder + "\\" + 'dofa.shp'
                    , {}, fields_schema_dofa, False)
print 'e4', result

#e_ssites = r'Shapefile:	D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160614\ds\schoolS_o2upd.shp'
fields_schema_ssites = {}
fields_schema_ssites['TYPE'] = 'TYPE'
fields_schema_ssites['OWNERSHIP'] = 'OWNERSHIP'
fields_schema_ssites['NAME'] = 'NAME'
fields_schema_ssites['PACCESS'] = 'PACCESS'
#fields_schema_ssites['P_BUILD'] = 'P_BUILD'

e_ssites_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_ssites, def_output_folder)
arcpy.Copy_management(e_ssites, e_ssites_copy)

myhelpers.addNewField(e_ssites_copy, 'TEXT', 'TYPE', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_ssites_copy, 'TEXT', 'OWNERSHIP', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_ssites_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (e_ssites_copy, "e_ssites_copy")
arcpy.CalculateField_management("e_ssites_copy", 'OWNERSHIP', "'School Board'", "PYTHON_9.3")
arcpy.CalculateField_management("e_ssites_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
arcpy.CalculateField_management("e_ssites_copy", 'TYPE', "'OS'", "PYTHON_9.3")

result = ms.mergeDS(result, e_ssites_copy
                     , def_output_folder + "\\" + 'ssites.shp'
                    , {}, fields_schema_ssites, False)
print 'e5', result




#e_sportfields = r'D:\abykov\BigProjectFiles\151005 Edmonton Open Space Master Plan\os_160614\ds\sfields_o2upd.shp'
fields_schema_sportf = {}
fields_schema_sportf['SF_Type'] = 'TYPE'
fields_schema_sportf['TYPE'] = 'TYPE2'
fields_schema_sportf['OWNERSHIP'] = 'OWNER'
fields_schema_sportf['NAME'] = 'NAME'
fields_schema_sportf['P_BUILD'] = 'P_BUILD'
fields_schema_sportf['PACCESS'] = 'PACCESS'

e_sportfields_copy = myhelpers.getNewFilePathWithDateNoSpaces(e_sportfields, def_output_folder)
arcpy.Copy_management(e_sportfields, e_sportfields_copy)
if not myhelpers.fieldExist(e_sportfields_copy, 'P_BUILD'):
    percentOfIntersection.getPercentOf2FCIntersections(e_sportfields_copy, rooflines, False, '', 'A_BUILD', 'P_BUILD')

myhelpers.addNewField(e_sportfields_copy, 'TEXT', 'TYPE2', 50, None, None, None, None, None, True)
myhelpers.addNewField(e_sportfields_copy, 'TEXT', 'PACCESS', 50, None, None, None, None, None, True)

arcpy.MakeFeatureLayer_management (e_sportfields_copy, "e_sportfields_copy")
arcpy.SelectLayerByAttribute_management ("e_sportfields_copy", "NEW_SELECTION", "\"OWNER\" IN('Private' , 'University of Alberta' , 'Unknown')")
arcpy.CalculateField_management("e_sportfields_copy", 'PACCESS', "'NO'", "PYTHON_9.3")
arcpy.CalculateField_management("e_sportfields_copy", 'TYPE2', "'NOT OS'", "PYTHON_9.3")
arcpy.SelectLayerByAttribute_management ("e_sportfields_copy", "NEW_SELECTION", "\"OWNER\" NOT IN('Private' , 'University of Alberta' , 'Unknown')")
arcpy.CalculateField_management("e_sportfields_copy", 'PACCESS', "'YES'", "PYTHON_9.3")
arcpy.CalculateField_management("e_sportfields_copy", 'TYPE2', "'OS'", "PYTHON_9.3")

result = ms.mergeDS(result, e_sportfields_copy
                     , def_output_folder + "\\" + 'sfields.shp'
                    , {}, fields_schema_sportf, False)
print 'e6', result

#check perc of buildings to see if there is possible errors
percentOfIntersection.getPercentOf2FCIntersections(result, rooflines, False, '', 'A_BUILD', 'P2_BUILD')

#same names
 #capitalize
 #Open Space -> OS

#layering
#PARK + CEMETERY + OS + POS + NOT OS
