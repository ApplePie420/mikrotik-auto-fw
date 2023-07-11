# import all the bullshit we need
from textual.app import App, ComposeResult
from textual.widgets import Button, SelectionList, Label
from textual.widgets.selection_list import Selection
from textual.containers import Horizontal
import json
import os

# path where addresses are
filenames = os.listdir("./lists/cidr")
# create object with Selections for the SelectionList widget
selections = []
i = 0
for file in filenames:
    selections.append(Selection(str(file).split(".")[0], str(file), False))
    i += 1

# main app
class GenerateApp(App):
    # some styles for the app
    CSS_PATH = "./src/style.css"

    def compose(self) -> ComposeResult:
        # top row, containing selections
        yield Horizontal(
            SelectionList(*selections)
        )
        # middle row with buttons, thin
        yield Horizontal(
            Button("Generate IP list", id="generate", variant="success"),
            Button("Exit", id="exit", variant="error"),
            classes="thin"
        )
        # bottom row with status label, thin
        yield Horizontal(
            Label(""), classes="thin"
        )

    # nice name for the SelectionList
    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Select IP lists"

    # button events
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # generate button
        if(event.button.id == "generate"):
            # open config file for writing
            with open("./src/config.json", "w") as f:
                # create JSON object/dict
                jsonO = {
                    "lists_enabled": [
                        
                    ]
                }
                # populate the dict
                for item in self.query_one(SelectionList).selected:
                    jsonO["lists_enabled"].append(item)
                # write data to the file
                json.dump(jsonO, f, indent=4)

            # update status label and focus on the exit button
            self.query_one(Label).update("Success")
            self.query_one("#exit").focus()

        # exit button
        if(event.button.id == "exit"):
            self.exit()

# run the app
if __name__ == "__main__":
    app = GenerateApp()
    app.run()