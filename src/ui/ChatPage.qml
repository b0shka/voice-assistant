import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

Page {
	background: Rectangle {
		color: page.color
	}

	header: TitlePage {
		title_page: qsTr("Чат")
	}

	ColumnLayout {
		anchors.fill: parent

		ListView {
			id: chat_commands
			Layout.fillWidth: true
			Layout.fillHeight: true
			Layout.bottomMargin: 75
			verticalLayoutDirection: ListView.BottomToTop
			spacing: g_margin
			ScrollBar.vertical: ScrollBar {}

			model: commandsModel
			delegate: Rectangle {
				width: text_command.contentWidth + g_margin*2
				height: text_command.contentHeight + g_margin*2
				anchors.right: model.from === "me" ? chat_commands.contentItem.right : undefined
				anchors.left: model.from === "assistant" ? chat_commands.contentItem.left : undefined
				anchors.margins: g_margin
				color: model.from === "me" ? my_message_color : assistant_message_color
				radius: g_radius

				Text {
					id: text_command
					anchors.verticalCenter: parent.verticalCenter
					anchors.left: parent.left
					anchors.margins: g_margin
					text: model.text
					color: text_color
					font.pixelSize: 15
					font.family: 'Arial'
					width: 310
					wrapMode: TextEdit.WordWrap
				}
			}
		}

		ListModel {
			id: commandsModel

			ListElement {
				text: "У вас нет новых сообщений"
				from: "assistant"
			}
			ListElement {
				text: "Посмотреть сообщения в Вконтакте"
				from: "me"
			}
			ListElement {
				text: "Сообщения в телеграм успешно очищены"
				from: "assistant"
			}
			ListElement {
				text: "Очистить"
				from: "me"
			}
			ListElement {
				text: "Какое действие вы хотите выполнить?"
				from: "assistant"
			}
			ListElement {
				text: "Сообщения в телеграм"
				from: "me"
			}
			ListElement {
				text: "У вас пока нет уведомлений"
				from: "assistant"
			}
			ListElement {
				text: "Мои уведомления"
				from: "me"
			}
		}

		Rectangle {
			id: command_action
			Layout.fillWidth: true

			ButtonIcon {
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.bottom: parent.bottom
				width: 60
				height: 60
				radius: 100
				opacity: 0.8

				width_image: 30
				height_image: 50
				path_icon: "icons/microphone.png"
				color_icon: "gray"
				color_background: bg_color
				onIconClicked: {

				}
			}

			ButtonIcon {
				anchors.right: parent.right
				anchors.bottom: parent.bottom
				width: 35
				height: 35
				radius: 100

				width_image: 25
				height_image: 25
				path_icon: "icons/keyboard.png"
				color_icon: "gray"
				color_background: page.color
				onIconClicked: {

				}
			}
		}
	}
}
