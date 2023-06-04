from odoo import models, fields, api

class tipoSituacionok(models.Model):
    _name = 'gestionoperativa.tiposituacion'
    _description = 'TIPO SITUACIÓN'

    name = fields.Char(string="NOMBRE DE SITUACIÓN:") 
    
class tipoSituacion(models.Model):
    _name = 'gestionoperativa.configaviestadodetalle'
    _description = 'TIPO SITUACIÓN CONFIG CREO'
    # _rec_name = 'situacion_id'

    
    situacion_id = fields.Many2one(string='Parte Operativa', comodel_name='gestionoperativa.tiposituacion', ondelete='restrict') 
    estado_id = fields.Many2one(string='Parte Operativa', comodel_name='gestionoperativa.configaviestado', ondelete='restrict') 
    tipo_operacion_ids = fields.Many2many(string='Tipo de Operacion', comodel_name='gestionoperativa.tipooperacion', relation='gestionoperativa_tiposituacion_tipooperacion_rel', ondelete='restrict')


    def name_get(self):
        result = []        
        for componente in self:                  
            if componente.tipo_operacion_ids:
                dentro_del_parentesis_ids = self.env['gestionoperativa.tipooperacion'].search([('id','in',componente.tipo_operacion_ids.ids)]).mapped('name')
                dentro_del_parentesis_con_comas= ", ".join(dentro_del_parentesis_ids)
                name = componente.situacion_id.name + " (" + dentro_del_parentesis_con_comas + " ) "
                # for tipo in componente.categoria_id.tipo_ids:
                #     name = componente.grupo_id.name + " / " + componente.categoria_id.name + " / " + str(tipo.name) + " / " + componente.name 
            else:
                name = componente.situacion_id.name
            result.append((componente.id, name))    
        return result


