from odoo import models, fields, api
from odoo.exceptions import UserError
import openai
import json

class AiAgentWizard(models.TransientModel):
    _name = 'ai.agent.wizard'
    _description = 'Asistente IA con Base de Conocimiento OCA'

    prompt = fields.Text(string="Consulta / Instrucción", required=True)
    response = fields.Html(string="Respuesta IA", readonly=True)
    
    # Opciones
    use_knowledge_base = fields.Boolean(string="Buscar en Documentación", default=True)

    def action_ask_ai(self):
        """ 1. Busca en Wiki. 2. Pregunta a la IA. """
        self.ensure_one()
        
        # A. CONTEXTO DEL REGISTRO ACTUAL
        record_context = ""
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        
        if active_model and active_id:
            try:
                record = self.env[active_model].browse(active_id)
                data = record.read()[0]
                clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool)) and not str(k).startswith('message_')}
                record_context = json.dumps(clean_data, default=str)
            except:
                pass

        # B. BÚSQUEDA EN BASE DE CONOCIMIENTO (document.page)
        knowledge_text = ""
        if self.use_knowledge_base:
            keywords = [w for w in self.prompt.split() if len(w) > 3]
            
            final_docs = self.env['document.page']
            if keywords:
                # Buscar documentos que contengan ALGUNA palabra clave
                for word in keywords:
                    # Buscamos en 'name' (título) O 'content' (contenido)
                    found = self.env['document.page'].search(['|', ('name', 'ilike', word), ('content', 'ilike', word)], limit=2)
                    final_docs |= found # Sumamos resultados
                
                if final_docs:
                    knowledge_text = "📚 INFORMACIÓN DE TU DOCUMENTACIÓN INTERNA:\n"
                    for doc in final_docs[:3]: 
                        preview = doc.content[:1500] if doc.content else "Sin contenido"
                        knowledge_text += f"--- ARTÍCULO: {doc.name} ---\n{preview}\n\n"

        # C. PROMPT FINAL
        system_msg = "Eres un experto en Odoo. Usa la 'INFORMACIÓN DE DOCUMENTACIÓN INTERNA' si existe para responder. Si no, usa tu conocimiento general. Responde en HTML limpio."
        user_msg = f"""
        Contexto Registro: {record_context}
        
        {knowledge_text}
        
        Pregunta: {self.prompt}
        """

        # D. LLAMADA A OLLAMA
        try:
            client = openai.OpenAI(base_url="http://ollama:11434/v1", api_key="ollama")
            completion = client.chat.completions.create(
                model="llama3.2:1b",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ]
            )
            self.response = completion.choices[0].message.content
        except Exception as e:
            self.response = f"<span style='color:red'>Error Ollama: {str(e)}</span>"

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.agent.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': self.env.context
        }

    def action_save_to_knowledge(self):
        """ Guarda la respuesta generada como un nuevo Document Page """
        self.ensure_one()
        if not self.response:
            raise UserError("No hay respuesta para guardar.")

        title = (self.prompt[:40] + '...') if len(self.prompt) > 40 else self.prompt
        
        # CREAR EN DOCUMENT.PAGE
        new_page = self.env['document.page'].create({
            'name': title,
            'content': self.response, 
            'type': 'content'
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'document.page',
            'res_id': new_page.id,
            'view_mode': 'form',
            'target': 'current',
        }