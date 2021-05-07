from kivy.uix.boxlayout import BoxLayout

from graphics.customWidgets.betterButton import BetterButton


class BuildingButtonsHandler(BoxLayout):
    def redo_buttons(self, button_ids: list[str]):
        print(button_ids)
        for button in self.children:
            self.remove_widget(button)

        button_id: str
        for button_id in button_ids:
            button = BetterButton(button_id=button_id)
            print(button)
            self.add_widget(button)
