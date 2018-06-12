# -*- coding: utf-8 -*-

RED = True
BLACK = False
Balance = 0
LeftLeaning = -1
RightLeaning = 1

class zhu_node(object):
    def __init__(self, data, pleft = None, pright = None):
        self.data = data
        self._left = pleft
        self._right = pright

    def __repr__(self):
        return str(self.data)

class zhu_redBlackNode(zhu_node):
    def __init__(self, data, color, pleft = None, pright = None):
        super(zhu_redBlackNode, self).__init__(data, pleft, pright)
        self.color = color

    def __repr__(self):
        return str(self.data)+ ('[RED]'if self.color == RED else '[BLACK]')


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
        return max(self._getHeight(node._left), self._getHeight(node._right)) + 1;

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

    def foundSubNode(self, node):
        n = node._right
        while n._left != None:
            n = n._left
        return n

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
        self._size -= 1
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


class zhu_redBlackBinaryTree(zhu_binaryTree):
    def __init__(self):
        super(zhu_redBlackBinaryTree, self).__init__()
        self._height = 0
        self.balance = Balance

    def getHeight(self):
        return self._height

    def isRed(self, node):
        if node != None and node.color == RED:
            return True
        return False

    def rotateLeft(self, node):#左边深度不变，右边深度-1 if n.color==RED else 0
        n = node._right
        n.color = node.color
        node._right = n._left
        node.color = RED
        n._left = node
        return n

    def rotateRight(self, node):#右边深度不变，左边深度-1 if n.color==RED else 0
        n = node._left
        n.color = node.color
        node._left = n._right
        node.color = RED
        n._right = node
        return n

    def flipColor(self, node):#左右深度不变，保持平衡(特例：根节点左右+1)
        if node.color == BLACK:
            node.color = RED
            node._left.color = BLACK
            node._right.color = BLACK
        return node

    def retainRBT(self, node):#从叶子节点向上路径，保持红黑树性质（素质三连~）
        if not self.isRed(node._left) and self.isRed(node._right):#使红节点作为父节点的左节点（沿着左上传递）
            node = self.rotateLeft(node)
        if self.isRed(node._left) and self.isRed(node._left._left):#解决连续两个红节点冲突（沿着右上传递遇到了红节点）
            node = self.rotateRight(node)
        if self.isRed(node._left) and self.isRed(node._right):#解决黑节点左右节点都为红节点
            node = self.flipColor(node)
        return node

    def retainBalance(self, node):
        if self.balance != Balance:
            if self.balance == RightLeaning:
                if node._right.color == RED:  # 右边节点为红色
                    node = self.rotateLeft(node)  # 左旋（左右高度不变）
                    node._left.color = BLACK  # 左节点变黑（左高度+1，完全平衡鸟）
                    self.balance = Balance
                else:
                    node._right.color = RED  # 右节点变红（右高度-1，局部平衡鸟）
                    node = self.rotateLeft(node)  # 左旋（左右高度不变）
                    if node.color == RED:  # 若node为红，染黑node使完全平衡
                        node.color = BLACK
                        self.balance = Balance
                node._left = self.retainRBT(node._left)
            else:
                if node._left.color == RED:  # 左边节点为红色
                    node = self.rotateRight(node)  # 右旋（左右高度不变）
                    node._right.color = BLACK  # 右节点变黑（右高度+1，完全平衡鸟）
                    self.balance = Balance
                else:
                    node._left.color = RED  # 右节点变红（右高度-1，局部平衡鸟）
                    node = self.rotateRight(node)  # 右旋（左右高度不变）
                    if node.color == RED:  # 若node为红，染黑node使完全平衡
                        node.color = BLACK
                        self.balance = Balance
                node._right = self.retainRBT(node._right)
        node = self.retainRBT(node)
        return node

    def setItem(self, key, value):
        super(zhu_redBlackBinaryTree, self).setItem(key, value)
        if self.root.color == RED:
            self._height += 1
            self.root.color = BLACK

    def _setItem(self, node, key, value):
        if node == None:
            self._size += 1
            return zhu_redBlackNode((key, value), RED) #插入的节点用红链接相连
        if key == node.data[0]:
            node.data = (key, value)
        elif key < node.data[0]:
            node._left = self._setItem(node._left, key, value)
        else:
            node._right = self._setItem(node._right, key, value)
        node = self.retainRBT(node)
        return node

    def removeItem(self, key):
        self.root = self._removeItem(self.root, key)
        if self.balance != Balance:
            self._height -= 1
            self.balance = Balance #直到根节点前都不平衡（没遇到红节点），整体高度已经-1，处于平衡状态鸟

    #由于红黑树的性质，并且默认左旋，红节点一定在左子树，删除的一定是左叶子节点（特例为case3）
    # case1：删除叶子节点为红节点，并且左右为None, 删除不破坏平衡
    # case2：删除叶子节点为黑节点，并且左右为None，删除破坏平衡(特例：删除叶子节点在父节点右边修正一下)
    # case3：删除叶子节点为黑节点，并且左为红节点，右为None，转变成case1，不破坏平衡
    def _removeItem(self, node, key):
        if node == None:
            print('%s not found'%key)
            return
        if key == node.data[0]:
            if node.color == RED and node._left == None and node._right == None:#case1
                self._size -= 1
                self.balance = Balance #后继节点为红节点，直接删除
                return None
            if node.color == BLACK and node._left == None and node._right == None:#case2
                self._size -= 1
                if self.balance == Balance: #说明没寻找后继节点
                    self.balance = LeftLeaning
                else:
                    self.balance = RightLeaning #后继节点的上位节点必然在其父节点的左子树，直到被替换的节点（拐点），因此右倾
                return None
            if node.color == BLACK and node._left != None and node._right == None:#case3
                node.data = node._left.data
                node._left = self._removeItem(node._left, node.data[0]) #转变成case1
                return node
            t = self.foundSubNode(node)#寻找后继节点
            node.data = t.data#狸猫换太子
            self.balance = not Balance #迭代前设置一个flag(左右倾任选)
            node._right = self._removeItem(node._right, node.data[0]) #转变为case1（后继节点为红）或case2（后继节点为黑）
            if self.balance != Balance: #拐点的不平衡状态为左倾（删去的节点在右子树）
                self.balance = LeftLeaning
        elif key < node.data[0]:
            node._left = self._removeItem(node._left, key)
        else:
            node._right = self._removeItem(node._right, key)
        node = self.retainBalance(node)
        return node

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
