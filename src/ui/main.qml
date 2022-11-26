import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

ApplicationWindow {
	id: mainWindow
	visible: true
	width: 510
	minimumWidth: 510
	maximumWidth: 510
	height: 640
	minimumHeight: 640
	maximumHeight: 640
	title: qsTr("Голосовой ассистент")

	//flags: Qt.FramelessWindowHint
	//property int previousX
	//property int previousY

	function popPage() {
		stackView.pop();
	}

	readonly property int g_margin: 10
	readonly property int g_radius: 10
	readonly property color bg_color: "#17212b"
	readonly property color my_message_color: "#346391"
	readonly property color assistant_message_color: "#545353"
	readonly property color panel_color: "#0e1621"
	readonly property color text_color: "white"

	/*
	MouseArea {
		id: topArea
		height: 5
		anchors {
			top: parent.top
			left: parent.left
			right: parent.right
		}
		cursorShape: Qt.SizeVerCursor

		onPressed: {
			previousY = mouseY
		}

		onMouseYChanged: {
			var dy = mouseY - previousY
			mainWindow.setY(mainWindow.y + dy)
			mainWindow.setHeight(mainWindow.height - dy)
		}
	}

	MouseArea {
		id: bottomArea
		height: 5
		anchors {
			bottom: parent.bottom
			left: parent.left
			right: parent.right
		}
		cursorShape: Qt.SizeVerCursor

		onPressed: {
			previousY = mouseY
		}

		onMouseYChanged: {
			var dy = mouseY - previousY
			mainWindow.setHeight(mainWindow.height + dy)
		}
	}

	MouseArea {
		id: leftArea
		width: 5
		anchors {
			top: topArea.bottom
			bottom: bottomArea.top
			left: parent.left
		}
		cursorShape: Qt.SizeHorCursor

		onPressed: {
			previousX = mouseX
		}

		onMouseXChanged: {
			var dx = mouseX - previousX
			mainWindow.setX(mainWindow.x + dx)
			mainWindow.setWidth(mainWindow.width - dx)
		}
	}

	MouseArea {
		id: rightArea
		width: 5
		anchors {
			top: topArea.bottom
			bottom: bottomArea.top
			right: parent.right
		}
		cursorShape:  Qt.SizeHorCursor

		onPressed: {
			previousX = mouseX
		}

		onMouseXChanged: {
			var dx = mouseX - previousX
			mainWindow.setWidth(mainWindow.width + dx)
		}
	}

	MouseArea {
		anchors {
			top: topArea.bottom
			bottom: bottomArea.top
			left: leftArea.right
			right: rightArea.left
		}

		onPressed: {
			previousX = mouseX
			previousY = mouseY
		}

		onMouseXChanged: {
			var dx = mouseX - previousX
			mainWindow.setX(mainWindow.x + dx)
		}

		onMouseYChanged: {
			var dy = mouseY - previousY
			mainWindow.setY(mainWindow.y + dy)
		}
	}
	*/

	Rectangle {
		id: root
		anchors.fill: parent

		Row {
			Rectangle {
				id: menu
				width: 70
				height: 640
				color: panel_color

				Column {
					anchors.fill: parent
					anchors.topMargin: g_margin
					spacing: g_margin

					ItemMenu {
						icons_path: "icons/chat.png"
						onItemClicked: {
							stackView.clear();
							stackView.push(chatPage);
						}
					}

					ItemMenu {
						icons_path: "icons/notifications.png"
						onItemClicked: {
							stackView.clear();
							stackView.push(notificationsPage);
						}
					}

					ItemMenu {
						icons_path: "icons/contacts.png"
						onItemClicked: {
							stackView.clear();
							stackView.push(contactsPage);
						}
					}
				}

			}

			Rectangle {
				id: page
				width: 440
				height: 640
				color: bg_color

				StackView {
					id: stackView
					anchors.fill: parent
					initialItem: chatPage
				}

				ChatPage {
					id: chatPage
					title: qsTr("Чат")
				}

				NotificationsPage {
					id: notificationsPage
					visible: false
					title: qsTr("Уведомления")
				}

				ContactsPage {
					id: contactsPage
					visible: false
					title: qsTr("Контакты")
				}

			}
		}
	}
}
