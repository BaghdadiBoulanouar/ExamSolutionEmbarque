import datetime, time


def get_date_now():
    return str(datetime.datetime.now().minute)


class Task:

    def __init__(self, NAME, PERIOD, EXECUTION_TIME, PRIORITY=0, PRODUCE_OIL=0, NEED_OIL=0):
        self.NAME = NAME
        self.PERIOD = PERIOD
        self.EXECUTION_TIME = EXECUTION_TIME
        self.PRIORITY = PRIORITY  # 0 by default

        self.PRODUCE_OIL = PRODUCE_OIL
        self.NEED_OIL = NEED_OIL

        self.NEXT_DEADLINE = datetime.datetime.now()
        self.LAST_EXECUTED_TIME = datetime.datetime.now()

        self.EXECUTION_DONE = 100  # Big number by default

    def need_to_run(self):

        if datetime.datetime.now() > self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD):
            print("\tTask " + self.NAME + "\ŧFAILED deadline.\t" + str(
                self.EXECUTION_DONE / self.EXECUTION_TIME) + "% done.")
            self.NEXT_DEADLINE += datetime.timedelta(seconds=self.PERIOD)
            self.EXECUTION_DONE = 0

        if datetime.datetime.now() > self.NEXT_DEADLINE:
            return True

        return False

    def add_produce_oil(self):
        global tank
        if self.PRODUCE_OIL > 0 and tank + self.PRODUCE_OIL <= 50:
            tank = tank + self.PRODUCE_OIL
            print('the tank is filled to ', str(tank))


    def use_produce_oil(self):
        global tank
        if self.NEED_OIL > 0 and tank - self.NEED_OIL >= 0:
            tank = tank - self.NEED_OIL
            print('the tank is filled to ', str(tank))

    def compare_production(self):
        global wheel, motor
        product_new_element = False
        if self.NAME == 'Machine 1' and (wheel / 4) > motor:
            product_new_element = True

        if self.NAME == 'Machine 2' and (wheel / 4) < motor:
            product_new_element = True

        if self.NAME == 'Machine 2' and motor == (wheel / 4):
            product_new_element = True

        return product_new_element

    def product_element(self):
        global wheel
        global motor

        if self.NAME == 'Machine 1':
            motor = motor + 1
            print(self.NAME + ' product 1 motor. Number of motor : ' + str(motor))
        if self.NAME == 'Machine 2':
            wheel = wheel + 1
            print(self.NAME + ' product 1 wheel. Number of wheel : ' + str(wheel))



    def run(self):
        global timer

        print(str(timer) + ": " + get_date_now() + "\t=> " + self.NAME + " completed without interruption.")

        self.add_produce_oil()
        self.use_produce_oil()
        self.product_element()

        time.sleep(self.EXECUTION_TIME)
        self.NEXT_DEADLINE = self.NEXT_DEADLINE + datetime.timedelta(seconds=self.PERIOD)


if __name__ == "__main__":

    # Definition of all tasks and instanciation
    task_list = [
        Task(NAME='Pump 1', PERIOD=5, EXECUTION_TIME=2, PRODUCE_OIL=10),
        Task(NAME='Pump 2', PERIOD=15, EXECUTION_TIME=3, PRODUCE_OIL=20),
        Task(NAME='Machine 1', PERIOD=5, EXECUTION_TIME=5, NEED_OIL=25),
        Task(NAME='Machine 2', PERIOD=5, EXECUTION_TIME=3, NEED_OIL=5)]

    global timer
    timer = -1

    time_execution = 0

    global tank
    tank = 0

    global motor
    motor = 0

    global wheel
    wheel = 0

    task_pump = None

    # Global scheduling loop
    while (time_execution < 120):

        task_to_run = None
        task_priority = 0
        timer += 1

        # Choose the task to be run
        for current_task in task_list:

            current_task_need_to_run = current_task.need_to_run()

            if current_task.PRODUCE_OIL > 0 and tank + current_task.PRODUCE_OIL <= 50:
                if task_pump is None:
                    task_pump = current_task
                    task_to_run = current_task
                elif task_pump.NAME != current_task.NAME:
                    task_to_run = current_task


            if current_task.NEED_OIL > 0 and tank - current_task.NEED_OIL >= 0 and current_task.compare_production():
                task_to_run = current_task


        if task_to_run == None:
            time.sleep(1)
            print(str(timer) + "\tIdle")
        else:
            task_to_run.run()
            time_execution = time_execution + task_to_run.EXECUTION_TIME
