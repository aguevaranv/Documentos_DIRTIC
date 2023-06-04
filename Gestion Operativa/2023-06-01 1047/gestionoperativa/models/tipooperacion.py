from odoo import models, fields, api


class tipooperacion(models.Model):
    _name = 'gestionoperativa.tipooperacion'
    _description = 'TIPO DE OPERACIÓN AVIACIÓN NAVAL'

    name = fields.Char(string="NOMBRE DEL TIPO DE OPERACIÓN:")  
    