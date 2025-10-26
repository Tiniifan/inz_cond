from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
                              QFormLayout, QSpinBox, QCheckBox, QListWidget, QPushButton, 
                              QDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal

from gui.dialogs import AddFlagDialog, AddItemDialog

class PlaygroundPanel(QWidget):
    # Signal emitted when data changes
    data_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #2D2D30;")
        self.setMaximumHeight(250)
        
        self.playground_data = {}
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        panel_title = QLabel("PLAYGROUND CONFIGURATION")
        panel_title.setStyleSheet("color: #4DD0E1; font-size: 12px; font-weight: bold;")
        layout.addWidget(panel_title)
        
        # Create tabs
        self.playground_tabs = QTabWidget()
        self.playground_tabs.setStyleSheet("""
            QTabWidget::pane { background-color: #1E1E1E; border: 1px solid #3E3E3E; }
            QTabBar::tab { background-color: #2D2D30; color: #CCCCCC; padding: 5px 15px; }
            QTabBar::tab:selected { background-color: #1E1E1E; color: #4DD0E1; }
        """)
        
        layout.addWidget(self.playground_tabs)
        
        # Style
        style = """
            QSpinBox, QCheckBox, QListWidget, QPushButton {
                background-color: #3C3C3C;
                color: #CCCCCC;
                border: 1px solid #3E3E3E;
                padding: 3px;
            }
            QPushButton:hover { background-color: #4A4A4A; }
        """
        self.setStyleSheet(self.styleSheet() + style)
    
    def load_data(self, data):
        """Load playground data"""
        self.playground_data = data
        self._build_ui()
    
    def _build_ui(self):
        """Builds the interface with current data"""
        self.playground_tabs.clear()
        
        # Tab 1: Basic Values
        self._create_basic_tab()
        
        # Tab 2-5: Flags
        self._create_flag_tab("TEMP_BIT_FLAG", "Temp Bit Flags")
        self._create_flag_tab("TEMP_MAP_BIT_FLAG", "Temp Map Bit Flags")
        self._create_flag_tab("GLOBAL_BIT_FLAG", "Global Bit Flags")
        self._create_flag_tab("GLOBAL_T_BOX_FLAG", "Global TBox Flags")
        
        # Tab 6: Items
        self._create_items_tab()
    
    def _create_basic_tab(self):
        """Creates the basic values tab"""
        basic_tab = QWidget()
        basic_layout = QFormLayout(basic_tab)
        basic_layout.setContentsMargins(10, 10, 10, 10)
        
        self.sub_phase_spin = QSpinBox()
        self.sub_phase_spin.setRange(0, 999999999)
        self.sub_phase_spin.setValue(self.playground_data["SUB_PHASE_VALUE"])
        self.sub_phase_spin.valueChanged.connect(lambda v: self._update_value("SUB_PHASE_VALUE", v))
        basic_layout.addRow("SUB_PHASE_VALUE:", self.sub_phase_spin)
        
        self.phase_spin = QSpinBox()
        self.phase_spin.setRange(0, 999999999)
        self.phase_spin.setValue(self.playground_data["PHASE_VALUE"])
        self.phase_spin.valueChanged.connect(lambda v: self._update_value("PHASE_VALUE", v))
        basic_layout.addRow("PHASE_VALUE:", self.phase_spin)
        
        self.chapter_spin = QSpinBox()
        self.chapter_spin.setRange(0, 999999999)
        self.chapter_spin.setValue(self.playground_data["CHAPTER_VALUE"])
        self.chapter_spin.valueChanged.connect(lambda v: self._update_value("CHAPTER_VALUE", v))
        basic_layout.addRow("CHAPTER_VALUE:", self.chapter_spin)
        
        self.frame_chapter_spin = QSpinBox()
        self.frame_chapter_spin.setRange(0, 999999999)
        self.frame_chapter_spin.setValue(self.playground_data["FRAME_CHAPTER_VALUE"])
        self.frame_chapter_spin.valueChanged.connect(lambda v: self._update_value("FRAME_CHAPTER_VALUE", v))
        basic_layout.addRow("FRAME_CHAPTER_VALUE:", self.frame_chapter_spin)
        
        self.shop_open_check = QCheckBox()
        self.shop_open_check.setChecked(self.playground_data["SHOP_OPEN_VALUE"])
        self.shop_open_check.stateChanged.connect(lambda: self._update_value("SHOP_OPEN_VALUE", self.shop_open_check.isChecked()))
        basic_layout.addRow("SHOP_OPEN_VALUE:", self.shop_open_check)
        
        self.playground_tabs.addTab(basic_tab, "Basic")
    
    def _create_flag_tab(self, flag_name, tab_title):
        """Creates a tab to manage flags"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        list_widget = QListWidget()
        list_widget.setStyleSheet("background-color: #1E1E1E; color: #CCCCCC;")
        
        # Populate list
        for key, value in self.playground_data[flag_name].items():
            list_widget.addItem(f"{key}: {value}")
        
        layout.addWidget(list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(lambda: self._add_flag(flag_name, list_widget))
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self._remove_flag(flag_name, list_widget))
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        self.playground_tabs.addTab(tab, tab_title)
    
    def _create_items_tab(self):
        """Creates the tab to manage items"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.items_list = QListWidget()
        self.items_list.setStyleSheet("background-color: #1E1E1E; color: #CCCCCC;")
        
        # Populate list
        for item in self.playground_data["HAVE_ITEM"]:
            self.items_list.addItem(item)
        
        layout.addWidget(self.items_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self._add_item)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove Item")
        remove_btn.clicked.connect(self._remove_item)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        self.playground_tabs.addTab(tab, "Have Items")
    
    def _update_value(self, key, value):
        """Updates a value"""
        self.playground_data[key] = value
        self.data_changed.emit(self.playground_data)
    
    def _add_flag(self, flag_name, list_widget):
        """Adds a flag"""
        dialog = AddFlagDialog(self, f"Add {flag_name}")
        if dialog.exec() == QDialog.DialogCode.Accepted:
            key, value = dialog.get_values()
            self.playground_data[flag_name][str(key)] = value
            list_widget.addItem(f"{key}: {value}")
            self.data_changed.emit(self.playground_data)
    
    def _remove_flag(self, flag_name, list_widget):
        """Removes a flag"""
        current_item = list_widget.currentItem()
        if current_item:
            key = current_item.text().split(":")[0].strip()
            if key in self.playground_data[flag_name]:
                del self.playground_data[flag_name][key]
            list_widget.takeItem(list_widget.currentRow())
            self.data_changed.emit(self.playground_data)
    
    def _add_item(self):
        """Add an item"""
        dialog = AddItemDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            item = dialog.get_value()
            if item:
                self.playground_data["HAVE_ITEM"].append(item)
                self.items_list.addItem(item)
                self.data_changed.emit(self.playground_data)
    
    def _remove_item(self):
        """Deletes an item"""
        current_item = self.items_list.currentItem()
        if current_item:
            item_text = current_item.text()
            if item_text in self.playground_data["HAVE_ITEM"]:
                self.playground_data["HAVE_ITEM"].remove(item_text)
            self.items_list.takeItem(self.items_list.currentRow())
            self.data_changed.emit(self.playground_data)