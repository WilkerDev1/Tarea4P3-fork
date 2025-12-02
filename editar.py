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
    print("🔵 Prueba: Editar Tarea...")
    driver.get(BASE_LOGIN_URL)
    time.sleep(1)

    # Login
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    # Crear tarea para editar
    tarea_original = "Tarea para editar"
    driver.find_element(By.ID, "taskInput").send_keys(tarea_original)
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Abrir modal (primer botón de editar)
    editar_btn = driver.find_element(By.CSS_SELECTOR, "#taskList li:last-child button.btn-primary")
    editar_btn.click()
    time.sleep(1)

    # Editar
    edit_input = driver.find_element(By.ID, "editTaskInput")
    edit_input.clear()
    tarea_editada = "Tarea editada en Arch Linux"
    edit_input.send_keys(tarea_editada)

    driver.find_element(By.ID, "saveEditBtn").click()
    time.sleep(1)

    # Verificar
    tareas = driver.find_elements(By.CSS_SELECTOR, "#taskList li span")
    textos = [t.text for t in tareas]

    if tarea_editada in textos:
        resultado = "✅ Prueba editar tarea: PASÓ"
    else:
        resultado = "❌ Prueba editar tarea: FALLÓ"

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    driver.save_screenshot(f"screenshots/prueba_editar_tarea_{timestamp}.png")
    
    with open("reporte_prueba_editar.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en editar:", e)

finally:
    time.sleep(2)
    driver.quit()