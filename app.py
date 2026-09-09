from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from screeninfo import get_monitors
import subprocess
import json
import time
import sys
import logging
import re
logging.basicConfig(
    filename="app.log", 
    filemode="a", 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO 
)
def Locate(driver, selector):
    try:
        object = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"{selector}"))
        )
    except:
        object = False
    return object
def ClearLines(lines):
        for i in range(lines):
            sys.stdout.write("\033[1A\033[2K\r")
        sys.stdout.flush()
def Clicking(driver, object):
            try:
                object.click()
            except:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", object)
                    object.click()
                except:
                    driver.execute_script("arguments[0].click();", object)
def Timer(timerObject):
        objectTime = timerObject.get_attribute("textContent").strip()
        hours_match = re.search(r'(\d+)h', objectTime)
        mins_match = re.search(r'(\d+)m', objectTime)
        secs_match = re.search(r'(\d+)s', objectTime)
        hours = int(hours_match.group(1)) if hours_match else 0
        minutes = int(mins_match.group(1)) if mins_match else 0
        seconds = int(secs_match.group(1)) if secs_match else 0
        time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return time
def CountDown(countObject, message):
        Timeremaining = countObject - datetime.now()
        TimeSeconds = int(Timeremaining.total_seconds())
        h = TimeSeconds // 3600
        m = (TimeSeconds % 3600) // 60
        s = TimeSeconds % 60
        if h > 0:
            sys.stdout.write(f"\r{message}: {h:02d}h {m:02d}m {s:02d}s" + " " * 10)
        elif m > 0:
            sys.stdout.write(f"\r{message}: {m:02d}m {s:02d}s" + " " * 10)
        else:
            sys.stdout.write(f"\r{message}: {s:02d}s" + " " * 10)
        sys.stdout.flush()
def ReturnToHome(driver):
        time.sleep(2)
        driver.get("https://firefaucet.win")
        time.sleep(2)
