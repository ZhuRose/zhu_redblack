# -*- coding: utf-8 -*-

from zhu_binaryTree import zhu_node, zhu_binaryTree

RED = True
BLACK = False
Balance = 0
LeftLeaning = -1
RightLeaning = 1
class zhu_redBlackNode(zhu_node):
    def __init__(self, data, color, pleft = None, pright = None):
        super(zhu_redBlackNode, self).__init__(data, pleft, pright)
        self.color = color

    def __repr__(self):
        return str(self.data)+ ('[RED]'if self.color == RED else '[BLACK]')

class zhu_redBlackBinaryTree(zhu_binaryTree):
    def __init__(self):
        super(zhu_redBlackBinaryTree, self).__init__()
        self._height = 0

    def getHeight(self):
        return self._height

    def isRed(self, node):
        if node != None and node.color == RED:
            return True
        return False

    def rotateLeft(self, node):#左边深度不变，右边深度-1(n为黑节点)或不变（n为红节点）
        n = node._right
        n.color = node.color
        node._right = n._left
        node.color = RED
        n._left = node
        return n

    def rotateRight(self, node):#右边深度不变，左边深度-1(n为黑节点)或不变（n为红节点）
        n = node._left
        n.color = node.color
        node._left = n._right
        node.color = RED
        n._right = node
        return n

    def flipColor(self, node):#左右深度不变，保持平衡
        if node.color == BLACK:
            node.color = RED
            node._left.color = BLACK
            node._right.color = BLACK
        return node

    def retainRBT(self, node):#保持红黑树性质（素质三连~）
        if not self.isRed(node._left) and self.isRed(node._right):#使红节点作为父节点的左节点（沿着左上传递）
            node = self.rotateLeft(node)
        if self.isRed(node._left) and self.isRed(node._left._left):#解决连续两个红节点冲突（沿着右上传递遇到了红节点）
            node = self.rotateRight(node)
        if self.isRed(node._left) and self.isRed(node._right):#解决黑节点左右节点都为红节点
            node = self.flipColor(node)
        return node

    def retainBalance(self, node):#保持左右子树高度相等
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
        if self.root.color == RED:#根节点触发了flipColor
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
        self.balance = Balance
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
