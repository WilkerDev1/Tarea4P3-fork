from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os
from datetime import datetime

# --- CONFIGURACIÓN LINUX ---
RUTE_DRIVER = '/usr/bin/chromedriver'
service = Service(executable_path=RUTE_DRIVER)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)
# ---------------------------

BASE_LOGIN_URL = "http://localhost:8000/login.html"

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

try:
    print("🔵 Prueba: Eliminar Tarea...")
    driver.get(BASE_LOGIN_URL)
    time.sleep(1)

    # Login
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Crear tarea para eliminar
    tarea = "Tarea a eliminar"
    driver.find_element(By.ID, "taskInput").send_keys(tarea)
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Eliminar (última tarea agregada para no borrar otras si hay)
    eliminar_btn = driver.find_element(By.CSS_SELECTOR, "#taskList li:last-child button.btn-danger")
    eliminar_btn.click()
    time.sleep(1)

    # Verificar
    tareas = driver.find_elements(By.CSS_SELECTOR, "#taskList li span")
    textos = [t.text for t in tareas]

    if tarea not in textos:
        resultado = "✅ Prueba eliminar tarea: PASÓ"
    else:
        resultado = "❌ Prueba eliminar tarea: FALLÓ"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"screenshots/prueba_eliminar_tarea_{timestamp}.png")

    with open("reporte_prueba_eliminar.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en eliminar:", e)

finally:
    time.sleep(2)
    driver.quit()