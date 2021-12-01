def monitor(func):
    # Attribute to a function (i.e. static variable)
    monitor.thresholds = {}

    def __wrapper(self, recipient, value, transaction_date : datetime):
        if self.owner not in monitor.thresholds:
            monitor.thresholds[self.owner] = 50
        if value > monitor.thresholds[self.owner]:
            L.warning(f'{self.owner} New highest value transferred: {value}')
            monitor.thresholds[self.owner] = value

        func(self, recipient, value, transaction_date)

    return __wrapper
