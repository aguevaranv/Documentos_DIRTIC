from odoo import models, fields, api

class tipoPlataforma(models.Model):
    _name = 'gestionoperativa.tipoplataforma'
    _description = 'TIPO DE PLATAFORMA'

    name = fields.Char(string="TIPO DE PLATAFORMA:")        
