from xml.dom import minidom
from xml.dom.minidom import Document
from xml.dom.minicompat import NodeList
import json

class CFDI3:
    """
    Representación de un CFDI de tipo Nómina.
    
    Atributos verbosos.
    """
    def __init__(self, filepath: str) -> None:
        self.xml = minidom.parse(filepath)

        schemaLista = {
            'General' : ['Total', 'SubTotal', 'Descuento', 'Fecha', 'Serie', 'Sello', 'NoCertificado', 'Certificado'],
            'Emisor' : ['Nombre', 'RegimenFiscal', 'Rfc'],
            'Concepto' : ['ClaveProdServ', 'ClaveUnidad', 'Descripción', 'Cantidad', 'Descuento', 'Importe', 'ValorUnitario'],
            'Nomina' : ['FechaInicialPago', 'FechaFinalPago', 'FechaPago', 'NumDiasPagados', 'TotalDeducciones', 'TotalPercepciones'],
            'Percepciones' : ['TotalExento', 'TotalGravado', 'TotalSueldos'],
            'DesglosePercepciones' : ['Concepto', 'ImporteGravado', 'ImporteExento', 'TipoPercepcion'],
            'Deducciones' : ['TotalImpuestosRetenidos', 'TotalOtrasDeducciones', 'TotalImpuestosTrasladados'],
            }
    
        """ Datos generales del CFDI """
        self.General = self.xml.getElementsByTagName('cfdi:Comprobante')
        self.comprobante = {}
        for elemento in schemaLista:
            try:
                self.comprobante.update(
                    {
                        f'{elemento}': self.General.item(0).attributes[f'{elemento}'].value
                    })
            except:
                self.comprobante.update(
                    {
                        f'{elemento}': None
                    })

        """ Datos del emisor del CFDI """
        self.Emisor = self.xml.getElementsByTagName('cfdi:Emisor')

        """ Datos de los conceptos del CFDI """
        self.Concepto = self.xml.getElementsByTagName('cfdi:Concepto')

        """ Datos de la nómina """
        self.Nomina = self.xml.getElementsByTagName('nomina12:Nomina')

        """ Total de percepciones del asalariado """
        self.Percepciones = self.xml.getElementsByTagName('nomina12:Percepciones')

        """ Listado de las percepciones """
        self.DesglosePercepciones = self.xml.getElementsByTagName('nomina12:Percepcion')

        """ Total de Deducciones del asalariado """
        self.Deducciones = self.xml.getElementsByTagName('nomina12:Deducciones')

        """ Listado de las deducciones """
        self.DesgloseDeducciones = self.xml.getElementsByTagName('nomina12:Deduccion')
        self.listaDeducciones = [
            {
                'Clave': itemDeduccion.attributes['Clave'].value,
                'Concepto': itemDeduccion.attributes['Concepto'].value,
                'Importe': itemDeduccion.attributes['Importe'].value,
                'TipoDeduccion': itemDeduccion.attributes['TipoDeduccion'].value
            }
            for itemDeduccion in self.DesgloseDeducciones]

        """ Timbrado Fiscal """
        self.TimbreFiscal = self.xml.getElementsByTagName('tfd:TimbreFiscalDigital')
        self.fechaTimbrado = self.TimbreFiscal.item(0).attributes['FechaTimbrado'].value
        self.noCertSAT = self.TimbreFiscal.item(0).attributes['NoCertificadoSAT'].value
        self.selloCFD = self.TimbreFiscal.item(0).attributes['SelloCFD'].value
        self.selloSAT = self.TimbreFiscal.item(0).attributes['SelloSAT'].value
        self.uuid = self.TimbreFiscal.item(0).attributes['UUID'].value

    def to_dict(self) -> dict:
        """
        Convierte los valores del CFDI a diccionario.
        """
        _dict = {}
        for attribute, value in self.__dict__.items():
            if not isinstance(value, NodeList) and not isinstance(value, Document):
                _dict.update({attribute: value})

        return _dict

    def to_json(self) -> json:
        """
        Convierte los valores del CFDI a formato JSON.
        """
        return json.dumps(self.to_dict(), indent=4)