__author__ = 'abykov'

def getPercentOf2FCIntersections (fc1, buildings, int_area_field_name = '', int_perc_field_name = '', field4classes = '', classes2intersect = []):
    import arcpy

    #add default locations
    #add area calculation 2 original dataset

    import myhelpers

   #will add attribute POLY_AREA with area in SquareMeters
    area_field_name = 'POLY_AREA'
    arcpy.AddGeometryAttributes_management(
        Input_Features=fc1
        , Geometry_Properties="AREA"
        , Length_Unit=""
        , Area_Unit="SQUARE_METERS"
        , Coordinate_System="")

    #add intersection
    fc_intersected = myhelpers.getNewFilePathWithDateNoSpaces(fc1)
    fc_intersected2 = myhelpers.getNewFilePathWithDateNoSpaces(fc_intersected)

    arcpy.Intersect_analysis(
        in_features=[fc1, buildings]
        , out_feature_class = fc_intersected
        , join_attributes="ALL"
        , cluster_tolerance="-1 Unknown"
        , output_type="INPUT"
    )

    join_fieldName_in_intersected = arcpy.ListFields(fc_intersected)[2].name

    arcpy.Dissolve_management(
        in_features=fc_intersected
        , out_feature_class=fc_intersected2
        , dissolve_field=join_fieldName_in_intersected
        , statistics_fields=""
        , multi_part="MULTI_PART"
        , unsplit_lines="UNSPLIT_LINES"
    )

    #add area calculation 2 intersection
    arcpy.AddGeometryAttributes_management(
        Input_Features=fc_intersected2
        , Geometry_Properties="AREA"
        , Length_Unit=""
        , Area_Unit="SQUARE_METERS"
        , Coordinate_System="")

    #todo with classes and class field
    if field4classes == '' and classes2intersect == []:
        pass
    else:
        print 'NOT IMPLEMENTED YET!'

    #rename area of intersection area fieldname
    if int_area_field_name <> '':
        field_name_4area = int_area_field_name
    else:
        field_name_4area = 'int_area'

    myhelpers.renameField(fc_intersected2, area_field_name, field_name_4area)

    #delete filed if exists
    if myhelpers.fieldExist(fc1, field_name_4area):
       arcpy.DeleteField_management(fc1, [field_name_4area])

    #join class and area
    arcpy.JoinField_management(
        in_data=fc1
        , in_field="FID"
        , join_table=fc_intersected2
        , join_field=join_fieldName_in_intersected
        , fields=field_name_4area
    )

    if int_perc_field_name <> '':
        perc_field_name = int_perc_field_name
    else:
        perc_field_name = 'int_perc'
    #calculate ratio\percent
    myhelpers.addNewField(fc1, "Double", perc_field_name, 20)
    arcpy.CalculateField_management(fc1, perc_field_name, "(!"+field_name_4area+"!*100)/!"+area_field_name+'!', "PYTHON_9.3")

    #add field selection with classes
    #add classes list
    pass

#example
#import fileLocations
#getPercentOf2FCIntersections(fileLocations.edm_feature1, fileLocations.edm_feature2)