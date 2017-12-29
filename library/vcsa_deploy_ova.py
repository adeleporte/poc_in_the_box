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



def main():
    module = AnsibleModule(
        argument_spec=dict(
            vcsa_deploy_tool_path=dict(required=True, type='str'),
            template=dict(required=True, type='str'),
            vm_name=dict(required=True, type='str')
        ),
        supports_check_mode=True
    )

    vcsa_deploy = '{}/vcsa-deploy'.format(module.params['vcsa_deploy_tool_path'])
    vcsa_template = '{}'.format(module.params['template'])
    ova_tool_result = module.run_command([vcsa_deploy, 'install', '--accept-eula', '--acknowledge-ceip', '--no-esx-ssl-verify', vcsa_template])
    #ova_tool_result = module.run_command('ls')

    if ova_tool_result[0] != 0:
        module.fail_json(msg='Failed to deploy VCSA, error message from vcsa_deploy is: {}'.format(ova_tool_result[2]))

    module.exit_json(changed=True, ova_tool_result=ova_tool_result)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
