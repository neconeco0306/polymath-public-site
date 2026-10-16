"""Anonymous desktop/mobile Chrome smoke tests for the actual public Render site."""
from __future__ import annotations
import json
import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

BASE = "https://polymath-research-jp.onrender.com"
OUT = Path("browser-audit-screenshots")


def chrome_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--hide-scrollbars")
    binary = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if binary:
        opts.binary_location = binary
    driver_locations = [
        shutil.which("chromedriver"),
        "/usr/local/share/chromedriver-linux64/chromedriver",
        os.environ.get("CHROMEWEBDRIVER", "") + "/chromedriver",
    ]
    path = next((p for p in driver_locations if p and Path(p).is_file()), None)
    return webdriver.Chrome(service=Service(executable_path=path) if path else Service(), options=opts)


def assert_true(value, message):
    if not value:
        raise AssertionError(message)


def run():
    OUT.mkdir(exist_ok=True)
    browser = chrome_driver()
    checks = []
    try:
        for width, height in ((320, 820), (390, 844), (768, 950), (1440, 900)):
            browser.set_window_size(max(width, 500), height)
            browser.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": height, "deviceScaleFactor": 1, "mobile": width <= 768
            })
            browser.get(BASE + "/?qa=1")
            WebDriverWait(browser, 20).until(
                lambda d: d.find_element(By.ID, "research-index").is_displayed()
            )
            metrics = browser.execute_script("""
                return {
                  inner: innerWidth,
                  document: document.documentElement.scrollWidth,
                  body: document.body.scrollWidth,
                  client: document.documentElement.clientWidth,
                  items: document.querySelectorAll('.catalog-item').length,
                  links: [...document.querySelectorAll('a')].filter(a=>a.href.includes('github.com')).length
                };
            """)
            assert_true(metrics["items"] == 15, f"missing research entries at {width}: {metrics}")
            assert_true(metrics["links"] >= 1, f"missing GitHub link at {width}")
            assert_true(metrics["document"] <= metrics["inner"] + 3, f"horizontal overflow at {width}: {metrics}")
            assert_true(metrics["body"] <= metrics["inner"] + 3, f"body overflow at {width}: {metrics}")
            root = browser.find_element(By.ID, "root-btn")
            browser.execute_script("arguments[0].scrollIntoView({block:'center'})", root)
            geometry = browser.execute_script("const r=arguments[0].getBoundingClientRect(); return {top:r.top,bottom:r.bottom,viewport:innerHeight,scroll:scrollY}", root)
            print(f"DEBUG demo button {width}px {geometry}",flush=True)
            assert_true(geometry["top"]>=0 and geometry["bottom"]<=geometry["viewport"]+2, f"button outside viewport: {geometry}")
            root.click()
            assert_true(browser.find_element(By.ID, "declared-count").text == "1", "source demo click failed")
            reset = browser.find_element(By.ID, "naive-btn")
            browser.execute_script("arguments[0].scrollIntoView({block:'center'})", reset)
            reset.click()
            assert_true(browser.find_element(By.ID, "declared-count").text == "13", "source reset click failed")
            path = OUT / f"homepage-{width}.png"
            browser.save_screenshot(str(path))
            checks.append({"page": "/", "viewport": width, "research_items": metrics["items"], "overflow": False, "buttons": "pass"})
            print(f"PASS live homepage {width}px / 15 research items / no horizontal overflow / buttons",flush=True)

        for name, first, second in (
            ("kepler-227", "real", "wrong"),
            ("period-search", "both", "validation"),
        ):
            browser.set_window_size(500, 844)
            browser.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
                "width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True
            })
            browser.get(BASE + "/experiments/" + name + ".html?qa=1")
            WebDriverWait(browser, 20).until(lambda d: d.find_element(By.ID, second).is_displayed())
            button = browser.find_element(By.ID, second)
            browser.execute_script("arguments[0].scrollIntoView({block:'center'})", button)
            button.click()
            assert_true(browser.find_element(By.ID, second).get_attribute("aria-pressed") == "true", name + " toggle did not activate")
            button = browser.find_element(By.ID, first)
            browser.execute_script("arguments[0].scrollIntoView({block:'center'})", button)
            button.click()
            assert_true(browser.find_element(By.ID, first).get_attribute("aria-pressed") == "true", name + " toggle did not reset")
            errors = browser.execute_script("return {width:innerWidth,doc:document.documentElement.scrollWidth}")
            assert_true(errors["doc"] <= errors["width"]+3, name + " overflows phone screen")
            browser.save_screenshot(str(OUT / (name + "-390.png")))
            checks.append({"page": name, "viewport": 390, "overflow": False, "buttons": "pass"})
            print(f"PASS live {name} 390px / no overflow / interactive toggle",flush=True)

        (OUT / "result.json").write_text(json.dumps(checks, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
        print("PASS 6 live browser scenarios",flush=True)
    finally:
        browser.quit()


if __name__ == "__main__":
    run()
