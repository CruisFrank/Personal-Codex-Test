"""Circuit component graphics items for the circuit designer application."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple, Type

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QBrush, QFont, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsObject


@dataclass(frozen=True)
class ComponentDefinition:
    """Definition for a circuit component available in the palette."""

    name: str
    description: str
    factory: Callable[[], "CircuitComponentItem"]


class CircuitComponentItem(QGraphicsObject):
    """Base class for all visual circuit elements."""

    def __init__(self, label: str = "") -> None:
        super().__init__()
        self.label = label
        self.setFlags(
            QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self) -> QRectF:  # pragma: no cover - Qt invoked
        return QRectF(-40, -25, 80, 50)

    def paint(self, painter: QPainter, option, widget=None) -> None:  # pragma: no cover - Qt invoked
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_symbol(painter)
        if self.label:
            font = QFont()
            font.setPointSize(8)
            painter.setFont(font)
            painter.setPen(QPen(Qt.black))
            painter.drawText(self.boundingRect(), Qt.AlignBottom | Qt.AlignHCenter, self.label)

    # The subclasses override this to paint their shape.
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover - Qt invoked
        raise NotImplementedError


class AmmeterItem(CircuitComponentItem):
    def __init__(self) -> None:
        super().__init__("A")

    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(QPointF(0, 0), 18, 18)


class VoltmeterItem(CircuitComponentItem):
    def __init__(self) -> None:
        super().__init__("V")

    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(QPointF(0, 0), 18, 18)


class FixedResistorItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-30, 0, -15, 0)
        painter.drawRect(-15, -8, 30, 16)
        painter.drawLine(15, 0, 30, 0)


class RheostatItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-35, 0, -15, 0)
        painter.drawRect(-15, -10, 40, 20)
        painter.drawLine(25, 0, 35, 0)
        painter.drawLine(-10, -12, 30, 12)
        painter.drawEllipse(QPointF(10, -5), 4, 4)


class ResistanceBoxItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(-25, -15, 50, 30)
        painter.drawLine(-20, -15, -20, -25)
        painter.drawLine(0, -15, 0, -25)
        painter.drawLine(20, -15, 20, -25)


class LampItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-35, 0, -15, 0)
        painter.drawLine(15, 0, 35, 0)
        painter.drawEllipse(QPointF(0, 0), 15, 15)
        painter.drawArc(-12, -12, 24, 24, 30 * 16, 120 * 16)


class MotorItem(CircuitComponentItem):
    def __init__(self) -> None:
        super().__init__("M")

    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(QPointF(0, 0), 18, 18)
        painter.drawLine(-18, 0, 18, 0)
        painter.drawLine(0, -18, 0, 18)


class BellItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawArc(-15, -15, 30, 30, 30 * 16, 120 * 16)
        painter.drawLine(-35, 0, -15, 0)
        painter.drawLine(15, 0, 35, 0)
        painter.drawLine(0, -15, 0, -25)
        painter.drawLine(0, -25, 10, -30)
        painter.drawEllipse(QPointF(10, -30), 3, 3)


class PowerSupplyItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-30, 0, -5, 0)
        painter.drawLine(-5, -15, -5, 15)
        painter.drawLine(5, -10, 5, 10)
        painter.drawLine(5, 0, 30, 0)


class SwitchItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-35, 0, -10, 0)
        painter.drawLine(10, 0, 35, 0)
        painter.drawLine(-10, 0, 10, -10)
        painter.drawEllipse(QPointF(10, 0), 4, 4)


class DoubleThrowSwitchItem(CircuitComponentItem):
    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(-35, 0, -10, 0)
        painter.drawLine(-10, 0, 10, -10)
        painter.drawLine(10, -10, 35, -10)
        painter.drawLine(10, -10, 35, 10)
        painter.drawEllipse(QPointF(35, -10), 4, 4)
        painter.drawEllipse(QPointF(35, 10), 4, 4)


class WireNodeItem(CircuitComponentItem):
    def __init__(self) -> None:
        super().__init__("")

    def draw_symbol(self, painter: QPainter) -> None:  # pragma: no cover
        painter.setBrush(QBrush(Qt.black))
        painter.drawEllipse(QPointF(0, 0), 3, 3)


class WireItem(QGraphicsItem):
    def __init__(self, start: QPointF, end: QPointF) -> None:
        super().__init__()
        self.start = start
        self.end = end
        self.setZValue(-1)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self) -> QRectF:  # pragma: no cover - Qt invoked
        pen_width = 4
        extra = pen_width / 2
        x1, y1 = self.start.x(), self.start.y()
        x2, y2 = self.end.x(), self.end.y()
        return QRectF(min(x1, x2) - extra, min(y1, y2) - extra, abs(x1 - x2) + pen_width, abs(y1 - y2) + pen_width)

    def paint(self, painter: QPainter, option, widget=None) -> None:  # pragma: no cover - Qt invoked
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.darkGray, 3, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(self.start, self.end)


COMPONENTS: Dict[str, ComponentDefinition] = {
    "Power Supply": ComponentDefinition(
        name="直流电源",
        description="标准的直流电源符号",
        factory=PowerSupplyItem,
    ),
    "Switch": ComponentDefinition(
        name="开关",
        description="常闭开关，可旋转表示开合状态",
        factory=SwitchItem,
    ),
    "Double Throw Switch": ComponentDefinition(
        name="单刀双掷开关",
        description="单刀双掷转换开关",
        factory=DoubleThrowSwitchItem,
    ),
    "Ammeter": ComponentDefinition(
        name="电流表",
        description="圆形表头带A标识",
        factory=AmmeterItem,
    ),
    "Voltmeter": ComponentDefinition(
        name="电压表",
        description="圆形表头带V标识",
        factory=VoltmeterItem,
    ),
    "Fixed Resistor": ComponentDefinition(
        name="定值电阻",
        description="矩形符号的定值电阻",
        factory=FixedResistorItem,
    ),
    "Rheostat": ComponentDefinition(
        name="滑动变阻器",
        description="带斜杠的滑动变阻器",
        factory=RheostatItem,
    ),
    "Resistance Box": ComponentDefinition(
        name="电阻箱",
        description="带拔塞的电阻箱",
        factory=ResistanceBoxItem,
    ),
    "Lamp": ComponentDefinition(
        name="小灯泡",
        description="灯泡符号",
        factory=LampItem,
    ),
    "Motor": ComponentDefinition(
        name="电动机",
        description="电动机符号",
        factory=MotorItem,
    ),
    "Bell": ComponentDefinition(
        name="电铃",
        description="电铃符号",
        factory=BellItem,
    ),
    "Wire Node": ComponentDefinition(
        name="导线节点",
        description="用于连接导线的节点",
        factory=WireNodeItem,
    ),
}
