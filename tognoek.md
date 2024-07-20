## NOTE
- ### EDIT MAP
  - Có Left - Right - Top - Bottom
  - Cái này là nó sẽ căn theo hướng mà được chọn
  - Ví dụ là Left - Top thì Block mới sẽ đi tìm một Block theo tung độ hoặc hành độ, tìm được thì nó sẽ đứng làm sao cho Block mới sẽ ở ên Trái của Block vừa đặt và sẽ căn theo bên Trên
  - Thử là biết
  - 1 - Left
  - 2 - Right
  - 3 - Top
  - 4 - Bottom
  - 5 - Center
  - Alt + C hoặc T để vào và ra trạng thái thái chọn vùng
  - Alt + D để xóa các Block được chọn
  - Ctr + Z để quay lại bước bước bộ nhớ 30 
  - Để ghi giá trị thì chỉ được chọn 1 block


## Lưu ý khi tạo map

| Tên               | Lưu ý                                                                                                                                                                                                                                                                                                               |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cách viết giá trị | Chỉ nhận giá trị 0-9 và dấu **,** để phân biệt.                                                                                                                                                                                                                                                                     |
| Saw               | Bạn viết dữ liệu cho trap này để nhận biết chúng sẽ di chuyển thế nào. Ví dụ bạn ghi 2 saw có giá trị 1,1 và 1,2 thì 1 sẽ là id của chúng để biết có chung id hay không, còn 1 và 2 phía sau là thứ tự di chuyển. Nếu chỉ có 1 giá trị thì saw sẽ đứng yên. Hướng ghi chuyển là từ giá trị nhỏ tới giá trị lớn hơn. |