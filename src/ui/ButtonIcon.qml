import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

Rectangle {
	anchors.margins: g_margin
	color: button_mouse_area.containsPress ? Qt.darker(color_background, 0.6) : color_background

	property alias width_image: button_icon.width
	property alias height_image: button_icon.height
	property alias path_icon: button_icon.source
	property alias color_icon: color_button_icon.color
	property color color_background

	signal iconClicked()

	Image {
		id: button_icon
		anchors.centerIn: parent
	}

	ColorOverlay {
		id: color_button_icon
		anchors.fill: button_icon
		source: button_icon
	}

	MouseArea {
		id: button_mouse_area
		anchors.fill: parent
		onClicked: {
			iconClicked();
		}
	}
}
