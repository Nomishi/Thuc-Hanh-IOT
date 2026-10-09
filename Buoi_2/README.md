# Thực hành lập trình Python với giao thức AMQP

## Thành viên nhóm

| Họ tên | Mã sinh viên | Lớp |
|---|---|---|
| Nguyễn Hoàng Nam | B23DCCN584 | D23CNPM05 |
| Nguyễn Khánh Linh | B23DCCN486 | D23CNPM05 |
| Lê Hiển Long | B23DCCN500 | D23CNPM04 |

## Cấu trúc thư mục

```
Thuc-Hanh-IOT/
└── Buoi_2/
    ├── producer_bai1.py
    ├── consumer_bai1.py
    ├── sensor_producer_bai2.py
    ├── monitor_consumer_bai2.py
    ├── alert_producer_bai3.py
    ├── warning_consumer_bai3.py
    ├── critical_consumer_bai3.py
    └── README.md
```

## Broker sử dụng

**RabbitMQ** chạy local bằng **Docker** (image `rabbitmq:management`):

- Host: `localhost`
- Port AMQP: `5672`
- Giao diện quản lý web: http://localhost:15672
- Tài khoản mặc định: `guest` / `guest`

### Cài đặt và cấu hình broker (Docker)

1. **Mở Docker Desktop** và đợi đến khi Docker Engine ở trạng thái đang chạy (Running).
2. **Tải image và tạo container RabbitMQ** (chỉ cần làm một lần):
   ```
   docker pull rabbitmq:management
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
   ```
   Image `management` đã bật sẵn giao diện quản lý, không cần cấu hình thêm.
3. **Kiểm tra broker đang chạy:**
   ```
   docker ps
   ```
   Thấy container `rabbitmq` ở trạng thái `Up` với port `5672` và `15672` là đúng. Đợi khoảng 10 đến 20 giây cho RabbitMQ khởi động xong, sau đó có thể vào http://localhost:15672 (đăng nhập `guest` / `guest`) để xem queue, exchange, binding.
4. **Các lần sau** (sau khi khởi động lại máy hoặc tắt Docker), mở Docker Desktop rồi chạy:
   ```
   docker start rabbitmq
   ```
5. **Dừng và xóa broker** khi không dùng nữa:
   ```
   docker stop rabbitmq
   docker rm rabbitmq
   ```

Cấu hình mặc định (host `localhost`, port `5672`, tài khoản `guest`) đủ dùng cho bài thực hành, không cần sửa file cấu hình.

Nếu dùng broker khác (ví dụ broker dùng chung của lớp), sửa biến `HOST` và `PORT` ở đầu mỗi file `.py` (nếu broker yêu cầu tài khoản riêng thì thêm `credentials` vào `pika.ConnectionParameters`).

## Yêu cầu môi trường

- Python 3.x
- Thư viện `pika`
- Docker Desktop (để chạy RabbitMQ)

```
pip install pika
```

## Cách chạy

Từ thư mục gốc của repo, di chuyển vào thư mục bài làm:

```
cd Buoi_2
```

Mỗi chương trình chạy trong một terminal riêng. Bấm `Ctrl+C` để dừng chương trình chạy liên tục.

### Bài 1: Gửi và nhận message cơ bản qua queue

Queue: `iot_lab_queue`

```
python consumer_bai1.py
python producer_bai1.py
```

- `producer_bai1.py` gửi 3 message liên tiếp, mỗi message gồm lời chào, mã sinh viên và họ tên của cả 3 thành viên trong nhóm.
- `consumer_bai1.py` chạy liên tục, mỗi khi nhận message thì in ra nội dung và thời điểm nhận.

### Bài 2: Mô phỏng cảm biến IoT gửi dữ liệu môi trường

Queue: `sensor_data_queue`

```
python monitor_consumer_bai2.py
python sensor_producer_bai2.py
```

- `sensor_producer_bai2.py` gửi dữ liệu mỗi 3 giây, payload dạng JSON:
  ```json
  {"device_id": "sensor01", "temperature": 29.5, "humidity": 62.1, "timestamp": "14:05:21"}
  ```
  Nhiệt độ sinh ngẫu nhiên trong khoảng 25 đến 40, độ ẩm trong khoảng 30 đến 80. Trường `timestamp` là phần mở rộng (thời gian gửi).
- `monitor_consumer_bai2.py` in mã thiết bị, nhiệt độ, độ ẩm và cảnh báo:
  - Nhiệt độ > 35: `CANH BAO: Nhiet do cao`
  - Độ ẩm < 40: `CANH BAO: Do am thap`

### Bài 3: Điều phối cảnh báo IoT với exchange

Exchange: `iot_alert_exchange` (kiểu `direct`)

Mở 3 terminal, chạy **hai consumer trước**, producer sau cùng:

```
python warning_consumer_bai3.py
python critical_consumer_bai3.py
python alert_producer_bai3.py
```

- `alert_producer_bai3.py` khai báo exchange `iot_alert_exchange` và gửi 3 cảnh báo với routing key `info`, `warning`, `critical`.
- `warning_consumer_bai3.py` tạo queue `warning_queue`, bind với exchange bằng routing key `warning`.
- `critical_consumer_bai3.py` tạo queue `critical_queue`, bind với exchange bằng routing key `critical`.

Lưu ý: phải chạy consumer trước vì queue chỉ nhận được message sau khi đã được bind với exchange. Message `info` không có queue nào bind nên bị broker bỏ đi (đúng với yêu cầu đề bài).

## Kết quả đạt được

- **Bài 1:** producer gửi message vào queue `iot_lab_queue`, consumer nhận và hiển thị đúng nội dung và thời điểm nhận. Consumer chạy liên tục đến khi bấm Ctrl+C.

  ```
  Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN584 - Nguyen Hoang Nam | B23DCCN486 - Nguyen Khanh Linh | B23DCCN500 - Le Hien Long - lan 1
  Thoi gian nhan: 16:23:11
  ```

- **Bài 2:** cảm biến gửi JSON tuần hoàn mỗi 3 giây, consumer phân tích dữ liệu và cảnh báo đúng điều kiện ngưỡng.

  ```
  Device: sensor01
  Temperature: 39.0
  Humidity: 34.4
  CANH BAO: Nhiet do cao
  CANH BAO: Do am thap
  ```

- **Bài 3:** exchange `direct` phân phối message đúng nơi nhận: `warning` chỉ vào `warning_queue`, `critical` chỉ vào `critical_queue`, `info` không queue nào nhận.

  ```
  [warning_queue] Da nhan: Nhiet do phong may vuot nguong muc warning
  [critical_queue] Da nhan: Cam bien kho lanh mat ket noi muc critical
  ```

## Các thành phần AMQP sử dụng

| Thành phần | Vai trò trong bài |
|---|---|
| Producer | Chương trình gửi message (`basic_publish`) |
| Queue | Hàng đợi lưu message (`queue_declare`) |
| Consumer | Chương trình nhận message (`basic_consume`, `basic_ack`) |
| Exchange | Nhận message từ producer và chuyển vào queue (Bài 1, 2 dùng exchange mặc định, Bài 3 dùng `direct` exchange) |
| Routing key | Nhãn để exchange chọn queue (`info`, `warning`, `critical`) |
| Binding | Liên kết queue với exchange theo routing key (`queue_bind`) |