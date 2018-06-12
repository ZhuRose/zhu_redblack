# -*- coding: utf-8 -*-

class zhu_node(object):
    def __init__(self, data, pleft = None, pright = None):
        self.data = data
        self._left = pleft
        self._right = pright

    def __repr__(self):
        return str(self.data)

class zhu_binaryTree(object):
    def __init__(self):
        self.root = None
        self._size = 0

    def getSize(self):
        return self._size

    def getHeight(self):
        return self._getHeight(self.root)

    def _getHeight(self, node):
        if node == None:
            return 0
        return max(self._getHeight(node._left), self._getHeight(node._right)) + 1

    def foundSubNode(self, node): #右子树的后继节点
        n = node._right
        while n._left != None:
            n = n._left
        return n

    def getItem(self, key):
        return self._getItem(self.root, key)

    def _getItem(self, node, key):
        if node == None:
            print('%s not found'%key)
            return
        if key == node.data[0]:
            return node.data[1]
        elif key < node.data[0]:
            return self._getItem(node._left, key)
        else:
            return self._getItem(node._right, key)

    def setItem(self, key, value):
        self.root = self._setItem(self.root, key, value)

    def _setItem(self, node, key, value):
        if node == None:
            self._size += 1
            return zhu_node((key, value))
        if key == node.data[0]:
            node.data = (key, value)
        elif key < node.data[0]:
            node._left = self._setItem(node._left, key, value)
        else:
            node._right = self._setItem(node._right, key, value)
        self._size += 1
        return node

    def removeItem(self, key):
        self.root = self.removeItem(self.root, key)

    def _removeItem(self, node, key):
        if node == None:
            print('%s not found'%key)
            return
        if key == node.data[0]:
            if node._right == None:#1
                self._size -= 1
                return node._left
            if node._left == None:#2
                self._size -= 1
                return node._right
            t = self.foundSubNode(node)#寻找后继节点
            node.data = t.data#狸猫换太子
            node._right = self._removeItem(node._right, node.data[0]) #转变为#2
        elif key < node.data[0]:
            node._left = self._removeItem(node._left, key)
        else:
            node._right = self._removeItem(node._right, key)
        return node

    def middleTraverse(self, node): #中序遍历
        if node == None:
            return 'null'
        return self.middleTraverse(node._left) +'-' + str(node) + '-' + self.middleTraverse(node._right)

    def __getitem__(self, item):
        return self.getItem(item)

    def __setitem__(self, key, value):
        return self.setItem(key, value)

    def __repr__(self):
        return self.middleTraverse(self.root)
