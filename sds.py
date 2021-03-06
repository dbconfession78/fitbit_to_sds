from helper_functions import raise_error
from sds_client import SdsClient
from sds_stream import SdsStream
from sds_type import SdsType
from sds_type_data import SdsTypeData
from sds_type_property import SdsTypeProperty

"""
sds: contains SequentialDataStore class definition
"""


class SequentialDataStore:
    """Class definition for the SDS component of the application"""
    # def __init__(self, config, weather_station):
    def __init__(self, config):
        self.config = config
        self.namespace_id = self.config.get('Configurations', 'Namespace')
        self.lasts = {}
        self.streams = {}
        self.types = {}
        self.client = self.init_client()

    def init_client(self):
        """Initializes SDS Client"""
        client = SdsClient(self.config.get('Access', 'TenantId'),
                           self.config.get('Access', 'Address'),
                           self.config.get('Credentials', 'ClientId'),
                           self.config.get('Credentials', 'ClientSecret'))

        if not client:
            self.raise_error("init_client(): Failed to create SdsClient")
        return client

    def init_type(self, type_id, prop_names):
        """Prepares a new  SdsType object for value population"""
        sds_type = SdsType()
        sds_type.Id = type_id
        sds_type.name = type_id
        sds_type.description = "This is a sample SDS type for storing " \
                               "{} events".format(sds_type.name)

        # Please refer to the following link for an up-to-date listing of
        # type codes when assigning a type code to a new SdsType:
        # osisoft-edge.readthedocs.io/en/latest/Qi_Types.html#sdstypecode
        sds_type.sds_type_code = 1
        sds_type.Properties = []

        double_type = SdsType()
        double_type.Id = 'double_type'
        double_type.sds_type_code = 14

        date_time_type = SdsType()
        date_time_type.Id = "date_time_type"
        date_time_type.sds_type_code = 16

        time_prop = SdsTypeProperty()
        time_prop.Id = 'Time'
        time_prop.SdsType = date_time_type
        time_prop.IsKey = True
        sds_type.Properties.append(time_prop)

        for prop_name in prop_names:
            prop = SdsTypeProperty()
            prop.Id = prop_name
            prop.Name = prop_name
            prop.SdsType = double_type
            sds_type.Properties.append(prop)

        sds_type = self.client.get_or_create_type(self.namespace_id,
                                                  sds_type)
        if not sds_type:
            self.raise_error("init_type() ERROR: Failed to create type")
        self.types[type_id] = sds_type

        return True

    def init_stream(self, type_id, stream_id):
        """Initializes an SdsStream object"""
        sds_stream = SdsStream(stream_id=stream_id, name=stream_id,
                               description="A stream to store {} "
                                           "events".format(type_id),
                               type_id=type_id)
        self.client.create_or_update_stream(self.namespace_id, sds_stream)
        if not sds_stream:
            self.raise_error("init_stream() ERROR: Failed to initialize "
                             "stream")
        self.streams[sds_stream.Id] = sds_stream
        return sds_stream

    # def to_sds(self, device, feed, time_key):
    def to_sds(self, id_prefix, time_key, value):
        """Wrapper for SdsClient's 'update_value' method"""
        # type_id = device.name.lower()
        type_id = id_prefix + "type"
        # type_id = id_prefix + "-Type-" + str(uuid.uuid1())
        stream_id = id_prefix + "stream"
        # stream_id = id_prefix + "-Stream-" + str(uuid.uuid1())
        sds_type = self.types.get(type_id)
        should_setup = False
        if not sds_type:
            type_id = type_id.lower().replace(' ', '_')
            print("Creating SDS Type, '{}'".format(
                type_id))

        metric_names = ["sleep"]
        if self.init_type(type_id, metric_names):
            sds_stream = self.streams.get(stream_id)
            if not sds_stream:
                print("Creating SDS Stream, '{}'".format(stream_id))
                print("---------------------------" + ("-" * len(stream_id) + "--"))
                should_setup = True

            stream = self.init_stream(type_id, stream_id)
            if should_setup:
                    print("SDS Setup complete\n")

            print("-------------------------------" + ("-" * len(stream_id)))
            print("Writing new data to SDS Stream, '{}".format(stream_id))
            print("-------------------------------" + ("-" * len(stream_id)))
            metric_dict = {"sleep": value}
            event = self.next_event(type_id, metric_dict, time_key=time_key)
            if not event:
                self.raise_error("to_sds() ERROR: Failed to create event")
            for k, v in event.__dict__.items():

                if k != "prop_names":
                    if k == "sleep":
                        print("{}: {} hours, {} minutes".format(k, v//60, v % 60))
                    else:
                        print("{}: {}".format(k, v))

            print()
            self.write_single_event_to_sds(event, stream.Id)

    def raise_error(self, message):
        """Wrapper for helper_functions method, 'raise_error'"""
        raise_error(self.client, self.namespace_id,
                    [t.Id for t in self.types],
                    message)

    # TODO: get data from SDS
    # def from_sds(self, start):
    #     """Reads all device events for all locations written to SDS during
    #     current session"""
    #     events_read_from_sds = []
    #     if not self.types and not self.streams:
    #         return events_read_from_sds
    #     for loc in self.ws.locations:
    #         for device in loc.devices:
    #             type_id = device.name
    #             if self.init_type(type_id=type_id,
    #                               prop_names=device.metric_names):
    #                 self.init_stream(type_id)
    #
    #                 value_class = SdsTypeData(type_id=device.name,
    #                                           prop_names=device.metric_names)
    #
    #                 session_events_written = self.client.get_window_values(
    #                     self.namespace_id,
    #                     type_id,
    #                     value_class,
    #                     start=start,
    #                     end=datetime.utcnow()
    #                 )
    #
    #                 if session_events_written:
    #                     events_read_from_sds.append(session_events_written)
    #         return events_read_from_sds

    def write_single_event_to_sds(self, event, stream_id):
        """Writes an 'SdsTypeData' object to SDS"""
        last = self.lasts.get(event.type_id)
        if last is None or last.time != event.time:
            self.lasts[event.type_id] = event
            self.client.update_value(self.namespace_id, stream_id, event)

    def read_last_event_in_sds(self, stream_id, field_names, type_id):
        """Wrapper for SdsClient's 'get_last_value' method"""
        value_type = SdsTypeData(prop_names=field_names, type_id=type_id)
        return self.client.get_last_value(self.namespace_id,
                                          stream_id, value_type)

    @staticmethod
    def next_event(type_id, event_dict, time_key=None):
        """Creates and prepares an 'SdSTypeData' object for transfer to SDS"""
        event = SdsTypeData(type_id=type_id, time=time_key)
        [event.__setattr__(list(event_dict.keys())[i], value)
         for i, value in enumerate(event_dict.values())]
        return event
