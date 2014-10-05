from subprocess import Popen, PIPE

import natlink
from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, Function, Mimic,
                       StartApp, IntegerRef)


# import quickfiles2

def qf():
    # focus problems
    Popen([r"C:\Python27_x86\pythonw.exe", "C:\\Python27_x86\\Scripts\\quickfiles2-script.py"])

    # print 'quickfiles'
    # output=Popen(r"C:\Python27_x86\pythonw.exe C:\\Python27_x86\\Scripts\\quickfiles2-script.py", shell=True, creationflags=0x08000000(), stdout=PIPE, stderr=PIPE)
    # print output.stdout.read()
    # print output.stderr.read()

    # focus problems
    # Popen('C:\\Python27_x86\\Scripts\\quickfiles2.exe', creationflags=0x08000000)

    # shows a console window
    # Popen('C:\\Python27_x86\\Scripts\\quickfiles2.exe')

    # locks dragon
    # quickfiles2.main()



grammar = Grammar("global")


def snore(**kw):
    natlink.setMicState('sleeping')


example_rule = MappingRule(
    name="global",    # The name of the rule.
    mapping={
        'scratch': Mimic('scratch', 'that'),

        'Pick <n>': Key('down/5:%(n)d, enter'),
        'Pick Minus <n>': Key('up/5:%(n)d, enter'),
        'swap': Key('w-tab/5'),
        '<n> swap': Key('w-tab/5:%(n)d'),
        'swap <text>': FocusWindow(title='%(text)s'),
        'win left': Key('w-left'),
        'win right': Key('w-right'),
        'desk <n>': Key('cas-f%(n)d'),

        'snore': Function(snore),

        'quick files': Function(qf),
        'quick files <n>': StartApp(r"C:\Python27\pythonw.exe", r"C:\documents\voice\quick_files.py %(n)d"),

        'Show task [manager]': Key('cs-escape'),
            # "": Key("c-p"),
            #  "save [file]":            Key("c-s"),
            #  "save [file] as":         Key("a-f, a"),
            #  "save [file] as <text>":  Key("a-f, a/20") + Text("%(text)s"),
            # find something scratch "find <text>":            Key("c-f/20") + Text("%(text)s\n"),
            #


        #
        # Words and phrases

        'import clarus': Text('import brighttrac2 as clarus'),
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
