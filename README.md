# Pac-man game coding

## Một vài kiến thức được sử dụng trong pygame

### 1. ```pygame.transform.flip```

được sử dụng để lật hoặc quay một hình ảnh theo trục x hoặc y. Hàm này có cú pháp như sau

```python
pygame.transform.flip(Surface, xbool, ybool)
```

> Surface: Đối tượng hình ảnh hoặc bề mặt (surface) bạn muốn lật.
> xbool: Nếu xbool là True, thì hình ảnh sẽ được lật theo trục x.
> ybool: Nếu ybool là True, thì hình ảnh sẽ được lật theo trục y.

### 2. ```pygame.time.Clock()```

Được sử dụng để tạo một đối tượng đồng hồ (clock).

Đối tượng này thường được sử dụng để giữ cho trò chơi chạy với tốc độ xác định, đặc biệt là khi vòng lặp game chạy.

Đối tượng Clock cung cấp các phương thức như ``tick(fps)`` để kiểm soát tốc độ khung hình của trò chơi. Hàm ``tick`` sẽ trì hoãn vòng lặp cho đến khi đã đủ thời gian để duy trì tốc độ khung hình mong muốn (fps).