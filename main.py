#!/usr/bin/env python3
from nicegui import ui

# Initial camera data
camera_data = [
    {'name': 'Camera 1', 'reserved': 'Available'},
    {'name': 'Camera 2', 'reserved': 'Available'},
    {'name': 'Camera 3', 'reserved': 'Available'},
]

selected_camera = None  # Store the selected camera


def on_selection(event):
    """Store the selected camera when a row is clicked."""
    global selected_camera
    selected_camera = event.args['data']['name']  # Get selected camera name

def show_reservation_dialog():
    """show dialouge for user selection"""
with ui.dialog() as dialog, ui.card():
    ui.label(f'Reserving {selected_camera}')
    start_date = ui.input('Start Date (DD-MM-YY)')
    end_date = ui.input('End Date (DD-MM-YYYY)')

    def confirm():
        reserve_camera(start_date.value, end_date.value,)
        dialog.close()
        
        ui.button('Confirm', on_click=confirm)
        ui.button('Cancel', on_click=dialog.close)
        
    dialog.open()


    
def reserve_camera():
    """Update the selected camera's reservation status."""
    global selected_camera
    if selected_camera and start_date and end_date:
        for camera in camera_data:
            if camera['name'] == selected_camera:
                camera['reserved'] = f'Reserved from {start_date} to {end_date}'
                break
        grid.update()  # Refresh the table
    else: 
        ui.notify('Please enter valid dates', type='warning')
    


# Create the grid with row selection enabled
grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name'},
        {'headerName': 'Reserved', 'field': 'reserved'},
    ],
    'rowData': camera_data,
    'rowSelection': 'single',  # Allow single row selection
}).classes('max-h-40')

grid.on('rowSelected', on_selection)  # Listen for row selection

# Reserve button
ui.button('Reserve', on_click=show_reservation_dialog)

ui.run()
