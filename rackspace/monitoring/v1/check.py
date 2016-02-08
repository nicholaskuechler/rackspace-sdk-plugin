# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import format
from openstack import resource
from openstack import utils
from rackspace.monitoring import monitoring_service


class Check(resource.Resource):
    base_path = '/entities/%(entity_id)s/checks'
    resources_key = 'values'
    service = monitoring_service.MonitoringService()

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_retrieve = True
    allow_update = True

    # Properties
    #: List of active suppressions. *Type: list*
    active_suppressions = resource.prop('active_suppressions', type=list)
    #: Creation timestamp.
    #: Time is shown in Coordinated Universal Time (UTC) as the number
    #: of milliseconds that have elapsed since January 1, 1970. *Type: int*
    created_at = resource.prop('created_at', type=int)
    #: Details specific to the check. *Type: dict*
    details = resource.prop('details', type=dict)
    #: The ID of the entity
    entity_id = resource.prop('entity_id')
    #: The period in seconds for a check. The value must be greater than
    #: the minimum period set on your account. *Type: int*
    frequency = resource.prop('period', type=int)
    #: Disables the check. *Type: bool*
    is_disabled = resource.prop('disabled', type=format.BoolStr)
    #: Arbitrary key/value pairs. *Type: dict*
    metadata = resource.prop('metadata', type=dict)
    #: List of monitoring zones to poll from. *Type: list*
    #: Note: This argument is only required for remote (non-agent) checks.
    monitoring_zones = resource.prop('monitoring_zones_poll', type=list)
    #: A friendly label for a check
    name = resource.prop('label')
    #: List of scheduled suppressions. *Type: list*
    scheduled_suppressions = resource.prop('scheduled_suppressions', type=list)
    #: A key in the entity's ip_addresses hash used to resolve this check to
    #: an IP address. Mutually exclusive with `target_hostname`.
    target_alias = resource.prop('target_alias')
    #: The hostname this check should target.
    #: Mutually exclusive with `target_alias`.
    target_hostname = resource.prop('target_hostname')
    #: Determines how to resolve the check target.
    target_resolver = resource.prop('target_resolver')
    #: The timeout in seconds for a check.
    #: This has to be less than the frequency. *Type: int*
    timeout = resource.prop('timeout', type=int)
    #: The type of check
    type_id = resource.prop('type')
    #: Update timestamp.
    #: Time is shown in Coordinated Universal Time (UTC) as the number
    #: of milliseconds that have elapsed since January 1, 1970. *Type: int*
    updated_at = resource.prop('updated_at', type=int)

    def metrics(self, session):
        """List metrics for the check

        This operation returns a response body that lists the metrics
        associated with your check. A single check usually generates several
        metrics. For example, http checks generate the following metrics:
        `bytes`, `code`, `duration`, `truncated`, `tt_connect`, `tt_firstbyte`.

        Metrics generated by remote checks are generated for each
        monitoring zone where the check is issued.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :returns: ``list``
        """
        url = utils.urljoin(
            'entities', self.entity_id, 'checks', self.id, 'metrics')
        resp = session.get(url, endpoint_filter=self.service).json()
        return resp['values']

    def test(self, session):
        """Test an existing check

        This operation does NOT cause the already-created check to be run,
        but rather creates a duplicate check with the same parameters as the
        original, and performs the test using that. You can copy the results of
        a test check response and paste it directly into a test alarm.

        :param session: The session to use for making this request.
        :type session: :class:`~openstack.session.Session`
        :returns: ``list``
        """
        url = utils.urljoin(
            'entities', self.entity_id, 'checks', self.id, 'test')
        resp = session.get(url, endpoint_filter=self.service).json()
        return resp
