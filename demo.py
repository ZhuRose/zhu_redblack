# -*- coding: utf-8 -*-
from zhu_redBlackTree import zhu_redBlackBinaryTree

if __name__ == '__main__':
    bt = zhu_redBlackBinaryTree()
    bt[10] = ''
    bt[5] = ''
    bt[15] = ''
    bt[2] = ''
    bt[12] = ''
    bt[8] = ''
    bt[18] = ''
    bt[1] = ''
    bt[3] = ''
    bt[6] = ''
    bt[9] = ''
    print(bt)
    print(bt.getHeight())
    print(bt.root)
    bt.removeItem(10)
    print(bt)
    print(bt.getHeight())
    print(bt.root)