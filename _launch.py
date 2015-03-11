from dragonfly import (Grammar, MappingRule, Choice, Text, Key, Function)
from dragonglue.command import send_command

grammar = Grammar("launch")


applications = {
	'sublime': 'w-s',
    'pycharm': 'w-d',
    'chrome': 'w-f',
    'logs': 'w-j',
    'SQL': 'w-k',
    'IPython': 'w-l',
    'shell': 'w-semicolon',
    'terminal': 'w-a',
    # 'spotify': 'spotify /home/dan/bin/spotify',
}

# aliases
applications['charm'] = applications['pycharm']
applications['termie'] = applications['terminal']


def Command(cmd):
    def ex(application=''):
        # print 'execute', cmd + application
        send_command(cmd + application)

    return Function(ex)


launch_rule = MappingRule(
    name="launch",
    mapping={
        'Do run': Key('w-x'),

        'get <application>': Key('%(application)s'),
        # 're-browse': Key('w-F'),

        'voice sync': Command('subl --command voice_sync'),

        '(touch | refresh) multi-edit': Command('touch /home/drocco/source/voice/natlink/commands/_multiedit.py'),
    },
    extras=[
    	Choice('application', applications)
    ]
)

grammar.add_rule(launch_rule)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
