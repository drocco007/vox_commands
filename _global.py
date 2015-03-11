from subprocess import Popen, PIPE

import natlink
from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, Function, Mimic,
                       StartApp, IntegerRef)


grammar = Grammar("global")


def snore(**kw):
    natlink.setMicState('sleeping')


example_rule = MappingRule(
    name="global",
    mapping={
        'scratch': Mimic('scratch', 'that'),

        'Pick <n>': Key('down/5:%(n)d, enter'),
        'Pick Minus <n>': Key('up/5:%(n)d, enter'),
        'swap': Key('w-tab/5'),
        '<n> swap': Key('w-tab/5:%(n)d'),
        'swap <text>': FocusWindow(title='%(text)s'),
        'win left': Key('w-left'),
        'win right': Key('w-right'),
        'desk <n>': Key('w-%(n)d'),

        'snore': Function(snore),

        'Show task [manager]': Key('cs-escape'),


        #
        # Words and phrases

        'import clarus': Text('import brighttrac2 as clarus'),
    },
    extras=[
        Dictation("text"),
            IntegerRef("n", 1, 100),
       ],
    )


# Add the action rule to the grammar instance.
grammar.add_rule(example_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
