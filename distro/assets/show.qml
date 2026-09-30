import QtQuick 2.0
import calamares.slideshow 1.0

Presentation {
    id: presentation
    Timer {
        interval: 15000
        running: true
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }
    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#061326"
            Image {
                source: "logo.png"
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 32
                width: parent.width * 0.50
                height: parent.height * 0.50
                fillMode: Image.PreserveAspectFit
            }
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 80
                text: "Welcome to Cachuntu"
                color: "#F0F7FF"
                font.family: "Inter"
                font.pixelSize: 34
            }
            Text {
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 42
                text: "KDE Plasma by default. Your desktop, your choice."
                color: "#4DE4D1"
                font.family: "Inter"
                font.pixelSize: 18
            }
        }
    }
    Slide {
        Rectangle {
            anchors.fill: parent
            color: "#061326"
            Text {
                anchors.centerIn: parent
                width: parent.width * 0.8
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                text: "Built on Ubuntu 26.04 LTS\nBtrfs by default. Gaming, multimedia and development tools are optional."
                color: "#F0F7FF"
                font.family: "Inter"
                font.pixelSize: 28
            }
        }
    }
}
