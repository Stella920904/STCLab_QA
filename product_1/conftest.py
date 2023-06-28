import pytest
from selenium import webdriver
from contextlib import contextmanager
from selenium.webdriver.common.by import By
import datetime
import time 
from dotenv import load_dotenv
from browser_setup import browser
import os

# 환경 변수 불러오기 (테스트 세팅값 불러오기)
load_dotenv()
test_url = os.getenv("TEST_URL")
test_login_id = os.getenv("LOGIN_ID")
test_login_pw = os.getenv("LOGIN_PW")


# 재사용되는 페이지들 !!
# scope가 모듈일 경우 모듈 단위로 재사용함.
@pytest.fixture(scope="module")
def browser_with_login(browser):
    console_url = test_url
    login_id = test_login_id
    login_pw = test_login_pw
    
    browser.get(console_url)
    browser.find_element(By.NAME, 'email').send_keys(login_id)
    browser.find_element(By.NAME, 'password').send_keys(login_pw)
    browser.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div/form/button').click()
    
    time.sleep(3)
    
    yield browser


# 아래는 테스트 관련 설정!!
# 딱히 수정안해도 됨

# 스크린샷 파일 명 설정 (Test Case 함수 명으로)
@pytest.fixture(scope="function", autouse=True)
def error_file_path(request):
    file_path = f'./screenshots/{datetime.datetime.now().strftime("%m%d%H%M")}_{request.node.name}.png'
    yield file_path

# Assert 에러(검증 코드가 틀렸을때) OR 코드 자체 에러 (html 요소가 없을 때 등) fail 처리
@contextmanager
def handle_fail(browser, error_file_path):
    try:
        yield
    except AssertionError:
        print(error_file_path)
        browser.save_screenshot(error_file_path)
        pytest.fail("Assertion error occurred")
    except Exception:
        browser.save_screenshot(error_file_path)
        pytest.fail("Exception occurred")