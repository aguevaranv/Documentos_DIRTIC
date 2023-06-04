from odoo import models, fields, api

class tipoResultado(models.Model):
    _name = 'gestionoperativa.tiporesultado'
    _description = 'TIPO DE RESULTADO'

    name = fields.Char(string="TIPO DE RESULTADO:")        
