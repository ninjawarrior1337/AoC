from enum import Enum
import json
from utils import AoCDay

class Packet():
    raw = ""
    version: int
    type: int
    data: int
    sub_packets: list["Packet"] = []

    def __len__(self) -> int:
        return len(self.raw)

    def __str__(self) -> str:
        return json.dumps(self.__dict__)

    def parse_data(self, data_str: str):
        if self.type == 4:
            data = ""
            for i in range(0, len(data_str), 5):
                piece = data_str[i:i+5]
                bytes = piece[1:]
                data = data+bytes
                self.raw += piece

                if piece[0] == "0":
                    break

            self.data = int(data, 2)
            
        elif self.type != 4:
            LT = int(data_str[0], 2)
            T = int(data_str[1:14], 2) if LT == 0 else int(data_str[1:12], 2)
            packet_str = data_str[14:] if LT == 0 else data_str[12:]
            l = 0
            packet_ct = 0
            print(LT, T, data_str, packet_str, l)
            if LT == 0:
                while l < T:
                    p = Packet(packet_str[l:])
                    self.sub_packets.append(p)
                    l += len(p)
            else:
                while packet_ct < T:
                    p = Packet(packet_str[l:])
                    self.sub_packets.append(p)
                    l += len(p)
                    packet_ct+=1

    def __init__(self, raw: str) -> None:
        self.version = int(raw[0:3], 2)
        self.type = int(raw[3: 6], 2)
        self.raw = f"{raw[0:3]}{raw[3: 6]}"
        print(raw)
        self.parse_data(raw[6:])

class Day16(AoCDay):
    bits: list[str]
    
    def __init__(self, linesRaw: str) -> None:
        super().__init__(linesRaw)
        self.bits = bin(int(self.lines[0], 16))[2:]

    def part1(self):
        p = Packet(self.bits)
        print([p.data for p in p.sub_packets])