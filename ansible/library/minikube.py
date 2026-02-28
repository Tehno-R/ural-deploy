#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', default='present', choices=['present', 'absent']),
        )
    )

    deb_path = '/tmp/minikube_latest_amd64.deb'
    url = 'https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb'

    if module.params['state'] == 'present':
        rc, _, _ = module.run_command('which minikube')
        if rc == 0:
            module.exit_json(changed=False, msg='minikube already installed')

        # скачать
        rc, out, err = module.run_command(f'curl -LO {deb_path} {url}')
        if rc != 0:
            module.fail_json(msg=f'download failed: {err}')

        # установить
        rc, out, err = module.run_command(f'dpkg -i {deb_path}')
        if rc != 0:
            module.fail_json(msg=f'install failed: {err}')

        os.remove(deb_path)
        module.exit_json(changed=True, msg='minikube installed')

    elif module.params['state'] == 'absent':
        rc, _, _ = module.run_command('which minikube')
        if rc != 0:
            module.exit_json(changed=False, msg='minikube not installed')

        rc, out, err = module.run_command('dpkg -r minikube')
        if rc != 0:
            module.fail_json(msg=f'uninstall failed: {err}')

        module.exit_json(changed=True, msg='minikube removed')

if __name__ == '__main__':
    main()