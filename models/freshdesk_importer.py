from odoo import models, fields, api
from odoo.exceptions import UserError
import base64
import xml.etree.ElementTree as ET
import logging

_logger = logging.getLogger(__name__)

class FreshdeskImportWizard(models.TransientModel):
    _name = 'freshdesk.import.wizard'
    _description = 'Importador Freshdesk XML'

    file_xml = fields.Binary(string="Archivo XML (Solutions.xml)", required=True)
    filename = fields.Char(string="Nombre de archivo")

    def action_import_xml(self):
        self.ensure_one()
        try:
            file_content = base64.b64decode(self.file_xml)
            root = ET.fromstring(file_content)
        except Exception as e:
            raise UserError(f"Error leyendo XML: {str(e)}")

        count_cat = 0
        count_fold = 0
        count_art = 0

        # 1. Crear una Página Raíz Maestra para tenerlo todo ordenado
        master_root = self.env['document.page'].create({
            'name': 'Importación Freshdesk',
            'type': 'category',
            'content': '<p>Contenido importado desde Solutions.xml</p>'
        })

        # 2. Buscar Categorías (solution-category)
        # Usamos .// para encontrar las categorías sin importar la raíz principal
        for category in root.findall('.//solution-category'):
            cat_name = self._get_text(category, 'name')
            cat_desc = self._get_text(category, 'description')
            
            # Crear Página de Categoría
            cat_page = self._create_page(cat_name, cat_desc, master_root.id)
            count_cat += 1

            # 3. Buscar Carpetas dentro (folders -> solution-folder)
            folders_node = category.find('folders')
            if folders_node is not None:
                for folder in folders_node.findall('solution-folder'):
                    fold_name = self._get_text(folder, 'name')
                    fold_desc = self._get_text(folder, 'description')

                    # Crear Página de Carpeta (Hija de Categoría)
                    fold_page = self._create_page(fold_name, fold_desc, cat_page.id)
                    count_fold += 1

                    # 4. Buscar Artículos dentro (articles -> solution-article)
                    articles_node = folder.find('articles')
                    if articles_node is not None:
                        for article in articles_node.findall('solution-article'):
                            # EN ARTÍCULOS: El título es 'title' y el contenido 'description'
                            art_title = self._get_text(article, 'title')
                            art_body = self._get_text(article, 'description')

                            # Crear Artículo (Hijo de Carpeta)
                            self._create_page(art_title, art_body, fold_page.id)
                            count_art += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Importación Completada',
                'message': f'Se crearon: {count_cat} Categorías, {count_fold} Carpetas y {count_art} Artículos.',
                'type': 'success',
                'sticky': False,
            }
        }

    def _get_text(self, node, tag_name):
        """ Extrae texto seguro, devolviendo string vacío si es None """
        found = node.find(tag_name)
        if found is not None and found.text:
            return found.text
        return ""

    def _create_page(self, name, content, parent_id):
        return self.env['document.page'].create({
            'name': name or "Sin Nombre",
            'content': content or "",
            'parent_id': parent_id,
            'type': 'content' 
        })