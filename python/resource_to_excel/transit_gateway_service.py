class transit_gateway:
    def __init__(self, transit_service):
        self.tsg = transit_service


    def get_name_tag(self, tag_list):
        result = ''
        for tag_info in tag_list:
            if tag_info.get('Key') == 'Name':
                result = tag_info.get('Value')
        return result

    def vpn_describe_cgw(self):
        cgw_list = self.tsg.describe_customer_gateways()
        #필요 정보
        #'Name', 'ID', 'Owner ID', 'State'
        print('----------cgw info--------')
        print(cgw_list)

        result = []
        for cgw_info in cgw_list.get('CustomerGateways'):
            tag_list = cgw_info.get('Tags')
            name = self.get_name_tag(tag_list)
            id = cgw_info.get('CustomerGatewayId')
            state = cgw_info.get('State')
            type = cgw_info.get('Type')
            ip_info = cgw_info.get('IpAddress')
            bgp_asn = cgw_info.get('BgpAsn')

            result.append((name, id, state, type, ip_info, bgp_asn))

        return result

    def vpn_describe_conn(self):
        vpn_conn_list = self.tsg.describe_vpn_connections()
        #필요 정보
        #'Name', 'id', state, vpg, trasit gateway, cgw, cgw addr, type, category
        print('----------vpn conn info--------')
        print(vpn_conn_list)

        result = []
        for vpn_conn_info in vpn_conn_list.get('VpnConnections'):
            tags = vpn_conn_info.get('Tags')
            name = self.get_name_tag(tags)
            id = vpn_conn_info.get('VpnConnectionId')
            state = vpn_conn_info.get('OwnerId')
            vpg_info = vpn_conn_info.get('State')
            tsg_info = vpn_conn_info.get('TransitGatewayId')
            cgw_info = vpn_conn_info.get('CustomerGatewayId')
            cgw_ip = vpn_conn_info.get('')
            type = vpn_conn_info.get('Type')
            category = vpn_conn_info.get('Category')

            result.append((name, id, state, vpg_info, tsg_info, cgw_info, cgw_ip, type, category))

        return result

    def tsg_describe_info(self):
        tsg_list = self.tsg.describe_transit_gateways()
        #필요 정보
        #'Name', 'ID', 'Owner ID', 'State'
        print('----------transit gateway info--------')
        print(tsg_list)

        result = []
        for tsg_info in tsg_list.get('TransitGateways'):
            name = tsg_info.get('Description')
            id = tsg_info.get('TransitGatewayId')
            owner_id = tsg_info.get('OwnerId')
            state = tsg_info.get('State')

            result.append((name, id, owner_id, state))

        return result

    def tsg_describe_attach_info(self):
        tsg_attach_list = self.tsg.describe_transit_gateway_attachments()
        #필요 정보
        #'Name', 'ID', 'Owner ID', 'State'
        print('----------transit gateway attach info--------')
        print(tsg_attach_list)

        result = []

        for tsg_attach_info in tsg_attach_list.get('TransitGateways'):
            tags = tsg_attach_info.get('Tags')
            name = self.get_name_tag(tags)
            tsg_attach_id = tsg_attach_info.get('TransitGatewayAttachmentId')
            tsg_id = tsg_attach_info.get('TransitGatewayId')
            type = tsg_attach_info.get('ResourceType')
            state = tsg_attach_info.get('State')
            ass_id = tsg_attach_info.get('Association').get('TransitGatewayRouteTableId')
            ass_state = tsg_attach_info.get('Association').get('State')


            result.append((name, tsg_attach_id, tsg_id, type, state, ass_id, ass_state))

        return result

    # def tg_describe_virtual_interface(self):
    #     vi_list = self.dx.describe_virtual_interfaces()
    #     #print('vi_list 정보')
    #     #print(vi_list)
    #     result = []
    #     for vi_info in vi_list.get('virtualInterfaces'):
    #         vi_name = vi_info.get('virtualInterfaceName')
    #         vi_id = vi_info.get('virtualInterfaceId')
    #         region = vi_info.get('region')
    #         connection_id = vi_info.get('connectionId')
    #         vlan = vi_info.get('vlan')
    #         vi_type = vi_info.get('virtualInterfaceType')
    #         vi_state = vi_info.get('virtualInterfaceState')
    #
    #         result.append((vi_name, vi_id, region, connection_id, vlan, vi_type, vi_state))
    #
    #     return result
    #
    # def tg_describe_gateways(self):
    #     gateway_list = self.dx.describe_direct_connect_gateways()
    #     #print('gateway_list 정보')
    #     #print(gateway_list)
    #     result = []
    #     for gateway_info in gateway_list.get('directConnectGateways'):
    #
    #         name = gateway_info.get('directConnectGatewayName')
    #         id = gateway_info.get('directConnectGatewayId')
    #         account_num = gateway_info.get('ownerAccount')
    #         asn = gateway_info.get('amazonSideAsn')
    #         state = gateway_info.get('directConnectGatewayState')
    #
    #         result.append((name, id, account_num, asn, state))
    #
    #     return result, gateway_list.get('directConnectGateways')
    #
    # def tg_describe_virtual_interface_attachments(self, gw_list):
    #
    #     result = []
    #     for gw_info in gw_list:
    #         attach_list = self.dx.describe_direct_connect_gateway_attachments(directConnectGatewayId=gw_info.get('directConnectGatewayId'))
    #         #print('attach_list 정보')
    #         #print(attach_list)
    #         for attach_info in attach_list.get('directConnectGatewayAttachments'):
    #             gw_name = gw_info.get('directConnectGatewayName')
    #             gw_id = gw_info.get('directConnectGatewayId')
    #             vi_id = attach_info.get('virtualInterfaceId')
    #             region = attach_info.get('virtualInterfaceRegion')
    #             account_num = attach_info.get('virtualInterfaceOwnerAccount')
    #             type = attach_info.get('attachmentType')
    #             state = attach_info.get('attachmentState')
    #
    #             result.append((gw_name, gw_id, vi_id, region, account_num, type, state))
    #
    #     return result
    #
    # def tg_describe_gateway_association(self, gw_list):
    #     #assoc_list = self.dx.describe_direct_connect_gateway_associations(directConnectGatewayId='string')
    #     #print('assoc_list 정보')
    #     #print(assoc_list)
    #
    #     result = []
    #     for gw_info in gw_list:
    #         assoc_list = self.dx.describe_direct_connect_gateway_associations(directConnectGatewayId=gw_info.get('directConnectGatewayId'))
    #         print('attach_list 정보')
    #         print(assoc_list)
    #         for assoc_info in assoc_list.get('directConnectGatewayAssociations'):
    #             assoc_detail = assoc_info.get('associatedGateway')
    #
    #             gw_name = gw_info.get('directConnectGatewayName')
    #             gw_id = gw_info.get('directConnectGatewayId')
    #
    #             assoc_id = assoc_detail.get('id')
    #             region = assoc_detail.get('region')
    #             account = assoc_detail.get('ownerAccount')
    #
    #             allow_pre_list = ''
    #             for allow_pre_info in assoc_info.get('allowedPrefixesToDirectConnectGateway'):
    #                 cidr_info = allow_pre_info.get('cidr')
    #                 allow_pre_list += cidr_info + ' | '
    #
    #             assoc_type = assoc_detail.get('type')
    #             assoc_state = assoc_info.get('associated')
    #
    #             result.append((gw_name, gw_id, assoc_id, region, account, allow_pre_list, assoc_type, assoc_state))
    #
    #     return result

    def describe_main(self):
        #connection_list = self.dx.describe_connections()
        #cgw info
        cgw_result = self.vpn_describe_cgw()
        #vpn conn info
        vpn_conn_result = self.vpn_describe_conn()
        #transit gateway_info
        tsg_result = self.tsg_describe_info()
        #transit gateway attach info
        tsg_attach_result = self.tsg_describe_attach_info()

        # Virtual interface is type == 2
        # dx_vi_result = self.dx_describe_virtual_interface()
        # # Direct Connect gateways is type == 3
        # dx_gate_result, gw_list = self.dx_describe_gateways()
        # if gw_list == [] or gw_list == None or gw_list == '':
        #     dx_vi_attach_result = []
        #     dx_gate_assoc_result = []
        # else:
        #     # Virtual interface attachments is type == 4
        #     dx_vi_attach_result = self.dx_describe_virtual_interface_attachments(gw_list)
        #     # Gateway associations is type == 5
        #     dx_gate_assoc_result = self.dx_describe_gateway_association(gw_list)

        return tsg_result