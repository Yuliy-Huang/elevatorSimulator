import sys
sys.path.append('/Users/huangyao/PycharmProjects/elevatorSimulator')

from views.building import Building
from views.elevator import Elevator
import logging
logger = logging.getLogger('elevatorLogger')
logger.setLevel(logging.DEBUG)

bottom = -1
top = 10
building = Building(bottom, top)
elevator = Elevator(bottom, top)


def elevator_start():
    while True:
        logger.info('------ 当前楼层 ：{}'.format(elevator.current_floor))
        data = building.get_data_by_index(elevator.current_floor)
        furthest_floor = building.get_furthest_floor(elevator.current_floor, elevator.is_up)
        building.update_floor_data(elevator.current_floor, elevator.run_elevator(furthest_floor, data))
        logger.info('------ 楼的 floor_data ------')
        logger.info(building.floor_data)

        if (elevator.is_up and furthest_floor > elevator.current_floor) or (not elevator.is_up and furthest_floor < elevator.current_floor):
            elevator.move()
            logger.info('------ move ------')

        if building.is_elevator_pause() and elevator.person_data.empty:
            logger.info('******* break ******** {}'.format(elevator.current_floor))
            break




if __name__ == '__main__':
    elevator_start()
