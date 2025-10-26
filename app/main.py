"""Main entry point for the Junior Physics Circuit Designer application."""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QIcon, QKeySequence
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .components import COMPONENTS, CircuitComponentItem, ComponentDefinition, WireItem


@dataclass
class WireDraft:
    start: QPointF


class CircuitScene(QGraphicsScene):
    """Scene with a subtle grid to help aligning components."""

    def __init__(self) -> None:
        super().__init__(-800, -600, 1600, 1200)
        self._grid_color = QColor(220, 220, 220)
        self._grid_size = 25

    def drawBackground(self, painter, rect):  # pragma: no cover - Qt invoked
        super().drawBackground(painter, rect)
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        lines = []
        for x in range(left - (left % self._grid_size), right, self._grid_size):
            lines.append(((x, top), (x, bottom)))
        for y in range(top - (top % self._grid_size), bottom, self._grid_size):
            lines.append(((left, y), (right, y)))
        painter.setPen(QColor(self._grid_color))
        for (x1, y1), (x2, y2) in lines:
            painter.drawLine(x1, y1, x2, y2)


class PaletteWidget(QWidget):
    """Simple palette with component list and helper text."""

    def __init__(self, on_add_component) -> None:
        super().__init__()
        self.on_add_component = on_add_component
        layout = QVBoxLayout(self)
        header = QLabel("元件库")
        header.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 4px;")
        layout.addWidget(header)

        hint = QLabel("双击元件添加到画布，选择后可旋转或删除。")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #555;")
        layout.addWidget(hint)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        for key, definition in COMPONENTS.items():
            item = QListWidgetItem(definition.name)
            item.setData(Qt.UserRole, key)
            item.setToolTip(definition.description)
            self.list_widget.addItem(item)
        self.list_widget.itemDoubleClicked.connect(self._handle_item_double_click)
        layout.addWidget(self.list_widget)
        layout.addStretch()

    def _handle_item_double_click(self, item: QListWidgetItem) -> None:
        key = item.data(Qt.UserRole)
        if key:
            self.on_add_component(COMPONENTS[key])


class CanvasView(QGraphicsView):
    """Custom view to support panning with middle mouse button."""

    def __init__(self, scene: CircuitScene) -> None:
        super().__init__(scene)
        self.setRenderHint(self.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setBackgroundBrush(QColor(250, 250, 252))
        self._panning = False
        self._last_pan_point: Optional[QPointF] = None

    def wheelEvent(self, event):  # pragma: no cover - Qt invoked
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.25 if event.angleDelta().y() > 0 else 0.8
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event):  # pragma: no cover - Qt invoked
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._last_pan_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):  # pragma: no cover - Qt invoked
        if self._panning and self._last_pan_point is not None:
            delta = event.pos() - self._last_pan_point
            self._last_pan_point = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # pragma: no cover - Qt invoked
        if event.button() == Qt.MiddleButton and self._panning:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    """Main window for the circuit designer."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("初中物理电路图绘制器 1.0")
        self.resize(1200, 800)
        self.scene = CircuitScene()
        self.view = CanvasView(self.scene)
        self._wire_draft: Optional[WireDraft] = None

        palette = PaletteWidget(self._add_component_to_scene)

        splitter = QSplitter()
        splitter.addWidget(palette)
        splitter.addWidget(self.view)
        splitter.setSizes([250, 950])

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        self._build_toolbar()
        self._build_menus()

    # region UI helpers
    def _build_toolbar(self) -> None:
        toolbar = QToolBar("工具")
        toolbar.setIconSize(toolbar.iconSize())
        self.addToolBar(toolbar)

        self.wire_action = QAction(QIcon.fromTheme("draw-line"), "导线模式", self)
        self.wire_action.setCheckable(True)
        self.wire_action.setStatusTip("启用后在画布上点击两次画直线导线")
        toolbar.addAction(self.wire_action)

        rotate_left = QAction("左转90°", self)
        rotate_left.setShortcut(QKeySequence("Ctrl+L"))
        rotate_left.triggered.connect(lambda: self._rotate_selected(-90))
        toolbar.addAction(rotate_left)

        rotate_right = QAction("右转90°", self)
        rotate_right.setShortcut(QKeySequence("Ctrl+R"))
        rotate_right.triggered.connect(lambda: self._rotate_selected(90))
        toolbar.addAction(rotate_right)

        delete_action = QAction("删除", self)
        delete_action.setShortcut(QKeySequence.Delete)
        delete_action.triggered.connect(self._delete_selected)
        toolbar.addAction(delete_action)

        reset_action = QAction("清空画布", self)
        reset_action.triggered.connect(lambda: self.scene.clear())
        toolbar.addAction(reset_action)

    def _build_menus(self) -> None:
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件(&F)")
        file_menu.addAction("退出", self.close)

        help_menu = menubar.addMenu("帮助(&H)")
        about_action = help_menu.addAction("关于")
        about_action.triggered.connect(self._show_about)

    # endregion

    # region Scene manipulation helpers
    def _add_component_to_scene(self, definition: ComponentDefinition) -> None:
        item = definition.factory()
        item.setPos(self.view.mapToScene(self.view.viewport().rect().center()))
        self.scene.addItem(item)

    def _rotate_selected(self, angle: int) -> None:
        for item in self.scene.selectedItems():
            if isinstance(item, CircuitComponentItem):
                item.setRotation(item.rotation() + angle)

    def _delete_selected(self) -> None:
        for item in list(self.scene.selectedItems()):
            self.scene.removeItem(item)

    # endregion

    def mousePressEvent(self, event):  # pragma: no cover - Qt invoked
        if self.wire_action.isChecked() and event.button() == Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos() - self.view.pos())
            if self._wire_draft is None:
                self._wire_draft = WireDraft(start=scene_pos)
            else:
                wire = WireItem(self._wire_draft.start, scene_pos)
                self.scene.addItem(wire)
                self._wire_draft = None
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):  # pragma: no cover - Qt invoked
        if self._wire_draft is not None and self.wire_action.isChecked():
            scene_pos = self.view.mapToScene(event.pos() - self.view.pos())
            self.statusBar().showMessage(f"导线起点：({self._wire_draft.start.x():.0f}, {self._wire_draft.start.y():.0f}) → 当前：({scene_pos.x():.0f}, {scene_pos.y():.0f})")
        else:
            self.statusBar().clearMessage()
        super().mouseMoveEvent(event)

    def _show_about(self) -> None:
        QMessageBox.about(self, "关于", "")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
