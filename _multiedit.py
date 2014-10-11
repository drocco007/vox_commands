import os

from dragonfly import *
from dragonglue import LinuxAppContext
import natlink


release = Key("shift:up, ctrl:up")


def config_factory(name='multi edit'):
    config = Config(name)
    config.cmd = Section("Language section")
    config.cmd.map = Item({},
        namespace={
            "Key": Key,
            "Text": Text,
            # 'Text': lambda x: Mimic([x])
        }
    )

    return config

config = config_factory()
namespace = config.load()

#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file.
#  Each of these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
        if name.startswith("format_") and callable(function):
            spoken_form = function.__doc__.strip()

            # We wrap generation of the Function action in a function so
            #  that its *function* variable will be local.  Otherwise it
            #  would change during the next iteration of the namespace loop.
            def wrap_function(function):
                def _function(dictation):
                    formatted_text = function(dictation)
                    # Text(formatted_text).execute()
                    # Mimic(formatted_text).execute()
                    # natlink.playString(formatted_text)
                    Paste(formatted_text).execute()

                return Function(_function)

            action = wrap_function(function)
            format_functions[spoken_form] = action


# Here we define the text formatting rule.
# The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions:
    class FormatRule(MappingRule):

        mapping = format_functions
        extras = [Dictation("dictation")]

else:
    FormatRule = None


#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these
#  include special elements like the number with name "n"
#  or the dictation with name "text".  This rule is not
#  exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its "value" when
#  processing a recognition will be the right side of the
#  mapping: an action.
# Note that this rule does not execute these actions, it
#  simply returns them when it's value() method is called.
#  For example "up 4" will give the value Key("up:4").
# More information about Key() actions can be found here:
#  http://dragonfly.googlecode.com/svn/trunk/dragonfly/documentation/actionkey.html
class KeystrokeRule(MappingRule):
    exported = False

    mapping = config.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        IntegerRef("n2", 1, 100),
        IntegerRef("digit", 1, 10),
        IntegerRef("digit2", 1, 10),
        Dictation("text"),
        Dictation("text2"),
        Choice('extension', {
            'text': 'txt',
            'yaml': 'yaml'
        })
    ]
    defaults = {
        "n": 1,
    }
    # Note: when processing a recognition, the *value* of
    #  this rule will be an action object from the right side
    #  of the mapping given above.  This is default behavior
    #  of the MappingRule class' value() method.  It also
    #  substitutes any "%(...)." within the action spec
    #  with the appropriate spoken values.


#---------------------------------------------------------------------------
# Here we create an element which is the sequence of keystrokes.

# First we create an element that references the keystroke rule.
#  Note: when processing a recognition, the *value* of this element
#  will be the value of the referenced rule: an action.
alternatives = [RuleRef(rule=KeystrokeRule())]
if FormatRule:
    alternatives.append(RuleRef(rule=FormatRule()))
single_action = Alternative(alternatives)

# Second we create a repetition of keystroke elements.
#  This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element
#  the name "sequence" so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element
#  will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name="sequence")


def create_sequence(name=None, mapping=None, extras=None, defaults=None, context=None, exported=None):
    alternatives = [RuleRef(rule=KeystrokeRule(name='{}_keys'.format(name), mapping=mapping, extras=extras, defaults=defaults, context=context, exported=exported))]
    if FormatRule:
        alternatives.append(RuleRef(rule=FormatRule(name='{}_format'.format(name))))
    single_action = Alternative(alternatives)

    return Repetition(single_action, min=1, max=16, name="sequence")


#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

# This is the rule that actually handles recognitions.
#  When a recognition occurs, it's _process_recognition()
#  method will be called.  It receives information about the
#  recognition in the "extras" argument: the sequence of
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence, # Sequence of actions defined above.
        IntegerRef("n", 1, 100), # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1, # Default repeat count.
    }

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    #     . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
        # Mimic('\\no-caps-on').execute()

        sequence = extras["sequence"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):
            for action in sequence:
                action.execute()

        release.execute()

        # Mimic('\\no-caps-on', '\\no-space-on').execute()
        # Mimic('\\no-caps-on').execute()

#---------------------------------------------------------------------------
# Create and load this module's grammar.

class MultiContextGrammar(Grammar):
    def __init__(self, name):
        super(MultiContextGrammar, self).__init__(name)

        self.find_rules()
        self.load_rules()
        self.init_rules()

    def find_rules(self):
        editing_rules = os.path.join(os.path.dirname(__file__), 'editing_rules')
        self.editing_rules = [os.path.join(editing_rules, filename) for filename in os.listdir(editing_rules)]
        # print self.editing_rules

    def load_rules(self):
        self.base = config

        self.rule_definitions = {}

        for rule_filename in self.editing_rules:
            program = os.path.splitext(os.path.basename(rule_filename))[0]
            _config = config_factory(program)
            _config.load(rule_filename)
            object.__setattr__(_config, 'module_path', config.module_path)
            self.rule_definitions[program] = _config

    def init_rules(self):
        base_context = None

        for stem, config in self.rule_definitions.iteritems():
            command_mapping = self.base.cmd.map.copy()
            command_mapping.update(config.cmd.map)
            context = LinuxAppContext(executable=stem)
            sequence = create_sequence(name=stem, mapping=command_mapping)
            rule = RepeatRule(name=stem, extras=[sequence, IntegerRef("n", 1, 100)], context=context)

            self.add_rule(rule)

            if base_context:
                base_context |= ~context
            else:
                base_context = ~context

        self.add_rule(RepeatRule('base', context=base_context))

    # def _process_begin(self, executable, title, handle):
    #     print self.rule_definitions.keys()
    #
    #     for stem, config in self.rule_definitions.iteritems():
    #         if stem in executable:
    #             print 'match', stem, '->', executable
    #             break
    #     else:
    #         print 'no match for', executable


grammar = MultiContextGrammar("multi edit")   # Create this module's grammar.
grammar.load()                    # Load the grammar.

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
