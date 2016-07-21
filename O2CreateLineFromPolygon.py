__author__ = 'abykov'

import arcpy

def createPolylineFromXY(xy_coordinates, result_name, spatial_reference = None):
    import os

    featureList = []

    if arcpy.Exists(result_name):
        arcpy.Delete_management(result_name)

    if spatial_reference is not None:
            arcpy.CreateFeatureclass_management(
            os.path.dirname(result_name),
            os.path.basename(result_name),
            "POLYLINE",
            #template =
            '',
            #has_m =
            'DISABLED',
            #has_z =
            'DISABLED',
            spatial_reference
            )
    else:
        arcpy.CreateFeatureclass_management(
            os.path.dirname(result_name),
            os.path.basename(result_name),
            "POLYLINE")

    featureList = []
    cursor = arcpy.InsertCursor(result_name)
    feat = cursor.newRow()
    point = arcpy.Point()
    array = arcpy.Array()

    for index in range(len(xy_coordinates)-1):
        print str(index) + ', ' + str(index+1)
        print xy_coordinates[index], xy_coordinates[index+1]

        point.X = xy_coordinates[index][0]
        point.Y = xy_coordinates[index][1]
        array.add(point)
        point.X = xy_coordinates[index+1][0]
        point.Y = xy_coordinates[index+1][1]
        array.add(point)
        # Create a Polyline object based on the array of points
        polyline = arcpy.Polyline(array)
        # Clear the array for future use
        array.removeAll()
        # Append to the list of Polyline objects
        featureList.append(polyline)
        # Insert the feature
        feat.shape = polyline
        cursor.insertRow(feat)
    del feat
    del cursor

def createPolylineFromPolygon(in_fc, out_fc):
    xy_coordinates = []

    spatialReference = arcpy.Describe(in_fc).spatialReference

    for feature in arcpy.da.SearchCursor(in_fc,["OID@" ,"SHAPE@", "SHAPE@WKT"]):
        #print 'f: '+ str(feature[0])
        #print 's: '+ str(feature[2])
        for vertices in feature[1]:
            for vertex in vertices:
                #print str(vertex).split(" ")[0:2]
                xy_coordinates.append(str(vertex).split(" ")[0:2])

    createPolylineFromXY(xy_coordinates, out_fc, spatialReference)

def main(in_fc, out_fc):
    createPolylineFromPolygon(in_fc, out_fc)

in_fc = r'D:\TEMP\testSquare.shp'
out_fc = r"D:\TEMP\CCTemp.gdb\testSquareLines"
main(in_fc, out_fc)