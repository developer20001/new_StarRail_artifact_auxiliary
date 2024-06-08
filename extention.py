'''拓展组件封装：系统级鼠标事件；增强下拉选择框'''

from PySide6.QtGui import Qt
from PySide6.QtCore import QObject, Signal, Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QComboBox, QCompleter, QListWidget, QCheckBox, QListWidgetItem, QLineEdit
from pynput import mouse

# 外部/系统级鼠标事件处理
class OutsideMouseManager(QObject):
    right_click = Signal(int, int)
    left_click = Signal(int, int)

    def __init__(self, parent = None):
        super().__init__(parent)
        self._listener = mouse.Listener(on_click = self._handle_click)
        self._listener.start()
    
    def _handle_click(self, x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            self.right_click.emit(x, y)
        if button == mouse.Button.left and pressed:
            self.left_click.emit(x, y)
    def stop(self):
        self._listener.stop()

# 增强选择框
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.ClickFocus)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)


# 自定义控件-点击按钮下拉CheckBox列表
class XCombobox(QComboBox):
    # 有item被选择时，发出信号
    itemChecked = Signal(list)
    def __init__(self, allText="全选", parent=None):
        super().__init__(parent)
        # 全选文本
        self.allText = allText
        # 保存QCheckBox控件
        self._checks = []

        # 通过setView()设置下拉列表控件,将下拉列表框弹出控件设置为给定的itemView,
        # 在本案例中，将其设置为QListWidget
        listwgt = QListWidget(self)
        self.setView(listwgt)
        ## 在调用setWiew函数后，如果使用的是便捷视图，例如（QListWidget、QTableWidget、QTreeWidget）等，需要调用setModel函数
        self.setModel(listwgt.model())

        # 通过setLineEdit用QLineEdit替换原有的文本显示控件，并设置为只读模式。
        lineEdit = QLineEdit(self)
        lineEdit.setReadOnly(True)
        self.setLineEdit(lineEdit)

        # 添加“全选”项
        self.add_item(allText)

    def add_item(self, text: str):
        # 定义CheckBox
        check = QCheckBox(text, self.view())
        # 给添加的CheckBox都绑定信号，目的是每次Check都能作出响应。
        check.stateChanged.connect(self.on_state_changed)
        self._checks.append(check)
        item = QListWidgetItem(self.view())
        self.view().addItem(item)
        self.view().setItemWidget(item, check)

        self.update_ui()

    def add_items(self, texts: list):
        # 添加多个item
        for text in texts:
            self.add_item(text)

    def clear(self):
        # 移除所有Item
        self.view().clear()

    def get_selected(self):
        # 获取被选中的Item
        sel_data = []
        for chk in self._checks:
            if self._checks[0] == chk:
                continue
            # 如果CheckBox是选中状态，则添加到列表中
            if chk.checkState() == Qt.Checked:
                sel_data.append(chk.text())
        return sel_data
    def set_selected(self,sel_data):
        # 设置选中的Item
        for chk in self._checks:
            if self._checks[0] == chk:
                continue
            # 如果CheckBox的文本在列表中，则设置为选中状态
            # chk.blockSignals(True)
            if chk.text() in sel_data:
                chk.setCheckState(Qt.Checked)
            else:
                chk.setCheckState(Qt.Unchecked)
            # chk.blockSignals(False)

    def set_all_state(self, state):
        # 设置“全选”按钮状态
        for chk in self._checks:
            chk.blockSignals(True)
            chk.setCheckState(Qt.CheckState(state))
            chk.blockSignals(False)

    def check_all_state(self):
        # 检查子选项是否达成全选
        for chk in self._checks:
            if self._checks[0] == chk:
                continue
            if chk.checkState() != Qt.Checked:
                return Qt.Unchecked
        return Qt.Checked

    def check_no_state(self):
        # 检查子选项是否达成全选
        for chk in self._checks:
            if chk.checkState() == Qt.Checked:
                return False
        return True

    def on_state_changed(self, state):
        # 根据Check选择状态改变时，改变lineEdit的文本显示内容
        if self.sender() == self._checks[0]:
            self.set_all_state(state)
        else:
            itemState = self.check_all_state()
            self._checks[0].blockSignals(True)
            self._checks[0].setCheckState(Qt.CheckState(itemState))
            self._checks[0].blockSignals(False)

        self.update_ui()
    def update_ui(self):
        if self._checks[0].checkState() == Qt.Checked:
            self.lineEdit().setText(self.allText)
        elif self.check_no_state():
            self.lineEdit().setText("未选择")
        else:
            sel_data = self.get_selected()
            self.itemChecked.emit(sel_data)
            self.lineEdit().setText(';'.join(sel_data))
