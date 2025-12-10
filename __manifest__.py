{
    'name': 'Odoo AI Agent',
    'version': '1.0',
    'summary': 'Asistente IA Contextual para Odoo 18',
    'author': 'Tu Nombre',
    'depends': ['base', 'web', 'document_page'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_agent_view.xml',
        'views/freshdesk_import_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}