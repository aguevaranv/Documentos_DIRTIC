from odoo import models, fields, api

class ResultadosObtenidos(models.Model):
    _name = 'gestionoperativa.resultadosobtenidos'
    _description = 'Resultados Obtenidos'
    _rec_name = 'tiporesultado_id'

    tiporesultado_id = fields.Many2one('gestionoperativa.tiporesultado', string='Tipo de Resultado')
    cantidad = fields.Integer(string='Cantidad')
    latitude = fields.Float(string='LATITUDE')
    longitude = fields.Float(string='LONGITUDE')
    observacion = fields.Text(string='Observación')

    name = fields.Char(string="Código de la Misión", store="False")
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment', relation='gestionoperativa_resultobte_attachm_rel',
        column1='resultadosobtenidos_id', column2='attachment_id', string='Archivo Adjunto')

    lineaparteavi_id = fields.Many2one('gestionoperativa.parteopeavidetalle', string='Detalle del Parte Aéreo')
