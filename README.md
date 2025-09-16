# 💡 Ngân hàng Ý tưởng - Data For Life

Một ứng dụng web được xây dựng bằng Streamlit để tìm kiếm và khám phá các ý tưởng từ cuộc thi "Dữ liệu với Cuộc sống - Data For Life" do Bộ Công an tổ chức.

![Demo ứng dụng](demo.png)

## 📌 Giới thiệu

Dự án này bao gồm hai thành phần chính:
1.  **Một script thu thập dữ liệu (crawler)**: Tự động lấy toàn bộ thông tin các ý tưởng từ trang [idea-bank của Data For Life](https://dataforlife.vn/idea-bank/) và lưu dưới dạng file CSV.
2.  **Một ứng dụng web tìm kiếm**: Cung cấp một giao diện thân thiện, giúp người dùng dễ dàng tìm kiếm, lọc và xem thông tin chi tiết về từng ý tưởng đã thu thập được.

## ✨ Tính năng

-   **Giao diện Tìm kiếm Trực quan**: Dễ dàng tìm kiếm ý tưởng theo bất kỳ từ khóa nào (ví dụ: y tế, giao thông, môi trường, logistics...).
-   **Hiển thị Chi tiết**: Xem thông tin đầy đủ của mỗi ý tưởng bao gồm đề xuất, đối tượng, tác động, bối cảnh... trong một giao diện có thể mở rộng/thu gọn (expander).
-   **Tự động Thu thập Dữ liệu**: Script đi kèm (`scripts/crawl_data.py`) giúp tự động cào và cập nhật dữ liệu mới nhất từ trang web gốc.
-   **Tối ưu hóa Tốc độ**: Sử dụng cache của Streamlit để tăng tốc độ tải dữ liệu sau lần đầu tiên.

## 🛠️ Công nghệ sử dụng

-   **Ngôn ngữ**: Python
-   **Web Framework**: Streamlit
-   **Thu thập dữ liệu**: Requests, BeautifulSoup4
-   **Xử lý dữ liệu**: Pandas

## 📁 Cấu trúc Dự án

```
.
├── data/                  # Thư mục chứa dữ liệu (được .gitignore bỏ qua)
│   └── CSV_dataset.csv
├── scripts/
│   └── crawl_data.py      # Script để thu thập dữ liệu từ website
├── .gitignore             # Các file/thư mục bị Git bỏ qua
├── app.py                 # File ứng dụng Streamlit chính
├── LICENSE                # Giấy phép sử dụng mã nguồn
├── README.md              # File giới thiệu dự án
└── requirements.txt       # Các thư viện Python cần thiết
```

## 🚀 Hướng dẫn Cài đặt và Chạy

Bạn cần có [Python 3.8+](https://www.python.org/downloads/) được cài đặt trên máy.

**1. Clone repository này về máy:**

```bash
git clone https://github.com/hungthikcode/Dataforlife-ideas-search.git
cd TEN_REPO_CUA_BAN
```

**2. (Khuyến khích) Tạo và kích hoạt môi trường ảo:**

```bash
# Đối với Windows
python -m venv venv
.\venv\Scripts\activate

# Đối với macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Cài đặt các thư viện cần thiết:**

```bash
pip install -r requirements.txt
```

**4. Chạy script để thu thập dữ liệu:**

Lần đầu tiên chạy, bạn **bắt buộc** phải chạy script này để tạo file `data/CSV_dataset.csv`. Nếu không có file này, ứng dụng sẽ báo lỗi.

```bash
python scripts/crawl_data.py
```
*Lưu ý: Quá trình này có thể mất vài phút tùy thuộc vào số lượng bài viết và tốc độ mạng của bạn.*

**5. Khởi chạy ứng dụng Streamlit:**

```bash
streamlit run app.py
```

Sau khi chạy lệnh trên, một tab mới trên trình duyệt sẽ tự động mở ra với địa chỉ `http://localhost:8501`. Giờ đây bạn có thể bắt đầu tìm kiếm!

## 📄 Giấy phép

Dự án này được cấp phép theo [Giấy phép MIT](LICENSE). Xem file `LICENSE` để biết thêm chi tiết.