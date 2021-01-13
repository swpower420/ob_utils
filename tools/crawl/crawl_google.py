from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import json
import urllib3
import os
from concurrent.futures import ProcessPoolExecutor

from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor

retries = urllib3.Retry(connect=5, read=2, redirect=5)
http = urllib3.PoolManager(retries=retries)


def norm_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    return path


def save_image_src(src, path, name, ext):
    path = norm_path(path)
    print(path)

    if not os.path.isdir(path):
        os.mkdir(path)

    req = http.request('GET', src, timeout=3)
    raw_img = req.data

    save_path = os.path.join(path, '{}.{}'.format(name, ext))
    with open(save_path, "wb") as f:
        f.write(raw_img)

    print(save_path)


def main(res_dir, webdriver_path, keyword):
    # https://selenium-python.readthedocs.io/api.html?highlight=location_once_scrolled_into_view#module-selenium.webdriver.common.touch_actions
    driver = webdriver.Chrome(webdriver_path)

    driver.implicitly_wait(3)

    driver.get('https://www.google.co.kr/imghp')
    driver.find_element_by_name('q').send_keys(keyword)

    btn_search = driver.find_elements_by_xpath('//button[@aria-label="Google 검색"]')[0]
    btn_search.click()
    time.sleep(1)

    driver.implicitly_wait(3)
    action = ActionChains(driver)

    executor = ThreadPoolExecutor(max_workers=3)

    idx_last = 0
    cnt = 0
    while True:
        if cnt == 5:
            exit()

        find_result = driver.find_elements_by_class_name("mode-cell thumb")
        find_result = find_result[idx_last:]
        idx_last += len(find_result)

        print(find_result)
        for e in find_result:
            img_src = json.loads(e.get_attribute('innerHTML'))["ou"]
            img_ext = json.loads(e.get_attribute('innerHTML'))["ity"]
            # save_image_src(img_src, './save', str(time.time_ns()), img_ext)
            executor.submit(save_image_src, res_dir, keyword, str(time.time()), img_ext)

        action.send_keys(Keys.PAGE_DOWN).perform()

        isShowBottom = driver.find_element_by_id("fbarcnt").is_displayed()  # 마지막 바닥 요소
        isShowMoreButton = driver.find_element_by_id('smb').is_displayed()  # 버튼 요소

        if isShowMoreButton:
            time.sleep(1)
            driver.find_element_by_id('smb').click()

        if isShowBottom and not isShowMoreButton:
            # 마지막 바닥과 버튼 요소가 보이지 않으므로 검색이 끝난것으로 판단하고 종료
            exit()

        cnt += 1


if __name__ == '__main__':
    keyword = ''
    # webdriver = 'notebook/web/chromedriver'
    webdriver_path = "test/chromedriver_win32/chromedriver.exe"
    res_dir = "google크롤링/test"

    if not os.path.isdir(res_dir):
        os.mkdir(res_dir)

    main(res_dir, webdriver_path=webdriver_path, keyword=keyword)