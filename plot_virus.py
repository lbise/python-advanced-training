#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class Scenario(object):
    def __init__(self, incubation_duration, duration, critical, lockdown_duration, celebrations, r0):
        """
            Constructor for the virus spread scenario

            Parameters:
            incubation_duration: Number of days before the R0 actually changes
            duration: Number of days of simulation
            critical: Thresold for triggering lockdowns
            lockdown_duration: Lockdown duration in days
            celebrations: List of individual dates of celebrations
            r0: Dictionary containing values for high, lockdown and regular
        """
        self.incubation_duration = incubation_duration
        self.duration = duration
        self.critical = critical
        self.lockdown_duration = lockdown_duration
        self.celebrations = celebrations
        self.r0 = r0
        self.remain_lockdown = 0
        self.lockdowns = []
        self.r0_history = deque([1] * self.incubation_duration)
        print('len={}'.format(len(self.r0_history)))

    def next(self, num_former_cases:int, day):
        """
            Simulates one day
        """
        r0 = self.r0['regular']
        if self.remain_lockdown > 0:
            self.remain_lockdown -= 1
            r0 = self.r0['lockdown']
        elif num_former_cases >= self.critical:
            print('New lockdown day={} end={}'.format(day, day + self.lockdown_duration))
            self.remain_lockdown = self.lockdown_duration
            self.lockdowns.append({'start': day, 'end': day + self.lockdown_duration})

#        if self.remain_lockdown == 0:
#            if num_former_cases >= self.critical:
#                print('New lockdown day={} end={}'.format(day, day + self.lockdown_duration))
#                self.remain_lockdown = self.lockdown_duration
#                self.lockdowns.append({'start': day, 'end': day + self.lockdown_duration})
#        else:
#            self.remain_lockdown -= 1
#            r0 = self.r0['lockdown']

        if day in self.celebrations:
            r0 *= self.r0['high']

        self.r0_history.append(r0)
        r0 = self.r0_history.popleft()

        num_case = r0 * num_former_cases
        print('day{}: r0={} cases={}'.format(day, r0, num_case))
        return num_case

    def plot(self):
        """
            Create the plot using the scenario attributes
        """
        fig, ax = plt.subplots()
        plt.title('Lockdowns of {} days above {} cases, with {} celebrations and {} days of incubation'.format(self.lockdown_duration, self.critical, len(self.celebrations), self.incubation_duration))
        ax.set_xlabel('days')
        ax.set_ylabel('COVID-19 positive cases')

        self.cases_history = [1]
        for i in range(1, self.duration):
            self.cases_history.append(self.next(self.cases_history[i-1], i))

        # Ensure last lockdown is terminated properly
        if self.lockdowns[-1]['end'] == -1:
            self.lockdowns[-1]['end'] = self.duration

        for lockdown in self.lockdowns:
            ax.fill_between([lockdown['start'], lockdown['end']], 0, 1, color='green', alpha=0.1, label='lockdown', transform=ax.get_xaxis_transform())

        for celebration in self.celebrations:
            plt.axvline(celebration, color='red', label='celebration')

        ax.plot(self.cases_history, label='COVID-19 cases')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    s = Scenario(
        incubation_duration = 15,     # Number of days before the R0 actually changes
        duration = 300,               # Days of simulation
        critical = 5000,              # Threshold for triggering lockdowns
        lockdown_duration = 60,       # Lockdown duration in days
        celebrations = [
                        74, 75, 76,   # Individual dates of celebrations
                        210, 211, 212
                       ],
        r0 = {
            "high": 2,          # R0 applied for celebrations
            "lockdown": 0.9,    # R0 applied for lockdowns
            "regular": 1.2,     # R0 applied for all other cases
        }
    )

    s.plot()
