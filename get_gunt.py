from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import time # time.sleepはデバッグ目的で残すこともありますが、基本的にはWebDriverWaitを推奨

# ログインURL
LOGIN_URL = "http://133.63.95.163/CycloOrdering2009/Login.aspx"

# Sele1.8.2.pyのWebDriver設定を適用
# Geckodriverのパスを設定 (あなたの環境に合わせて変更してください)
driver_path = r'C:\Program Files\Mozilla Firefox\geckodriver.exe'
# Firefoxのバイナリパスを設定 (あなたの環境に合わせて変更してください)
firefox_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Firefoxオプションの設定
options = Options()
options.binary_location = firefox_binary_path
# 必要であれば、headlessモードなどでブラウザを非表示で実行できます
# options.add_argument("--headless")

# Geckodriverを指定してサービスを設定
service = Service(executable_path=driver_path)

# Firefox WebDriverを起動
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get(LOGIN_URL)

    # ユーザー名とパスワードを入力してログイン
    driver.find_element(By.ID, "txtUserName").send_keys("nengaki")
    driver.find_element(By.ID, "txtPassword").send_keys("nengaki")
    driver.find_element(By.ID, "btnLogin").click()

    # ログイン後のページが完全にロードされるまで待機
    # scheduleBarクラスの要素が出現するまで最大10秒待つ
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scheduleBar"))
        )
    except Exception as e:
        print(f"スケジュールバーの出現待機中にエラーが発生しました: {e}")
        print("ログイン後のHTMLをファイルに保存します。")
        with open("after_login_error.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.quit()
        exit() # エラーが発生した場合はここで終了

    # ログイン後のHTMLを手動で確認するために保存
    with open("after_login.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("ログイン後のHTMLを 'after_login.html' に保存しました。手動で確認してください。")

    # HTMLを取得してBeautifulSoupでパース
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # scheduleBar内の文字を取得
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
                # 各子divの内容を「 / 」で結合して表示
                print(f"  内容: {' / '.join(texts)}")
            else:
                print("  内容: (テキストなし)")

except Exception as e:
    print(f"スクリプト実行中に予期せぬエラーが発生しました: {e}")
finally:
    driver.quit()
