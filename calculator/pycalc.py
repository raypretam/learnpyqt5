
import sys
from functools import partial

from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

#Create a subclass to handel the GUI of the calculator
class PyCalcUI(QMainWindow):
    #PyCalc's View(GUI).
    def __init__(self):
        super(PyCalcUI,self).__init__()

        #Window Properties.
        self.setWindowTitle('PyCalC')
        self.setFixedSize(435,435)

        #Central Widget.
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        #Create the display and buttons
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):

        #Create display widget
        self.display = QLineEdit()

        #Set display properties
        self.display.setFixedHeight(55)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        #Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        #Create the buttons.
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(75, 75)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            # Add buttonsLayout to the general layout
            self.generalLayout.addLayout(buttonsLayout)


    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')

#Create the controller class to connect the GUI and the model
class PyCalcCtrl:

    def __init__(self,model,view):
        self._view = view
        self._evaluate = model
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self,sub_exp):

        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):

        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=','C'}:
                btn.clicked.connect(partial(self._buildExpression,btnText))
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)


ERROR_MSG = 'Error'
#Evaluate expression helper funtion
def evaluateExpression(expression):
    try:
        result = str(eval(expression,{},{}))
    except Exception:
        retult = ERROR_MSG

    return result


    #Client Mode
def main():
    #Create instance of QApplication
    pycalc = QApplication(sys.argv)

    #Show the GUI
    view = PyCalcUI()
    view.show()

    #Create instance of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model,view=view)

    #Execute main event loop
    sys.exit(pycalc.exec_())

if __name__=='__main__':
    main()
