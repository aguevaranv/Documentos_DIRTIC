from odoo import models, fields, api
import requests
import json

class gestionoperativater(models.Model):
    _name = 'gestionoperativa.parteopeter'
    _description = 'PARTE OPERATIVO TERRESTRE'

    create_date = fields.Datetime(string='Fecha de Elaboración:', readonly=True, default=fields.Datetime.now)
    create_uid = fields.Many2one(readonly=True, comodel_name='res.users', ondelete='restrict')
    gestionoperativater_ids = fields.One2many(string='Detalle Parte Operativo', comodel_name='gestionoperativa.parteopeavidetalleter', inverse_name='parteopeter_id',)
 
class gestionoperativater2(models.Model):
    _name = 'gestionoperativa.parteopeavidetalleter'
    _description = 'gestionoperativa.parteopeavidetalleter'

    parteopeter_id = fields.Many2one(string='Parte Operativa', comodel_name='gestionoperativa.parteopeter', ondelete='restrict')
    unidad_id = fields.Many2one(string='UNIDAD', comodel_name='gestionoperativa.configter', ondelete='restrict',)
    unidad_id_domain = fields.Char ( compute = "_compute_unidad_ter_id_domain" , readonly = True, store = False, )
    fecha_desde = fields.Date(string='DESDE')
    fecha_hasta = fields.Date(string='HASTA')
    posicion_actual = fields.Text()
    cond_operativa = fields.Char(string="Street")
    observacion = fields.Text()

    latitude = fields.Float(string='Latitude')
    longitude = fields.Float(string='Longitude')

    @api.depends('unidad_id')
    def _compute_unidad_ter_id_domain(self):
        for record in self:
            if(record.parteopeter_id):
                todas_unidades = self.env['gestionoperativa.configter'].search([('visible','=',True)])        
                unidades_ingresadas = record.parteopeter_id.gestionoperativater_ids.unidad_id 
                restantes = todas_unidades - unidades_ingresadas 
                record.unidad_id_domain = json.dumps([('id' , 'in' , restantes.ids)])
    