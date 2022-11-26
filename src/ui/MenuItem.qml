import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

Rectangle {
	id: menu_item
	//property alias path_icon: item_icon.source
	//signal itemClicked

	width: 80
	height: 80
	color: panel_color

	Image {
		id: item_icon
		anchors.centerIn: parent
		width: 30
		height: 30
		source: "icons/chat.png"
	}

	ColorOverlay {
		anchors.fill: item_icon
		source: item_icon
		color: "white"
	}

	MouseArea {
		anchors.fill: parent
		onClicked: {
			menu_item.itemClicked();
		}
	}
}
