
# Jewelry Obelisco — Project

Academic summary and project guide for university submission.

## Description

This is a static web project (HTML/CSS/JS) that simulates a jewelry store called "Jewelry Obelisco" and includes an automated test framework written in Python using Selenium and PyTest to validate critical functionality.

The repository contains:
- A website: front-end pages (index, catalog, detail, cart, contact).
- Cart and checkout logic (localStorage, UI, validation, animations).
- An automated test framework (POM) with utilities and data-driven tests (CSV/Excel).

## Project structure

- `website/` — Site code (HTML, CSS, JS, assets).
	- `index.html`, `catalogo.html`, `detalle.html`, `cart.html`, `contacto.html`, `style.css`, `cart.js`, `assets/`.
- `pages/` — Page Object Model classes (Python) for tests.
- `tests/` — PyTest test cases (authentication, shopping, e2e, cross-browser, iframe).
- `utils/` — Utilities: `WebDriverFactory.py`, `WaitUtility.py`, `ExcelUtility.py`.
- `test_data/` — `login_credentials.csv`, `login_credentials.xlsx`.
# Proyecto: Tienda Web E2E + Framework de Pruebas

## Resumen profesional

Este repositorio contiene una tienda web de ejemplo junto con un framework de pruebas E2E implementado con Selenium, pytest y un patrón Page Object Model (POM). El proyecto ha sido preparado y corregido para entrega académica: se arreglaron selectores rotos, se endurecieron utilidades de Excel/CSV, se creó un exportador a XLSX compatible con Katalon y se generó un reporte HTML autocontenido con los 28 casos de prueba seleccionados.

## Contenido del repositorio

- `website/` — Código del sitio (HTML, CSS, JS, assets).
- `pages/` — Clases POM usadas por las pruebas.
- `tests/` — Casos de prueba (pytest).
- `utils/` — Utilidades (por ejemplo `ExcelUtility.py`, `WebDriverFactory.py`).
- `scripts/` — Scripts auxiliares (por ejemplo `generate_katalon_xlsx.py`).
- `test_results/` — Carpetas con reportes y archivos generados (HTML, XLSX).

## Cambios principales realizados

Para estabilizar el proyecto y dejarlo listo para entrega se aplicaron las siguientes correcciones:

- `pages/CatalogPage.py`: corrección de selectores para coincidir con `website/catalogo.html`.
- `pages/CartPage.py`: sincronización de selectores y adaptación del flujo de checkout para invocar funciones JS de la página cuando fue necesario.
- `pages/ContactPage.py`: localizadores actualizados a IDs en español (`nombre`, `mensaje`) para resolver fallos en pruebas con iframes.
- `utils/ExcelUtility.py`: robustecimiento en la lectura/escritura de Excel/CSV.
- `scripts/generate_katalon_xlsx.py`: nuevo script para exportar la lista de pruebas seleccionadas a un XLSX para Katalon; ahora limita la exportación a 28 pruebas curadas.

## Archivos front-end validados

- `website/catalogo.html`
- `website/cart.html` y `website/cart.js`
- `website/contacto.html`

## Requisitos y dependencias

- Python 3.12+
- Navegadores soportados: Google Chrome, Mozilla Firefox
- Dependencias Python (instalar con pip): `selenium`, `webdriver-manager`, `pytest`, `pytest-html`, `openpyxl`.

Instalación rápida (PowerShell):

```powershell
python -m pip install -U pip
python -m pip install selenium webdriver-manager pytest pytest-html openpyxl
```

## Ejecutar el sitio localmente

El sitio es estático; puede abrir `website/index.html` directamente o servirlo con un servidor simple:

```powershell
cd website
python -m http.server 8000
# Abrir http://localhost:8000
```

## Ejecutar la suite de pruebas

Comando recomendado para ejecutar las pruebas seleccionadas y generar el reporte HTML autocontenido:

```powershell
python -m pytest -q --maxfail=1 --html=test_results/pytest_selected_report.html --self-contained-html
```

Notas de ejecución:

- La lista curada de pruebas se encuentra en `tests/selected_tests.txt`.
- Las pruebas usan POM en `pages/` y utilidades en `utils/`.

## Generar Excel para Katalon

El script `scripts/generate_katalon_xlsx.py` convierte `tests/selected_tests.txt` en `test_results/katalon_selected_tests.xlsx`. Si el archivo de entrada contiene más de 28 entradas, el script recorta la lista a las 28 pruebas curadas y lo indica en la salida.

Ejecutar (PowerShell):

```powershell
python .\scripts\generate_katalon_xlsx.py
```

Salida esperada (si hay más de 28 entradas):

```
Input contained 29 tests; trimming to 28.
Wrote 28 tests to test_results\\katalon_selected_tests.xlsx
```

## Artefactos generados

- Reporte de pytest (autocontenido): `test_results/pytest_selected_report.html`
- Excel exportado para Katalon: `test_results/katalon_selected_tests.xlsx` (28 filas)

## Recomendaciones para entrega

- Incluye `test_results/pytest_selected_report.html` y `test_results/katalon_selected_tests.xlsx` en el paquete de entrega si la guía lo permite.
- Añade `requirements.txt` al repositorio si deseas fijar versiones exactas para reproducibilidad.
- Verifica localmente la ejecución de pruebas antes de enviar.

## Comandos útiles de Git (PowerShell)

```powershell
git add .
git commit -m "Preparación entrega: corrección POM, script Katalon, reporte pytest"
git push origin main
```

## Siguientes pasos que puedo hacer por ti

- Verificar el contenido de `test_results/katalon_selected_tests.xlsx` y abrir el archivo.
- Añadir un `requirements.txt` y un `CONTRIBUTING.md` con pasos rápidos.
- Hacer el commit de los cambios y abrir un PR en tu repositorio.

---
Fecha de actualización: 2026-01-13



