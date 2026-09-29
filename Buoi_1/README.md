# Thực hành lập trình Python với giao thức MQTT

## Thành viên nhóm

| Họ tên | Mã sinh viên | Lớp |
|---|---|---|
| Nguyễn Hoàng Nam | B23DCCN584 | D23CNPM05 |
| Nguyễn Khánh Linh | B23DCCN486 | D23CNPM05 |
| Lê Hiển Long | B23DCCN500 | D23CNPM04 |

## Cấu trúc thư mục

```
Thuc-Hanh-IOT/
└── Buoi_1/
    ├── publisher_bai1.py
    ├── subscriber_bai1.py
    ├── sensor_publisher_bai2.py
    ├── monitor_subscriber_bai2.py
    ├── device_bai3.py
    ├── controller_bai3.py
    └── README.md
```

## Broker sử dụng

**Eclipse Mosquitto 2.1.2** chạy local:

- Host: `localhost`
- Port: `1883`

### Cài đặt và cấu hình broker

**Windows**

1. Tải bản cài đặt tại https://mosquitto.org/download và cài đặt bình thường.
2. Mosquitto tự chạy như một Windows service. Kiểm tra bằng lệnh `sc query mosquitto`, thấy `STATE: RUNNING` là broker đang chạy.
3. Nếu service chưa chạy, mở cmd bằng quyền Administrator và gõ `net start mosquitto`.

**Linux (Ubuntu/Xubuntu)**

```
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

**Ghi chú cấu hình:** Mosquitto 2.x mặc định chạy ở chế độ "local only", chỉ nhận kết nối từ chính máy đang chạy broker. Chế độ này đủ cho bài thực hành vì toàn bộ chương trình chạy trên cùng một máy, nên không cần sửa file `mosquitto.conf`.

**Kiểm tra broker hoạt động:** mở 2 terminal.

```
mosquitto_sub -h localhost -t iot/lab/message
mosquitto_pub -h localhost -t iot/lab/message -m "test"
```

Terminal đầu hiện `test` là broker hoạt động bình thường.

Nếu muốn dùng broker khác, chỉ cần sửa hai biến `BROKER` và `PORT` ở đầu mỗi file `.py`.

## Yêu cầu môi trường

- Python 3.x
- Thư viện `paho-mqtt` 2.x

```
pip install paho-mqtt
```

Code dùng `mqtt.CallbackAPIVersion.VERSION2` của paho-mqtt 2.x. Nếu dùng paho-mqtt 1.x thì phải sửa lại cách khởi tạo client và chữ ký hàm `on_connect`.

## Cách chạy

Từ thư mục gốc của repo, di chuyển vào thư mục bài làm:

```
cd Buoi_1
```

Mỗi chương trình chạy trong một terminal riêng. Luôn chạy phía **nhận** (subscriber, monitor, device) **trước**, phía **gửi** sau. Bấm `Ctrl+C` để dừng chương trình chạy liên tục.

### Bài 1: Gửi và nhận thông điệp cơ bản

Topic: `iot/lab/message`

```
python subscriber_bai1.py
python publisher_bai1.py
```

- `publisher_bai1.py` gửi 3 thông điệp, mỗi thông điệp gồm lời chào, mã sinh viên và họ tên của một thành viên trong nhóm.
- `subscriber_bai1.py` chạy liên tục, mỗi khi nhận tin thì in ra Topic, Payload và Time.

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

Topic: `iot/lab/sensor01/data`

```
python monitor_subscriber_bai2.py
python sensor_publisher_bai2.py
```

- `sensor_publisher_bai2.py` gửi dữ liệu mỗi 3 giây, payload dạng JSON:
  ```json
  {"device_id": "sensor01", "temperature": 28.5, "humidity": 65.2}
  ```
  Nhiệt độ sinh ngẫu nhiên trong khoảng 25 đến 40 °C, độ ẩm trong khoảng 30 đến 80 %.
- `monitor_subscriber_bai2.py` in dữ liệu nhận được và cảnh báo:
  - Nhiệt độ > 35 °C: `CANH BAO: Nhiet do cao`
  - Độ ẩm < 40 %: `CANH BAO: Do am thap`

### Bài 3: Điều khiển đèn thông minh

Topic: `iot/lab/light01/cmd` (lệnh) và `iot/lab/light01/status` (trạng thái)

```
python device_bai3.py
python controller_bai3.py
```

- `device_bai3.py` (đèn) subscribe topic `cmd`. Nhận `ON` hoặc `OFF` thì đổi trạng thái và publish trạng thái mới lên topic `status`, dạng:
  ```json
  {"device_id":"light01","status":"ON"}
  ```
  Lệnh không hợp lệ bị bỏ qua. Khi khởi động, thiết bị gửi trạng thái ban đầu (`OFF`).
- `controller_bai3.py` cho nhập lệnh từ bàn phím (`ON`, `OFF`, `EXIT`), publish lên topic `cmd`, đồng thời subscribe topic `status` để hiển thị trạng thái đèn. Nhập sai lệnh thì báo lỗi, nhập `EXIT` để thoát.

## Kết quả đạt được

- **Bài 1:** publisher gửi đúng topic, subscriber nhận đúng dữ liệu và hiển thị rõ Topic, Payload, Time. Subscriber chạy liên tục đến khi bấm Ctrl+C, publisher gửi nhiều thông điệp liên tiếp.
- **Bài 2:** cảm biến gửi JSON tuần hoàn mỗi 3 giây, monitor phân tích được dữ liệu và cảnh báo đúng điều kiện ngưỡng.
- **Bài 3:** điều khiển được thiết bị qua MQTT, thiết bị phản hồi đúng trạng thái, giao tiếp hai chiều thông qua hai topic `cmd` và `status`. Có xử lý lệnh sai và lệnh `EXIT`.

## Mô hình tổ chức topic

Dữ liệu được tổ chức theo mô hình thiết bị, topic, payload:

| Thiết bị | Topic | Chiều | Payload |
|---|---|---|---|
| Thông điệp chung | `iot/lab/message` | publisher → subscriber | Chuỗi văn bản |
| sensor01 | `iot/lab/sensor01/data` | sensor → monitor | JSON nhiệt độ, độ ẩm |
| light01 | `iot/lab/light01/cmd` | controller → đèn | `ON` / `OFF` |
| light01 | `iot/lab/light01/status` | đèn → controller | JSON trạng thái |