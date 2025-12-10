from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import xml.etree.ElementTree as ET
import logging

_logger = logging.getLogger(__name__)

class FreshdeskImportWizard(models.TransientModel):
    _name = 'freshdesk.import.wizard'
    _description = 'Importador de Soluciones XML'

    file_xml = fields.Binary(string="Archivo XML (Solutions.xml)", required=True)
    filename = fields.Char(string="Nombre de archivo")

    def action_import_xml(self):
        """ Parsea el XML de Freshdesk y recrea la estructura en document.page """
        self.ensure_one()
        
        try:
            # 1. Decodificar archivo
            file_content = base64.b64decode(self.file_xml)
            root = ET.fromstring(file_content)
        except Exception as e:
            raise UserError(f"No se pudo leer el archivo XML. Asegúrate de que es válido. Error: {str(e)}")

        count_articles = 0
        count_folders = 0

        # El XML de Freshdesk suele ser: <solutions> -> <category> -> <folders> -> <folder> -> <articles> -> <article>
        
        # 2. Recorremos CATEGORÍAS
        for category in root.findall('category'):
            cat_name = self._get_node_text(category, 'name') or "Sin Categoría"
            
            # Crear Página Padre (Categoría)
            cat_page = self._create_page(cat_name, content=f"<h1>Categoría: {cat_name}</h1>", parent_id=False)

            # 3. Recorremos CARPETAS dentro de la categoría
            folders_node = category.find('folders')
            if folders_node is not None:
                for folder in folders_node.findall('folder'):
                    folder_name = self._get_node_text(folder, 'name') or "Sin Carpeta"
                    
                    # Crear Sub-página (Carpeta) vinculada a la Categoría
                    folder_page = self._create_page(folder_name, content=f"<h2>Carpeta: {folder_name}</h2>", parent_id=cat_page.id)
                    count_folders += 1

                    # 4. Recorremos ARTÍCULOS dentro de la carpeta
                    articles_node = folder.find('articles')
                    if articles_node is not None:
                        for article in articles_node.findall('article'):
                            # Freshdesk usa <subject> para el título y <description> para el HTML
                            art_title = self._get_node_text(article, 'subject') or "Sin Título"
                            art_body = self._get_node_text(article, 'description') or ""

                            # Crear el Artículo final vinculado a la Carpeta
                            self._create_page(art_title, content=art_body, parent_id=folder_page.id)
                            count_articles += 1

        # 5. Notificación de éxito
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Importación Exitosa',
                'message': f'Se han creado {count_folders} carpetas y {count_articles} artículos en la Base de Conocimiento.',
                'type': 'success',
                'sticky': False,
            }
        }

    def _get_node_text(self, parent, tag_name):
        """ Ayuda para extraer texto evitando errores si el tag no existe """
        node = parent.find(tag_name)
        return node.text if node is not None else ""

    def _create_page(self, name, content, parent_id=False):
        """ Crea el registro en document.page """
        vals = {
            'name': name,
            'content': content,
            'parent_id': parent_id,
            'type': 'content', # O 'category' si tu versión de document_page lo distingue
        }
        return self.env['document.page'].create(vals)