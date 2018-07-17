#!/usr/bin/python
#
# Copyright (C) 2018 Kristian Sloth Lauszus. All rights reserved.
#
# Contact information
# -------------------
# Kristian Sloth Lauszus
# Web      :  http://www.lauszus.com
# e-mail   :  lauszus@gmail.com

from . import *

ID_CLOSE_OPEN = 0x101  # uint8_t, 0 = stop, 1 = close, 2 = open

ID_SCREEN_ON_OFF = 0x102  # uint8_t, 0 = off, 1 = on

ID_BOARD_ERROR_CODE = 0x103  # uint8_t: 0 = flight controller, 1 = retraction, uint16_t: error code

# GPS
ID_TIME_SPEED_COURSE = 0x104  # uint32_t, uint16_t, uint16_t - scaling = 1, 100., 100.

# GPS position
ID_GPS_POS = 0x105  # float, float - scaling = 1., 1.

# IMUs
ID_IMU0_ACCX_ACCY = 0x106  # float, float - scaling = 1., 1.
ID_IMU0_ACCZ_GYROX = 0x107  # float, float - scaling = 1., 1.
ID_IMU0_GYROY_GYROZ = 0x108  # float, float - scaling = 1., 1.

ID_IMU1_ACCX_ACCY = 0x109  # float, float - scaling = 1., 1.
ID_IMU1_ACCZ_GYROX = 0x10A  # float, float - scaling = 1., 1.
ID_IMU1_GYROY_GYROZ = 0x10B  # float, float - scaling = 1., 1.

# Gyroscope low-pass filtered values
ID_IMU0_GYROX_GYROY_LPF = 0x10C  # float, float - scaling = 1., 1.
ID_IMU01_GYROZ_GYROX_LPF = 0x10D  # float, float - scaling = 1., 1.
ID_IMU1_GYROY_GYROZ_LPF = 0x10E  # float, float - scaling = 1., 1.

# IMU temperature sensors
ID_IMU_TEMPERATURES = 0x10F  # float, float - scaling = 1., 1.

# Attitude
ID_ROLL_PITCH = 0x110  # float, float - scaling = 1., 1.
ID_ROLL_PITCH_REF = 0x111  # float, float - scaling = 1., 1.

# Kalman height acceleration estimate and fictitious acceleration
ID_KAL_ACC_FICACC = 0x112  # float, float - scaling = 1., 1.

# Roll controller
ID_ROLL_PID = 0x113  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.

# Altitude
ID_ULTRA_REF_HEIGHT = 0x114  # float, float - scaling = 1., 1.
ID_KAL_HEIGHT_VEL = 0x115  # float, float - scaling = 1., 1.
ID_HEIGHT_PID = 0x116  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.

# Foil
ID_PORT_STARBOARD_FOIL = 0x117  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.
ID_AFT_FOIL = 0x118  # int16_t, int16_t - scaling = 100., 100.

# Pump
ID_HYDRAULIC_PUMP = 0x119  # float, float - scaling = 1., 1.

# Hydraulic actuators
ID_PORT_ACT_PID = 0x11A  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.
ID_STARBOARD_ACT_PID = 0x11B  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.

# Pitch
ID_PITCH_PID = 0x11C  # int16_t, int16_t, int16_t, int16_t - scaling = 100., 100., 100., 100.

ID_CALIBRATE_IMU = 0x11D
ID_CHARGING_CURRENT = 0x11E  # uint16_t - scaling = 10.

ID_KAL_ATTITUDE = 0x11F  # float, float - scaling = 1., 1.
ID_ROLL_ULTRA_DRIFT = 0x120  # float, float - scaling = 1., 1.
ID_ACC_ATTITUDE_DRIFT = 0x121  # float, float - scaling = 1., 1.

# BMS messages
ID_BMS_CELL_VOLTAGE_STATS_1 = 0x140  # uint16_t, uint16_t, uint16_t, uint16_t - scaling = 1.0e4, 1.0e4, 1.0e4, 1
ID_BMS_CELL_VOLTAGE_STATS_2 = 0x141  # uint8_t, uint8_t, uint8_t, uint8_t, uint16_t - scaling = 1, 1, 1, 1, 10.
ID_BMS_CELL_TEMPERATURE_STATS = 0x142  # int8_t, uint8_t, uint8_t, int8_t, uint8_t, uint8_t, uint16_t - scaling = 1, 1, 1, 1, 1, 1, 1
ID_BMS_PACK_IQ = 0x143  # int32_t, int16_t, uint16_t - scaling = 1.0e5, 100., 10.
ID_BMS_CHARGER_STATUS = 0x144  # uint8_t, uint16_t, uint16_t, uint8_t, uint8_t, uint8_t - scaling = 1, 10., 10., 1, 1, 1
ID_BMS_CHARGER_TX_FRAME = 0x145  # uint16_t, uint16_t, uint8_t - scaling = 10., 10., 1

