# Sistema de Cotizaciones - Capital & Farmer

## Instalación

1. Clone el repositorio:

```bash
git clone https://github.com/GiedraAlexandra19/PinoHuarsaya-capital-farmer-exam.git
cd PinoHuarsaya-capital-farmer-exam
```
2. Instale las dependencias:

```bash
pip install -r requirements.txt
```
3. Ejecute la aplicación:

```bash
python app.py
```

## Uso

- Acceder a: http://localhost:5000

- Iniciar sesión con usuario y contraseña (admin / 1234)

- Completar el formulario de cotización indicando tipo de servicio y descripción del caso

- El sistema:

    1. Calcula un precio base según el servicio

    2. Llama a una IA externa para analizar el caso legal

    3. Obtiene:

      - Nivel de complejidad (Baja, Media o Alta)

      - Ajuste de precio sugerido (0%, 25%, 50%)

      - Servicios adicionales recomendados

      - Una propuesta profesional redactada

    4. Guarda la cotización en una base de datos SQLite

    5. Muestra al usuario la cotización en formato JSON

## APIs utilizadas

Groq API – acceso al modelo LLaMA 3 (llama3-8b-8192)

Se conecta vía httpx con llamadas HTTP directas (sin librerías propietarias)

## Funcionalidades bonus

✅ Autenticación básica (login/logout) 

✅ Diseño responsive para móvil 

✅ Validaciones de formulario en frontend (HTML5)

✅ Tests unitarios simples 

✅ Commits organizados y descriptivos 

✅ Uso de IA sin librerías propietarias
