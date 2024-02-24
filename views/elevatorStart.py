import sys
sys.path.append('/Users/huangyao/PycharmProjects/elevatorSimulator')

from views.building import Building
from views.elevator import Elevator

bottom = -1
top = 10
building = Building(bottom, top)
elevator = Elevator(bottom, top)


def elevator_start():
    while True:
        print('------ 当前楼层 ：{}'.format(elevator.current_floor), flush=True)
        current_floor_data = building.get_data_by_index(elevator.current_floor)
        print('------ 当前楼的 floor_data ------', flush=True)
        print(current_floor_data, flush=True)

        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)

        person_not_in = elevator.run_elevator(furthest_floor, current_floor_data)

        building.update_floor_data(elevator.current_floor, person_not_in)
        print('------ 楼的 floor_data ------', flush=True)
        print(building.floor_data, flush=True)

        if building.is_elevator_pause() and elevator.person_data.empty:
            elevator.auto_reverse()
            print('******* break ******** {}'.format(elevator.current_floor), flush=True)
            break
        else:
            elevator.move()
            print('************** move ***************', flush=True)


if __name__ == '__main__':
    elevator_start()
