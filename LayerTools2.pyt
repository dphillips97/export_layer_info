import arcpy
import os
import csv


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Layer Tools"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ListLayerSource]


class ListLayerSource(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Layer Info"
        self.description = "This tool generates a csv with info for all layers in the current (open) map document. It will not list group layers."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First Parameter
        out_path = arcpy.Parameter(
            displayName = "Output Path",
            name = "out_path",
            datatype = "DEFolder",
            parameterType = "Required",
            direction = "Input")
            
        # Second Parameter
        csv_name = arcpy.Parameter(
            displayName = "Name of csv without \".csv\"",
            name = "csv_name",
            datatype = "GPString",
            parameterType = "Required",
            direction = "Input")
        
        params = [out_path, csv_name]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        # eat shit, esri
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        out_path = parameters[0].valueAsText
        csv_name = parameters[1].valueAsText
        
        #set mxd to current/active mxd
        mxd = arcpy.mapping.MapDocument("CURRENT")

        #format output name and filepath
        out_path = os.path.join(out_path, csv_name + ".csv")

        with open(out_path, 'wb') as f:

            #create writer object
            writer = csv.writer(f)
            
            #create header rows and write to file
            header = ['Path', 'Name', 'Data_Type', 'Coord_Sys', 'Data_Frame']
            writer.writerow(header)
            
            # loop thru df to get df name
            for df in arcpy.mapping.ListDataFrames(mxd):
                #loop thru layers in df
                for layer in arcpy.mapping.ListLayers(mxd, '', df):
                    # Create empty list
                    layer_info = []
                    
                    try:
                        # Get layer info
                        desc = arcpy.Describe(layer)   
                        
                        # Append each feature to list
                        layer_info.append(desc.catalogPath)
                        layer_info.append(desc.name)
                        
                        try:
                            layer_info.append(desc.dataType)
                        except:
                            layer_info.append('other data type')
                        
                        layer_info.append(desc.spatialReference.name)
                        layer_info.append(df.name)
                        
                        # Write to csv
                        writer.writerow(layer_info)
                    except:
                        arcpy.AddWarning("Couldn't get info for: \"{0}\"".format(layer))
                        continue
        return
