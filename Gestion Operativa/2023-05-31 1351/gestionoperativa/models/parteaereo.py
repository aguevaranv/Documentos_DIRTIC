from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import json
from pytz import timezone
from datetime import timedelta

class parteOpeAviCabecera(models.Model):
    _name = 'gestionoperativa.parteopeavicabecera'
    _description = 'PARTE OPERATIVO AVIACION NAVAL'
    
    @api.depends('gestionoperativa_ids') #calculo de reporte
    def _compute_parteavi(self):
        for record in self:
            _total_operativos = 0
            _total_no_operativos = 0
            _total_prueba = 0
            _total_en_operacion = 0

            for linea in record.gestionoperativa_ids:
                if(linea.estado.estado == 'OPERATIVO'):
                    _total_operativos += 1
                elif(linea.estado.estado == 'NO OPERATIVO'):
                    _total_no_operativos += 1
                elif(linea.estado.estado == 'PRUEBA'):
                    _total_prueba += 1

                if(linea.en_operacion == True):
                    _total_en_operacion += 1

            record.total_operativos = _total_operativos
            record.total_no_operativos = _total_no_operativos
            record.total_prueba = _total_prueba
            record.total = _total_operativos + _total_no_operativos + _total_prueba
            record.total_en_operacion = _total_en_operacion

    create_date = fields.Datetime(string='Fecha de Elaboración:', readonly=True, default=fields.Datetime.now)
    create_uid = fields.Many2one(string='Parte operativo creado por:', readonly=True, comodel_name='res.users', ondelete='restrict')
    gestionoperativa_ids = fields.One2many(string='Detalle Parte Operativo', comodel_name='gestionoperativa.parteopeavidetalle', inverse_name='parteope_id',)
    total_operativos = fields.Char(string='Total operativos: ', compute='_compute_parteavi')
    total_no_operativos = fields.Char(string='Total no operativos: ', compute='_compute_parteavi')
    total_prueba = fields.Char(string='Total prueba: ', compute='_compute_parteavi')
    total = fields.Char(string='Total aviones: ', compute='_compute_parteavi')
    total_en_operacion = fields.Char(string='Total Aviones en operación: ', compute='_compute_parteavi')

    year = fields.Integer(string='Año', compute='_compute_date', store=True)
    mes = fields.Selection(string='Mes',compute='_compute_date', store=True, selection=[('ENERO', 'ENERO'), ('FEBRERO', 'FEBRERO'), ('MARZO', 'MARZO'), ('ABRIL', 'ABRIL'), ('MAYO', 'MAYO'), ('JUNIO', 'JUNIO'), ('JULIO', 'JULIO'), ('AGOSTO', 'AGOSTO'), ('SEPTIEMBRE', 'SEPTIEMBRE'), ('OCTUBRE', 'OCTUBRE'), ('NOVIEMBRE', 'NOVIEMBRE'), ('DICIEMBRE', 'DICIEMBRE')], tracking=True)
    day = fields.Integer(string='Día', compute='_compute_date', store=True)


