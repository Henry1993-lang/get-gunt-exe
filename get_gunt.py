from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import time

# ログインURL
LOGIN_URL = "http://133.63.95.163/CycloOrdering2009/Login.aspx"

# 環境に合わせてパスを修正
driver_path = r'C:\Program Files\Mozilla Firefox\geckodriver.exe'
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

options = Options()
options.binary_location = firefox_binary_path
# options.add_argument("--headless")  # 必要に応じて

service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get(LOGIN_URL)

    # 正しいIDで、ユーザー名欄が現れるまで待つ
    user_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Login1_UserName"))
    )
    user_input.send_keys("nengaki")
    driver.find_element(By.ID, "Login1_Password").send_keys("nengaki")
    driver.find_element(By.ID, "Login1_LoginButton").click()

    # ログイン後、スケジュールバーが出現するまで待つ
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scheduleBar"))
        )
    except Exception as e:
        print(f"スケジュールバーの出現待機中にエラーが発生しました: {e}")
        with open("after_login_error.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        exit()

    # ログイン後のHTMLを保存
    with open("after_login.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("ログイン後のHTMLを 'after_login.html' に保存しました。手動で確認してください。")

    # ガントバー情報を取得・表示
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    bars = soup.find_all("div", class_="scheduleBar")

    print("\n▼ ガントバー内の内容 ▼")
    if not bars:
        print("「scheduleBar」クラスを持つ要素が見つかりませんでした。")
    else:
        for i, bar in enumerate(bars, 1):
            title = bar.get("title", "").strip()
            texts = [div.get_text(strip=True) for div in bar.find_all("div")]
            print(f"■ ガントバー{i}")
            if title:
                print(f"  申込者情報: {title}")
            if texts:
                print(f"  内容: {' / '.join(texts)}")
            else:
                print("  内容: (テキストなし)")

except Exception as e:
    print(f"スクリプト実行中に予期せぬエラーが発生しました: {e}")
    with open("login_error.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
finally:
    driver.quit()
