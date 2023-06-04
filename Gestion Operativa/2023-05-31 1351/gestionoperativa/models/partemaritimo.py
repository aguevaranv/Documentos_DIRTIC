from odoo import models, fields, api
import requests
import json

class gestionoperativamar(models.Model):
    _name = 'gestionoperativa.parteopemar'
    _description = 'PARTE OPERATIVO MARITIMO'

    create_date = fields.Datetime(string='Fecha de Elaboración:', readonly=True, default=fields.Datetime.now)
    create_uid = fields.Many2one(readonly=True, comodel_name='res.users', ondelete='restrict')
    gestionoperativamar_ids = fields.One2many(string='Detalle Parte Operativo', comodel_name='gestionoperativa.parteopeavidetallemar', inverse_name='parteopemar_id', copy=True)
 
class gestionoperativamar2(models.Model):
    _name = 'gestionoperativa.parteopeavidetallemar'
    _description = 'gestionoperativa.parteopeavidetallemar'

    parteopemar_id = fields.Many2one(string='Parte Operativa', comodel_name='gestionoperativa.parteopemar', ondelete='restrict')
    unidad_id = fields.Many2one(string='UNIDAD', domain=lambda self : [('id', '=',self.env['gestionoperativa.configmar'].search([('visible','=',True)]).reparto_ids.ids)], comodel_name='res.company', ondelete='restrict',)
    unidad_id_domain = fields.Char ( compute = "_compute_unidad_id_domain" , readonly = True, store = False, )
    fecha_desde = fields.Date(string='DESDE')
    fecha_hasta = fields.Date(string='HASTA')
    posicion_actual = fields.Text()
    cond_operativa = fields.Char(string="Street")
    observacion = fields.Text()

    latitude = fields.Float(string='Latitude')
    longitude = fields.Float(string='Longitude')

    @api.depends('unidad_id')
    def _compute_unidad_id_domain(self):
        for record in self:
            if(record.parteopemar_id):
                todas_unidades = self.env['gestionoperativa.configmar'].search([('visible','=',True)]).reparto_ids        
                unidades_ingresadas = record.parteopemar_id.gestionoperativamar_ids.unidad_id 
                restantes = todas_unidades - unidades_ingresadas 
                record.unidad_id_domain = json.dumps([('id' , 'in' , restantes.ids)])