from playwright.sync_api import sync_playwright

def run():
    # Khởi tạo Playwright và mở trình duyệt Chromium (giống Chrome)
    with sync_playwright() as p:
        # headless=False giúp bạn quan sát được trình duyệt chạy thực tế
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Đi tới trang Google
        print("Đang truy cập Google...")
        page.goto("https://www.google.com")

        # 2. Tìm ô tìm kiếm và nhập nội dung
        # Trong Playwright, ta có thể tìm theo thuộc tính 'name' của ô input
        page.locator("id=APjFqb").fill("Playwright Python")

        # 3. Nhấn phím Enter để tìm kiếm
        page.keyboard.press("Enter")

        # Đợi một chút để xem kết quả
        page.wait_for_timeout(3000)

        print("Hoàn thành bài test!")
        browser.close()


if __name__ == "__main__":
    run()

klklklklkioi