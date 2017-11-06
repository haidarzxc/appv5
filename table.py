from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class TableHeader(Label):
    pass


class Record(Label):
    pass


class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.cols = 3
        self.size_hint_y= None
        self.bind(minimum_height=self.setter('height'))
        self.spacing= '1dp'
        self.fetchData()
        self.renderData()

    def fetchData(self):
        self.data = [
            {'name': 'Alfa', 'score': 'Bravo', 'car': 'charley'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'},
            {'name': 'dummy', 'score': '0', 'car': 'none'}
        ]

    def renderData(self):
        self.clear_widgets()
        for i in xrange(len(self.data)):
            if i < 1:
                row = self.createHeader(i)
            else:
                row = self.createRecord(i)
            for item in row:
                self.add_widget(item)

    def createHeader(self, i):
        x=[]
        for k in self.data[i]:
            column = TableHeader(text=self.data[i][k])
            x.append(column)
        return x

    def createRecord(self, i):
        x=[]
        for k in self.data[i]:
            column = Record(text=self.data[i][k])
            x.append(column)
        return x