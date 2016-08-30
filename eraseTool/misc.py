import arcpy

def printout(msg):
    print msg
    arcpy.AddMessage(msg)

class LicenseError(Exception):
    pass
class ProductError(Exception):
    pass
# check necessary licenses or product level
def checkLicenses(licenses = None, product_lvls = None):
    result = False
    try:
        if licenses:
            for e in licenses:
                if arcpy.CheckExtension(e):
                    arcpy.CheckOutExtension(e)
                    result = True
                else:
                    raise LicenseError

    except LicenseError:
        printout('ERROR:Some of these'+str(licenses) +'licenses are unavailable!')
    try:
        if product_lvls:
            if arcpy.ProductInfo() not in product_lvls:
                raise ProductError
            else:
                result = True
    except ProductError:
        printout('ERROR:You have inappropriate ArcGIS product level!')
    return result

def newFileName(path, currnm):
    import os
    result = path+'/'+currnm
    if os.path.isfile(result):
        i = 0
        fn, fe = os.path.splitext(currnm)
        while os.path.isfile(result):
            i += 1
            result = path + '/'+fn+str(i)+fe
    return result

# create folders (int, res, orig)
def create_folder(data_path):
    import os
    printout('Creation of the folders in '+data_path)
    if not os.path.exists(data_path):
        try:
            os.makedirs(data_path)
        except:
            printout('CANNOT BE CREATED: ' + data_path)