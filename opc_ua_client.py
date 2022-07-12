import device
from config import config
from opcua import Client, ua

client = Client(config['OPC_SERVER'])
node_list = []


def get_status():
    try:
        client.connect()
        root = client.get_root_node()
        return root if root else False
    except:
        return False
    finally:
        client.disconnect()


def delete_node_list():
    global node_list
    node_list = []

def update_values():
    delete_node_list()
    try:
        client.connect()
        for node in device.device['data']:
            if node.get('namespace') and node.get('identifier'):
                nd = client.get_node("ns={};i={}".format(node.get('namespace'), node.get('identifier')))
                if nd.get_type_definition():
                    node_list.append({
                        'type':       'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                        'name':       nd.get_display_name().Text,
                        'namespace':  nd.nodeid.NamespaceIndex,
                        'identifier': nd.nodeid.Identifier,
                        'parent':     nd.get_parent().get_display_name().Text,
                        'value':      nd.get_value(),
                    })
                else:
                    node_list.append({
                        'type':       None,
                        'name':       'NODE NOT FOUND...',
                        'namespace':  node.get('namespace'),
                        'identifier': node.get('identifier'),
                        'parent':     None,
                        'value':      None,
                    })
    except:
        return False
    finally:
        client.disconnect()

        # def browse_recursive(node):
        #     for childId in node.get_children():
        #         ch = client.get_node(childId)
        #         # print(level, ch.get_display_name().Text, ch)
        #         if ch.get_node_class() == ua.NodeClass.Object:
        #             object_list.append({
        #                 'type': 'object',
        #                 'name': ch.get_display_name().Text,
        #                 'namespace': str(ch.nodeid.NamespaceIndex),
        #                 'identifier': str(ch.nodeid.Identifier),
        #                 'parent': ch.get_parent().get_display_name().Text,
        #                 'parent_namespace': str(ch.get_parent().nodeid.NamespaceIndex),
        #                 'parent_identifier': str(ch.get_parent().nodeid.Identifier),
        #                  })
        #             # print('OBJECT: ', ch.get_display_name().Text)
        #             browse_recursive(ch)
        #         elif ch.get_node_class() == ua.NodeClass.Variable:
        #
        #             # print(value)
        #             object_list.append({
        #                 'type':       'variable',
        #                 'name':       ch.get_display_name().Text,
        #                 'namespace':  ch.nodeid.NamespaceIndex,
        #                 'identifier': ch.nodeid.Identifier,
        #                 'parent': ch.get_parent().get_display_name().Text,
        #                 'parent_namespace':  str(ch.get_parent().nodeid.NamespaceIndex),
        #                 'parent_identifier': str(ch.get_parent().nodeid.Identifier),
        #                 'value': ch.get_value() if type(ch.get_value()) in [float, str, bool, int] else None
        #             })
                    # print('   |   ', ch.get_display_name().Text, ch.nodeid.NamespaceIndex, ch.nodeid.Identifier, ch.get_value())



                    # if ch.get_display_name().Text in ['Simulation', 'Objects']:
                    #     browse_recursive(ch)
                # elif ch.get_node_class() == ua.NodeClass.Variable:
                #     print(' --| ', "{bn} has value {val}".format(
                #                     bn=ch.get_browse_name(),
                #                     val=str(ch.get_value()))
                #                 )
                # if ch.get_node_class() == ua.NodeClass.Object:
                #     browse_recursive(ch)
                # elif ch.get_node_class() == ua.NodeClass.Variable:
                #     try:
                #         print("{bn} has value {val}".format(
                #             bn=ch.get_browse_name(),
                #             val=str(ch.get_value()))
                #         )
                #     # except ua.uaerrors._auto.BadWaitingForInitialData:
                #     except ua.UaStatusCodeError as e:
                #         print(e)
                        # pass

        # browse_recursive(root)
        # return object_list

        # root = client.get_root_node()
        # print("Objects node is: ", root)
        # objects = client.get_objects_node()
        # print("Objects node is: ", objects)
        # print("Children of root are: ", root.get_children())
        #
        # # for nod in root.get_children():
        # objects = client.get_objects_node()
        # print(objects)
        # print(objects.get_variables())
        # print("childs og objects are: ", objects.get_children())
        # print(objects.get)
        # for n  in client:
        #     print(n.get_variables())
            # for n in nod.get_children():
            #     print()
            #     print(' -- ' + str(n))

        # a = client.get_node("ns=3;i=1007")
        # # print(a)
        # value = a.get_value()
        #
        # # a.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # value = value * 2
        # a.set_value(value) # set node value using implicit data type
        # # print(value)

def read_value(namespace, identifier):
    try:
        client.connect()
        nd = client.get_node("ns={};i={}".format(namespace, identifier))
        if nd.get_type_definition():
            return {
                'type': 'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                'name': nd.get_display_name().Text,
                'namespace': nd.nodeid.NamespaceIndex,
                'identifier': nd.nodeid.Identifier,
                'parent': nd.get_parent().get_display_name().Text,
                'value': nd.get_value(),
            }
    except:
        return False
    finally:
        client.disconnect()


def write_value(namespace, identifier, value):
    try:
        client.connect()
        nd = client.get_node("ns={};i={}".format(namespace, identifier))
        if nd.get_type_definition():
            variant_type = nd.get_data_type_as_variant_type()
            if variant_type == ua.VariantType.Boolean:
                nd.set_value(False if value == 'False' or value == '0' else True)
            elif variant_type == ua.VariantType.String:
                nd.set_value(str(value))
            elif variant_type in (ua.VariantType.Float, ua.VariantType.Double):
                nd.set_value(float(value))
            elif variant_type in (ua.VariantType.Int32, ua.VariantType.Int16, ua.VariantType.Int64):
                nd.set_value(int(value))
            return {
                'type': 'object' if nd.get_node_class() == ua.NodeClass.Object else 'variable',
                'name': nd.get_display_name().Text,
                'namespace': nd.nodeid.NamespaceIndex,
                'identifier': nd.nodeid.Identifier,
                'parent': nd.get_parent().get_display_name().Text,
                'value': nd.get_value(),
            }
    except Exception as e:
        print(e)
        return False
    finally:
        client.disconnect()
