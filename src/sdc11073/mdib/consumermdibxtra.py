"""Extra methods for consumer mdib."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sdc11073 import observableproperties as properties

if TYPE_CHECKING:
    from sdc11073.loghelper import LoggerAdapter
    from sdc11073.pysoap.msgreader import ReceivedMessage

    from .consumermdib import ConsumerMdib
    from .statecontainers import AbstractStateProtocol


class ConsumerMdibMethods:
    """Extra methods for consumer mdib tht are not core functionality."""

    def __init__(self, consumer_mdib: ConsumerMdib, logger: LoggerAdapter):
        self._mdib = consumer_mdib
        self._sdc_client = consumer_mdib.sdc_client
        self._logger = logger

    def mk_proposed_state(self, descriptor_handle: str,
                          copy_current_state: bool = True,
                          handle: str | None = None) -> AbstractStateProtocol:
        """Create a new state that can be used as proposed state in according operations.

        The new state is not part of mdib!.

        :param descriptor_handle: the descriptor
        :param copy_current_state: if True, all members of existing state will be copied to new state
        :param handle: if this is a multi state class, and the handle is not None,
                      this is the handle of the existing state that shall be used for copy.
        :return: a new state container
        """
        descr = self._mdib.descriptions.handle.get_one(descriptor_handle)
        new_state = self._mdib.data_model.mk_state_container(descr)
        if copy_current_state:
            lookup = self._mdib.context_states if new_state.is_context_state else self._mdib.states
            if new_state.is_multi_state:
                if handle is None:  # new state
                    return new_state
                old_state = lookup.handle.get_one(handle)
            else:
                old_state = lookup.descriptor_handle.get_one(descriptor_handle)
            new_state.update_from_other_container(old_state)
        return new_state

    def sync_context_states(self):
        """Sync context states with provider.

        Requests all context states from device and deletes all local context states that are not
        available in response from Device.
        """
        self._logger.info('_sync_context_states called')
        context_service = self._sdc_client.client('Context')
        response = context_service.get_context_states()
        context_state_containers = response.result.ContextState

        devices_context_state_handles = [s.Handle for s in context_state_containers]
        with self._mdib.context_states.lock:
            for obj in self._mdib.context_states.objects:
                if obj.Handle not in devices_context_state_handles:
                    self._mdib.context_states.remove_object_no_lock(obj)

    def bind_to_client_observables(self):
        """Connect the mdib with the notifications from consumer."""
        properties.bind(self._sdc_client, waveform_report=self._on_waveform_report)
        properties.bind(self._sdc_client, episodic_metric_report=self._on_episodic_metric_report)
        properties.bind(self._sdc_client, episodic_alert_report=self._on_episodic_alert_report)
        properties.bind(self._sdc_client, episodic_context_report=self._on_episodic_context_report)
        properties.bind(self._sdc_client, episodic_component_report=self._on_episodic_component_report)
        properties.bind(self._sdc_client, description_modification_report=self._on_description_modification_report)
        properties.bind(self._sdc_client, episodic_operational_state_report=self._on_operational_state_report)

    def _on_episodic_metric_report(self, received_message_data: ReceivedMessage):
        cls = self._mdib.data_model.msg_types.EpisodicMetricReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_metric_states_report(received_message_data.mdib_version_group, report)

    def _on_episodic_alert_report(self, received_message_data: ReceivedMessage):
        cls = self._mdib.data_model.msg_types.EpisodicAlertReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_alert_states_report(received_message_data.mdib_version_group, report)

    def _on_operational_state_report(self, received_message_data: ReceivedMessage):
        cls = self._mdib.data_model.msg_types.EpisodicOperationalStateReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_operational_states_report(received_message_data.mdib_version_group, report)

    def _on_waveform_report(self, received_message_data: ReceivedMessage):
        """Handle waveform report."""
        cls = self._mdib.data_model.msg_types.WaveformStream
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_waveform_states(received_message_data.mdib_version_group, report.State)

    def _on_episodic_context_report(self, received_message_data: ReceivedMessage):
        """Handle episodic context report."""
        cls = self._mdib.data_model.msg_types.EpisodicContextReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_context_states_report(received_message_data.mdib_version_group, report)

    def _on_episodic_component_report(self, received_message_data: ReceivedMessage):
        """Handle episodic component report.

        The EpisodicComponentReport is sent if at least one property of at least one component state has changed
        and SHOULD contain only the changed component states.
        Components are MDSs, VMDs, Channels. Not metrics and alarms.
        """
        cls = self._mdib.data_model.msg_types.EpisodicComponentReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_component_states_report(received_message_data.mdib_version_group, report)

    def _on_description_modification_report(self, received_message_data: ReceivedMessage):
        """Handle description modification report.

        The EpisodicComponentReport is sent if at least one property of at least one component state has changed
        and SHOULD contain only the changed component states.
        Components are MDSs, VMDs, Channels. Not metrics and alarms.
        """
        cls = self._mdib.data_model.msg_types.DescriptionModificationReport
        report = cls.from_node(received_message_data.p_msg.msg_node)
        self._mdib.process_incoming_description_modifications(received_message_data.mdib_version_group, report)
