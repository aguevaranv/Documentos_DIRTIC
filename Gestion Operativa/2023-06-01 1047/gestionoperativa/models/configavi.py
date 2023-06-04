from odoo import models, fields, api

class configaviestado(models.Model):
    _name = 'gestionoperativa.configaviestado'
    _description = 'PARTE OPERATIVO AVIACION NAVAL'
    _rec_name = 'estado'

    estado = fields.Selection(string='ESTADO', selection=[('OPERATIVO', 'OPERATIVO'), ('PRUEBA', 'PRUEBA'), ('NO OPERATIVO', 'NO OPERATIVO')], tracking=True)    
    configaviestadodetalle_ids = fields.One2many(string='DETALLE DE LA CONFIGURACIÓN',  comodel_name='gestionoperativa.configaviestadodetalle', inverse_name='estado_id')
