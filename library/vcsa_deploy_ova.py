#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2015 VMware, Inc. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# MODIFIED FROM YFAUSER VERSION


__author__ = 'adeleporte'


from pyVim import connect
from pyVmomi import vim
import requests
import ssl
import atexit


def find_virtual_machine(content, searched_vm_name):
    virtual_machines = get_all_objs(content, [vim.VirtualMachine])
    for vm in virtual_machines:
        if vm.name == searched_vm_name:
            return vm
    return None


def get_all_objs(content, vimtype):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
        obj.update({managed_object_ref: managed_object_ref.name})
    return obj


def connect_to_api(vchost, vc_user, vc_pwd):
    if hasattr(ssl, 'SSLContext'):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
    else:
        context = None
    if context:
        service_instance = connect.SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd, sslContext=context)
    else:
        service_instance = connect.SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd)

    atexit.register(connect.Disconnect, service_instance)

    return service_instance.RetrieveContent()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vcsa_deploy_tool_path=dict(required=True, type='str'),
            template=dict(required=True, type='str'),
            vm_name=dict(required=True, type='str')
        ),
        supports_check_mode=True
    )

    vcsa_appliance_vm = find_virtual_machine(content, module.params['vmname'])

    if vcsa_appliance_vm:
        #module.fail_json(msg='A VM with the name {} was already present')
        module.exit_json(changed=False, vcsa_appliance_vm=str(vcsa_appliance_vm))

    if module.check_mode:
        module.exit_json(changed=True)

    vcsa_deploy = '{}/vcsa-deploy'.format(module.params['vcsa_deploy_tool_path'])
    vcsa_template = '{}'.format(module.params['template'])
    ova_tool_result = module.run_command(vcsa_deploy, '--accept-eula', '--acknowledge-ceip', '--no-esx-ssl-verify', vcsa_template)

    if ova_tool_result[0] != 0:
        module.fail_json(msg='Failed to deploy OVA, error message from vcsa_deploy is: {}'.format(ova_tool_result[1]))

    module.exit_json(changed=True, ova_tool_result=ova_tool_result)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
