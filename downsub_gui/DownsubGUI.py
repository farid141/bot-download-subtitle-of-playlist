from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
from downsub.downsub import Downsub


class DownsubGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bot Playlist Subtitle')
        self.le_playlist_link = QLineEdit('insert link', self)

        start_button = QPushButton(text='start')
        start_button.clicked.connect(self.start_download)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.le_playlist_link)
        input_layout.addWidget(start_button)

        self.setLayout(input_layout)

    def start_download(self):
        link = self.le_playlist_link.text()

        # create webdriver object
        job_inst = Downsub(link)
        # this will enter youtube playlist link and navigate to first page
        job_inst.land_first_page()

        next_page = 1
        count = 0
        while(next_page):
            # finding every playlist section on current page
            playlists = job_inst.find_playlist_section()

            print(f"len of playlist in current page{len(playlists)}")

            for playlist in playlists:
                # clicking download srt button
                print(f"{count}-subtitle")
                count += 1
                job_inst.download_subtitles(playlist)

            # go to the next page
            next_page = job_inst.check_pagination()
