from enum import Enum
from utils import AoCDay

class Packet():
    version: int
    type: int
    data: int
    sub_packets: list["Packet"]
    
    def parse_data(self, data_str: str):
        if self.type == 4:
            data = ""
            for i in range(0, len(data_str), 5):
                piece = data_str[i:i+5]
                bytes = piece[1:]
                data = data+bytes

                if piece[0] == "0":
                    break

            self.data = int(data, 2)
            
        elif self.type != 4:
            pass

    def __init__(self, raw: str) -> None:
        self.version = int(raw[0:3], 2)
        self.type = int(raw[3: 6], 2)
        self.parse_data(raw[6:])

class Day16(AoCDay):
    bits: str
    
    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.bits = bin(int(self.lines[0], 16))[2:]

    def part1(self):
        print(Packet(self.bits).data)