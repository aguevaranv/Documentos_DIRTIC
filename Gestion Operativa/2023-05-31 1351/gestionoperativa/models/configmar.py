from odoo import models, fields, api

class configmar(models.Model):
    _name = 'gestionoperativa.configmar'
    _description = 'PARTE OPERATIVO AVIACION NAVAL'

    name = fields.Char(string="NOMBRE GRUPO MARITIMO:")        
    
    
    # tripulante_ids = fields.Many2many(string='PERSONAL A CONTROLAR:', domain=lambda self : [('id', '=',self.env['vuelo_base.qualification'].search([]).tripulante_id.ids)], comodel_name='hr.employee', relation='vuelo_base_tripul_employ_rel', column1='employee_id', column2='tripulante_id')
    reparto_ids = fields.Many2many(string='Unidades:', comodel_name='res.company', relation='gestionope_config_repa_rel', column1='reparto_id', column2='configmar_id')
    visible  = fields.Boolean(default="True", string='Visible')

    
    
    