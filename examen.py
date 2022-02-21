import datetime
import time
import threading
import random


################################################################################
#   Watchdog to stop tasks
################################################################################
class Watchdog(threading.Thread):
    period = -1

    ############################################################################
    def __init__(self, period):

        self.period = period

        threading.Thread.__init__(self)

    ############################################################################
    def run(self):

        print(" : Starting watchdog")

        self.current_cpt = self.period

        while (1):

            if (self.current_cpt >= 0):

                self.current_cpt -= 1
                time.sleep(1)
            else:
                print("!!! Watchdog stops tasks.")
                global watchdog
                watchdog = True
                self.current_cpt = self.period


################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():
    name = None
    priority = -1
    period = -1
    execution_time = -1
    last_deadline = -1
    last_execution_time = None

    ############################################################################
    def __init__(self, name, priority, period, execution_time, last_execution):

        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.last_execution_time = last_execution

    ############################################################################
    def run(self):

        # Update last_execution_time
        self.last_execution_time = datetime.datetime.now()

        global watchdog

        execution_time = random.randint(2, 15)

        print(self.name + " : Starting task (" + self.last_execution_time.strftime(
            "%H:%M:%S") + ") : execution time = " + str(execution_time))

        while (watchdog == False):

            execution_time -= 1

            time.sleep(1)

            if (execution_time <= 0):
                print(self.name + " : Terminating normally (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
                return

        print(self.name + " : Pre-empting task (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':

    # Init and instanciation of watchdog
    global watchdog
    watchdog = False

    nbr_motors = 0              #nombre de motors
    nbr_wheels= 0             #nombre de roues
    tank_full = 0                # il sera plein a 50

    my_watchdog = Watchdog(period=10)  # Watchdog 10 seconds
    my_watchdog.start()

    # Instanciation of task objects
    task_list = []

    last_execution = datetime.datetime.now()

    task_list.append(my_task(name="Pump1", priority=1, period=5, execution_time=2, last_execution=last_execution))
    task_list.append(my_task(name="Pump2", priority=1, period=15, execution_time=3, last_execution=last_execution))
    task_list.append(my_task(name="Machine1", priority=1, period=5, execution_time=5, last_execution=last_execution))
    task_list.append(my_task(name="Machine2", priority=1, period=5, execution_time=3, last_execution=last_execution))

    # Global scheduling loop
    while (1):

        print("Scheduler tick : " + datetime.datetime.now().strftime("%H:%M:%S"))

        # Reinit watchdog

        watchdog = False
        my_watchdog.current_cpt = 10

        # Get current time and find the task with Earliest deadline or most priority regarding algorithm choice

        task_to_run = None

        earliest_deadline = datetime.datetime.now() + datetime.timedelta(
            minutes=2)  # Init ... not perfect but will do the job

        for current_task in task_list:

            current_task_next_deadline = current_task.last_execution_time + datetime.timedelta(
                seconds=current_task.period)

            print("\tDeadline for task " + current_task.name + " : " + current_task_next_deadline.strftime("%H:%M:%S"))

            if (current_task_next_deadline < earliest_deadline):
                earliest_deadline = current_task_next_deadline

                if current_task.name == 'Pump1' and not tank_full >= 50:
                    tank_full=tank_full+10
                    task_to_run = current_task
                if current_task.name == 'Pump2' and not tank_full >= 50:
                    tank_full=tank_full+20
                    task_to_run = current_task
                if current_task.name == 'Machine1' and (nbr_wheels/4)>nbr_motors:
                    nbr_motors += 1
                    task_to_run = current_task
                if current_task.name == 'Machine2' and (nbr_wheels/4)<nbr_motors:
                    nbr_wheels += 1
                    task_to_run = current_task

            # print("\tPriority to task : " + current_task.name)

        # Start task selected by scheduler
        task_to_run.run()




