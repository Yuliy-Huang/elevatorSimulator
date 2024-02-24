import pandas as pd
import time


class Elevator(object):
    def __init__(self, bottom_floor, top_floor, current_floor: int = 1):
        self.each_floor_height = 5  # meter
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.current_floor = current_floor
        self.is_up = 1  # 1: up，0：down
        self.speed = 1  # meter per second
        self.door_open_time = 3  # second, door open and close time
        self.max_weight = 1000   # kg
        self.weight = 0
        self.max_persons = 12
        self.persons = 0
        self.person_data = pd.DataFrame(columns=['current_floor', 'weight', 'is_up', 'target_floor'])

    def clear_person_data(self):
        self.weight = 0
        self.persons = 0
        self.person_data = pd.DataFrame()

    def update_elevator_data(self, data, agg='add'):
        """update weight, persons and person_data in the elevator"""
        if agg == 'add':
            if round(self.weight + data['weight'].sum(), 2) > self.max_weight or self.persons + len(data) > self.max_persons:
                raise Exception('Elevator is overweight')
            self.weight = round(self.weight + data['weight'].sum(), 2)
            self.persons = self.persons + len(data)
            self.person_data = pd.concat([self.person_data, data])
        elif agg == 'sub':
            self.weight = round(self.weight - data['weight'].sum(), 2)
            self.persons = self.persons - len(data)
            self.person_data.drop(data.index, inplace=True)
        else:
            raise Exception('Input operator error')
        print('Elevator: update_elevator_data --- done ---self.person_data : ', self.person_data)

    def move(self):
        """update current_floor after the elevator starts moving"""
        if self.is_up:
            self.current_floor += 1
        else:
            self.current_floor -= 1

        if not self.current_floor:
            self.current_floor = self.current_floor + 1 if self.is_up else self.current_floor - 1

        time.sleep(self.each_floor_height/self.speed)

    def door_open_or_close(self):
        time.sleep(self.door_open_time)

    def reverse_when_reached_furthest(self, furthest_floor):
        """the elevator changes direction after it reaches the furthest floor"""
        if self.current_floor == self.top_floor:
            self.is_up = 0
        elif self.current_floor == self.bottom_floor:
            self.is_up = 1
        elif self.current_floor == furthest_floor:
            self.is_up = 0 if self.is_up else 1

    def whether_reverse(self, target_floor):
        """return which direction the elevator should go next"""
        if self.is_up and target_floor < self.current_floor:
            self.is_up = 0
        elif not self.is_up and target_floor > self.current_floor:
            self.is_up = 1

    def get_out_of_elevator(self):
        """get out of the elevator, """
        self.person_data.reset_index(drop=True, inplace=True)
        data = self.person_data.copy()
        if len(data) > 0:
            data = data[data['target_floor'] == self.current_floor].copy()
            print('Elevator: get_out_of_elevator ---- data : ', data)
            self.update_elevator_data(data, 'sub')

    def enter_elevator(self, data):
        """enter the elevator, """
        if not data:
            return data
        elevator_data = pd.DataFrame(data)
        # print('enter_elevator --- whole data : ', elevator_data)
        data_same_direction = elevator_data[elevator_data['is_up'] == self.is_up].copy()
        print('Elevator: enter_elevator --- data_same_direction : ', data_same_direction)
        self.update_elevator_data(data_same_direction, 'add')
        data_opposite_direction = elevator_data[elevator_data['is_up'] != self.is_up].copy()
        return data_opposite_direction.to_dict(orient='records')

    def run_elevator(self, target_floor, data):
        """start run elevator, return people who will not enter elevator"""
        self.reverse_when_reached_furthest(self.bottom_floor) # todo delete
        # self.door_open_or_close()  # todo delete
        self.get_out_of_elevator()
        data_not_in = self.enter_elevator(data)
        print('Elevator: --- elevator --- data_not_in : ', data_not_in)
        self.whether_reverse(target_floor)  #todo
        # self.door_open_or_close()  # todo delete
        return data_not_in

