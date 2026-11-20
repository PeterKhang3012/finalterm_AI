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
