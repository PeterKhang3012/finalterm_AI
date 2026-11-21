# Kakuro — Task 3

Bộ giải mô hình hóa Kakuro thành bài toán thỏa mãn ràng buộc (CSP). Chương trình thu hẹp miền giá trị của từng ô, sau đó dùng tìm kiếm theo chiều sâu (DFS) và quay lui khi cần thử nhiều khả năng. Mục tiêu là tìm lời giải đầu tiên. Luật chơi có thể xem tại [Kakuro trên Wikipedia](https://en.wikipedia.org/wiki/Kakuro).

## Biến và điều kiện ràng buộc

- Mỗi ô trắng (`.`) là một biến có tọa độ `(hàng, cột)`, đánh số từ 1. Miền ban đầu của mỗi ô là `{1, 2, ..., 9}`.
- Ô `#` là ô đen. Ô gợi ý có dạng `dọc/ngang`, trong đó `0` biểu thị hướng không có dãy. Một dãy gồm các ô trắng liên tiếp ngay bên dưới hoặc ngay bên phải ô gợi ý.
- Mỗi ô trắng thuộc một dãy ngang và một dãy dọc. Trong mỗi dãy, các chữ số phải khác nhau và tổng của chúng phải bằng số gợi ý. Một chữ số vẫn có thể xuất hiện ở nhiều dãy nếu từng dãy đều thỏa ràng buộc.

## Sinh ứng viên và loại giá trị

Với dãy dài `k` có tổng `S`, `model.py` lấy các tổ hợp `k` chữ số khác nhau từ 1 đến 9, giữ những tổ hợp có tổng bằng `S`, rồi sinh các hoán vị để xét thứ tự điền. Danh sách ứng viên được lưu đệm theo cặp `(k, S)` để các dãy cùng độ dài và tổng dùng lại.

Ở mỗi lượt lan truyền, bộ giải chỉ giữ các ứng viên có từng chữ số nằm trong miền hiện tại của ô tương ứng. Miền mới của mỗi ô gồm đúng các chữ số xuất hiện ở vị trí của ô đó trong ít nhất một ứng viên còn lại. Vì vậy, mỗi giá trị bị loại đều không có cách hoàn thành dãy đang xét với các miền hiện tại.

Ví dụ, dãy hai ô có tổng 4 có hai ứng viên `(1, 3)` và `(3, 1)`. Nếu ràng buộc dọc đã thu hẹp miền ô đầu xuống `{1, 2}`, chỉ `(1, 3)` còn phù hợp. Miền ô đầu trở thành `{1}`, miền ô thứ hai trở thành `{3}`.

Khi miền của một ô thay đổi, dãy giao với ô đó được đưa vào hàng đợi để kiểm tra lại. Quá trình lặp đến khi hàng đợi rỗng hoặc một dãy không còn ứng viên. Cách lọc này duy trì tính nhất quán cung tổng quát (GAC) cho các ràng buộc theo dãy.

## Heuristic MRV và quay lui

Sau khi lan truyền, nếu còn ô có nhiều giá trị, bộ giải dùng **MRV** (*Minimum Remaining Values*). Điểm của một ô là số lượng giá trị còn lại trong miền của nó. Bộ giải chọn ô có điểm nhỏ nhất trong số các ô có điểm lớn hơn 1. Ví dụ, ô có miền `{2, 7}` được chọn trước ô có miền `{1, 4, 8}`. Nếu bằng điểm, bộ giải chọn ô xuất hiện trước khi duyệt bảng từ trên xuống, từ trái sang phải.

1. Thử từng giá trị trong miền ô đã chọn theo thứ tự tăng dần. Mỗi lần thử dùng một bản sao của các miền và gán miền của ô về đúng một giá trị.
2. Lan truyền từ hai dãy chứa ô vừa gán. Nếu một dãy hết ứng viên, nhánh hiện tại không thể dẫn đến lời giải. Bộ giải quay lui và thử giá trị tiếp theo từ trạng thái trước khi gán.
3. Nếu sau khi lan truyền mỗi ô chỉ còn một giá trị, bộ giải trả về lời giải đầu tiên. Nếu đã duyệt hết các nhánh mà chưa tìm được lời giải, chương trình báo bảng không có lời giải.

## Chạy và kiểm tra kết quả

Từ thư mục `task_3`, chạy `python -B kakuro_game/kokuro_game.py` để mở giao diện và theo dõi từng bước. Chạy `python -B kakuro_game/kokuro_game.py --solve` để in lời giải và thống kê số bước lan truyền, số lần thử, số lần quay lui và thời gian cho từng bảng. Chế độ dòng lệnh kiểm tra lại rằng tất cả ô trắng đã được điền, mỗi giá trị thuộc `1..9` và mọi dãy đều đúng tổng, đúng điều kiện không lặp.


Trong giao diện, chọn **Minh họa quay lui 4×4** và bấm **Bước tiếp** hoặc **Tự chạy** để xem bước quay lui. Tất cả ô vừa được khôi phục miền sẽ chuyển sang màu tím. Nhật ký hiển thị miền trước và sau của một ô được khôi phục.

## Kết quả bảng 9×9

### Bảng lời giải

Ký hiệu `#` đại diện cho ô đen hoặc ô gợi ý.

```text
# # # # # # # # #
# # 5 9 8 # 1 2 #
# # 2 7 1 3 4 6 5
# 8 6 # # 1 2 8 9
# 9 8 # 3 2 8 9 #
# # 9 8 6 5 # 7 5
# 3 4 5 2 # # 4 2
# 9 3 7 1 6 8 5 #
# # 7 9 # 1 4 3 #
```

### Kiểm tra 28 dãy

Cả **28/28 dãy** đều đạt. Mỗi dãy có tổng đúng bằng gợi ý và không lặp chữ số. Tọa độ trong bảng là vị trí của ô gợi ý, tính từ 1.

| Ô gợi ý (hàng, cột) | Hướng | Phép cộng từ lời giải | Tổng gợi ý | Kết quả |
| --- | --- | --- | ---: | --- |
| (1, 3) | Dọc | 5 + 2 + 6 + 8 + 9 + 4 + 3 + 7 = 44 | 44 | Đạt |
| (1, 4) | Dọc | 9 + 7 = 16 | 16 | Đạt |
| (1, 5) | Dọc | 8 + 1 = 9 | 9 | Đạt |
| (1, 7) | Dọc | 1 + 4 + 2 + 8 = 15 | 15 | Đạt |
| (1, 8) | Dọc | 2 + 6 + 8 + 9 + 7 + 4 + 5 + 3 = 44 | 44 | Đạt |
| (2, 2) | Ngang | 5 + 9 + 8 = 22 | 22 | Đạt |
| (2, 6) | Dọc | 3 + 1 + 2 + 5 = 11 | 11 | Đạt |
| (2, 6) | Ngang | 1 + 2 = 3 | 3 | Đạt |
| (2, 9) | Dọc | 5 + 9 = 14 | 14 | Đạt |
| (3, 2) | Dọc | 8 + 9 = 17 | 17 | Đạt |
| (3, 2) | Ngang | 2 + 7 + 1 + 3 + 4 + 6 + 5 = 28 | 28 | Đạt |
| (4, 1) | Ngang | 8 + 6 = 14 | 14 | Đạt |
| (4, 5) | Dọc | 3 + 6 + 2 + 1 = 12 | 12 | Đạt |
| (4, 5) | Ngang | 1 + 2 + 8 + 9 = 20 | 20 | Đạt |
| (5, 1) | Ngang | 9 + 8 = 17 | 17 | Đạt |
| (5, 4) | Dọc | 8 + 5 + 7 + 9 = 29 | 29 | Đạt |
| (5, 4) | Ngang | 3 + 2 + 8 + 9 = 22 | 22 | Đạt |
| (5, 9) | Dọc | 5 + 2 = 7 | 7 | Đạt |
| (6, 2) | Dọc | 3 + 9 = 12 | 12 | Đạt |
| (6, 2) | Ngang | 9 + 8 + 6 + 5 = 28 | 28 | Đạt |
| (6, 7) | Ngang | 7 + 5 = 12 | 12 | Đạt |
| (7, 1) | Ngang | 3 + 4 + 5 + 2 = 14 | 14 | Đạt |
| (7, 6) | Dọc | 6 + 1 = 7 | 7 | Đạt |
| (7, 7) | Dọc | 8 + 4 = 12 | 12 | Đạt |
| (7, 7) | Ngang | 4 + 2 = 6 | 6 | Đạt |
| (8, 1) | Ngang | 9 + 3 + 7 + 1 + 6 + 8 + 5 = 39 | 39 | Đạt |
| (9, 2) | Ngang | 7 + 9 = 16 | 16 | Đạt |
| (9, 5) | Ngang | 1 + 4 + 3 = 8 | 8 | Đạt |

### Số bước và thời gian

Máy đo dùng Intel Core Ultra 7 155H (16 lõi, 22 luồng), khoảng 31,6 GiB RAM, Windows 11 Home 64-bit (build 26200) và Python 3.11.9 64-bit.

Chạy riêng bảng `COMPLEX` trong cùng một tiến trình Python, theo 5 cặp lượt đo. Đầu mỗi cặp, gọi `_run_candidates.cache_clear()` để chạy với bộ nhớ đệm rỗng. Sau đó chạy lại ngay và giữ nguyên 21 mục đã lưu theo khóa `(độ dài dãy, tổng gợi ý)`. Đo bằng `time.perf_counter()` từ trước khi tạo bộ giải đến khi duyệt xong `solve_steps()`. Thời gian đo gồm lan truyền và đếm các bước, còn kiểm tra nghiệm, in kết quả và chạy giao diện nằm ngoài khoảng đo.

| Cặp | Bộ nhớ đệm rỗng (ms) | Bộ nhớ đệm đã có dữ liệu (ms) |
| ---: | ---: | ---: |
| 1 | 226,627 | 223,978 |
| 2 | 234,758 | 232,844 |
| 3 | 219,900 | 216,658 |
| 4 | 227,151 | 221,711 |
| 5 | 222,648 | 222,918 |
| **Trung vị** | **226,627** | **222,918** |

Cả 10 lượt đều có **79 bước lan truyền, 0 lần thử, 0 mâu thuẫn, 0 lần quay lui và 1 sự kiện báo đã tìm được lời giải**. Bảng này được giải hoàn toàn bằng lan truyền. Bộ nhớ đệm dùng lại danh sách hoán vị ứng viên. Mỗi lượt vẫn phải lọc các hoán vị đó theo miền hiện tại của từng ô.
