import pandas as pd
from views.randomData import InitFloorPeopleData


class Building(object):
    def __init__(self, bottom_floor: int = -1, top_floor: int = 20):
        """init building"""
        # self.each_floor_height = 3  # meter
        self.bottom_floor = bottom_floor
        self.top_floor = top_floor
        self.floor_data = pd.DataFrame(columns=['current_floor', 'weight', 'is_up', 'target_floor'])

    def set_floor_data(self):
        data = InitFloorPeopleData(bottom_floor=self.bottom_floor, top_floor=self.top_floor).several_persons()
        # print('Building: set_floor_data --- InitFloorPeopleData --- data: ', data)
        if len(data) == 0:
            data = InitFloorPeopleData(bottom_floor=self.bottom_floor, top_floor=self.top_floor).several_persons()
            print('Building: set_floor_data ---2222---- InitFloorPeopleData --- data: ', data)
        new_data = pd.concat([pd.DataFrame(i, index=[0]) for i in data])
        self.floor_data = pd.concat([self.floor_data, new_data])
        # print('Building: set_floor_data -- done -- self.floor_data : ', self.floor_data)

    def set_one_person_data(self, data):
        new_data = pd.concat([pd.DataFrame(i, index=[0]) for i in data])
        self.floor_data = pd.concat([self.floor_data, new_data])
        # print('Building: set_one_person_data -- done -- self.floor_data : ', self.floor_data)

    def clear_floor_data(self):
        self.floor_data = pd.DataFrame()

    def is_elevator_pause(self):
        """if nobody in the building calls the elevator, return True"""
        return self.floor_data.empty

    def get_data_by_index(self, floor_index):
        """get people data according to the floor index"""
        if not floor_index or floor_index < self.bottom_floor or floor_index > self.top_floor:
            raise Exception('Input floor index error')
        return self.floor_data[self.floor_data['current_floor'] == floor_index].to_dict(orient='records') if len(self.floor_data) > 0 else []

    def get_called_floors(self):
        """get the floors where somebody called the elevator and the direction"""
        if self.floor_data.empty:
            return pd.DataFrame(columns=['current_floor', 'is_up', 'elevator_run_direction'])
        floor_data = self.floor_data[['current_floor', 'is_up']].drop_duplicates(
            subset=['current_floor', 'is_up']).sort_values('current_floor').copy()
        floor_data['elevator_run_direction'] = floor_data.apply(
            lambda x: abs(x[1] - 1) if x[0] == self.top_floor or x[0] == self.bottom_floor else x[1], axis=1)
        # print('Building: get_called_floors --- floor_data : {}'.format(floor_data))
        return floor_data

    def get_furthest_floor(self, current_floor, is_up=1):
        """in the direction of the elevator, get the furthest called floor from the current floor"""
        floor_data = self.get_called_floors()
        same_direction_data = floor_data[floor_data['elevator_run_direction'] == is_up].copy()
        distinct_direction_data = floor_data[floor_data['elevator_run_direction'] != is_up].copy()
        # print('Building: get_furthest_floor --- {} is_up : {}'.format(current_floor, is_up))
        if is_up:
            floor_list = \
            same_direction_data[same_direction_data['current_floor'] >= current_floor].sort_values('current_floor',
                                                                                                   ascending=False)[
                'current_floor'].unique().tolist()
            # print('Building: up get_furthest_floor -- floor_list : {}'.format(floor_list))

            if len(floor_list) == 0:
                floor_list = \
                    distinct_direction_data[distinct_direction_data['current_floor'] >= current_floor].sort_values(
                        'current_floor',
                        ascending=False)[
                        'current_floor'].unique().tolist()
                # print('Building: up get_furthest_floor --ififif-- floor_list : {}'.format(floor_list))
        else:
            floor_list = \
            same_direction_data[same_direction_data['current_floor'] <= current_floor].sort_values('current_floor',
                                                                                                   ascending=True)[
                'current_floor'].unique().tolist()
            # print('Building: down get_furthest_floor -- floor_list : {}'.format(floor_list))
            if len(floor_list) == 0:
                floor_list = \
                    distinct_direction_data[distinct_direction_data['current_floor'] <= current_floor].sort_values(
                        'current_floor',
                        ascending=True)[
                        'current_floor'].unique().tolist()
                # print('Building: down get_furthest_floor --ififif-- floor_list : {}'.format(floor_list))

        # print('Building: **** get_furthest_floor --- finally -- floor_list : {}'.format(floor_list))
        res = floor_list[0] if len(floor_list) > 0 else 0
        # print('Building: get_furthest_floor -- return res : ', res)
        return res

    def update_floor_data(self, floor_index, data):
        """When the elevator arrived, someone will enter the elevator, then the floor_data will be reduced"""
        # print('Building: -- update_floor_data -- current floor -- data :')
        # print(data)
        if not floor_index or floor_index < self.bottom_floor or floor_index > self.top_floor:
            raise Exception('Input floor index error')
        # print('Building: update_floor_data -- start -- self.floor_data : ')
        # print(self.floor_data)
        if len(self.floor_data) > 0:
            self.floor_data = self.floor_data[self.floor_data['current_floor'] != floor_index]
        self.floor_data = pd.concat([self.floor_data, pd.DataFrame(data)])
        self.floor_data.reset_index(drop=True, inplace=True)
        # print('Building: update_floor_data -- done -- self.floor_data : ')
        # print(self.floor_data)
