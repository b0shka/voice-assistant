import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.0

Label {
	property alias title_page: text_title.text

    height: 60
    background: Rectangle {
        color: page.color
    }

    Text {
		id: text_title
		anchors.centerIn: parent
        font.pixelSize: 23
        font.bold: true
        font.family: 'Arial'
        color: text_color
    }
}
