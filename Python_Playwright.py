# from playwright.sync_api import sync_playwright
#
# def run():
#     # Khởi tạo Playwright và mở trình duyệt Chromium (giống Chrome)
#     with sync_playwright() as p:
#         # headless=False giúp bạn quan sát được trình duyệt chạy thực tế
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#
#         # 1. Đi tới trang Google
#         print("Đang truy cập Google...")
#         page.goto("https://www.google.com")
#
#         # 2. Tìm ô tìm kiếm và nhập nội dung
#         # Trong Playwright, ta có thể tìm theo thuộc tính 'name' của ô input
#         page.locator("id=APjFqb").fill("Playwright Python")
#         page.wait_for_timeout(3000)
#         # 3. Nhấn phím Enter để tìm kiếm
#         page.keyboard.press("Enter")
#
#         # Đợi một chút để xem kết quả
#         page.wait_for_timeout(3000)
#
#         print("Hoàn thành bài test!")
#         browser.close()
#
#
# if __name__ == "__main__":
#     run()
#


import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill("tomsmith")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("SuperSecretPassword!")
    page.get_by_role("button", name=" Login").click()
    # Thêm dòng này vào cuối kịch bản đăng nhập, sau khi nhấn Login
    # Kiểm tra xem có chuyển hướng đến trang 'secure' hay không
    expect(page).to_have_url(re.compile(".*secure"))
    # Kiểm tra xem thông báo thành công có hiển thị không
    success_message = page.locator("#flash")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("You logged into a secure area!")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
