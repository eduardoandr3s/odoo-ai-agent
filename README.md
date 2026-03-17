# 🤖 Odoo AI Agent (V18)

Módulo especializado para **Odoo v18** que integra un Agente de Inteligencia Artificial diseñado para interactuar con la base de conocimiento y la documentación de los módulos de la **OCA (Odoo Community Association)**.

## 🌟 Descripción

Este agente permite a los usuarios de Odoo realizar consultas en lenguaje natural sobre la configuración y el funcionamiento de los módulos. Utiliza capacidades de IA para indexar y consultar documentos técnicos, facilitando el soporte y la implementación de soluciones basadas en el estándar de la comunidad.

## 🚀 Características principales

- **Integración Nativa:** Desarrollado específicamente para el framework de Odoo 18.
- **Consulta de Base de Conocimiento:** Capacidad para leer y procesar documentación del módulo `knowledge` y recursos de la OCA.
- **Asistente Inteligente:** Interfaz diseñada para resolver dudas técnicas y funcionales de forma inmediata.
- **Seguridad Odoo:** Respeta el sistema de reglas de acceso (ACLs) y grupos de seguridad nativos de la plataforma.

## 🛠️ Tecnologías

- **Lenguaje:** Python 3.12+
- **ERP:** Odoo 18.0 (Community/Enterprise)
- **IA:** Preparado para integración con LLMs (OpenAI/LangChain) para el procesamiento de lenguaje.
- **Módulos dependientes:** `base`, `knowledge`.

## 📂 Estructura del Módulo

- `models/`: Lógica del agente y procesamiento de datos.
- `views/`: Interfaces de usuario integradas en el backend de Odoo.
- `security/`: Definición de permisos y grupos de acceso.
- `__manifest__.py`: Metadatos y dependencias del módulo.

## 🔧 Instalación

1.  Clona este repositorio dentro de tu carpeta de `addons`:
    ```bash
    git clone [https://github.com/eduardoandr3s/odoo-ai-agent.git](https://github.com/eduardoandr3s/odoo-ai-agent.git)
    ```
2.  Asegúrate de tener instaladas las dependencias de Python necesarias (ver archivo de requisitos si aplica).
3.  Actualiza la lista de módulos en tu instancia de Odoo.
4.  Instala el módulo **"Agente de IA para Odoo"**.

## 📝 Notas de Desarrollo

Este proyecto se encuentra en desarrollo activo como parte de mi especialización en el ecosistema Odoo y tecnologías de IA. Se enfoca en mejorar la accesibilidad a la documentación técnica para consultores y desarrolladores.

---
Desarrollado por [Eduardo Andrés](https://github.com/eduardoandr3s)
