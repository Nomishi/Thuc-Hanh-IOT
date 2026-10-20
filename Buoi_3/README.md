# Thực hành lập trình Python với giao thức CoAP

## 1. Thông tin nhóm thực hiện

| Họ tên | Mã sinh viên | Lớp |
|---|---|---|
| Nguyễn Hoàng Nam | B23DCCN584 | D23CNPM05 |
| Nguyễn Khánh Linh | B23DCCN486 | D23CNPM05 |
| Lê Hiển Long | B23DCCN500 | D23CNPM04 |

## 2. Cấu trúc thư mục

```
Thuc-Hanh-IOT/
└── Buoi_3/
    ├── bai1/
    │   ├── coap_server_bai1.py
    │   └── coap_client_bai1.py
    ├── bai2/
    │   ├── sensor_server_bai2.py
    │   └── monitor_client_bai2.py
    ├── bai3/
    │   ├── light_server_bai3.py
    │   ├── light_controller_bai3.py
    │   └── light_monitor_bai3.py
    └── README.md
```

## 3. Phiên bản Python và thư viện

- Python 3.10 trở lên
- `aiocoap` 0.4.17

CoAP chạy trên UDP (cổng mặc định 5683), **không cần cài MQTT Broker hay RabbitMQ**. Server và Client đều do nhóm tự viết bằng Python.

## 4. Cài đặt môi trường

```
python -m pip install aiocoap
```

Kiểm tra: `python -m pip show aiocoap` (hiện `Name: aiocoap`).

## 5. Địa chỉ IP, cổng và URI các tài nguyên

| Bài | Tài nguyên | URI | Phương thức |
|---|---|---|---|
| 1 | Thông điệp | `coap://127.0.0.1:5683/iot/lab/message` | GET, POST |
| 2 | Cảm biến sensor01 | `coap://127.0.0.1:5683/iot/lab/sensor01/data` | GET |
| 3 | Đèn light01 | `coap://127.0.0.1:5683/iot/lab/light01/status` | GET, PUT, Observe |

- Giao thức: CoAP over UDP, cổng `5683`.
- Địa chỉ mặc định là `127.0.0.1` (máy local), tương đương `localhost`. Nhóm dùng `127.0.0.1` thay cho `localhost` vì trên Windows `localhost` có thể được phân giải thành IPv6 (`::1`) trong khi Server lắng nghe trên IPv4, dẫn đến Client không kết nối được.
- Trên Windows, Server phải bind vào một địa chỉ IP cụ thể (không dùng `0.0.0.0`), nên biến `HOST` ở đầu mỗi file Server được đặt là `127.0.0.1`.

### Chạy Server và Client trên hai máy khác nhau

1. Trong file Server, đổi `HOST` thành địa chỉ IP của máy chạy Server (ví dụ `192.168.1.10`).
2. Trong file Client, đổi `SERVER` thành cùng địa chỉ IP đó.
3. Trên máy chạy Server, mở tường lửa cho **UDP cổng 5683** (Windows Defender Firewall, Inbound Rules, New Rule, Port, UDP, 5683).

## 6. Cách chạy từng chương trình

Mỗi chương trình chạy trong một terminal riêng, đứng trong thư mục tương ứng (bắt đầu từ thư mục `Buoi_3`). **Chạy Server trước, Client sau.** Bấm `Ctrl+C` để dừng.

### Bài 1: Gửi và nhận thông điệp CoAP cơ bản

```
cd bai1
python coap_server_bai1.py        # terminal 1
python coap_client_bai1.py        # terminal 2
```

- Server cung cấp tài nguyên `/iot/lab/message`: GET trả lời chào, POST nhận thông điệp và hiển thị nội dung cùng thời điểm nhận.
- Client gửi GET, sau đó gửi POST 3 lần liên tiếp (mỗi thông điệp chứa họ tên và mã sinh viên của cả 3 thành viên), rồi GET lại để nhận thông điệp POST gần nhất.
- Client còn thử truy cập tài nguyên không tồn tại (nhận mã `4.04 Not Found`) và xử lý lỗi khi Server không hoạt động (timeout hoặc lỗi kết nối).

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

```
cd bai2
python sensor_server_bai2.py      # terminal 1
python monitor_client_bai2.py     # terminal 2
```

- Server tự cập nhật dữ liệu cảm biến mỗi 3 giây (nhiệt độ ngẫu nhiên 25 đến 40 °C, độ ẩm 30 đến 80 %). GET trả về JSON với `Content-Format: application/json`:
  ```json
  {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2, "timestamp": "10:20:03"}
  ```
- Client gửi GET mỗi 3 giây, hiển thị mã thiết bị, nhiệt độ, độ ẩm, thời điểm nhận và cảnh báo:
  - Nhiệt độ > 35 °C: `CANH BAO: Nhiet do cao`
  - Độ ẩm < 40 %: `CANH BAO: Do am thap`
  - Không vi phạm: `Trang thai: Binh thuong`
- Khi bấm Ctrl+C, Client in số lần GET thành công và thời gian phản hồi trung bình. Khi Server không phản hồi, Client báo lỗi và tiếp tục thử lại.

