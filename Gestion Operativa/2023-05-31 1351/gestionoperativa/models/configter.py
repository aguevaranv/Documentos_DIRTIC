from odoo import models, fields, api

class configter(models.Model):
    _name = 'gestionoperativa.configter'
    _description = 'PARTE OPERATIVO AVIACION TERRRESTRE'

    name = fields.Char(string="NOMBRE ECHO:")        
    visible  = fields.Boolean(default="True", string='Visible')
    