def Main():
    currency = False
    booster = False
    print("\033[?25l")
    ClearLines(1)
    while True:
        try:
            if not currency:
                while True:
                    try:
                        print("the following are the currencies available at https://firefaucet.win\n")
                        currencies = ["btc","bnb","usdt","ada","eth","doge","ltc","dash","trx","nano","xmr","zec","dgb","sol","usdc","xrp"]
                        for i, coin in enumerate(currencies, start=1):
                            print(f"{i}. {coin.upper()}")
                        userInput = input("\nPlease enter number of currency you like to claim (1-16): ")
                        if userInput.isdigit() and 1 <= int(userInput) <= len(currencies):
                            choice = int(userInput) - 1
                            currency = currencies[choice]
                            break
                        else:
                            print("invaild input. please try again and enter a number (1-16).")
                            time.sleep(2)
                            ClearLines(1)
                    except:
                        time.sleep(1)
                    finally:
                        ClearLines(20)
            if not booster:
                while True:
                    try:
                        print("the following options are how faster you want to earn your currency\n")
                        boosts = ["1x", "2x", "3x", "4x"]
                        boostsText = ["slowest currency earn, but fastest level up", "slow currency earn, but fast level up", "fast currency earn, but slow level up", "fastest currency earn, but slowest level up"]
                        for i, boost in enumerate(boosts, start=1):
                            print(f"{boost} {boostsText[i-1]}")
                        userInput2 = input("\nPlease enter number of boost you like to claim (1-4): ")
                        if userInput2.isdigit() and 1 <= int(userInput2) <= len(boosts):
                            choice = int(userInput2) - 1
                            booster = boosts[choice]
                            break
                        else:
                            print("invaild input. please try again and enter a number (1-4).")
                            time.sleep(2)
                            ClearLines(1)
                    except:
                        time.sleep(1)
                    finally:
                        ClearLines(8)
            print("\033[1mAutomation running. \033[3mKeep this window open.\033[23m\033[22m")
            with open('config.json', 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)
            if len(get_monitors()) > 1:
                position = "2045,0"
            else:
                position = "0,0"
            chrome = subprocess.Popen([config["chrome"], f"--user-data-dir={config["profile"]}", f"--remote-debugging-port={config["port"]}", "--disable-gpu", "--disable-dev-shm-usage", "--window-size=300,300", f"--window-position={position}"])
            options = Options()
            options.add_experimental_option("debuggerAddress", f"127.0.0.1:{config["port"]}")
            driver = webdriver.Chrome(options=options)
            driver.get("https://firefaucet.win/login/")
            time.sleep(5)
            while True:
                if driver.current_url == "https://firefaucet.win/login/":
                    username = Locate(driver, "#username")
                    username.send_keys(Keys.CONTROL + "a")
                    username.send_keys(Keys.DELETE)
                    username.send_keys(config["username"])
                    password = Locate(driver, "#password")
                    password.send_keys(Keys.CONTROL + "a")
                    password.send_keys(Keys.DELETE)
                    password.send_keys(config["password"])
                    loginBtn = Locate(driver, "button[value='Login']")
                    Clicking(driver, loginBtn)
                    time.sleep(2)
                else:
                    break
            claims = 0
            daily = Locate(driver, "a[href='/daily']")
            if "available" in daily.get_attribute("class"):
                Clicking(driver, daily)
                while True:
                    dailyBtn = Locate(driver, "button.daily-claim-btn")
                    Clicking(driver, dailyBtn)
                    try:
                        dailyWon = Locate(driver, "#won")
                        dailyWonText = dailyWon.get_attribute("textContent")
                        dailyWonValue = dailyWonText.split()
                        if int(dailyWonValue[0]) > 0:
                            break
                    except:
                        pass
                    time.sleep(1)
                ReturnToHome(driver)
            faucet = Locate(driver, "#faucet_btn")
            faucetText = faucet.get_attribute("textContent")
            if "Ready" in faucetText:
                Clicking(driver, faucet)
                faucetTitle = Locate(driver, ".faucet-title")
                if "Reward Claimed" in faucetTitle.text:
                    ReturnToHome(driver)
                else:
                    while True:
                        faucetBtn = Locate(driver, "#faucet-submit-btn")
                        Clicking(driver, faucetBtn)
                        faucetWon = Locate(driver, "#faucet-won")
                        faucetWonText = faucetWon.get_attribute("textContent")
                        faucetWonValue = faucetWonText.split()
                        if int(faucetWonValue[0]) > 0:
                            break
                        time.sleep(1)
                    ReturnToHome(driver)
            elif "(Limit Reached)" in faucetText:
                claims = 1
            if claims >= 1:
                targetTime = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
                targetMessage = "Max daily claims reached. Refresh in"
            else:
                target = Locate(driver, ".faucet-timer-display")
                targetTime = datetime.now() + Timer(target)
                targetMessage = "Next claim in"
            taskBadge = Locate(driver, "#data__tasks_available_to_collect")
            if int(taskBadge.get_attribute("textContent").strip()) > 0:
                taskBtn = Locate(driver, "a[href='/tasks/']")
                Clicking(driver, taskBtn)
                tasksToCollect = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dt-section__grid button.task-card__action--ready"))
                )
                for i, task in enumerate(tasksToCollect, start=1):
                    if "ready" in task.get_attribute("class"):
                        Clicking(driver, task)
                        time.sleep(2)
                ReturnToHome(driver)
            autoClaimTime = Locate(driver, ".af-w-timeleft")
            autoClaimTimeText = autoClaimTime.get_attribute("textContent")
            if "Done" in autoClaimTimeText:
                Clicking(driver, autoClaimTime)
                time.sleep(2)
                autoClaimStop = Locate(driver, ".af-stop-btn")
                Clicking(driver, autoClaimStop)
                ReturnToHome(driver)
            else:
                coins = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".coin-chip"))
                )
                for i, coin in enumerate(coins, start=1):
                    if "selected" in coin.get_attribute("class"):
                        Clicking(driver, coin)
                    tag = coin.find_element(By.TAG_NAME, "input")
                    if currency in tag.get_attribute("id"):
                        Clicking(driver, coin)
                time.sleep(2)
                boostCard = Locate(driver, f"#boost_{booster}")
                Clicking(driver, boostCard)
                startBtn = Locate(driver, "#start-button")
                Clicking(driver, startBtn)
                ReturnToHome(driver)
                autoClaimTimeNext = Locate(driver, ".af-w-timeleft")
                timeToWait = Timer(autoClaimTimeNext)
                if timeToWait == timedelta(0):
                    if targetTime == datetime.now().replace(hour=17, minute=0, second=0, microsecond=0):
                        nextTime = datetime.now() + timedelta(minutes=20)
                        nextmessage = "Not enough fuel for auto faucet. Checking again in"
                    else:
                        nextTime = targetTime
                        nextmessage = "Not enough fuel for auto faucet. Waiting for next claim in"
                else:
                    nextTime = datetime.now() + timeToWait + timedelta(minutes=1)
                    nextmessage = "Stopping auto faucet in"
            time.sleep(2)
        except Exception as e:
            logging.exception("An unhandled exception occurred during execution: ")
        finally:
            try:
                driver.quit()
            except: 
                chrome.terminate()
            finally:
                chrome.kill()
            while True:
                currentTime = datetime.now()
                if currentTime >= targetTime:
                    break
                elif currentTime >= nextTime:
                    break
                CountDown(nextTime, nextmessage)
                print("")
                CountDown(targetTime, targetMessage)
                print("\033[2A")
                time.sleep(1)
            print("\033[1B")
            ClearLines(3)
if __name__ == "__main__":
    Main()