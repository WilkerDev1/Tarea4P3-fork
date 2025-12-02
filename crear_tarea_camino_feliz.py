from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

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
    print("🔵 Prueba: Crear Tarea...")
    driver.get(BASE_LOGIN_URL)
    time.sleep(1)

    # Login
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    if "crud.html" not in driver.current_url:
        raise Exception("Fallo en login, no redirigió a CRUD")

    # Crear tarea
    tarea = "Tarea desde Selenium Linux"
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.send_keys(tarea)
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Verificar
    tareas = driver.find_elements(By.CSS_SELECTOR, "#taskList li span")
    textos = [t.text for t in tareas]

    if tarea in textos:
        resultado = "✅ Prueba login + crear tarea: PASÓ"
    else:
        resultado = "❌ Prueba login + crear tarea: FALLÓ"

    driver.save_screenshot("screenshots/prueba_login_crear_tarea.png")
    with open("reporte_prueba_login_crear.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error:", e)

finally:
    time.sleep(2)
    driver.quit()