#!/usr/bin/env python3
import sys
import os
import urllib.request
import xml.etree.ElementTree as ET
import re
import datetime

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QComboBox, QMessageBox
)

# Global EPG URL
EPG_URL = "http://1ere-serrvices.com:80/xmltv.php?username=363ys5p123e&password=perv0j5t8x&type=m3u_plus&output=mpegts"

def fetch_epg_data():
    """Fetch and parse the XMLTV data from EPG_URL.
    Returns a list of programme dicts with keys: channel, title, start, stop, and optionally image.
    We assume that if an image URL is provided in the XML, it would be in an attribute called 'img'."""
    try:
        response = urllib.request.urlopen(EPG_URL)
        content = response.read()
        root = ET.fromstring(content)
        programmes = []
        for prog in root.findall("programme"):
            start = prog.get("start")
            stop = prog.get("stop")
            channel = prog.get("channel")
            title_elem = prog.find("title")
            title = title_elem.text if title_elem is not None else "No Title"
            # Optional: get an image URL/attribute from XML data if provided.
            img = prog.get("img", "")
            programmes.append({
                "channel": channel,
                "title": title,
                "start": start,
                "stop": stop,
                "img": img
            })
        return programmes
    except Exception as e:
        print("Error fetching EPG:", e)
        return []

def parse_xmltv_time(time_str):
    """
    Parse XMLTV time string. Assume format is YYYYMMDDHHMMSS (ignoring timezone).
    Returns a datetime.datetime object.
    """
    try:
        return datetime.datetime.strptime(time_str[:14], "%Y%m%d%H%M%S")
    except Exception as e:
        print("Time parse error:", e)
        return None

class EPGWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPTVking - EPG")
        self.resize(1200, 600)
        self.all_programmes = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Top controls layout
        controls_layout = QHBoxLayout()
        
        # Search field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search channels/programs...")
        self.search_field.textChanged.connect(self.update_table)
        controls_layout.addWidget(self.search_field)
        
        # Category filter (e.g., All Channels, Sports Channels)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["All Channels", "Sports Channels"])
        self.category_combo.currentIndexChanged.connect(self.update_table)
        controls_layout.addWidget(self.category_combo)
        
        # Time range selection (6, 12, or 24 hours)
        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems(["6 hours", "12 hours", "24 hours"])
        self.time_range_combo.currentIndexChanged.connect(self.update_table)
        controls_layout.addWidget(self.time_range_combo)
        
        # New: Hide channels by country codes (e.g., "US,UK")
        self.hide_channels_field = QLineEdit()
        self.hide_channels_field.setPlaceholderText("Hide channels by country codes (e.g. US,UK)")
        self.hide_channels_field.textChanged.connect(self.update_table)
        controls_layout.addWidget(self.hide_channels_field)
        
        # Refresh button
        refresh_button = QPushButton("Refresh EPG")
        refresh_button.clicked.connect(self.refresh_epg)
        controls_layout.addWidget(refresh_button)
        
        main_layout.addLayout(controls_layout)
        
        # Summary label: total live channels (unique channels in filtered data)
        self.summary_label = QLabel("Loading EPG...")
        main_layout.addWidget(self.summary_label)
        
        # EPG grid table. First column is for channel info (image or text).
        self.table = QTableWidget()
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        
        # Initial load
        self.refresh_epg()

    def refresh_epg(self):
        self.all_programmes = fetch_epg_data()
        if not self.all_programmes:
            QMessageBox.warning(self, "EPG Error", "Failed to fetch EPG data.")
            return
        self.update_table()

    def update_table(self):
        # === Filtering channels based on search, category, and hide country codes ===
        search_text = self.search_field.text().strip().lower()
        category_filter = self.category_combo.currentText()
        hide_text = self.hide_channels_field.text().strip()
        hide_codes = [code.strip().upper() for code in hide_text.split(",") if code.strip()]
        
        # Build unique channel list from all programmes.
        channels = sorted({prog["channel"] for prog in self.all_programmes})
        
        # Apply search filter.
        if search_text:
            channels = [c for c in channels if search_text in c.lower()]
        # Apply category filter; demo: channels containing "sport" for sports channels.
        if category_filter == "Sports Channels":
            channels = [c for c in channels if "sport" in c.lower()]
        # Apply hide channels filter based on country codes.
        if hide_codes:
            channels = [
                c for c in channels
                if not any(c.upper().startswith(code + "_") or c.upper().startswith(code + "-") for code in hide_codes)
            ]
        self.filtered_channels = channels
        self.summary_label.setText(f"Live Channels: {len(channels)}")
        
        # === Determine grid time range ===
        selected_range_text = self.time_range_combo.currentText()
        if "6" in selected_range_text:
            hours = 6
        elif "12" in selected_range_text:
            hours = 12
        elif "24" in selected_range_text:
            hours = 24
        else:
            hours = 6
        
        now = datetime.datetime.now()
        grid_start = now.replace(minute=0, second=0, microsecond=0)
        grid_start = grid_start.replace(minute=0) if now.minute < 30 else grid_start.replace(minute=30)
        grid_end = grid_start + datetime.timedelta(hours=hours)
        
        # Create 30-minute time slots.
        time_slots = []
        t = grid_start
        while t < grid_end:
            time_slots.append(t)
            t += datetime.timedelta(minutes=30)
        num_slots = len(time_slots)
        total_columns = num_slots + 1  # First column for channel info.
        num_rows = len(self.filtered_channels)
        
        # === Setup table structure ===
        self.table.clear()
        self.table.setRowCount(num_rows)
        self.table.setColumnCount(total_columns)
        header_labels = ["Channel"] + [t.strftime("%H:%M") for t in time_slots]
        self.table.setHorizontalHeaderLabels(header_labels)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        # Dictionary to record if a channel row uses an image.
        channel_has_image = {}
        
        # === Set channel info column ===
        for row, chan in enumerate(self.filtered_channels):
            # Check for an image in /data/channel_images/ (png or jpg)
            img_path = os.path.join("data", "channel_images", f"{chan}.png")
            if not os.path.exists(img_path):
                img_path = os.path.join("data", "channel_images", f"{chan}.jpg")
            if os.path.exists(img_path):
                pixmap = QtGui.QPixmap(img_path)
                label = QLabel()
                # Fix the label size so that the image is scaled to fill the cell.
                label.setFixedSize(80, 80)
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                self.table.setCellWidget(row, 0, label)
                channel_has_image[chan] = True
            else:
                item = QTableWidgetItem(chan)
                self.table.setItem(row, 0, item)
                channel_has_image[chan] = False
        
        # === Occupancy grid to avoid overlapping spans ===
        occupancy = [[False for _ in range(total_columns)] for _ in range(num_rows)]
        
        # === Place programme items in the grid ===
        for prog in self.all_programmes:
            chan = prog["channel"]
            if chan not in self.filtered_channels:
                continue
            prog_start = parse_xmltv_time(prog["start"])
            prog_stop = parse_xmltv_time(prog["stop"])
            if not prog_start or not prog_stop:
                continue
            if prog_stop < grid_start or prog_start > grid_end:
                continue
            effective_start = max(prog_start, grid_start)
            effective_stop = min(prog_stop, grid_end)
            delta_start = effective_start - grid_start
            col_start = int(delta_start.total_seconds() // (30 * 60)) + 1  # +1 for channel info column.
            delta_duration = effective_stop - effective_start
            col_span = max(1, int(delta_duration.total_seconds() // (30 * 60)))
            try:
                row = self.filtered_channels.index(chan)
            except ValueError:
                continue
            
            # Check occupancy to prevent overlapping spans.
            if any(occupancy[row][c] for c in range(col_start, min(col_start + col_span, total_columns))):
                continue
            
            for c in range(col_start, min(col_start + col_span, total_columns)):
                occupancy[row][c] = True
            
            text = f"{prog['title']}\n({effective_start.strftime('%H:%M')}-{effective_stop.strftime('%H:%M')})"
            item = QTableWidgetItem(text)
            if effective_start <= datetime.datetime.now() <= effective_stop:
                item.setBackground(QtGui.QColor("#ffcccb"))
            else:
                item.setBackground(QtGui.QColor("#cce5ff"))
            item.setToolTip(f"Channel: {chan}\nTitle: {prog['title']}\nStart: {prog_start}\nStop: {prog_stop}")
            self.table.setItem(row, col_start, item)
            if col_span > 1:
                try:
                    self.table.setSpan(row, col_start, 1, col_span)
                except Exception as e:
                    print("Error setting span:", e)
        
        # === Set row heights: larger if channel image exists, else default height.
        for row, chan in enumerate(self.filtered_channels):
            if channel_has_image.get(chan, False):
                self.table.setRowHeight(row, 80)
            else:
                self.table.setRowHeight(row, 50)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPTVking - EPG Prototype")
        self.resize(1200, 700)
        self.epg_widget = EPGWindow()
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(self.epg_widget)
        self.setCentralWidget(central)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
