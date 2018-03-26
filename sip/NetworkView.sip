%Module(name=NetworkView, call_super_init=True, keyword_arguments="Optional")
%DefaultMetatype PyQt5.QtCore.pyqtWrapperType
%DefaultSupertype sip.simplewrapper
%Include Node.sip
%Include Edge.sip
%Include NetworkScene.sip