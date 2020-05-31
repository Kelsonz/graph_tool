from PIL import Image
import math


class exp:
    def __init__(self, filename):
        # 载入图像
        self.filename = filename
        self.im = Image.open(filename)
        self.format = self.im.format
        self.mode = self.im.mode
        # 获得图片属性
        self.xsize, self.ysize = self.im.size
        self.rgb = list(self.im.getdata())

    # 给新通道赋值
    def set_data(self, y, x, data):
        index = y * self.new_xsize + x
        self.new_rgb[index] = data

    # 获得旧通道的值
    def get_data(self, y, x):
        index = y * self.xsize + x
        return self.rgb[index]

    # 保存图像
    def save(self):
        fname = 'aim.' + self.format
        self.new_im.putdata(self.new_rgb)
        self.new_im.save(fname)
        return fname

    # 生成新图像
    def new_image(self, xsize, ysize):
        self.new_xsize = xsize
        self.new_ysize = ysize
        self.new_im = Image.new(self.mode, (xsize, ysize))
        if self.mode == 'L':
            self.new_rgb = [0] * (xsize * ysize)
        elif self.mode == 'RGB':
            self.new_rgb = [(0, 0, 0)] * (xsize * ysize)
        elif self.mode == 'RGBA':
            self.new_rgb = [(0, 0, 0, 0)] * (xsize * ysize)

    # 旋转
    def rotate(self, degree):
        # 计算旋转矩阵的cos, sin值
        # 由于是从新图像往回推所以角度取负值
        cos = math.cos(math.radians(-degree))
        sin = math.sin(math.radians(-degree))
        # 计算新画布大小
        d = int(math.sqrt(math.pow(self.xsize, 2) + math.pow(self.ysize, 2)))
        x = y = d
        # 生成用于旋转的新图像
        self.new_image(x, y)
        for j in range(y):
            for i in range(x):
                # 计算在原图中的坐标
                X = (i - x / 2) * cos + (j - y / 2) * sin + self.xsize / 2
                Y = -(i - x / 2) * sin + (j - y / 2) * cos + self.ysize / 2
                if X >= self.xsize - 1 or Y >= self.ysize - 1 or X < 0 or Y < 0:
                    pass
                elif int(X) == X and int(Y) == Y:
                    self.set_data(j, i, self.get_data(int(Y), int(X)))
                else:
                    # 若生成坐标为小数，使用双线性插值的结果
                    self.deltax = X - int(X)
                    self.deltay = Y - int(Y)
                    xx = int(X) + 1
                    yy = int(Y) + 1
                    xy00 = self.get_data(yy, int(X))
                    xy01 = self.get_data(int(Y), int(X))
                    xy10 = self.get_data(yy, xx)
                    xy11 = self.get_data(int(Y), xx)
                    rgb = self.rgb_double_interpolating(xy00, xy01, xy10, xy11)
                    self.set_data(j, i, rgb)
        # 保存生成的图像
        self.save()

    # 图像反转
    def flip(self, axis='x'):
        self.new_image(self.xsize, self.ysize)
        for j in range(self.ysize):
            for i in range(self.xsize):
                X = Y = 0
                if axis is 'y':
                    X = self.xsize - 1 - i
                    Y = j
                elif axis is 'x':
                    X = i
                    Y = self.ysize - 1 - j
                self.set_data(j, i, self.get_data(Y, X))
        self.save()

    # 图像缩放
    def resize(self, new_size):
        new_x = new_y = cx = cy = 0
        # 如果给的是具体的像素值(元组)
        if isinstance(new_size, tuple):
            cx = self.xsize / new_size[0]
            cy = self.ysize / new_size[1]
            new_x = new_size[0]
            new_y = new_size[1]
        # 如果给的是具体的倍数
        elif isinstance(new_size, float) or isinstance(new_size, int):
            cx = 1 / new_size
            cy = 1 / new_size
            new_x = int(self.xsize / cx)
            new_y = int(self.ysize / cy)
        self.new_image(new_x, new_y)
        for j in range(new_y):
            for i in range(new_x):
                X = int(cx * i)
                Y = int(cy * j)
                self.set_data(j, i, self.get_data(Y, X))
        self.save()

    # 图像平移
    def move(self, x, y):
        x = int(x)
        y = int(y)
        self.new_image(x + self.xsize, y + self.ysize)
        for j in range(self.ysize + y):
            for i in range(self.xsize + x):
                X = i - x
                Y = j - y
                # 空出黑边
                if X >= self.xsize - 1 or Y >= self.ysize - 1 or X < 0 or Y < 0:
                    pass
                else:
                    self.set_data(j, i, self.get_data(Y, X))
        self.save()

    # RGB通道双线性插值
    def rgb_double_interpolating(self, xy00, xy01, xy10, xy11):
        if self.mode == 'L':
            return int(self.func(xy00, xy01, xy10, xy11))
        else:
            r = int(self.func(xy00[0], xy01[0], xy10[0], xy11[0]))
            g = int(self.func(xy00[1], xy01[1], xy10[1], xy11[1]))
            b = int(self.func(xy00[2], xy01[2], xy10[2], xy11[2]))
            if self.mode == 'RGBA':
                a = int(self.func(xy00[3], xy01[3], xy10[3], xy11[3]))
                return (r, g, b, a)
            else:
                return (r, g, b)

    # 双线性插值
    def func(self, xy00, xy01, xy10, xy11):
        a = (1 - self.deltax) * xy00 + self.deltax * xy01
        b = (1 - self.deltax) * xy10 + self.deltax * xy11
        return (1 - self.deltay) * b + self.deltay * a


if __name__ == '__main__':
    t = exp('img/tool.png')

    t.rotate(30)
