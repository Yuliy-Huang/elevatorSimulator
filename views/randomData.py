import random


class InitPeopleData(object):
    def __init__(self, current_floor: int, bottom_floor: int, top_floor: int, is_up: int = -1, weight: float = 0,
                 target_floor: int = 0):
        self.current_floor = current_floor
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.weight = round(random.uniform(20, 120), 2) if not weight else weight
        self.is_up = random.randint(0, 1) if is_up == -1 else is_up
        self.target_floor = self.where_to_go() if not target_floor else target_floor

    def where_to_go(self):
        if self.current_floor == self.bottom_floor:
            self.is_up = 1
        elif self.current_floor == self.top_floor:
            self.is_up = 0

        if self.is_up == 1:
            return random.randint(self.current_floor + 1, self.top_floor)
        else:
            tmp = random.randint(self.bottom_floor, self.current_floor - 1)
            return -1 if tmp <= 0 else tmp

    def to_dict(self):
        return {
            'current_floor': self.current_floor,
            'weight': self.weight,
            'is_up': self.is_up,
            'target_floor': self.target_floor,
        }


class InitFloorPeopleData(object):
    def __init__(self, bottom_floor: int, top_floor: int):
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.called_floors = [i if i > 0 else -1 for i in
                              random.sample(range(1, top_floor + 1), random.randint(1, top_floor))]

    def several_persons(self):
        people_list = []
        for i in self.called_floors:
            for _ in range(1, random.randint(1, 5)):
                people = InitPeopleData(i, self.bottom_floor, self.top_floor).to_dict()
                people_list.append(people)
        return people_list

    def one_person(self, current_floor, is_up=-1, weight=0, target_floor=0):
        if is_up == -1:
            people_list = [InitPeopleData(current_floor, self.bottom_floor, self.top_floor).to_dict()]
        elif is_up != -1 and weight and target_floor:
            people_list = [
                InitPeopleData(current_floor, self.bottom_floor, self.top_floor, is_up, weight, target_floor).to_dict()]
        else:
            people_list =[InitPeopleData(current_floor, self.bottom_floor, self.top_floor, is_up).to_dict()]
        return people_list
