import sys
sys.path.append('/Users/huangyao/PycharmProjects/elevatorSimulator')

from views.building import Building
from views.elevator import Elevator

building = Building(-1, 20)
elevator = Elevator(-1, 20)


def elevator_start():
    while True:
        print('------ 当前楼层 ：', elevator.current_floor)
        data = building.get_data_by_index(elevator.current_floor)
        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)
        building.update_floor_data(elevator.current_floor, elevator.run_elevator(furthest_floor, data))
        print('------ 楼的 floor_data ------')
        print(building.floor_data)
        if building.is_elevator_pause() and elevator.person_data.empty:
            print('******* break ********')
            break


if __name__ == '__main__':
    elevator_start()
