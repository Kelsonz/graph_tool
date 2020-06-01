#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 载入图像，对图像边缘进行扩充处理，根据输入卷积核进行卷积操作
__author__ = 'Kelsonz Fu'

from math import atan as atan
from math import exp as exp
from math import pi as pi
from math import pow as pow
from math import sqrt as sqrt

from PIL import Image


class ImageFilter:
    def __init__(self, filename):
        # 载入图像
        self.filename = filename
        self.im = Image.open(filename)
        # 设定默认卷积核大小
        self.core_size = 3
        # edge表示扩张时核对应的边增加的宽度
        self.edge = int((self.core_size - 1) / 2)
        self.expand_mode = 'zero'
        # 获得图片属性
        self.xsize, self.ysize = self.im.size
        self.format = self.im.format
        self.mode = self.im.mode
        # 获得串、矩阵格式的L通道信息
        self.l_load = self.im.load()
        self.l_str = list()
        self.l_matrix = list()
        if self.mode == 'L':
            for j in range(self.ysize):
                row = list()
                for i in range(self.xsize):
                    row.append(self.l_load[i, j])
                    self.l_str.append(self.l_load[i, j])
                self.l_matrix.append(row)
        else:
            # 对于多通道，取一个通道分量
            for j in range(self.ysize):
                row = list()
                for i in range(self.xsize):
                    row.append(self.l_load[i, j][0])
                    self.l_str.append(self.l_load[i, j][0])
                self.l_matrix.append(row)

    # 修改图片对象
    def set_another_image(self, filename, mode='zero', size=3):
        # 载入图像
        self.filename = filename
        self.im = Image.open(filename)
        # 设定默认卷积核大小
        self.core_size = size
        # edge表示扩张时核对应的边增加的宽度
        self.edge = int((size - 1) / 2)
        self.expand_mode = mode
        # 获得图片属性
        self.xsize, self.ysize = self.im.size
        self.format = self.im.format
        self.mode = self.im.mode
        # 获得串、矩阵格式的L通道信息
        self.l_load = self.im.load()
        self.l_str = list()
        self.l_matrix = list()
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                row.append(self.l_load[i, j])
                self.l_str.append(self.l_load[i, j])
            self.l_matrix.append(row)

    # 获得图片的title
    def get_filename(self):
        return self.filename.split('.')[0]

    # 获得图片的格式
    def get_format(self):
        return self.filename.split('.')[1]

    # 设定卷积核大小，默认为3
    def set_core_size(self, size):
        self.core_size = size
        self.edge = int((self.core_size - 1) / 2)

    # 设定扩张模式
    def set_expand_mode(self, mode):
        self.expand_mode = mode

    # 矩阵卷积
    def matrix_convolution(self, matrix, kernel):
        # 定义卷积后串、矩阵
        new_l_matrix = list()
        new_l_str = list()
        # 开始进行卷积
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                # 获得子矩阵
                aim_matrix = self.get_aim_matrix(matrix, i + self.edge, j + self.edge)
                # 进行卷积
                result = self.convolution(aim_matrix, kernel)
                row.append(result)
                new_l_str.append(result)
            new_l_matrix.append(row)
        return new_l_matrix, new_l_str

    # 计算两个核与矩阵卷积后，结果取平方和再开根号的结果
    def square_add_concolution_result(self, matrix, kernel_1, kernel_2):
        # 使用一阶微分算子，卷积核大小设置为3
        self.set_core_size(3)
        matrix = self.expand(matrix)
        # 进行卷积
        matrix_1, _ = self.matrix_convolution(matrix, kernel_1)
        matrix_2, _ = self.matrix_convolution(matrix, kernel_2)
        # 对卷积结果分别取平方后再开根号
        result_matrix, theta, tang = self.matrix_square_add(matrix_1, matrix_2)
        return result_matrix, theta, tang

    # 计算两个核与矩阵卷积后相加的结果
    def add_convolution_result(self, matrix, kernel_1, kernel_2, hence, filtername):
        # 进行卷积
        matrix_1, _ = self.matrix_convolution(matrix, kernel_1)
        matrix_2, _ = self.matrix_convolution(matrix, kernel_2)
        new_l_matrix, new_l_str = self.matrix_add(matrix_1, matrix_2)

        if hence is True:
            new_l_matrix, new_l_str = self.matrix_add(self.l_matrix, new_l_matrix)
            filtername += '_hence'
        # 打印图片
        return self.put_image(new_l_str, filtername)

    # 计算梯度大小、方向、角度
    def matrix_square_add(self, matrix_1, matrix_2):
        sqaure_sum_matrix = list()
        theta_matrix = list()
        tan_matrix = list()
        infty = 100000

        for j in range(self.ysize):
            row_a = list()
            row_b = list()
            row_c = list()
            for i in range(self.xsize):
                row_a.append(square_sum(matrix_1[j][i], matrix_2[j][i]))
                # 对应分母为零的情况
                if matrix_1[j][i] == 0:
                    row_b.append(pi / 2)
                    row_c.append(infty)
                else:
                    row_b.append(atan(matrix_2[j][i] / matrix_1[j][i]))
                    row_c.append(matrix_2[j][i] / matrix_1[j][i])
            sqaure_sum_matrix.append(row_a)
            theta_matrix.append(row_b)
            tan_matrix.append(row_c)

        return sqaure_sum_matrix, theta_matrix, tan_matrix

    # 矩阵加
    def matrix_add(self, matrix_a, matrix_b):
        add_matrix = list()
        add_str = list()
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                row.append(matrix_a[j][i] + matrix_b[j][i])
                add_str.append(matrix_a[j][i] + matrix_b[j][i])
            add_matrix.append(row)

        return add_matrix, add_str

    # 矩阵减
    def matrix_sub(self, matrix_a, matrix_b):
        sub_matrix = list()
        sub_str = list()
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                row.append(matrix_a[j][i] - matrix_b[j][i])
                sub_str.append(matrix_a[j][i] - matrix_b[j][i])
            sub_matrix.append(row)

        return sub_matrix, sub_str

    # 双线性插值
    def get_g1_g2(self, matrix, theta, tangent):
        # 不同方位对应的角度以及像素值
        E = [0, matrix[1][2]]
        NE = [pi / 4, matrix[0][2]]
        N = [pi / 2, matrix[0][1]]
        NW = [pi / 2 + pi / 4, matrix[0][0]]
        W = [pi, matrix[1][0]]
        SW = [pi + pi / 4, matrix[2][0]]
        S = [- pi / 2, matrix[2][1]]
        SE = [- pi / 2 + pi / 4, matrix[2][2]]
        g1 = g2 = 0
        # 根据不同范围进行插值计算
        if E[0] <= theta < NE[0]:
            g1 = (1 - tangent) * E[1] + tangent * NE[1]
            g2 = (1 - tangent) * W[1] + tangent * SW[1]
        elif NE[0] <= theta <= N[0]:
            g1 = (1 - tangent) * NE[1] + tangent * N[1]
            g2 = (1 - tangent) * SW[1] + tangent * S[1]
        elif S[0] <= theta < SE[0]:
            g1 = (1 - tangent) * S[1] + tangent * SE[1]
            g2 = (1 - tangent) * N[1] + tangent * NW[1]
        elif SE[0] <= theta < E[0]:
            g1 = (1 - tangent) * SE[1] + tangent * E[1]
            g2 = (1 - tangent) * NW[1] + tangent * W[1]

        return g1, g2

    # 非极大值抑制
    def suppress_not_max(self, matrix, theta, tangent):
        # 边缘扩展
        matrix = self.expand(matrix)
        edge_matrix = list()
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                # 获得目标子矩阵
                aim_matrix = self.get_aim_matrix(matrix, i + self.edge, j + self.edge)
                # 根据梯度方向双插值得到g_1, g_2
                g_1, g_2 = self.get_g1_g2(aim_matrix, theta[j][i], tangent[j][i])
                # 非极大值抑制
                if matrix[j][i] >= g_1 and matrix[j][i] >= g_2:
                    row.append(2)
                else:
                    row.append(0)
            edge_matrix.append(row)

        return edge_matrix

    # 双阈值检测
    def double_threshould(self, matrix, edge_matrix, h, l):
        # edge矩阵
        # 2 强边
        # 1 弱边
        # 0 被抑制
        for j in range(self.ysize):
            for i in range(self.xsize):
                if edge_matrix[j][i] == 2:
                    if matrix[j][i] < l:
                        edge_matrix[j][i] = 0
                    elif l <= matrix[j][i] < h:
                        edge_matrix[j][i] = 1

        return edge_matrix

    # 孤立点抑制
    def single_suppress(self, matrix, threshould, low_t):
        self.set_core_size(3)
        self.set_expand_mode('zero')
        # 做变更的矩阵
        change = threshould
        # 扩张双阈值检测后的矩阵
        threshould = self.expand(threshould)
        # 开始检测
        for j in range(self.ysize):
            for i in range(self.xsize):
                # 获得该像素所在八领域矩阵，检测是否与强边联通，
                # 假如联通且像素值为low_threshould, 则把该像素设置成强边
                if threshould[j + self.edge][i + self.edge] == 2:
                    for x in range(3):
                        for y in range(3):
                            if threshould[j + x][i + y] == 1:
                                change[j + x - self.edge][i + y - self.edge] = 2

        # 根据最终的强弱边信息确定像素抑制情况
        str = list()
        for j in range(self.ysize):
            for i in range(self.xsize):
                if change[j][i] == 2:
                    matrix[j][i] = 255
                else:
                    matrix[j][i] = 0
                str.append(matrix[j][i])

        return matrix, str

    # canny边缘检测
    def canny(self, high=150, low=50, sigma=1.4, size=3, expand='zero'):

        # 设定高斯滤波卷积核大小
        self.set_core_size(size)
        self.set_expand_mode(expand)
        filter_name = 'canny'
        # 高斯平滑
        gauss_matrix, _ = self.gauss(sigma=sigma, size=size, expand='zero')
        # 计算梯度强度和方向，使用sobel算子
        kernel_1 = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        kernel_2 = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        # 卷积，并将卷积结果分别取平方后再开根号
        grad_matrix, theta_matrix, tan_matrix = self.square_add_concolution_result(gauss_matrix,
                                                                                   kernel_1,
                                                                                   kernel_2)
        # 非极大值抑制
        edge_matrix = self.suppress_not_max(grad_matrix, theta_matrix, tan_matrix)
        # 双阈值检测
        threshould_matrix = self.double_threshould(grad_matrix, edge_matrix, high, low)
        # 孤立点抑制
        new_l_matrix, new_l_str = self.single_suppress(grad_matrix, threshould_matrix, low)

        # 打印图片
        return self.put_image(new_l_str, filter_name)

    def round_str(self, str):
        for i in range(len(str)):
            str[i] = int(round(str[i]))
        return str

    # gauss平滑
    def gauss(self, sigma=1.4, size=3, expand='zero'):
        # 设定卷积核大小
        self.set_core_size(size)
        # 设定边缘扩展方式
        self.set_expand_mode(expand)
        # 获得高斯卷积核
        kernel = list()
        sum = 0
        for j in range(self.core_size):
            row = list()
            for i in range(self.core_size):
                a = pow((i - self.edge), 2) + pow((j - self.edge), 2)
                a = - a / (2 * pow(sigma, 2))
                b = 1 / (2 * pi * pow(sigma, 2))
                result = b * exp(a)
                sum += result
                row.append(result)
            kernel.append(row)
        # 归一化处理
        for j in range(self.core_size):
            for i in range(self.core_size):
                kernel[j][i] = kernel[j][i] / sum
        # 获得扩张后矩阵
        matrix = self.expand(self.l_matrix)
        # return concolution
        new_l_matrix, new_l_str = self.matrix_convolution(matrix, kernel)
        fname = self.put_image(self.round_str(new_l_str), 'gauss')
        return new_l_matrix, fname

    # 进行robert算子的卷积
    def robert(self, hence=False):
        # 设定卷积核大小
        self.set_core_size(3)
        # 设定filter名称
        filter_name = 'robert'
        # 获得卷积核
        kernel_1 = [[0, 0, 0], [0, -1, 0], [0, 0, 1]]
        kernel_2 = [[0, 0, 0], [0, 0, 1], [0, -1, 0]]
        # 获得扩张后矩阵
        matrix = self.expand(self.l_matrix)
        return self.add_convolution_result(matrix, kernel_1, kernel_2, hence, filter_name)

    # 进行prewitt算子的卷积
    def prewitt(self, hence=False):
        # 设定卷积核大小
        self.set_core_size(3)
        # 设定filter名称
        filter_name = 'prewitt'
        # 获得卷积核
        kernel_1 = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
        kernel_2 = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
        # 获得扩张后矩阵
        matrix = self.expand(self.l_matrix)
        return self.add_convolution_result(matrix, kernel_1, kernel_2, hence, filter_name)

    # 进行sobel算子的卷积
    def sobel(self, hence=False):
        # 设定卷积核大小
        self.set_core_size(3)
        # 设定filter名称
        filter_name = 'sobel'
        # 获得卷积核
        kernel_1 = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        kernel_2 = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        # 获得扩张后矩阵
        matrix = self.expand(self.l_matrix)
        return self.add_convolution_result(matrix, kernel_1, kernel_2, hence, filter_name)

    # 进行拉普拉斯算子的卷积
    def laplacian(self, area=8, hence=False):
        # 设定卷积核大小
        self.set_core_size(3)

        # 设定filter名称
        filter_name = 'laplacian_' + str(area)
        # 获得卷积核
        if area == 4 and hence is False:
            kernel = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        elif area == 4 and hence is True:
            kernel = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
            filter_name += '_hence'
        elif area == 8 and hence is False:
            kernel = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
        elif area == 8 and hence is True:
            kernel = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
            filter_name += '_hence'

        matrix = self.expand(self.l_matrix)
        # 进行卷积
        new_l_matrix, new_l_str = self.matrix_convolution(matrix, kernel)

        # 打印图片
        return self.put_image(new_l_str, filter_name)

    # 进行均值滤波
    def avg_filter(self, mode='zero', size=3):
        self.set_core_size(size)
        self.set_expand_mode(mode)
        # 计时

        # 获得均值滤波卷积核
        kernel = list()
        for i in range(self.core_size):
            row = list()
            for j in range(self.core_size):
                row.append(1 / (self.core_size * self.core_size))
            kernel.append(row)

        matrix = self.expand(self.l_matrix)
        # 进行卷积
        new_l_matrix, new_l_str = self.matrix_convolution(matrix, kernel)

        # 打印图片
        return self.put_image(new_l_str, filter='avg')

    # 进行中值滤波
    def medial_filter(self, mode='zero', size=3):
        self.set_core_size(size)
        self.set_expand_mode(mode)
        # 定义操作后串、矩阵
        new_l_str = list()
        new_l_matrix = list()
        # 获得操作对象
        expand_l_matrix = self.expand(self.l_matrix)
        # 进行卷积
        for j in range(self.ysize):
            row = list()
            for i in range(self.xsize):
                # 获得子矩阵
                aim_matrix = self.get_aim_matrix(expand_l_matrix, i, j)
                # 计算中位值
                result = self.get_medial(aim_matrix)
                row.append(result)
                new_l_str.append(result)
            new_l_matrix.append(row)

        return self.put_image(new_l_str, filter='medial')

    # 获得(i, j)坐标对应下的子矩阵
    def get_aim_matrix(self, matrix, i, j):
        # 对(i, j)进行重定位，移到矩阵左上角的坐标位置处
        i = i - self.edge
        j = j - self.edge
        aim_matrix = list()
        for y in range(self.core_size):
            row = list()
            for x in range(self.core_size):
                row.append(matrix[j + y][i + x])
            aim_matrix.append(row)
        return aim_matrix

    # 获得矩阵中位数
    def get_medial(self, matrix):
        temp = list()
        # 获得矩阵所有元素
        for i in range(self.core_size):
            temp = temp + matrix[i]
        # 排序
        temp.sort()
        # 返回中位值
        return temp[int((self.core_size * self.core_size - 1) / 2)]

    # 卷积
    def convolution(self, matrix, kernel):
        result = 0
        for i in range(self.core_size):
            for j in range(self.core_size):
                result += matrix[i][j] * kernel[i][j]
        return abs(result)

    # 进行边缘扩张
    def expand(self, matrix):
        if self.expand_mode == 'zero':
            return self.expand_by_zero(matrix)
        elif self.expand_mode == 'side':
            return self.expand_by_side(matrix)

    # 参照边缘像素的值，复制扩张
    def expand_by_side(self, matrix):
        expand_l_matrix = list()
        first_line = list()
        last_line = list()
        # 得到第一行和最后一行的列
        for i in range(self.xsize):
            first_line.append(matrix[0][i])
            last_line.append(matrix[self.ysize - 1][i])
        # 按列进行扩充
        for j in range(self.ysize + 2 * self.edge):
            # 在图像上方进行扩充
            if 0 <= j < self.edge:
                expand_l_matrix.append([0] * self.edge + first_line + [0] * self.edge)
            # 在图像下方进行扩充
            elif 0 <= j - self.ysize - self.edge < self.edge:
                expand_l_matrix.append([0] * self.edge + last_line + [0] * self.edge)
            # 在图像两边进行扩充(不包含最上最下的交界)
            else:
                # 将列坐标转化到扩张前矩阵的列坐标
                j = j - self.edge
                # 获得该行第一个元素与最后一个元素
                first = [matrix[j][0]]
                last = [matrix[j][self.xsize - 1]]
                expand_l_matrix.append(first * self.edge + matrix[j] + last * self.edge)

        return expand_l_matrix

    # 按照在边缘加零的方式扩张
    def expand_by_zero(self, matrix):
        expand_l_matrix = list()
        # 按列顺序扩充
        for j in range(self.ysize + 2 * self.edge):
            # 在最上部分和最下部分扩充
            if 0 <= j < self.edge or 0 <= j - self.ysize - self.edge < self.edge:
                temp = list()
                for i in range(self.xsize + 2 * self.edge):
                    temp.append(0)
                expand_l_matrix.append(temp)
            # 在两边(不包括与上下两边的交集)扩充
            else:
                temp = [0]
                expand_l_matrix.append(temp * self.edge + matrix[j - self.edge] + temp * self.edge)

        return expand_l_matrix

    # 将转换后的像素值写入图像并进行保存
    def put_image(self, data, filter):
        if self.mode != 'L':
            for i in range(len(data)):
                data[i] = (data[i], data[i], data[i])
        self.im.putdata(data)
        msg = 'aim' + '.' + self.get_format()
        self.im.save(msg)
        return msg

    # 图像相减
    def sub_image(self, y):
        sub_matrix, sub_str = self.matrix_sub(self.l_matrix, y.l_matrix)
        self.put_image(sub_str, 'sub_' + y.get_filename())
        return sub_matrix

    # 图像加法
    def add_image(self, y):
        sub_matrix, sub_str = self.matrix_add(self.l_matrix, y.l_matrix)
        self.put_image(sub_str, 'add_' + y.get_filename())
        return sub_matrix


# 取平方和后开根号
def square_sum(x, y):
    return sqrt(pow(x, 2) + pow(y, 2))
