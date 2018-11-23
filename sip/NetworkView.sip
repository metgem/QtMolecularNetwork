%Module(name=NetworkView, call_super_init=True, keyword_arguments="Optional")
%DefaultSupertype sip.simplewrapper
%Include config.sip
%Include Node.sip
%Include Edge.sip
%Include Style.sip
%Include NetworkScene.sip