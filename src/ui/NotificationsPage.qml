import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Page {
	background: Rectangle {
		color: page.color
	}

	header: TitlePage {
		title_page: qsTr("Уведомления")
	}

	Keys.onEscapePressed: {
		popPage();
	}
}
