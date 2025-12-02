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
    print("🔵 Prueba: Límite Tarea Vacía...")
    driver.get(BASE_LOGIN_URL)
    time.sleep(1)

    # Login
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Contar antes
    tareas_antes = driver.find_elements(By.CSS_SELECTOR, "#taskList li")
    cantidad_antes = len(tareas_antes)

    # Intentar enviar vacío
    driver.find_element(By.ID, "taskInput").clear()
    driver.find_element(By.ID, "taskInput").send_keys("") 
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Contar después
    tareas_despues = driver.find_elements(By.CSS_SELECTOR, "#taskList li")
    cantidad_despues = len(tareas_despues)

    if cantidad_despues == cantidad_antes:
        resultado = "✅ Prueba límite crear tarea vacía: PASÓ"
    else:
        resultado = "❌ Prueba límite crear tarea vacía: FALLÓ"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"screenshots/prueba_limite_tarea_vacia_{timestamp}.png")

    with open("reporte_prueba_limite_tarea_vacia.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en prueba límite:", e)

finally:
    time.sleep(2)
    driver.quit()