import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

Rectangle {
	property alias icons_path: item_icon.source
	signal itemClicked()

	width: 70
	height: 70
	color: item_mouse_area.containsPress ? Qt.darker(menu.color, 0.6) : menu.color

	Image {
		id: item_icon
		anchors.centerIn: parent
		width: 25
		height: 25
	}

	ColorOverlay {
		anchors.fill: item_icon
		source: item_icon
		color: "lightgray"
	}

	MouseArea {
		id: item_mouse_area
		anchors.fill: parent
		onClicked: {
			itemClicked();
		}
	}
}
