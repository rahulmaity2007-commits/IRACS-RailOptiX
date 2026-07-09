import sys
from PySide6.QtCore import Qt, QTimer, QTime
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)


class IRACSLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IRACS - Railway Control Login")
        self.setMinimumSize(600, 720)
        self.setStyleSheet(
            """
            QWidget {
                background: #0f172a;
                color: #e2e8f0;
                font-family: Segoe UI, Arial, sans-serif;
            }
            QLabel {
                color: #cbd5e1;
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                background: transparent;
                border: none;
                border-bottom: 1px solid rgba(148, 163, 184, 0.2);
                padding: 12px 0 10px 0;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-bottom: 1px solid rgba(59, 130, 246, 0.95);
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2563eb, stop:1 #1d4ed8);
                color: white;
                border-radius: 14px;
                padding: 14px;
                font-weight: 700;
                font-size: 14px;
                min-height: 46px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1d4ed8, stop:1 #2563eb);
            }
            QLabel#headerLabel {
                font-size: 20px;
                font-weight: 800;
                color: white;
                letter-spacing: 0.3px;
            }
            QLabel#subtitleLabel {
                font-size: 12px;
                color: #94a3b8;
                background: transparent;
                border: none;
                padding: 0;
            }
            QComboBox {
                padding-right: 30px;
            }
            """
        )

        central = QWidget(self)
        central.setStyleSheet(
            "QWidget {"
            "background-color: #0f172a;"
            "background-image: url(Indian_Railways_Logo.svg);"
            "background-repeat: no-repeat;"
            "background-position: top center;"
            "background-size: 180px 180px;"
            "background-attachment: fixed;"
            "}"
        )
        self.setCentralWidget(central)

        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(40, 100, 40, 40)
        outer_layout.setSpacing(0)
        outer_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        card = QWidget()
        card.setMinimumWidth(520)
        card.setMaximumWidth(640)
        card.setStyleSheet(
            "background: rgba(15, 23, 42, 0.88); "
            "border-radius: 28px;"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(18)

        title = QLabel("Indian Railway Automated Control System")
        title.setObjectName("headerLabel")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)
        title.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(title)

        badge = QLabel("RAILWAY CONTROL")
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            "background: rgba(37, 99, 235, 0.15); color: #c7d2fe; "
            "border-radius: 999px; font-size: 11px; font-weight: 700; padding: 8px 18px;"
        )
        card_layout.addWidget(badge)

        subtitle = QLabel("Decision Support & Operational Control Login")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setContentsMargins(0, 0, 0, 0)
        card_layout.addWidget(subtitle)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(48)
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(48)
        card_layout.addWidget(self.password_input)

        self.role_combo = QComboBox()
        self.role_combo.setMinimumHeight(48)
        self.role_combo.addItems(["Section Controller", "CRIS Administrator", "Operations Supervisor"])
        card_layout.addWidget(self.role_combo)

        button_row = QWidget()
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(14)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setMinimumHeight(46)
        button_layout.addWidget(login_button, 1)

        self.clock_label = QLabel("")
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setStyleSheet(
            "font-size: 14px; font-weight: 700; color: #e2e8f0; background: rgba(255,255,255,0.06); border-radius: 14px; padding: 12px;"
        )
        self.clock_label.setFixedWidth(140)
        button_layout.addWidget(self.clock_label)

        card_layout.addWidget(button_row)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #fca5a5; margin-top: 8px;")
        card_layout.addWidget(self.status_label)

        card_layout.addSpacing(8)
        card_layout.addStretch()

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        footer = QLabel("Railway operational login powered by IRACS")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 10px; color: rgba(203, 213, 225, 0.6); padding-top:12px;")
        card_layout.addWidget(footer)

        outer_layout.addStretch()
        outer_layout.addWidget(card, alignment=Qt.AlignHCenter)
        outer_layout.addStretch()

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        valid_users = {
            "Section Controller": {"controller": "rail123"},
            "CRIS Administrator": {"cris": "admin123"},
            "Operations Supervisor": {"ops": "ops123"},
        }

        if username and password:
            if username.lower() in valid_users[role] and valid_users[role][username.lower()] == password:
                self.status_label.setStyleSheet("color: #86efac; margin-top: 8px;")
                self.status_label.setText(f"Access granted. Welcome, {role}.")
                QMessageBox.information(
                    self,
                    "Login Successful",
                    f"Welcome {username}!\nYou can now manage train prioritization, crossings, overtakes, and loop-line allocation.",
                )
            else:
                self.status_label.setStyleSheet("color: #fca5a5; margin-top: 8px;")
                self.status_label.setText("Invalid username or password for the selected role.")
        else:
            self.status_label.setStyleSheet("color: #fca5a5; margin-top: 8px;")
            self.status_label.setText("Please enter both username and password.")

    def update_clock(self):
        now = QTime.currentTime()
        self.clock_label.setText(now.toString("hh:mm:ss AP"))

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()
        self.role_combo.setCurrentIndex(0)
        self.status_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IRACSLoginWindow()
    window.show()
    sys.exit(app.exec())