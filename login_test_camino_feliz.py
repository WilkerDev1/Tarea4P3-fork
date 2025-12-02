from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

# --- CONFIGURACIÓN PARA ARCH LINUX ---
# En Arch, el driver suele estar en /usr/bin/chromedriver. 
# Si usaste descarga manual, cambia esto a '/usr/local/bin/chromedriver'
RUTE_DRIVER = '/usr/bin/chromedriver'

service = Service(executable_path=RUTE_DRIVER)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Inicializamos el driver con la configuración correcta
driver = webdriver.Chrome(service=service, options=options)
# -------------------------------------

# URL DEL SERVIDOR LOCAL (Asegúrate de tener corriendo: python -m http.server 8000)
BASE_URL = "http://localhost:8000/login.html"

# Carpeta para capturas
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

try:
    print("🔵 Iniciando prueba de Login...")
    driver.get(BASE_URL)

    # Llenar campos
    # CORRECCIÓN: Tu login.html pide usuario "admin" y contraseña "1234"
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234") 
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Esperar redirección
    time.sleep(2)

    # Validar resultado
    if "crud.html" in driver.current_url:
        resultado = "✅ Camino feliz login: PASÓ"
    else:
        resultado = "❌ Camino feliz login: FALLÓ - No redireccionó a crud.html"

    # Guardar captura y reporte
    driver.save_screenshot("screenshots/login_camino_feliz.png")
    with open("reporte_login.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print(f"❌ Error crítico en la prueba: {e}")

finally:
    driver.quit()