# Command for moving the actuators
ID_SET_AFT_MODE = 0x150  # uint8_t, 0 = stop, 1 = foiling, 2 = shallow, 3 = trailing
ID_MOVE_AFT_ACT = 0x151  # byte0: 0 = aft pitch actuator, 1 = aft frame actuator, byte1: 0 = stop, -1 = down, 1 = up
ID_SET_RETRACTION = 0x152  # 0 = stop, 1 = retract left, 2 = extend left, 3 = retract right, 4 = extend right
ID_SET_LOCK_PIN = 0x153  # 0 = stop, 1 = unlock, 2 = lock
ID_LOCK_PIN_POS = 0x154  # uint8_t: 0 = left lock pin, 1 = right lock pin, uint16_t: position - scaling = 1, 10.

# Set PID values
# The messages are split up into two messages, as the maximum length of a CAN-Bus message is 8 bytes
# Kp, Ki, Kd, integrationLimit, Fc
# uint32_t, uint32_t, uint32_t, uint16_t, uint16_t
# 1.0e5, 1.0e5, 1.0e5, 100., 10.
ID_SET_PID_ROLL_1 = 0x160
ID_SET_PID_ROLL_2 = 0x161
ID_SET_PID_PITCH_1 = 0x162
ID_SET_PID_PITCH_2 = 0x163
ID_SET_PID_HEIGHT_1 = 0x164
ID_SET_PID_HEIGHT_2 = 0x165
ID_SET_PID_FWD_ACT_1 = 0x166
ID_SET_PID_FWD_ACT_2 = 0x167
# ID_SET_PID_AFT_ACT_1 = 0x168
# ID_SET_PID_AFT_ACT_2 = 0x169

# Get PID values
# Contains no data
ID_GET_PID_ROLL = 0x170
ID_GET_PID_PITCH = 0x171
ID_GET_PID_HEIGHT = 0x172
ID_GET_PID_FWD_ACT = 0x173
# ID_GET_PID_AFT_ACT = 0x174

# PowerTrack
POWERTRACK_NODE_ID = 0x15
ID_POWERTRACK_INFO_0 = CANOPEN_TPDO1 + POWERTRACK_NODE_ID  # uint8_t keys, uint8_t encoder_direction_counter, int16_t encoder_tick_counter, uint32_t reserved1

# Inverter values
INVERTER_NODE_ID = 1
ID_INVERTER_INFO_0 = CANOPEN_TPDO1 + INVERTER_NODE_ID  # int32_t speed, int16_t torque, int16_t current - scaling = 1, 16., 1
ID_INVERTER_INFO_1 = CANOPEN_TPDO2 + INVERTER_NODE_ID  # int16_t coolant_temperature, int16_t rotor_temperature, int8_t heatsink_temperature, uint16_t temperature_torque_scaling - scaling = 1, 1, 1, 256. / 100.
# ID_INVERTER_INFO_2 = CANOPEN_TPDO3 + INVERTER_NODE_ID  # uint16_t status_word, uint16_t highest_priority_fault, uint16_t dc_bus_capacitor_voltage, int16_t voltage_modulation - scaling = 1, 1, 16., 255. / 100.

# VESC status packets - OBS: they are big-endian
VESC_CAN_ID = 123
ID_VESC_CAN_PACKET_STATUS = (9 << 8) | VESC_CAN_ID  # int32_t, int16_t, int16_t - scaling = 4, 10, 10
ID_VESC_CAN_PACKET_STATUS_2 = (14 << 8) | VESC_CAN_ID  # int16_t, int16_t, int16_t, int16_t - scaling = 100, 10, 100, 100

