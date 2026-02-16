def kiem_tra_dang_nhap (username, password):
    print(f"Dang mo trinh duyet...")
    print(f"Nhap tai khoan: {username}")
    print(f"Nhap mat khau: {password}")
    # Logic kiem tra se nam o day
    print(f"Xac nhan dang nhap thanh cong!")

# Su dung ham nay cho nhieu tai khoan khac nhau
kiem_tra_dang_nhap("admin_01", "pass123")
kiem_tra_dang_nhap("user_test", "qwerty")