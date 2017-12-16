class Stock:
    name = ''
    df = ''
    start_date = ''
    end_date = ''

    def __init__(self, name, data):
        self.name = name
        self.df = data
        self.start_date = min(data['Date'])
        self.end_date = max(data['Date'])

