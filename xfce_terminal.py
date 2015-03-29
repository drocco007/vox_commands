from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, IntegerRef, Choice, Function)
from dragonglue import LinuxAppContext


context = LinuxAppContext(executable='xfce_terminal')
grammar = Grammar('terminal commands', context=context)


a_n = Key('a-%(n)d/5')
c_pgup = Key('c-pgup:%(n)d')
c_pgdown = Key('c-pgdown:%(n)d')

def go_to_tab(n):
    if n <= 9:
        a_n.execute({'n': n})
    else:
        a_n.execute({'n': 9})
        c_pgdown.execute({'n': n - 9})


def go_to_tab_right(n):
    a_n.execute({'n': 1})
    c_pgup.execute({'n': n})


environments = ('asppb', 'NHA', 'brighttrac', 'NASM', 'voice', 'EAS')
remote_targets = {
    'chef': 'chefc',
    'chef cee': 'chefc',
    'staging': 'chefdev3',
}

source_trees = {
    'EAS': '~/source/brightlink/eas/',
    'enviro': '~/source/brightlink/envirocert/',
    'NHA': '~/source/brightlink/nha/',
    'current post': '~/source/posts/stevedore_template_resolver',
    'sandbox': '~/source/sandbox/',
}


command_rule = MappingRule(
    name='terminal commands',
    mapping={
        'new tab': Key('cs-t'),
        'Close tab': Key('cs-w'),
        'entab': Key('c-pgdown'),
        'pretab': Key('c-pgup'),
        'Tab <n>': Function(go_to_tab),
        'Rab <n>': Function(go_to_tab_right),


        'Work on': Text('workon '),
        'Work on <client>': Text('workon %(client)s'),

        'ell ess': Text('ls'),
        'ess cee pee': Text('scp'),
        'pee SQL': Text('psql'),
        'make dir': Text('mkdir'),
        'sublime': Text('subl'),

        'Pseudo- <command>': Text('sudo %(command)s '),
        'Pseudo- ess you <user>': Text('sudo su %(user)s'),


        # Directory navigation

        'cd': Text('cd'),
        'cd pop': Text('cd ../'),
        'cd <source_tree>': Text('cd %(source_tree)s'),
        'Nav <source_tree>': Text('cd %(source_tree)s'),


        # docker

        '(docker | dock)': Text('docker '),
        '(docker | dock) PS': Text('docker ps'),
        '(docker | dock) PS all': Text('docker ps -a'),


        # git

        'git': Text('git '),
        'git all': Text('gitk --all') + Key('enter'),
        'git check out': Text('git checkout ') + Key('tab:2'),
        'git clone': Text('git clone '),
        'git clone clipboard': Text('git clone ') + Key('s-insert'),
        'git commit': Text('git ci'),
        'git commit all': Text('git ci -a'),
        'git merge tool': Text('git mergetool --tool=kdiff3'),
        'git push': Text('git push '),
        'git rebase': Text('git rebase ') + Key('tab:2'),
        'git svn (dcommit|de-commit)': Text('git svn dcommit'),
        'git svn rebase': Text('git svn rebase'),


        # pip

        'pip install': Text('pip install '),


        # Remote

        'connect <remote_target>': Text('ssh %(remote_target)s'),
        'connect Vagrant': Text('vagrant ssh'),
    },
    extras=[           # Special elements in the specs of the mapping.
        Dictation("text"),
        IntegerRef("n", 0, 100),  # Times to repeat the sequence.
        Choice('client', {k:k.lower() for k in environments}),
        Choice('remote_target', remote_targets),
        Choice('source_tree', source_trees),
        Choice('user', {k:k for k in ('postgres', )}),
        Choice('command', {
            'ess you': 'su',
            'Apt get': 'apt-get',
            'Apt get install': 'apt-get install',
        })
    ],
    )

# Add the action rule to the grammar instance.
grammar.add_rule(command_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
