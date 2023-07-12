from global_funcs import *
from textual.app import App, ComposeResult
from textual.widgets import Button, Label, Pretty, ListView, ListItem
from textual.containers import Horizontal
import re

# create our router connection
client = connect_to_router()

# function that just returns list of all rules created by auto-fw
def show_autofw_rules(client):
    a = exec_on_client(client, 'ip firewall filter print where comment~"auto-fw"', verbose=False)
    return a

# now let's do some majestic bullshittery to parse the absolutely retarded mikrotik output so we can use it
fw_rules = show_autofw_rules(client).split("\r\n")[1:]
# filter out empty items
while("" in fw_rules):
    fw_rules.remove("")

# thank you https://stackoverflow.com/a/4998460 for this
# it gets the completely fragmented array and it basically group elements by 2, since it splits comment and data apart and they belong together
N = 2
niceRules = [fw_rules[n:n+N] for n in range(0, len(fw_rules), N)]

# array of ListItems that'll be used in ListView
listItemObject = []
for rule in niceRules:
    listItemObject.append(ListItem(Label(rule[0] + rule[1])))
    
# main app
class DisplayFirewall(App):
    CSS_PATH = "./src/show_firewall.css"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            ListView(*listItemObject)
        )

if __name__ == "__main__":
    DisplayFirewall().run()