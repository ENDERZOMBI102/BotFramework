import sys
from importlib import _bootstrap  # type: ignore[attr-defined]
from types import ModuleType
from typing import Dict

from botframework.eventSystem import EventSystem

_RELOADING: dict[ str, ModuleType ] = {}


def reload(module: ModuleType, additionalSearchDict: Dict[str, ModuleType] = None) -> ModuleType | None:
	'''
	Reload the module and return it.

	The module must have been successfully imported before.

	:param module: The module to reload
	:param additionalSearchDict: An additional search path to use alongside sys.modules
	:return: The module
	'''
	if not module or not isinstance(module, ModuleType):
		raise TypeError('module argument must be a ModuleType instance')

	name = getattr( module.__spec__, 'name', module.__name__ )

	if additionalSearchDict is None:
		additionalSearchDict = {}

	useCustom = module in additionalSearchDict.values()

	if useCustom:
		if additionalSearchDict.get(name) is not module:
			raise ImportError(f'module {name} not found in sys.modules or in additional search dict', name=name)
	else:
		if sys.modules.get(name) is not module:
			raise ImportError(f'module {name} not found in sys.modules or in additional search dict', name=name)

	# remove all events listeners of this module
	EventSystem.INSTANCE.removeListeners(name)

	if name in _RELOADING:
		return _RELOADING[name]
	_RELOADING[name] = module
	try:
		parent_name = name.rpartition('.')[0]
		if parent_name:
			try:
				parent = additionalSearchDict[parent_name]
			except KeyError:
				try:
					parent = sys.modules[parent_name]
				except KeyError:
					msg = 'parent {!r} not in sys.modules nor in additional search dict'
					raise ImportError( msg.format(parent_name), name=parent_name ) from None
				else:
					pkgpath = parent.__path__  # type: ignore
			else:
				pkgpath = parent.__path__  # type: ignore
		else:
			pkgpath = None
		target = module
		spec = module.__spec__ = _bootstrap._find_spec(name, pkgpath, target)
		if spec is None:
			raise ModuleNotFoundError( f'spec not found for the module {name!r}', name=name )
		_bootstrap._exec(spec, module)
		# The module may have replaced itself in sys.modules!
		return additionalSearchDict[name] if useCustom else sys.modules[name]
	finally:
		try:
			del _RELOADING[name]
		except KeyError:
			pass
