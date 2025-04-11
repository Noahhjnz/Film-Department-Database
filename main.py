#!/usr/bin/env python3
from nicegui import ui
import pandas as pd
import re

CSV_FILE = 'camera_data.csv'

def is_valid_date(date):
    return re.match(r'^\d{2}-\d{2}-\d{4}$', date) is not None  # true or false

class Reservation:
    
    
    
    def __init__(self,event):
        self.camera_data = self.load_camera_data()
        self.selected_camera = None
        self.dialog = None
        self.start_date_input = None
        self.end_date_input = None

        self.grid = ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Reserved', 'field': 'reserved'},
            ],
            'rowData': self.camera_data,
            'rowSelection': 'single',
        }).classes('max-h-40')

        self.grid.on('rowSelected', self.on_selection)
        ui.button('Reserve', on_click=lambda: self.show_reservation_dialog(event))

    def load_camera_data(self):
        try:
            df = pd.read_csv(CSV_FILE)
            print(df.to_dict(orient='records'))
            return df.to_dict(orient='records')
        except FileNotFoundError:
            ui.notify(f'Error: {CSV_FILE} not found.', type='error')
            return []

    def on_selection(self, event):
        print(event.args['data']['name'])
        self.selected_camera = event.args['data']['name']
        print("Selected:", self.selected_camera)

    def show_reservation_dialog(self, event):
        if not self.selected_camera:
            ui.notify('Please select a camera first', type='warning')
            return

        self.dialog = ui.dialog()
        with self.dialog, ui.card():
            ui.label(f'Reserving {self.selected_camera}')
            self.start_date_input = ui.input('Start Date (DD-MM-YYYY)')
            self.end_date_input = ui.input('End Date (DD-MM-YYYY)')

            ui.button('Confirm', on_click=lambda:self.confirm_reservation(event))
            ui.button('Cancel', on_click=self.dialog.close)

        self.dialog.open()

    def confirm_reservation(self, event):
        start_date = self.start_date_input.value
        end_date = self.end_date_input.value

        if not is_valid_date(start_date) or not is_valid_date(end_date):
            ui.notify('Invalid date format. Please use DD-MM-YYYY.', type='warning')
            return

        self.reserve_camera( event, start_date, end_date)
        self.dialog.close()

    def reserve_camera(self, event, start_date, end_date):
        print(f"reserve {self.selected_camera}")
        print(f"reserve {event.args['data']['name']}")
        if self.selected_camera == event.args['data']['name']:
            for index, camera in enumerate(self.camera_data):
                if camera['name'] == self.selected_camera:
                    camera['reserved'] = f'Reserved from {start_date} to {end_date}'
                    self.camera_data[index] = camera  # Update the data in the list
                    break

            # Update the entire grid
            self.grid.options['data'] self.camera_data
            self.grid.update()
        else:
            ui.notify('No camera selected.', type='warning')

app = Reservation()
ui.run()