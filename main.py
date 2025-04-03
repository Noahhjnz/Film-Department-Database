#!/usr/bin/env python3
# Complex Technique - Third Party / Non Core Libary
from nicegui import ui
import pandas as pd
import re

# Complex Technique - Reading From Seperate File
CSV_FILE = 'camera_data.csv'  # Path to CSV file

def is_valid_date(date):
    """Validate date format DD-MM-YYYY using regex."""
    return re.match(r'^\d{2}-\d{2}-\d{4}$', date) is not None

# Complex Technique - Object Oriented Programming Using Classes    
# Complex Technique - Programming For A GUI  
class Reservation:
    def __init__(self):
        self.camera_data = self.load_camera_data()
        self.selected_camera = None

        # Create the grid with row selection enabled
        self.grid = ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Reserved', 'field': 'reserved'},
            ],
            'rowData': self.camera_data,
            'rowSelection': 'single',  # Allow single row selection
        }).classes('max-h-40')

        self.grid.on('rowSelected', self.on_selection)  # Listen for row selection
        # Reserve button
        ui.button('Reserve', on_click=self.show_reservation_dialog)
        
    def load_camera_data(self):
        """Load camera data from CSV file."""
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict(orient='records')
        except FileNotFoundError:
            ui.notify(f'Error: {CSV_FILE} not found.', type='error')
            return []

    def on_selection(self, event):
        self.selected_camera = event.args['data']['name']
        self.grid.update()  # Refresh the table
        print("on selection", self.selected_camera)

  

    def show_reservation_dialog(self):
        """Show dialogue for user selection"""
        print("show", self.selected_camera)
        if not self.selected_camera:
            ui.notify('Please select a camera first', type='warning')
            return
        
        with ui.dialog() as dialog, ui.card():
            ui.label(f'Reserving {self.selected_camera}')
            start_date = ui.input('Start Date (DD-MM-YY)')
            end_date = ui.input('End Date (DD-MM-YYYY)')
        

            def confirm():
                if not is_valid_date(start_date.value) or not is_valid_date(end_date.value):
                    ui.notify('Invalid date Format Please use DD-MM-YYYY.', type='warning')
                    return

                self.reserve_camera(start_date.value, end_date.value)
                dialog.close()

            ui.button('Confirm', on_click=confirm)
            ui.button('Cancel', on_click=dialog.close)

        dialog.open()

    def reserve_camera(self, start_date, end_date):
        """Update the selected camera's reservation status."""
        print("reserve", self.selected_camera)
        if self.selected_camera and start_date and end_date:
            for camera in self.camera_data:
                print("camera name", camera['name'])
                if camera['name'] == self.selected_camera:
                    camera['reserved'] = f'Reserved from {start_date} to {end_date}'
                    break
                self.grid.update()
            self.save_camera_data()  # Refresh the table
        else:
            ui.notify('Please enter valid dates.', type='warning')


# Create an instance of the Reservation
app = Reservation()

ui.run()