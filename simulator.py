import matplotlib.pyplot as plt
import numpy as np
import logging
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
        self.L = logging.getLogger(__name__)
        self.incubation_duration = incubation_duration
        self.duration = duration
        self.critical = critical
        self.lockdown_duration = lockdown_duration
        self.celebrations = celebrations
        self.r0 = r0
        self.remain_lockdown = 0
        self.lockdowns = []
        self.r0_history = deque([1] * self.incubation_duration)

    def next(self, num_former_cases:int, day):
        """
            Simulates one day
        """
        if day in [x['end'] for x in self.lockdowns]:
            self.L.info('Lockdown ended on day {}'.format(day))

        r0 = self.r0['regular']
        if self.remain_lockdown > 0:
            self.remain_lockdown -= 1
            self.L.debug('Remaining lock down days {}'.format(self.remain_lockdown))
            r0 = self.r0['lockdown']
        elif num_former_cases >= self.critical:
            self.L.warn('New lockdown day={} end={}'.format(day, day + self.lockdown_duration))
            self.remain_lockdown = self.lockdown_duration
            self.lockdowns.append({'start': day, 'end': day + self.lockdown_duration})

        if day in self.celebrations:
            r0 *= self.r0['high']

        self.r0_history.append(r0)
        r0 = self.r0_history.popleft()

        num_case = r0 * num_former_cases
        self.L.debug('day{}: r0={} cases={}'.format(day, r0, num_case))
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
