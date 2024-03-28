class TFmini:
    DEFAULT_BAUDRATE = 115200

    class OutputDataFormat:
        Standard = 0x01
        Pixhawk = 0x04

    class OutputDataUnit:
        MM = 0x00
        CM = 0x01

    class DetectionPattern:
        Auto = 0x00
        Fixed = 0x01

    class DistanceMode:
        Short = 0x02
        Long = 0x07

    class TriggerSource:
        Internal = 0x01
        External = 0x00

    class Baudrate:
        BAUD_9600 = 0
        BAUD_14400 = 1
        BAUD_19200 = 2
        BAUD_38400 = 3
        BAUD_56000 = 4
        BAUD_57600 = 5
        BAUD_115200 = 6
        BAUD_128000 = 7
        BAUD_230400 = 8
        BAUD_256000 = 9
        BAUD_460800 = 10
        BAUD_500000 = 11
        BAUD_512000 = 12

    def attach(self, s):
        self.stream = s

    def available(self):
        if not self.stream:
            return False

        self.update()
        if self.b_available:
            self.b_available = False
            return True
        else:
            return False

    def getDistance(self):
        return self.packet['distance']

    def getStrength(self):
        return self.packet['strength']

    def getIntegrationTime(self):
        return self.packet['int_time']

    def setOutputDataFormat(self, fmt):
        self.format = fmt
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, fmt, 0x06]))
        self.configEnd()

    def setOutputDataPeriod(self, ms):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([(ms >> 8) & 0x00FF, (ms >> 0) & 0x00FF, 0x00, 0x07]))
        self.configEnd()

    def setOutputDataUnit(self, unit):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, unit, 0x1A]))
        self.configEnd()

    def setDetectionPattern(self, pttr):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, pttr, 0x14]))
        self.configEnd()

    def setDistanceMode(self, mode):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, mode, 0x11]))
        self.configEnd()

    def setRangeLimit(self, mm):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([(mm >> 8) & 0x00FF, (mm >> 0) & 0x00FF, 0x01, 0x19]))
        self.configEnd()

    def disableRangeLimit(self):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, 0x00, 0x19]))
        self.configEnd()

    def setSignalStrengthThreshold(self, low, high, cm):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([low, 0x00, 0x00, 0x20]))
        self.sendHeader()
        self.stream.write(bytes([(high >> 8) & 0x00FF, (high >> 0) & 0x00FF, cm, 0x21]))
        self.configEnd()

    def setBaudRate(self, baud):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, baud, 0x08]))
        self.configEnd()

    def setTriggerSource(self, trigger):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, trigger, 0x40]))
        self.configEnd()

    def resetSettings(self):
        self.configBegin()
        self.sendHeader()
        self.stream.write(bytes([0xFF, 0xFF, 0xFF, 0xFF]))
        self.configEnd()

    def sendHeader(self):
        self.stream.write(bytes([0x42, 0x57, 0x02, 0x00]))

    def configBegin(self):
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, 0x01, 0x02]))

    def configEnd(self):
        self.sendHeader()
        self.stream.write(bytes([0x00, 0x00, 0x00, 0x02]))

    def update(self):
        while self.stream.available():
            data = self.stream.read(1)

            if self.format == self.OutputDataFormat.Pixhawk:
                print("Pixhawk Format NOT SUPPORTED YET")
                return

            if self.state != self.State.CHECKSUM:
                self.buffer['sum'] += data

            state = self.state
            if state == self.State.HEAD_L:
                self.reset()
                self.buffer['sum'] = data
                if data == self.RECV_FRAME_HEADER:
                    self.state = self.State.HEAD_H
            elif state == self.State.HEAD_H:
                if data == self.RECV_FRAME_HEADER:
                    self.state = self.State.DIST_L
                else:
                    self.state = self.State.HEAD_L
            elif state == self.State.DIST_L:
                self.buffer['distance'][0] = data
                self.state = self.State.DIST_H
            elif state == self.State.DIST_H:
                self.buffer['distance'][1] = data
                self.state = self.State.STRENGTH_L
            elif state == self.State.STRENGTH_L:
                self.buffer['strength'][0] = data
                self.state = self.State.STRENGTH_H
            elif state == self.State.STRENGTH_H:
                self.buffer['strength'][1] = data
                self.state = self.State.INT_TIME
            elif state == self.State.INT_TIME:
                self.buffer['int_time'] = data
                self.state = self.State.RESERVED
            elif state == self.State.RESERVED:
                self.state = self.State.CHECKSUM
            elif state == self.State.CHECKSUM:
                if self.buffer['sum'] == data:
                    self.packet = self.buffer
                    self.b_available = True
                else:
                    self.b_available = False
                self.reset()

    def reset(self):
        self.buffer = {'distance': [0, 0], 'strength': [0, 0], 'int_time': 0, 'sum': 0}
        self.state = self.State.HEAD_L

    RECV_FRAME_HEADER = 0x59

    def __init__(self):
        self.packet = {'distance': 0
