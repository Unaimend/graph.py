
from model import MainModel
from window import Window
from observer import Observer
from logger import logger

class MainController(Observer):
    """
    Implements the controller from MVC-Pattern
    :param model: The model from mvc
    :param view:  The view from mvc
    """


    def __init__(self, view: Window, model: MainModel):
        Observer.__init__(self)
        self.model = model
        self.view = view

        self.view.attach(self)
        self.model.attach(self)

    def update(self, arg) -> None:
        # pylint: disable=R0201
        """
        Function which gets called from observed objects
        :param arg: Arguments which the observed class wants to be transmitted
        """
        state = arg[0]
        logger.info("State: %s", str(state))

        if state == self.view.State.LOAD_GRAPH:
            logger.info("ctrl: Loadign new graph %s", arg[1])
        else:
            logger.info("Not handled by controller")



