import os
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QLineEdit, QListWidget, QHBoxLayout, QTabWidget, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon


CONFIG_FILE = os.path.join(os.path.expanduser("~"), "DummyGameLauncher_config.json")


class GameLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dummy's game launcher")
        self.setGeometry(200, 200, 500, 400)
        self.setWindowIcon(QIcon("logo.png"))

        # Load game data from config file
        self.games = self.load_games()

        # UI Components
        main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.game_tab = QWidget()
        self.info_tab = QWidget()

        # Game Tab Layout
        game_layout = QVBoxLayout()
        self.game_list = QListWidget()
        self.game_list.itemDoubleClicked.connect(self.launch_selected_game)
        game_layout.addWidget(self.game_list)

        button_layout = QHBoxLayout()
        self.add_game_button = QPushButton("Add Game")
        self.add_game_button.clicked.connect(self.add_game)
        self.remove_game_button = QPushButton("Remove Game")
        self.remove_game_button.clicked.connect(self.remove_game)
        button_layout.addWidget(self.add_game_button)
        button_layout.addWidget(self.remove_game_button)

        game_layout.addLayout(button_layout)
        self.game_tab.setLayout(game_layout)

        # Info Tab Layout
        info_layout = QVBoxLayout()

        # Changelog Section
        self.changelog_label = QLabel("Changelog:")
        self.changelog_text = QTextEdit()
        self.changelog_text.setReadOnly(True)
        self.changelog_text.setText("Version 0.1 Alpha\n- Initial release\n\nThis is the first release\n\nYou can add apps and game (rich presence for half life) but logo not working \n\nNext update may have better ui or working icon")
        
        # Credits Section
        self.credits_label = QLabel("Credits:")
        self.credits_text = QTextEdit()
        self.credits_text.setReadOnly(True)
        self.credits_text.setText("Dummy's Game Launcher\nCode: ChatGPT\n\nIdea: Dummylot \n\nSupervisor: Dummylot\n\nDebugging: Dummylot\n\nChannel: https://m.youtube.com/Dummylot0")

        info_layout.addWidget(self.changelog_label)
        info_layout.addWidget(self.changelog_text)
        info_layout.addWidget(self.credits_label)
        info_layout.addWidget(self.credits_text)

        self.info_tab.setLayout(info_layout)

        # Add tabs
        self.tabs.addTab(self.game_tab, "Games")
        self.tabs.addTab(self.info_tab, "Changelog & Credits")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # Populate game list
        self.refresh_game_list()

    def load_games(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_games(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.games, file, indent=4)

    def refresh_game_list(self):
        self.game_list.clear()
        for game_name in self.games:
            self.game_list.addItem(game_name)

    def add_game(self):
        game_path, _ = QFileDialog.getOpenFileName(self, "Select Game Executable")
        if not game_path:
            return

        game_name = os.path.basename(game_path)
        if game_name.lower() == "hl.exe":
            game_name = "Counter-Strike (Half-Life)"
            game_args = "-game cstrike"
        else:
            game_args = ""

        # Select game logo
        logo_path, _ = QFileDialog.getOpenFileName(self, "Select Game Logo (Optional)")
        if logo_path:
            logo_path = os.path.abspath(logo_path)

        self.games[game_name] = {"path": game_path, "args": game_args, "logo": logo_path}
        self.save_games()
        self.refresh_game_list()

    def remove_game(self):
        selected_item = self.game_list.currentItem()
        if selected_item:
            game_name = selected_item.text()
            del self.games[game_name]
            self.save_games()
            self.refresh_game_list()

    def launch_selected_game(self):
        selected_item = self.game_list.currentItem()
        if selected_item:
            game_name = selected_item.text()
            game_data = self.games[game_name]
            game_path = game_data["path"]
            game_args = game_data.get("args", "")
         
            try:
                # Launch the game with arguments
                if game_args:
                    subprocess.Popen([game_path] + game_args.split())
                else:
                    subprocess.Popen([game_path])
            except Exception as e:
                print(f"Error launching game: {e}")
if __name__ == "__main__":
    app = QApplication([])
    launcher = GameLauncher()
    launcher.show()
    app.exec_()