data_structs = {
    ID_TIME_SPEED_COURSE: (struct.Struct('<LHH'), 1, 100., 100. * math.pi / 180.),
    (ID_GPS_POS, ID_IMU0_ACCX_ACCY, ID_IMU1_ACCX_ACCY, ID_ULTRA_REF_HEIGHT, ID_KAL_HEIGHT_VEL, ID_HYDRAULIC_PUMP,
     ID_IMU_TEMPERATURES, ID_KAL_ACC_FICACC): struct.Struct('<ff'),
    (ID_IMU0_ACCZ_GYROX, ID_IMU1_ACCZ_GYROX): (struct.Struct('<ff'), 1., math.pi / 180.),
    # Convert the gyro rate into deg/s
    (ID_IMU0_GYROY_GYROZ, ID_IMU1_GYROY_GYROZ, ID_IMU0_GYROX_GYROY_LPF, ID_IMU01_GYROZ_GYROX_LPF,
     ID_IMU1_GYROY_GYROZ_LPF): (struct.Struct('<ff'), math.pi / 180., math.pi / 180.),
    # Convert the gyro rates into deg/s
    (ID_ROLL_PITCH, ID_ROLL_PITCH_REF, ID_KAL_ATTITUDE, ID_ROLL_ULTRA_DRIFT, ID_ACC_ATTITUDE_DRIFT):
        (struct.Struct('<ff'), math.pi / 180., math.pi / 180.),  # Convert the attitude into degrees
    (ID_ROLL_PID, ID_PITCH_PID, ID_HEIGHT_PID, ID_PORT_ACT_PID, ID_STARBOARD_ACT_PID):
        (struct.Struct('<hhhh'), 100., 100., 100., 100.),
    ID_PORT_STARBOARD_FOIL: (struct.Struct('<hhhh'), 100., 100., 100., 100.),
    ID_AFT_FOIL: (struct.Struct('<hh'), 100., 100.),
    ID_VESC_CAN_PACKET_STATUS: (struct.Struct('>lhh'), 4., 10., 10.),
    ID_VESC_CAN_PACKET_STATUS_2: (struct.Struct('>hhhh'), 100., 10., 100., 100.),
    ID_INVERTER_INFO_0: (struct.Struct('<lhh'), 1, 16., 1),
    ID_INVERTER_INFO_1: (struct.Struct('<hhbH'), 1, 1, 1, 256. / 100.),
    # ID_INVERTER_INFO_2: (struct.Struct('<HHHh'), 1, 1, 16., 255. / 100.),

    # BMS messages
    ID_BMS_CELL_VOLTAGE_STATS_1: (struct.Struct('<HHHH'), 1.0e4, 1.0e4, 1.0e4, 1),
    ID_BMS_CELL_VOLTAGE_STATS_2: (struct.Struct('<BBBBH'), 1, 1, 1, 1, 10.),
    ID_BMS_CELL_TEMPERATURE_STATS: (struct.Struct('<bBBbBBH'), 1, 1, 1, 1, 1, 1, 1),
    ID_BMS_PACK_IQ: (struct.Struct('<lhH'), 1.0e5, 100., 10.),
    ID_BMS_CHARGER_STATUS: (struct.Struct('<BHHBBB'), 1, 10., 10., 1, 1, 1),
    ID_BMS_CHARGER_TX_FRAME: (struct.Struct('<HHB'), 10., 10., 1),

    # These are only used for communication with the flight controller and are not logged
    (ID_CLOSE_OPEN, ID_SCREEN_ON_OFF, ID_SET_AFT_MODE, ID_SET_RETRACTION, ID_SET_LOCK_PIN): struct.Struct('<B'),
    ID_LOCK_PIN_POS: (struct.Struct('<BH'), 1, 10.),
    ID_CHARGING_CURRENT: (struct.Struct('<H'), 10.),
    ID_BOARD_ERROR_CODE: struct.Struct('<BH'),
    ID_MOVE_AFT_ACT: struct.Struct('<Bb'),
    ID_POWERTRACK_INFO_0: struct.Struct('<BBhL'),
    (ID_SET_PID_ROLL_1, ID_SET_PID_PITCH_1, ID_SET_PID_HEIGHT_1, ID_SET_PID_FWD_ACT_1): (struct.Struct('<LL'),
                                                                                         1.0e5, 1.0e5),
    (ID_SET_PID_ROLL_2, ID_SET_PID_PITCH_2, ID_SET_PID_HEIGHT_2, ID_SET_PID_FWD_ACT_2): (struct.Struct('<LHH'),
                                                                                         1.0e5, 100., 10.),
    (ID_GET_PID_ROLL, ID_GET_PID_PITCH, ID_GET_PID_HEIGHT, ID_GET_PID_FWD_ACT): None,
    ID_CALIBRATE_IMU: None,
}  # type: Dict[Union[bytes, Tuple[bytes, ...]], Union[struct.Struct, Tuple, None]]


if __name__ == '__main__':  # pragma: no cover
    # Catch ctrl+c
    try:
        ids = {}
        for key in data_structs.keys():
            value = data_structs[key]
            if not value:  # Check if None
                continue
            elif isinstance(value, tuple):
                # The scaling is given as an argument
                fmt = value[0].format.decode('UTF-8') + ':' + ':'.join(str(x) for x in value[1:])
            else:
                # No conversion is needed
                fmt = value.format.decode('UTF-8')

            # Store the format for each ID
            if isinstance(key, tuple):
                for k in key:
                    ids[k] = fmt
            else:
                ids[key] = fmt

        # Print all the IDs, their format and conversion string
        for key in sorted(ids.keys()):
            print('{:X}:{}'.format(key, ids[key]))

    except KeyboardInterrupt:
        pass
