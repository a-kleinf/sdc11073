import os
from lxml import etree as etree_
from .namespaces import Prefix_Namespace as Prefix
from .definitions_base import SchemaResolverBase
from .definitions_base import BaseDefinitions
from .mdib import descriptorcontainers as dc_final
from .mdib import statecontainers as sc_final

schemaFolder = os.path.join(os.path.dirname(__file__), 'xsd')

class _SchemaResolver(SchemaResolverBase):
    lookup_ext = {
            'http://standards.ieee.org/downloads/11073/11073-10207-2017/BICEPS_ParticipantModel.xsd': 'ParticipantModelSchemaFile',
            'http://standards.ieee.org/downloads/11073/11073-10207-2017/BICEPS_MessageModel.xsd': 'MessageModelSchemaFile',
            'http://standards.ieee.org/downloads/11073/11073-10207-2017/ExtensionPoint.xsd': 'ExtensionPointSchemaFile', }

# the following namespace definitions reflect the initial SDC standard.
# There might be changes or additions in the future, who knows...
#

_DPWS_SDCNamespace = 'http://standards.ieee.org/downloads/11073/11073-20701-2018'
_ActionsNamespace = _DPWS_SDCNamespace

class _SDC_v1_Actions(object):
    OperationInvokedReport = _ActionsNamespace + '/SetService/OperationInvokedReport'
    SetOperationInvokedReport = _ActionsNamespace + '/SetService/OperationInvokedReport'
    ContextOperationInvokedReport =  _ActionsNamespace + '/ContextService/OperationInvokedReport'
    EpisodicContextReport = _ActionsNamespace + '/ContextService/EpisodicContextReport'
    EpisodicMetricReport = _ActionsNamespace + '/StateEventService/EpisodicMetricReport'
    EpisodicOperationalStateReport = _ActionsNamespace + '/StateEventService/EpisodicOperationalStateReport'
    EpisodicAlertReport = _ActionsNamespace + '/StateEventService/EpisodicAlertReport'
    EpisodicComponentReport = _ActionsNamespace + '/StateEventService/EpisodicComponentReport'
    PeriodicContextReport = _ActionsNamespace + '/ContextService/PeriodicContextReport'
    PeriodicMetricReport = _ActionsNamespace + '/StateEventService/PeriodicMetricReport'
    PeriodicOperationalStateReport = _ActionsNamespace + '/StateEventService/PeriodicOperationalStateReport'
    PeriodicAlertReport = _ActionsNamespace + '/StateEventService/PeriodicAlertReport'
    PeriodicComponentReport = _ActionsNamespace + '/StateEventService/PeriodicComponentReport'
    SystemErrorReport = _ActionsNamespace + '/StateEventService/SystemErrorReport'
    Waveform = _ActionsNamespace + '/WaveformService/WaveformStream'
    DescriptionModificationReport = _ActionsNamespace + '/DescriptionEventService/DescriptionModificationReport'
    GetMdib = _ActionsNamespace + '/GetService/GetMdib'
    GetMdibResponse = _ActionsNamespace + '/GetService/GetMdibResponse'
    GetMdState = _ActionsNamespace + '/GetService/GetMdState'
    GetMdStateResponse = _ActionsNamespace + '/GetService/GetMdStateResponse'
    GetMdDescription = _ActionsNamespace + '/GetService/GetMdDescription'
    GetMdDescriptionResponse = _ActionsNamespace + '/GetService/GetMdDescriptionResponse'
    GetContainmentTree = _ActionsNamespace + '/GetService/GetContainmentTree'
    GetContainmentTreeResponse = _ActionsNamespace + '/GetService/GetContainmentTreeResponse'
    GetContextStates = _ActionsNamespace + '/ContextService/GetContextStates'
    GetContextStatesResponse = _ActionsNamespace + '/ContextService/GetContextStatesResponse'
    GetContextStatesByIdentification = _ActionsNamespace + '/ContextService/GetContextStatesByIdentification'
    GetContextStatesByIdentificationResponse = _ActionsNamespace + '/ContextService/GetContextStatesByIdentificationResponse'
    SetContextState = _ActionsNamespace + '/ContextService/SetContextState'
    SetContextStateResponse = _ActionsNamespace + '/ContextService/SetContextStateResponse'
    GetSupportedLanguages = _ActionsNamespace + '/LocalizationService/GetSupportedLanguages'
    GetSupportedLanguagesResponse = _ActionsNamespace + '/LocalizationService/GetSupportedLanguagesResponse'
    GetLocalizedText = _ActionsNamespace + '/LocalizationService/GetLocalizedText'
    GetLocalizedTextResponse = _ActionsNamespace + '/LocalizationService/GetLocalizedTextResponse'
    Activate = _ActionsNamespace + '/SetService/Activate'
    ActivateResponse = _ActionsNamespace + '/SetService/ActivateResponse'
    SetString = _ActionsNamespace + '/SetService/SetString'
    SetStringResponse = _ActionsNamespace + '/SetService/SetStringResponse'
    SetValue = _ActionsNamespace + '/SetService/SetValue'
    SetValueResponse = _ActionsNamespace + '/SetService/SetValueResponse'
    SetAlertState = _ActionsNamespace + '/SetService/SetAlertState'
    SetAlertStateResponse = _ActionsNamespace + '/SetService/SetAlertStateResponse'
    SetMetricState = _ActionsNamespace + '/SetService/SetMetricState'
    SetMetricStateResponse = _ActionsNamespace + '/SetService/SetMetricStateResponse'
    SetComponentState = _ActionsNamespace + '/SetService/SetComponentState'
    SetComponentStateResponse = _ActionsNamespace + '/SetService/SetComponentStateResponse'
    GetDescriptor = _ActionsNamespace + '/ContainmentTreeService/GetDescriptor'
    GetDescriptorResponse = _ActionsNamespace + '/ContainmentTreeService/GetDescriptorResponse'
    GetContainmentTree = _ActionsNamespace + '/ContainmentTreeService/GetContainmentTree'
    GetContainmentTreeResponse = _ActionsNamespace + '/ContainmentTreeService/GetContainmentTreeResponse'
    SubscriptionEnd = Prefix.WSE.namespace + '/SubscriptionEnd'



