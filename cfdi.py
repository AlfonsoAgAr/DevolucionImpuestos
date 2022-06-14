from xml.dom import minidom
from xml.dom.minidom import Document
from xml.dom.minicompat import NodeList
import json

schema = {
    'General' : ['Total', 'SubTotal', 'Descuento', 'Fecha', 'Serie', 'Sello', 'NoCertificado', 'Certificado'],
    'Emisor' : ['Nombre', 'RegimenFiscal', 'Rfc'],
    'Concepto' : ['ClaveProdServ', 'ClaveUnidad', 'Descripción', 'Cantidad', 'Descuento', 'Importe', 'ValorUnitario'],
    'Nomina' : ['FechaInicialPago', 'FechaFinalPago', 'FechaPago', 'NumDiasPagados', 'TotalDeducciones', 'TotalPercepciones'],
    'Percepciones' : ['TotalExento', 'TotalGravado', 'TotalSueldos'],
    'DesglosePercepciones' : ['Concepto', 'ImporteGravado', 'ImporteExento', 'TipoPercepcion'],
    'Deducciones' : ['TotalImpuestosRetenidos', 'TotalOtrasDeducciones', 'TotalImpuestosTrasladados'],
    'DesgloseDeducciones' : ['Clave', 'Concepto', 'Importe', 'TipoDeduccion'],
    'Timbrado' : ['FechaTimbrado', 'UUID', 'NoCertificadoSAT', 'SelloCFD', 'SelloSAT'],
    }
        
match = {
    'General' : 'cfdi:Comprobante',
    'Emisor' : 'cfdi:Emisor',
    'Concepto' : 'cfdi:Concepto',
    'Nomina' : 'nomina12:Nomina',
    'Percepciones' : 'nomina12:Percepciones',
    'DesglosePercepciones' : 'nomina12:Percepcion',
    'Deducciones' : 'nomina12:Deducciones',
    'DesgloseDeducciones' : 'nomina12:Deduccion',
    'Timbrado' : 'tfd:TimbreFiscalDigital',
}

class CFDI3:
    """
    Representación de un CFDI de tipo Nómina.
    """

    def __init__(self, filepath: str) -> None:
        self.xml = minidom.parse(filepath)

    @property
    def values(self) -> dict:
        cfdi = {}
        for match_key, match_value in match.items():

            tree = self.xml.getElementsByTagName(match_value)

            if match_key == 'DesglosePercepciones' or match_key == 'DesgloseDeducciones':
                _, i = {}, 0
                for node in tree:
                    try:
                        _.update({i : {key: value for (key, value) in node.attributes.items()}}); i += 1
                    except:
                        cfdi.update({match_key : None})

                cfdi.update({match_key : _})

            else:
                for node in schema.get(match_key):
                        try:
                            cfdi.update({node : tree.item(0).attributes[node].value})
                        except:
                            cfdi.update({node : None})
            
        return cfdi

    def to_json(self) -> json:
        """
        Convierte los valores del CFDI a formato JSON.
        """
        return json.dumps(self.values, indent=4)