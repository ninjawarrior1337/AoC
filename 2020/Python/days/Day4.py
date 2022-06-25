from utils import AoCDay
from typing import Optional
from pydantic import BaseModel, ValidationError, validator
import re


class Passport(BaseModel):
    byr: int
    iyr: int
    eyr: int
    hgt: str
    hcl: str
    ecl: str
    pid: str
    cid: Optional[str]

    @validator("byr")
    def byr_check(cls, v):
        if not 1920 <= v <= 2002:
            raise ValidationError("dates out of range")
        return v

    @validator("iyr")
    def iyr_check(cls, v):
        if not 2010 <= v <= 2020:
            raise ValidationError("dates out of range")
        return v

    @validator("eyr")
    def eyr_check(cls, v):
        if not 2020 <= v <= 2030:
            raise ValidationError("dates out of range")
        return v

    @validator("hgt")
    def hgt_check(cls, v):
        i = int(v[:-2])
        if "cm" in v:
            if 150 <= i <= 193:
                raise ValidationError("height unrealistic")
        if "in" in v:
            if 59 <= i <= 76:
                raise ValidationError("height unrealistic")
        return v

    @validator("hcl")
    def hcl_check(cls, v):
        e = ValidationError("invalid hex string")
        match = re.search(r'^#(?:[\da-fA-F]{3}){1,2}$', v)
        if not match:
            raise e
        return v

    @validator("ecl")
    def ecl_check(cls, v):
        valid = "amb blu brn gry grn hzl oth"
        if v in valid.split(" "):
            return v
        else:
            raise ValidationError("invalid ecl")

    @validator("pid")
    def pid_check(cls, v):
        if not re.search(r"^[0-9]{9}$", v):
            raise ValidationError("invalid pid")
        return v


class Day4(AoCDay):
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    def extract(self):
        self.lines.append("")
        passports = []
        passport = []
        for d in self.lines:
            if d != "":
                passport.append(d)
            else:
                passports.append(passport)
                passport = []

        def parse(pas: list):
            data = {}
            for p in pas:
                for a in p.split(" "):
                    k, v = a.split(":")
                    data[k] = v
            return data

        return map(parse, passports)

    def part1(self):
        self.p1 = 0
        for p in self.extract():
            if all(f in p.keys() for f in self.req_fields):
                self.p1 += 1

    def part2(self):
        self.p2 = 0
        for d in self.extract():
            print(d)
            Passport(**d)
            self.p2 += 1