#    VALORES POR DEFECTO PVS
    # @api.model
    # def default_get(self, fields):
    #     def cabecera_automatica(q,w):
    #         temp = int((datetime.datetime.now()+timedelta(days=w)).strftime("%m"))
    #         palabra_mes = self.transformar_palabra_mes(temp)
    #         a = datetime.datetime.now()+timedelta(days=w)
    #         b = datetime.datetime.now()+timedelta(days=q)


    def transformar_palabra_mes(self,mes):
        diccionario={"1":"ENERO", "2":"FEBRERO", "3":"MARZO", "4":"ABRIL", "5":"MAYO","6":"JUNIO", "7":"JULIO", "8":"AGOSTO", "9":"SEPTIEMBRE", 
                     "10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}     
        return diccionario.get(str(mes))

    @api.depends('create_date')
    def _compute_date(self):
        for record in self:
            adjusted_date = record.create_date - timedelta(hours=5)
            adjusted_date_ecuador = timezone('America/Guayaquil').localize(adjusted_date)
            record.year = adjusted_date_ecuador.year
            record.mes = self.transformar_palabra_mes(adjusted_date_ecuador.month)
            record.day = adjusted_date_ecuador.day

class parteOpeAviDetalle(models.Model):
    _name = 'gestionoperativa.parteopeavidetalle'
    _description = 'gestionoperativa.parteopeavidetalle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name= "situacion_id"

    @api.onchange('matricula_id')
    def _onchange_matricula(self):     
        if self.matricula_id: 
            estado = self.env['vuelo_base.aircraft'].search([('id', '=', self.matricula_id.id)]).estado
            self.estado = self.env['gestionoperativa.configaviestado'].search([('estado', '=', estado)])
      
        
    parteope_id = fields.Many2one(string='Parte Operativa', comodel_name='gestionoperativa.parteopeavicabecera', ondelete='restrict')
    modelo_id = fields.Many2one(string='MODELO', related="matricula_id.modelo_id", ondelete='restrict', store=True )   
    matricula_id_domain = fields.Char ( compute = "_compute_matricula_id_domain" , readonly = True, store = False, )
    matricula_id = fields.Many2one(string='MATRICULA', comodel_name='vuelo_base.aircraft', ondelete='restrict', tracking=True) 
    # estado = fields.Selection(string='ESTADO', selection=[('OPERATIVO', 'OPERATIVO'), ('PRUEBA', 'PRUEBA'), ('NO OPERATIVO', 'NO OPERATIVO')], tracking=True)
    estado = fields.Many2one(string='ESTADO:', comodel_name='gestionoperativa.configaviestado', ondelete='restrict', tracking=True)
    situacion_id = fields.Many2one(string='SITUACIÒN:', comodel_name='gestionoperativa.tiposituacion', ondelete='restrict')
    situacion_id_domain = fields.Char ( compute = "_compute_situacion_id_domain" , readonly = True, store = False, )
    tipo_operacion_id = fields.Many2one(string='TIPO/OPERACIÓN:', comodel_name='gestionoperativa.tipooperacion', ondelete='restrict')
    tipo_operacion_id_domain = fields.Char ( compute = "_compute_tipo_operacion_id_domain" , readonly = True, store = False, )
    tipo_plataforma_id = fields.Many2one(string='TIPO/PLATAFORMA:', comodel_name='gestionoperativa.tipoplataforma', ondelete='restrict')
    en_operacion  = fields.Boolean(default=False, string='EN OPERACIÓN')
    ruta_inicio_id = fields.Many2one(string='DECOLAJE', comodel_name='vuelo_base.ciudad', ondelete='restrict')
    ruta_fin_id = fields.Many2one(string='ATERRIZAJE', comodel_name='vuelo_base.ciudad', ondelete='restrict')
    observacion = fields.Text(string="OBSERVACIÓN")
    street = fields.Char(string="Street")
    map = fields.Char(compute='_compute_map_url')
    sidebar_subtitle = fields.Char(string='Subtítulo', compute='_compute_sidebar_subtitle')


    fecha_inicio = fields.Datetime(string='DESDE')
    fecha_fin = fields.Datetime(string='HASTA')
    resultados_obtenidos_ids = fields.One2many('gestionoperativa.resultadosobtenidos', 'lineaparteavi_id', string='Resultados Obtenidos')
   
   
   #borrar
    horas_dispo = fields.Float(string='HORAS DISPONIBLES')
    condicionIOV = fields.Selection(string='CONDICION IOV', selection=[('SI', 'SI'), ('NO', 'NO')])
    fecha_solu = fields.Date(string='FECHA ESTIMADA/SOLUCIÓN')
    latitude = fields.Float(string='LATITUDE')
    longitude = fields.Float(string='LONGITUDE')
   #Fin borrar


    _sql_constraints = [('name_unique', 'UNIQUE(parteope_id,matricula_id)',"No se puede tener matrículas duplicadas!!"),]
    

    def name_get(self):
        result = []        
        for componente in self:                  
            if componente.tipo_operacion_id:
                #  = self.env['gestionoperativa.tipooperacion'].search([('id','in',componente.tipo_operacion_id.id)]).mapped('name')
                dentro_del_parentesis_id = componente.tipo_operacion_id.name
                # dentro_del_parentesis_con_comas= ", ".join(dentro_del_parentesis_id)
                name = componente.matricula_id.name + " (" + dentro_del_parentesis_id + " ) "
                # for tipo in componente.categoria_id.tipo_ids:
                #     name = componente.grupo_id.name + " / " + componente.categoria_id.name + " / " + str(tipo.name) + " / " + componente.name 
            
            else:
                name = componente.matricula_id.name+ " (" + "NO TIENE TIPO DE OPERACION REGISTRADO" + " ) "
            result.append((componente.id, name))    
        return result


    def action_insertar_resultados_obtenidos(self):
        # a=0
        self.ensure_one()
        return {
            'name': 'Resultados Obtenidos',
            'res_model': 'gestionoperativa.resultadosobtenidos',
            'target': 'new',
            'views': [(self.env.ref('gestionoperativa.resultadosobtenidos_form').id, 'form')],
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'domain': [('lineaparteavi_id', '=', self.id)],
            'context': {'default_lineaparteavi_id': self.id}
        }     

    def action_ver_resultados_obtenidos(self):
        # a=0
        self.ensure_one()
        return {
            'name': 'Resultados Obtenidos',
            'res_model': 'gestionoperativa.resultadosobtenidos',
            'target': 'new',
            'views': [(self.env.ref('gestionoperativa.resultadosobtenidos_tree').id, 'tree')],
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
            'domain': [('lineaparteavi_id', '=', self.id)],
            'context': {'default_lineaparteavi_id': self.id}
        } 
    
    
    @api.onchange('estado')
    def _onchange_estado(self):
        for record in self:
            if record.estado:
                if (record.estado != 'OPERATIVO'):
                    record.en_operacion = False
                    record.situacion_id = False
                    record.tipo_operacion_id = False
                    

    @api.onchange('en_operacion')
    def _onchange_en_operac(self):
        for record in self:
            if record.matricula_id:
                if (record.estado != 'OPERATIVO')and (record.en_operacion == True):
                    record.en_operacion = False
                    raise ValidationError("Solo las unidades OPERATIVAS pueden estar en operación..")
                    # raise ValidationError("Ya existe el valor: %s , no se permiten valores duplicados dentro de una misma característica" % (record.en_operacion))  
                if (record.estado == 'OPERATIVO')and (record.en_operacion == True):
                    # raise ValidationError("Ya existe el valor: %s , no se permiten valores duplicados dentro de una misma característica" % (record.env.ref("gestionoperativa.data_situacion_operacion").id))  
                    record.situacion_id = record.env.ref("gestionoperativa.data_situacion_operacion").id

                if (record.estado == 'OPERATIVO')and (record.en_operacion == False):
                    record.situacion_id = record.env.ref("gestionoperativa.data_situacion_enbase").id


    @api.onchange('situacion_id')
    def _onchange_situacion(self):
        for record in self:
            if record.estado:
                if (record.estado != 'OPERATIVO'):
                    record.tipo_operacion_id = False  

    @api.onchange('fecha_inicio', 'fecha_fin')
    def _onchange_fechas(self):
        for record in self:
            if record.fecha_fin:
                if record.fecha_fin < record.fecha_inicio:
                    raise ValidationError("La fecha fin es menor que la fecha inicio")

    # @api.depends('grupo')
    # def _compute_tipo_escalafon_ids_domain(self):
    #     for record in self:    
    #         escalafones_todos= self.env['hr.organico.escalafon'].search([])
    #         escalafones_seleccionados= self.env['sie_digedo_curso.grupos_tipo_escalafon'].search([('grupo','!=',record.grupo)],limit=1).tipo_escalafon_ids
    #         restantes = escalafones_todos - escalafones_seleccionados        
    #         record.tipo_escalafon_ids_domain = json.dumps([('id' , 'in' , restantes.ids)])
        
    @api.depends('situacion_id')
    def _compute_tipo_operacion_id_domain(self):
        for record in self:
            if(record.situacion_id):
                tipo_operacion_ingresadas = self.env['gestionoperativa.configaviestadodetalle'].search([('situacion_id','=',record.situacion_id.id)]).mapped('tipo_operacion_ids')
                record.tipo_operacion_id_domain = json.dumps([('id' , 'in' , tipo_operacion_ingresadas.ids)])
                # record.tipo_operacion_id_domain = json.dumps([])
            else:
                record.tipo_operacion_id_domain = json.dumps([])


    @api.depends('estado')
    def _compute_situacion_id_domain(self):
        for record in self:
            if(record.estado):
                pre_configuracion_ingresadas = self.env['gestionoperativa.configaviestado'].search([('estado','=',record.estado.estado)],limit=1)
                # escalafones_seleccionados= self.env['gestionoperativa.configaviestado'].search([('estado','=',record.estado)],limit=1)
                # situacion_ingresadas = record.parteope_id.gestionoperativa_ids.situacion_id 
                record.situacion_id_domain = json.dumps([('id' , 'in' , pre_configuracion_ingresadas.configaviestadodetalle_ids.situacion_id.ids)])
            else:
                record.situacion_id_domain = json.dumps([])

    @api.depends('matricula_id')
    def _compute_matricula_id_domain(self):
        for record in self:
            if(record.parteope_id):
                matriculas_ingresadas = record.parteope_id.gestionoperativa_ids.matricula_id 
                record.matricula_id_domain = json.dumps([('id' , 'not in' , matriculas_ingresadas.ids)])
            else:
                record.matricula_id_domain = json.dumps([])

    @api.depends('modelo_id')
    def _compute_sidebar_subtitle(self):
        for record in self:
            record.sidebar_subtitle = record.modelo_id.name if record.modelo_id else ''

    @api.depends('latitude', 'longitude')
    def _compute_map_url(self):
        for record in self:
            if record.latitude and record.longitude:
                record.map = 'https://maps.google.com/maps?q={},{}'.format(record.latitude, record.longitude)
            else:
                record.map = False

    def geocode_address(self, address):
        
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyBssGJBKT8vsVQ0hKlq2tKGLQJFlQrVx74'
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            result = data['results'][0]
            location = result['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            self.latitude = latitude
            self.longitude = longitude

        return latitude, longitude
    
    def some_method(self):
        # Ejemplo de cómo llamar a la función geocode_address
        address = 'BASE NAVAL SUR, El Tiburón, Guayaquil'
        latitude, longitude = self.geocode_address(address)


    # def write(self, vals):
    #     a=0
    #     raise ValueError("valor eliminado:")
    #     if 'matricula_id' in vals or 'estado' in vals:
    #         # Verificar si se están modificando los campos relacionados
    #         if 'estado' in vals:
    #             # Obtener la fecha actual
    #             fecha_actual = fields.Date.context_today(self)
                
    #             # Obtener la fecha de la última modificación
    #             last_update = self.create_date
                
    #             # Calcular la diferencia en días
    #             diferencia_dias = (fecha_actual - last_update).days
                
    #             if diferencia_dias >= 1:
    #                 # Ha pasado un día o más, no se permite la actualización
    #                 valor_eliminado =vals.pop('estado')
    #                 raise ValueError("valor eliminado: {}".format(valor_eliminado))
                    
            
    #         # Actualizar la fecha de la última modificación del estado
    #         vals['create_date'] = fields.Date.today()
    #         # raise ValueError("entre a modificarte el related en todo {} valores: {}".format(self,values))
    #     return super(gestionoperativaline, self).write(vals)

    

    