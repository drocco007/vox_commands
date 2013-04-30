import natlink
from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, Function, Mimic,
                       StartApp, IntegerRef)


grammar = Grammar("global")


def snore(**kw):
    natlink.setMicState('sleeping')


example_rule = MappingRule(
    name="global",    # The name of the rule.
    mapping={
        'scratch': Mimic('scratch', 'that'),

        'Pick <n>': Key('down/5:%(n)d, enter'),
        'Pick Minus <n>': Key('up/5:%(n)d, enter'),
        'swap': Key('a-tab/5'),
        'swap <text>': FocusWindow(title='%(text)s'),
        'win left': Key('w-left'),
        'win right': Key('w-right'),

        'snore': Function(snore),


        'Do run': Key('w-r'),
        'quick files': StartApp(r"C:\Python27\pythonw.exe", r"C:\documents\voice\quick_files.py"),
        'quick files <n>': StartApp(r"C:\Python27\pythonw.exe", r"C:\documents\voice\quick_files.py %(n)d"),
            # "": Key("c-p"),
            #  "save [file]":            Key("c-s"),
            #  "save [file] as":         Key("a-f, a"),
            #  "save [file] as <text>":  Key("a-f, a/20") + Text("%(text)s"),
            # find something scratch "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
            },
    extras=[           # Special elements in the specs of the mapping.
            Dictation("text"),
                    IntegerRef("n", 1, 100),  # Times to repeat the sequence.

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
