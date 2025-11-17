#!/usr/bin/env python3
import sys, os, urllib.request, xml.etree.ElementTree as ET, re
import datetime

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QMessageBox
)

# Global EPG URL
EPG_URL = "http://1ere-serrvices.com:80/xmltv.php?username=363ys5p123e&password=perv0j5t8x&type=m3u_plus&output=mpegts"

def fetch_epg_data():
    """Fetch and parse the XMLTV data from EPG_URL.
    Returns a list of programme dicts with keys: channel, title, start, stop."""
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
            programmes.append({
                "channel": channel,
                "title": title,
                "start": start,
                "stop": stop
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

class EPGWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IPTVking - EPG")
        self.resize(1200, 600)
        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)
        
        # Summary label: total live channels (unique channels in EPG data)
        self.summary_label = QLabel("Loading EPG...")
        self.layout.addWidget(self.summary_label)
        
        # Button to refresh
        refresh_button = QPushButton("Refresh EPG")
        refresh_button.clicked.connect(self.refresh_epg)
        self.layout.addWidget(refresh_button)
        
        # EPG grid table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        
        # Load the EPG on startup
        self.refresh_epg()
    
    def refresh_epg(self):
        self.programmes = fetch_epg_data()
        if not self.programmes:
            QMessageBox.warning(self, "EPG Error", "Failed to fetch EPG data.")
            return
        # Build channel list (unique channels)
        channels = sorted({prog["channel"] for prog in self.programmes})
        self.channels = channels
        self.summary_label.setText(f"Live Channels: {len(channels)}")
        
        # Define grid time range: from current time (rounded down) to +6 hours
        now = datetime.datetime.now()
        grid_start = now.replace(minute=0, second=0, microsecond=0)
        # round down to nearest half hour
        if now.minute < 30:
            grid_start = grid_start.replace(minute=0)
        else:
            grid_start = grid_start.replace(minute=30)
        grid_end = grid_start + datetime.timedelta(hours=6)
        
        # Create time slots: each 30 minutes
        time_slots = []
        t = grid_start
        while t < grid_end:
            time_slots.append(t)
            t += datetime.timedelta(minutes=30)
        num_slots = len(time_slots)
        
        # Setup table: rows = channels, columns = time slots
        self.table.clear()
        self.table.setRowCount(len(channels))
        self.table.setColumnCount(num_slots)
        # Set horizontal headers to time labels
        header_labels = [t.strftime("%H:%M") for t in time_slots]
        self.table.setHorizontalHeaderLabels(header_labels)
        # Set vertical headers to channel names (or logos if available)
        self.table.setVerticalHeaderLabels(channels)
        
        # Adjust header sizes
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # For each programme, if it overlaps with grid time, place it in the correct row and column span.
        # Build a mapping: channel -> row index
        channel_to_row = {chan: idx for idx, chan in enumerate(channels)}
        
        # Clear all existing spans.
        for r in range(len(channels)):
            for c in range(num_slots):
                self.table.setItem(r, c, QTableWidgetItem(""))
        
        for prog in self.programmes:
            prog_start = parse_xmltv_time(prog["start"])
            prog_stop = parse_xmltv_time(prog["stop"])
            if not prog_start or not prog_stop:
                continue
            # Check if programme overlaps with grid range
            if prog_stop < grid_start or prog_start > grid_end:
                continue
            # Compute effective start and stop in grid
            effective_start = max(prog_start, grid_start)
            effective_stop = min(prog_stop, grid_end)
            # Compute column index and span (each column = 30 minutes)
            delta_start = effective_start - grid_start
            col_start = int(delta_start.total_seconds() // (30 * 60))
            delta_duration = effective_stop - effective_start
            col_span = max(1, int(delta_duration.total_seconds() // (30 * 60)))
            
            # Find row index from channel
            chan = prog["channel"]
            row = channel_to_row.get(chan)
            if row is None:
                continue
            
            # Create a table item with programme title and times
            text = f"{prog['title']}\n({effective_start.strftime('%H:%M')}-{effective_stop.strftime('%H:%M')})"
            item = QTableWidgetItem(text)
            # Highlight if current time is within programme
            if effective_start <= datetime.datetime.now() <= effective_stop:
                item.setBackground(QtGui.QColor("#ffcccb"))
            else:
                item.setBackground(QtGui.QColor("#cce5ff"))
            # Optionally, set tooltip with full details (channel, title, start, stop and record status), e.g.:'Channel: BBC One\nTitle: News at Six\nStart: 2021-09-01 18:00:00\nStop: 2021-09-01 18:30:00\nRecord: Yes'
            item.setToolTip(f"Channel: {chan}\nTitle: {prog['title']}\nStart: {prog_start}\nStop: {prog_stop}\nRecord:")# {prog.get('record', 'No')}")
            
            # Place the item in the table, spanning columns
            self.table.setItem(row, col_start, item)
            self.table.setSpan(row, col_start, 1, col_span)
        
        # Optional: Auto-resize row heights for best display.
        self.table.resizeRowsToContents()

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
