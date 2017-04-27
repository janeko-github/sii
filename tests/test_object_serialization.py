# coding=utf-8

from sii.resource import SII
import sii
from expects import *


class Period():
    def __init__(self, name):
        self.name = name


class Partner():
    def __init__(self, name, nif):
        self.name = name
        self.nif = nif


class InvoiceLineTaxes():
    def __init__(self, name, base_imponible):
        self.name = name
        self.base = base_imponible


class Invoice():
    def __init__(self, number, type, partner, amount_total, period_id, date_invoice, tax_line_ids):
        self.number = number
        self.type = type
        self.partner_id = partner
        self.period_id = period_id
        self.amount_total = amount_total
        self.date_invoice = date_invoice
        self.tax_line = tax_line_ids


with description("El XML Generado"):
    with before.all:
        period = Period(name='03/2016')
        tax_line = [
            InvoiceLineTaxes('IVA 21%', base_imponible=12.34),
            InvoiceLineTaxes('IBI 15%', base_imponible=56.78)
        ]
        self.partner = Partner(name='Francisco García', nif='12345678T')
        self.invoice = Invoice(
            number='F012345', type='out_invoice', partner=self.partner,
            amount_total=15, period_id=period, date_invoice='2016-03-25',
            tax_line_ids=tax_line
        )

        # TODO delete print object
        print '\n'
        print '========= FACTURA EJEMPLO ================'
        from pprintpp import pprint
        pprint(vars(self.invoice))
        print '=========================================='

        self.obj = SII.generate_object(self.invoice)

        # TODO delete print object
        print '\n'
        print '============ RESULTADO DEL DUMP ====================='
        pprint(self.obj)
        print '====================================================='

        self.cabecera = self.obj['SuministroLRFacturasEmitidas']['Cabecera']
        self.factura = self.obj[
            'SuministroLRFacturasEmitidas']['RegistroLRFacturasEmitidas']

    with description("en la cabecera"):
        with it("la versión es la versión del SII"):
            expect(self.cabecera['IDVersionSii']).to(equal(sii.__SII_VERSION__))
        with context("cuando es de tipo alta"):
            with it("el tipo de comunicación debe ser 'A0'"):
                expect(
                    self.cabecera['TipoComunicacion']).to(equal('A0'))

    with _description("en los datos del período"):
        with it("el ejercicio es el correspondiente al año de la factura"):
            pass
        with it("el período es el correspondiente al mes de la factura"):
            pass

    with _description("en los datos de la identificación de la factura"):
        with it("el NIF de la factura es el NIF del emisor"):
            pass
        with context("en las facturas emitidas"):
            with _it("el número de factura debe ser igual al número de la factura original"):
                pass
        with context("en las facturas recibidas"):
            with _it("el número de factura debe ser igual al número de factura"):
                pass
        with it("la fecha de la factura es la fecha de expedición de la factura"):
            pass

    with description("en la factura"):
        with it("el número de la factura debe ser igual que el de la factura original"):
            expect(self.factura['IDFactura']['NumSerieFacturaEmisor']).to(equal(self.invoice.number))

        with it("el tipo de la factura es 'F1'"):
            expect(self.factura['FacturaExpedida']['TipoFactura']).to(equal('F1'))
