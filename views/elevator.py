import pandas as pd
import time


class Elevator(object):
    def __init__(self, bottom_floor, top_floor, current_floor: int = 1):
        self.each_floor_height = 3  # meter
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.current_floor = current_floor
        self.furthest_target_floor = 0
        self.is_up = 1  # 1: up，0：down
        self.speed = 1  # meter per second
        self.door_open_time = 12  # second, door open and close time
        self.door_handle = 0
        self.max_weight = 1000  # kg
        self.weight = 0
        self.max_persons = 12
        self.persons = 0
        self.person_data = pd.DataFrame(columns=['current_floor', 'weight', 'is_up', 'target_floor'])

    def clear_person_data(self):
        self.weight = 0
        self.persons = 0
        self.person_data = pd.DataFrame()

    def get_furthest_target(self):
        """in the direction of the elevator, get the furthest target floor from the elevator"""
        # print('Elevator: get_furthest_target --- {} self.is_up : {}'.format(self.current_floor, self.is_up))
        if self.is_up:
            self.furthest_target_floor = self.person_data['target_floor'].max() if len(self.person_data) > 0 else 0
            # print('Elevator: up get_furthest_target -- self.furthest_target_floor : {}'.format(
            #     self.furthest_target_floor))
        else:
            self.furthest_target_floor = self.person_data['target_floor'].min() if len(self.person_data) > 0 else 0
            # print('Elevator: down get_furthest_target -- self.furthest_target_floor : {}'.format(
            #     self.furthest_target_floor))

    def update_elevator_data(self, data, agg='add'):
        """update weight, persons and person_data in the elevator"""
        if agg == 'add':
            if round(self.weight + data['weight'].sum(), 2) > self.max_weight or self.persons + len(
                    data) > self.max_persons:
                raise Exception('Elevator is overweight')
            self.weight = round(self.weight + data['weight'].sum(), 2)
            self.persons = self.persons + len(data)
            self.person_data = pd.concat([self.person_data, data])
            self.get_furthest_target()
        elif agg == 'sub':
            self.weight = round(self.weight - data['weight'].sum(), 2)
            self.persons = self.persons - len(data)
            self.person_data.drop(data.index, inplace=True)
            self.get_furthest_target()
        else:
            raise Exception('Input operator error')
        # print('Elevator: update_elevator_data --- done ---self.person_data : ', self.person_data)
        # print('Elevator: -- update_elevator_data -- self.furthest_target_floor : ', self.furthest_target_floor)

    def move(self):
        """update current_floor after the elevator starts moving"""
        if self.is_up:
            self.current_floor += 1
        else:
            self.current_floor -= 1

        if not self.current_floor:
            self.current_floor = self.current_floor + 1 if self.is_up else self.current_floor - 1
        time.sleep(self.each_floor_height / self.speed)

    def door_open(self):
        print('Elevator: ^^^^^^^^^^^^^^ door_open ^^^^^^^^^^^')
        time.sleep(self.door_open_time)

    def door_close(self):
        print('Elevator: ^^^^^^^^^^^^^^ door_close ^^^^^^^^^^^')
        time.sleep(self.door_open_time)
        self.door_handle = 0

    def auto_reverse(self):
        """the elevator changes direction after it reaches the furthest floor"""
        if self.current_floor == self.top_floor:
            self.is_up = 0
            # print('Elevator: auto_reverse --- top_floor -- self.is_up : ', self.is_up)
        elif self.current_floor == self.bottom_floor:
            self.is_up = 1
            # print('Elevator: auto_reverse --- bottom_floor -- self.is_up : ', self.is_up)
        else:
            self.is_up = 0 if self.is_up else 1
            # print('Elevator: auto_reverse --- reverse ----')

    def which_direction(self, furthest_floor, data_not_in):
        """return which direction the elevator should go next"""
        is_up = self.is_up
        most_far = self.furthest_target_floor
        # print('Elevator: --- which_direction 000 --- is_up : ', is_up)
        if furthest_floor:
            if self.is_up:
                most_far = self.furthest_target_floor if self.furthest_target_floor and self.furthest_target_floor > furthest_floor else furthest_floor
            else:
                most_far = self.furthest_target_floor if self.furthest_target_floor and self.furthest_target_floor < furthest_floor else furthest_floor
        # print('Elevator: --- which_direction --- most_far : ', most_far)
        if most_far == 0:
            self.is_up = 0 if self.is_up else 1
        elif self.is_up and most_far <= self.current_floor:
            self.is_up = 0
        elif not self.is_up and most_far >= self.current_floor:
            self.is_up = 1
        # print('Elevator: --- which_direction --- self.is_up : ', self.is_up)
        reverse = False
        if is_up != self.is_up:
            self.enter_elevator(data_not_in)
            reverse = True
        return reverse

    def get_out_of_elevator(self):
        """get out of the elevator, """
        self.person_data.reset_index(drop=True, inplace=True)
        data = self.person_data.copy()
        if len(data) > 0:
            data = data[data['target_floor'] == self.current_floor].copy()
            self.update_elevator_data(data, 'sub')

    def enter_elevator(self, data):
        """enter the elevator, """
        if not data:
            return data
        floor_data = pd.DataFrame(data)
        data_same_direction = floor_data[floor_data['is_up'] == self.is_up].copy()
        # print('Elevator: enter_elevator --- data_same_direction : ', data_same_direction)
        self.update_elevator_data(data_same_direction, 'add')
        data_opposite_direction = floor_data[floor_data['is_up'] != self.is_up].copy()
        return data_opposite_direction.to_dict(orient='records')

    def run_elevator(self, furthest_floor, data):
        """start run elevator, return people who will not enter elevator"""
        self.get_out_of_elevator()
        data_not_in = self.enter_elevator(data)
        print('Elevator: ************* elevator *************- door_handle : ', self.door_handle)
        if self.door_handle:
            self.door_open()
            self.door_close()
        print('Elevator: --- elevator --- data_not_in : ', data_not_in)
        reverse = self.which_direction(furthest_floor, data_not_in)
        if reverse:
            data_not_in = []
        return data_not_in