class SDC_v1_Definitions(BaseDefinitions):
    BICEPSNamespace_base = 'http://standards.ieee.org/downloads/11073/11073-10207-2017/'
    BICEPSNamespace = 'http://standards.ieee.org/downloads/11073/11073-10207-2017/SP'
    DPWS_SDCNamespace = _DPWS_SDCNamespace#'http://standards.ieee.org/downloads/11073/11073-20701-2018'
    MedicalDeviceTypeNamespace = 'http://standards.ieee.org/downloads/11073/11073-20702-2016'
    MessageModelNamespace = 'http://standards.ieee.org/downloads/11073/11073-10207-2017/message'
    ParticipantModelNamespace = 'http://standards.ieee.org/downloads/11073/11073-10207-2017/participant'
    ExtensionPointNamespace = 'http://standards.ieee.org/downloads/11073/11073-10207-2017/extension'
    MDPWSNameSpace = 'http://standards.ieee.org/downloads/11073/11073-20702-2016' # this name changed between WPF and SDC! IEEE correction
    MedicalDeviceType = etree_.QName(MedicalDeviceTypeNamespace, 'MedicalDevice')
    SDCDeviceType = etree_.QName(DPWS_SDCNamespace, 'SdcDevice')
    MessageModelSchemaFile = os.path.join(schemaFolder, 'BICEPS_MessageModel.xsd')
    ParticipantModelSchemaFile = os.path.join(schemaFolder, 'BICEPS_ParticipantModel.xsd')
    ExtensionPointSchemaFile = os.path.join(schemaFolder, 'ExtensionPoint.xsd')
    ActionsNamespace = DPWS_SDCNamespace
    PortTypeNamespace = DPWS_SDCNamespace

    MedicalDeviceTypesFilter = [BaseDefinitions.DpwsDeviceType, MedicalDeviceType]
    sc = sc_final
    dc = dc_final
    Actions = _SDC_v1_Actions
SDC_v1_Definitions.schemaResolver = _SchemaResolver(SDC_v1_Definitions)
