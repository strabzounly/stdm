from stdm.settings.registryconfig import QGISRegistryConfig
from .exceptions import TranslatorException
from .reader import OGRReader
from .writer import OGRWriter
from .value_translators import (
    MultipleEnumerationTranslator,
    SourceValueTranslator,
    ValueTranslatorManager,
    RelatedTableTranslator
)

_UIGroup = "UI"
_lastVectorDirKey = "lastVectorFileFilterDir"
_lastUploadDirKey = "lastUploadFilterDir"

def vectorFileDir():
    """
    Returns the directory of the last vector file accessed by QGIS.
    """
    qgisReg = QGISRegistryConfig(_UIGroup)
    regValues = qgisReg.read([_lastVectorDirKey])
    
    if len(regValues) == 0:
        return ""
    else:
        return regValues[_lastVectorDirKey]
    
def setVectorFileDir(dir):
    """
    Update the last vector file directory.
    """
    qgisReg = QGISRegistryConfig(_UIGroup)
    qgisReg.write({_lastVectorDirKey:dir})

def uploadFileDir():
    """
    Returns the directory of the last vector file accessed by QGIS.
    """
    qgisReg = QGISRegistryConfig(_UIGroup)
    regValues = qgisReg.read([_lastUploadDirKey])
    
    if len(regValues) == 0:
        return ""
    else:
        return regValues[_lastUploadDirKey]
    
def setUploadFileDir(dir):
    """
    Update the last vector file directory.
    """
    qgisReg = QGISRegistryConfig(_UIGroup)
    qgisReg.write({_lastUploadDirKey:dir})
    