### Bài 3: Giám sát và điều khiển đèn thông minh bằng CoAP Observe

Mở 3 terminal (cùng trong thư mục `bai3`), chạy Server trước, sau đó Monitor, cuối cùng Controller:

```
cd bai3
python light_server_bai3.py       # terminal 1
python light_monitor_bai3.py      # terminal 2
python light_controller_bai3.py   # terminal 3
```

- **Server** (`light_server_bai3.py`): tài nguyên `/iot/lab/light01/status` hỗ trợ GET, PUT và Observe. Trạng thái ban đầu `OFF`. PUT nhận payload:
  ```json
  {"device_id": "light01", "command": "ON"}
  ```
  Khi trạng thái **thực sự thay đổi**, Server cập nhật và thông báo cho tất cả Client đang Observe. Lệnh khác `ON`/`OFF`, payload sai định dạng hoặc sai mã thiết bị bị từ chối bằng mã `4.00 Bad Request`.
- **Controller** (`light_controller_bai3.py`): nhập `ON`, `OFF` (gửi PUT), `STATUS` (gửi GET) hoặc `EXIT`; nhập lệnh khác sẽ báo lỗi.
- **Monitor** (`light_monitor_bai3.py`): đăng ký CoAP Observe (`observe=0`), nhận trạng thái ban đầu và mọi thông báo thay đổi tiếp theo, hiển thị mã thiết bị, trạng thái và thời điểm nhận. Chương trình **không dùng vòng lặp GET** để phát hiện thay đổi. Có thể chạy nhiều Monitor cùng lúc, tất cả đều nhận thông báo.

## 7. Kết quả đạt được

- **Bài 1:** Server chạy và xử lý đúng GET (`2.05 Content`) và POST (`2.04 Changed`), hiển thị nội dung và thời điểm nhận. Client nhận và hiển thị đúng mã phản hồi, payload; xử lý được tài nguyên không tồn tại (`4.04 Not Found`) và lỗi kết nối khi Server không chạy.
- **Bài 2:** Server cập nhật dữ liệu mỗi 3 giây, trả JSON đúng định dạng kèm Content-Format `application/json`. Client truy vấn định kỳ, phân tích JSON, hiển thị đầy đủ thông tin và cảnh báo đúng điều kiện ngưỡng, thống kê số lần GET và thời gian phản hồi trung bình.
- **Bài 3:** Server quản lý tài nguyên đèn, PUT đổi trạng thái đúng lệnh, chỉ thông báo Observe khi trạng thái thay đổi, từ chối lệnh không hợp lệ. Controller điều khiển được đèn bằng ON/OFF/STATUS. Monitor đăng ký Observe thành công và tự động nhận thông báo (không dùng polling); nhiều Monitor nhận thông báo đồng thời.

## 8. Log minh chứng chương trình hoạt động

### Bài 1

Client:

```
CoAP Client
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message

Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server

Sending POST request...
Payload: Xin chao tu CoAP Client - B23DCCN584 - Nguyen Hoang Nam | B23DCCN486 - Nguyen Khanh Linh | B23DCCN500 - Le Hien Long - lan 1

Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep

...

Sending GET request toi tai nguyen khong ton tai...
URI: coap://127.0.0.1:5683/iot/lab/khong_ton_tai

Response:
Code: 4.04 Not Found
Payload:
```

Server:

```
CoAP Server started on port 5683
Resource: coap://127.0.0.1:5683/iot/lab/message
Bam Ctrl+C de dung.

GET request received: /iot/lab/message

POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN584 - Nguyen Hoang Nam | B23DCCN486 - Nguyen Khanh Linh | B23DCCN500 - Le Hien Long - lan 1
Time: 03:48:28
```

### Bài 2

Client (Monitoring):

```
[03:49:04] Received sensor data

Device: sensor01
Temperature: 26.2 C
Humidity: 39.8 %

CANH BAO: Do am thap

------------------------------

[03:49:10] Received sensor data

Device: sensor01
Temperature: 35.4 C
Humidity: 35.0 %

CANH BAO: Nhiet do cao
CANH BAO: Do am thap

------------------------------

[03:49:13] Received sensor data

Device: sensor01
Temperature: 33.7 C
Humidity: 52.8 %

Trang thai: Binh thuong
```

### Bài 3

Server:

```
CoAP Smart Light Server started...
Resource: /iot/lab/light01/status (coap://127.0.0.1:5683)

New Observe registration received

PUT request received:
Device: light01
Command: ON
Light state changed: OFF -> ON
Notify observers: ON

PUT request received:
Device: light01
Command: OFF
Light state changed: ON -> OFF
Notify observers: OFF
```

Controller:

```
Nhap lenh (ON/OFF/STATUS/EXIT): ON

Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01

Nhap lenh (ON/OFF/STATUS/EXIT): STATUS

Sending GET request...
Response:
{"device_id":"light01","status":"ON"}
```

Monitor:

```
Registering CoAP Observe...
Observe registration successful

[03:49:30] Initial State
Device: light01
Status: OFF

[03:49:33] State Updated
Device: light01
Status: ON

[03:49:36] State Updated
Device: light01
Status: OFF
```