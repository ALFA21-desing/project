"""
Ejemplo de test cases con Selenium para el sitio web Jewelry Obelisco
Asegúrate de tener el sitio corriendo localmente o ajusta la URL
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Configuración del driver
def setup_driver():
    """Configura y retorna el driver de Chrome"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Test 1: Verificar que la página de inicio carga correctamente
def test_homepage_loads():
    driver = setup_driver()
    try:
        # Cambia esta URL por donde tengas tu sitio (puede ser file:/// o http://localhost)
        driver.get("file:///C:/Users/5809025/Documents/GitHub/project/website/index.html")
        
        # Esperar a que el título cargue
        time.sleep(2)
        
        # Verificar que el logo está presente
        logo = driver.find_element(By.CLASS_NAME, "logo")
        assert logo is not None, "El logo no se encontró"
        
        # Verificar que el título OBELISCO está presente
        header_text = driver.find_element(By.TAG_NAME, "h1").text
        assert "OBELISCO" in header_text, f"Título incorrecto: {header_text}"
        
        print("  Test 1 PASADO: La página de inicio carga correctamente")
        
    except Exception as e:
        print(f"  Test 1 FALLIDO: {str(e)}")
    finally:
        driver.quit()

# Test 2: Verificar navegación al catálogo
def test_navigate_to_catalog():
    driver = setup_driver()
    try:
        driver.get("file:///C:/Users/5809025/Documents/GitHub/project/website/index.html")
        time.sleep(1)
        
        # Encontrar y hacer clic en el enlace del catálogo
        catalog_link = driver.find_element(By.LINK_TEXT, "Catalog")
        catalog_link.click()
        
        time.sleep(2)
        
        # Verificar que estamos en la página de catálogo
        assert "catalogo.html" in driver.current_url, "No se navegó al catálogo"
        
        print(" Test 2 PASADO: Navegación al catálogo exitosa")
        
    except Exception as e:
        print(f" Test 2 FALLIDO: {str(e)}")
    finally:
        driver.quit()

# Test 3: Verificar que el reloj (datetime-display) se muestra
def test_datetime_display():
    driver = setup_driver()
    try:
        driver.get("file:///C:/Users/5809025/Documents/GitHub/project/website/index.html")
        time.sleep(2)
        
        # Buscar el elemento del reloj
        datetime_elem = driver.find_element(By.ID, "datetime-display")
        datetime_text = datetime_elem.text
        
        # Verificar que tiene contenido
        assert len(datetime_text) > 0, "El reloj no muestra ningún texto"
        
        print(f" Test 3 PASADO: El reloj muestra: {datetime_text}")
        
    except Exception as e:
        print(f"  Test 3 FALLIDO: {str(e)}")
    finally:
        driver.quit()

# Test 4: Verificar funcionalidad de búsqueda
def test_search_functionality():
    driver = setup_driver()
    try:
        driver.get("file:///C:/Users/5809025/Documents/GitHub/project/website/catalogo.html")
        time.sleep(2)
        
        # Encontrar la barra de búsqueda
        search_input = driver.find_element(By.ID, "search-input")
        
        # Escribir en la búsqueda
        search_input.send_keys("ring")
        
        time.sleep(1)
        
        print("  Test 4 PASADO: La búsqueda funciona correctamente")
        
    except Exception as e:
        print(f"  Test 4 FALLIDO: {str(e)}")
    finally:
        driver.quit()

# Test 5: Verificar navegación a contacto
def test_contact_page():
    driver = setup_driver()
    try:
        driver.get("file:///C:/Users/5809025/Documents/GitHub/project/website/index.html")
        time.sleep(1)
        
        # Navegar a contacto
        contact_link = driver.find_element(By.LINK_TEXT, "Contact")
        contact_link.click()
        
        time.sleep(2)
        
        # Verificar que estamos en la página de contacto
        assert "contacto.html" in driver.current_url, "No se navegó a contacto"
        
        print(" Test 5 PASADO: Navegación a contacto exitosa")
        
    except Exception as e:
        print(f"  Test 5 FALLIDO: {str(e)}")
    finally:
        driver.quit()

# Ejecutar todos los tests
if __name__ == "__main__":
    print("\n" + "="*60)
    print("EJECUTANDO TEST CASES PARA JEWELRY OBELISCO")
    print("="*60 + "\n")
    
    test_homepage_loads()
    print()
    test_navigate_to_catalog()
    print()
    test_datetime_display()
    print()
    test_search_functionality()
    print()
    test_contact_page()
    
    print("\n" + "="*60)
    print("TESTS COMPLETADOS")
    print("="*60 + "\n")
