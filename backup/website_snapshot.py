import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import os
import webbrowser
from time import sleep

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

s = Screenshot()
url = 'https://www.google.com/maps/@13.748446,100.5343197,13z/data=!5m1!1e1'
s.capture(url, 'website.png')

