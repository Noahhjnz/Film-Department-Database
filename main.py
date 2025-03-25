#!/usr/bin/env python3
from nicegui import ui

class CameraReservationApp:
    def __init__(self):
        # Initial camera data
        self.camera_data = [
            {'name': 'Camera 1', 'reserved': 'Available'},
            {'name': 'Camera 2', 'reserved': 'Available'},
            {'name': 'Camera 3', 'reserved': 'Available'},
        ]
        self.selected_camera = None  # Store the selected camera

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

    def on_selection(self, event):
        """Store the selected camera when a row is clicked."""
        self.selected_camera = event.args['data']['name']  # Get selected camera name
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
            self.grid.update()  # Refresh the table
        else:
            ui.notify('Please enter valid dates.', type='warning')

# Create an instance of the CameraReservationApp
app = CameraReservationApp()

ui.run()