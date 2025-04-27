#!/usr/bin/env python3
# Complex Technique - Third Party / Non Core Libary
from datetime import datetime, timedelta
from nicegui import ui
import pandas as pd
import re
from datetime import date, datetime, timedelta

# Complex Technique - Reading From Seperate File
CSV_FILE = 'device_data.csv'  # Path to CSV file


def is_valid_date(date):
    """Validate date format DD-MM-YYYY using regex."""
    return re.match(r'^\d{2}-\d{2}-\d{4}$', date) is not None




# Complex Technique - Object Oriented Programming Using Classes
# Complex Technique - Programming For A GUI


class Reservation:
    def __init__(self):
        self.device_data = self.load_device_data()
        self.add_category_divider()
        self.selected_device = None

        self.grid = ui.aggrid({
            'defaultColDef': {
                'flex': 1,
                'tooltipShowDelay': 0,  # Instant show
                'tooltipHideDelay': 200,  # Optional: small delay to hide
            },
            'columnDefs': [
                {'headerName': 'Name', 'field': 'name', 'tooltipField': 'tooltip'},
                {'headerName': 'Reserved', 'field': 'reserved', 'tooltipField': 'tooltip'},
                {'field': 'is_divider', 'hide': True}
            ],
            'rowData': self.device_data,
            'rowSelection': 'single',
    }).classes('max-h-60')

        self.grid.on('rowSelected', self.on_selection)
        ui.button('Reserve', on_click=self.show_reservation_dialog)

    def load_device_data(self):
        """Load all device data from the CSV file."""
        try:
            df = pd.read_csv(CSV_FILE)
            records = df.to_dict(orient='records')
            for record in records:
                record['is_divider'] = False
                # Check if it's a camera (has resolution data)
                if pd.notna(record['resolution']):
                    record['tooltip'] = (
                        f"Resolution: {record['resolution']}\n"
                        f"Megapixels: {record['megapixels']}\n"
                        f"Lens Options: {record['lens_options']}"
                    )
                else:
                    # For non-camera devices, just show basic info
                    record['tooltip'] = f"Device: {record['name']}\nStatus: {record['reserved'] or 'Available'}"
            return records
        except FileNotFoundError:
            ui.notify(f'Error: {CSV_FILE} not found.', type='error')
        return []
    def add_category_divider(self):
        """Add divider rows between cameras, microphones, and headphones."""
        # Find the first microphone
        mic_index = next((i for i, item in enumerate(self.device_data)
                        if 'microphone' in item['name'].lower()), len(self.device_data))
        
        # Find the first headphone (after microphones)
        headphone_index = next((i for i, item in enumerate(self.device_data)
                            if 'headphone' in item['name'].lower()), len(self.device_data))
        
        # Insert microphone divider if microphones exist
        if mic_index < len(self.device_data):
            self.device_data.insert(mic_index, {
                'name': 'MICROPHONES',
                'reserved': '',
                'is_divider': True
            })
            
            # Adjust headphone index if we inserted a microphone divider
            if headphone_index > mic_index:
                headphone_index += 1
        
        # Insert headphone divider if headphones exist
        if headphone_index < len(self.device_data):
            self.device_data.insert(headphone_index, {
                'name': 'HEADPHONES',
                'reserved': '',
                'is_divider': True
            })
            
            
    def on_selection(self, event):
        row = event.args['data']
        if row.get('is_divider'):
            self.selected_device = None
            return  # prevents user from selecting divider
        self.selected_device = row
        print("Selected device:", self.selected_device)



    def show_reservation_dialog(self):
        if not self.selected_device:
            ui.notify('Please select a device first', type='warning')
            return

        with ui.dialog() as dialog, ui.card():
            ui.label(f"Reserving {self.selected_device['name']}")

            start_date = ui.input('Start Date (DD-MM-YYYY)', value=date.today().strftime('%d-%m-%Y'))
            duration = ui.input('Number of days to reserve (1-7)')

            def confirm():
                if not is_valid_date(start_date.value):
                    ui.notify('Invalid date format. Use DD-MM-YYYY.', type='warning')
                    return

                try:
                    days = int(duration.value)
                    if days < 1 or days > 7:
                        ui.notify('Reservation duration must be between 1 and 7 days.', type='warning')
                        return

                    start = datetime.strptime(start_date.value, '%d-%m-%Y')
                    end = start + timedelta(days=days)
                    end_date = end.strftime('%d-%m-%Y')
                    self.reserve_device(start_date.value, end_date)
                    dialog.close()
                except ValueError:
                    ui.notify('Please enter a whole number for the duration.', type='warning')

            with ui.row().classes('justify-end'):
                ui.button('Confirm', on_click=confirm)
                ui.button('Cancel', on_click=dialog.close)

        dialog.open()


    def reserve_device(self, start_date, end_date):
        """Reserve the selected device."""
        if self.selected_device and start_date and end_date:
            for device in self.device_data:
                if device['name'] == self.selected_device['name']:
                    device['reserved'] = f'Reserved from {start_date} to {end_date}'
                    break
            self.grid.options['rowData'] = self.device_data
            self.grid.update()
        else:
            ui.notify('Please enter valid dates.', type='warning')


# Start the app
app = Reservation()
ui.run()