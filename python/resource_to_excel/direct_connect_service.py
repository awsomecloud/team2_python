class direct_connect:
    def __init__(self, directconnect_service):
        self.dx = directconnect_service
        self.type = 0

    def dx_describe_connections(self):
        connection_list = self.dx.describe_connections()
        #print('connection_list 정보')
        #print(connection_list)

        result = []
        for connection_info in connection_list.get('connections'):
            name = connection_info.get('connectionName')
            conn_id = connection_info.get('connectionId')
            region = connection_info.get('region')

            if connection_info.get('location') == 'LGU57':
                location = 'LG U+ Pyeong-Chon Mega Center, Seoul, KOR'
            else:
                location = connection_info.get('location')

            bandwidth = connection_info.get('bandwidth')
            state = connection_info.get('connectionState')

            result.append((name, conn_id, region, location, bandwidth, state))

        return result

    def dx_describe_virtual_interface(self):
        vi_list = self.dx.describe_virtual_interfaces()
        #print('vi_list 정보')
        #print(vi_list)
        result = []
        for vi_info in vi_list.get('virtualInterfaces'):
            vi_name = vi_info.get('virtualInterfaceName')
            vi_id = vi_info.get('virtualInterfaceId')
            region = vi_info.get('region')
            connection_id = vi_info.get('connectionId')
            vlan = vi_info.get('vlan')
            vi_type = vi_info.get('virtualInterfaceType')
            vi_state = vi_info.get('virtualInterfaceState')

            result.append((vi_name, vi_id, region, connection_id, vlan, vi_type, vi_state))

        return result

    def dx_describe_gateways(self):
        gateway_list = self.dx.describe_direct_connect_gateways()
        #print('gateway_list 정보')
        #print(gateway_list)
        result = []
        for gateway_info in gateway_list.get('directConnectGateways'):

            name = gateway_info.get('directConnectGatewayName')
            id = gateway_info.get('directConnectGatewayId')
            account_num = gateway_info.get('ownerAccount')
            asn = gateway_info.get('amazonSideAsn')
            state = gateway_info.get('directConnectGatewayState')

            result.append((name, id, account_num, asn, state))

        return result, gateway_list.get('directConnectGateways')

    def dx_describe_virtual_interface_attachments(self, gw_list):

        result = []
        for gw_info in gw_list:
            attach_list = self.dx.describe_direct_connect_gateway_attachments(directConnectGatewayId=gw_info.get('directConnectGatewayId'))
            #print('attach_list 정보')
            #print(attach_list)
            for attach_info in attach_list.get('directConnectGatewayAttachments'):
                gw_name = gw_info.get('directConnectGatewayName')
                gw_id = gw_info.get('directConnectGatewayId')
                vi_id = attach_info.get('virtualInterfaceId')
                region = attach_info.get('virtualInterfaceRegion')
                account_num = attach_info.get('virtualInterfaceOwnerAccount')
                type = attach_info.get('attachmentType')
                state = attach_info.get('attachmentState')

                result.append((gw_name, gw_id, vi_id, region, account_num, type, state))

        return result

    def dx_describe_gateway_association(self, gw_list):
        #assoc_list = self.dx.describe_direct_connect_gateway_associations(directConnectGatewayId='string')
        #print('assoc_list 정보')
        #print(assoc_list)

        result = []
        for gw_info in gw_list:
            assoc_list = self.dx.describe_direct_connect_gateway_associations(directConnectGatewayId=gw_info.get('directConnectGatewayId'))
            print('attach_list 정보')
            print(assoc_list)
            for assoc_info in assoc_list.get('directConnectGatewayAssociations'):
                assoc_detail = assoc_info.get('associatedGateway')

                gw_name = gw_info.get('directConnectGatewayName')
                gw_id = gw_info.get('directConnectGatewayId')

                assoc_id = assoc_detail.get('id')
                region = assoc_detail.get('region')
                account = assoc_detail.get('ownerAccount')

                allow_pre_list = ''
                for allow_pre_info in assoc_info.get('allowedPrefixesToDirectConnectGateway'):
                    cidr_info = allow_pre_info.get('cidr')
                    allow_pre_list += cidr_info + ' | '

                assoc_type = assoc_detail.get('type')
                assoc_state = assoc_info.get('associated')

                result.append((gw_name, gw_id, assoc_id, region, account, allow_pre_list, assoc_type, assoc_state))

        return result

    def describe_main(self):
        #connection_list = self.dx.describe_connections()
        #dx_connection is type == 1
        dx_conn_result = self.dx_describe_connections()
        # Virtual interface is type == 2
        dx_vi_result = self.dx_describe_virtual_interface()
        # Direct Connect gateways is type == 3
        dx_gate_result, gw_list = self.dx_describe_gateways()
        if gw_list == [] or gw_list == None or gw_list == '':
            dx_vi_attach_result = []
            dx_gate_assoc_result = []
        else:
            # Virtual interface attachments is type == 4
            dx_vi_attach_result = self.dx_describe_virtual_interface_attachments(gw_list)
            # Gateway associations is type == 5
            dx_gate_assoc_result = self.dx_describe_gateway_association(gw_list)

        return dx_conn_result, dx_vi_result, dx_gate_result, dx_vi_attach_result, dx_gate_assoc_result