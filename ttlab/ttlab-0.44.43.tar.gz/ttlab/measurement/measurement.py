from .. import MassSpectrometer, FlowReactor, XPS, X0Reactor, OpticalSpectroscopy


def get_measurement_from_history_event(history_event, dbConnection):
    measurement = None

    if history_event['description'] == 'xps':
        measurement = _import_xps_from_history_event(history_event, dbConnection)
        measurement.history_event = history_event
    return measurement


def _import_X0_from_history_event(history_event,dbConnection):
    if history_event['file_id_fr'] is not None:
        grid_fr = dbConnection.get_gridfs_file(id=history['file_id_fr'])
    if history_event['file_id_ms'] is not None:
        grid_ms = dbConnection.get_gridfs_file(id=history_event['file_id_ms'])
    if history_event['file_id_ils'] is not None:
        grid_ils = dbConnection.get_gridfs_file(id=history_event['file_id_ils'])
    if history_event['file_id_lamp'] is not None:
        grid_lamp = dbConnection.get_gridfs_file(id=history_event['file_id_lamp'])
    return None


def _import_xps_from_history_event(history_event,dbConnection):
    grid_fs = dbConnection.get_gridfs_file(id = history_event['file_id'])
    if history_event['extra'] == 'survey':
        return XPS(gridfs_survey=grid_fs)
    return XPS(gridfs_multi=grid_fs)








