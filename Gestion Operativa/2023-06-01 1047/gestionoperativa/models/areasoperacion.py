from odoo import models, fields, api

class areasOperacion(models.Model):
    _name = 'gestionoperativa.areasoperacion'
    _description = 'AREAS OPERACIÓN'

    name = fields.Char(string="AREAS OPERACIÓN:")        
