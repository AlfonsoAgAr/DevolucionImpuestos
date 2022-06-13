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
    
        """ Datos generales del CFDI """
        self.General = self.xml.getElementsByTagName('cfdi:Comprobante')
        self.total = self.General.item(0).attributes['Total'].value
        self.subtotal = self.General.item(0).attributes['SubTotal'].value
        self.descuento = self.General.item(0).attributes['Descuento'].value
        self.fecha = self.General.item(0).attributes['Fecha'].value
        self.series = self.General.item(0).attributes['Serie'].value
        self.sello = self.General.item(0).attributes['Sello'].value
        self.noCertificado = self.General.item(0).attributes['NoCertificado'].value
        self.certificado = self.General.item(0).attributes['Certificado'].value

        """ Datos del emisor del CFDI """
        self.Emisor = self.xml.getElementsByTagName('cfdi:Emisor')
        self.nombreEmisor = self.Emisor.item(0).attributes['Nombre'].value
        self.regimenFiscal = self.Emisor.item(0).attributes['RegimenFiscal'].value
        self.rfcEmisor = self.Emisor.item(0).attributes['Rfc'].value

        """ Datos de los conceptos del CFDI """
        self.Concepto = self.xml.getElementsByTagName('cfdi:Concepto')
        self.clave = self.Concepto.item(0).attributes['ClaveProdServ'].value
        self.claveUnidad = self.Concepto.item(0).attributes['ClaveUnidad'].value
        self.descripcion = self.Concepto.item(0).attributes['Descripcion'].value
        self.cantidad = self.Concepto.item(0).attributes['Cantidad'].value
        self.descuento = self.Concepto.item(0).attributes['Descuento'].value
        self.importe = self.Concepto.item(0).attributes['Importe'].value
        self.valorUnitario = self.Concepto.item(0).attributes['ValorUnitario'].value

        """ Datos de la nómina """
        self.Nomina = self.xml.getElementsByTagName('nomina12:Nomina')
        self.fechaInicialPago = self.Nomina.item(0).attributes['FechaInicialPago'].value
        self.fechaFinalPago = self.Nomina.item(0).attributes['FechaFinalPago'].value
        self.fechaPago = self.Nomina.item(0).attributes['FechaPago'].value
        self.diasPagados = self.Nomina.item(0).attributes['NumDiasPagados'].value
        self.totalDeduccion = self.Nomina.item(0).attributes['TotalDeducciones'].value
        self.totalPercibido = self.Nomina.item(0).attributes['TotalPercepciones'].value

        """ Total de percepciones del asalariado """
        self.Percepciones = self.xml.getElementsByTagName('nomina12:Percepciones')
        self.totalExento = self.Percepciones.item(0).attributes['TotalExento'].value
        self.totalGravado = self.Percepciones.item(0).attributes['TotalGravado'].value
        self.totalSueldo = self.Percepciones.item(0).attributes['TotalSueldos'].value

        """ Listado de las percepciones """
        self.DesglosePercepciones = self.xml.getElementsByTagName('nomina12:Percepcion')
        self.listaPercepciones = [
            {
                'Concepto': itemPercepcion.attributes['Concepto'].value,
                'ImporteGravado': itemPercepcion.attributes['ImporteGravado'].value,
                'ImporteExento': itemPercepcion.attributes['ImporteExento'].value,
                'TipoPercepcion': itemPercepcion.attributes['TipoPercepcion'].value
            }
            for itemPercepcion in self.DesglosePercepciones]

        """ Total de Deducciones del asalariado """
        self.Deducciones = self.xml.getElementsByTagName('nomina12:Deducciones')
        self.impuestosRetenidos = self.Deducciones.item(0).attributes['TotalImpuestosRetenidos'].value
        self.otrasDeducciones = self.Deducciones.item(0).attributes['TotalOtrasDeducciones'].value

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