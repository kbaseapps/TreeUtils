import logging
import os
import shutil
import uuid

from DataFileUtil.DataFileUtilClient import DataFileUtil

class Utils:
    def __init__(self, config):
        self.cfg = config
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])

    @staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))

    def to_newick(self, params):
        """Convert an Tree to a Newick File"""
        files = {}

        res = self.dfu.get_objects({
            'object_refs': [params['input_ref']]
        })['data'][0]
        name = res['info'][1]
        if "KBaseTrees.Tree" not in res['info'][2]:
            raise ValueError("Supplied reference is not a Tree")

        files['file_path'] = os.path.join(params['destination_dir'], name + ".newick")
        with open(files['file_path'], 'w') as out_file:
            out_file.write(res['data']['tree'])

        return name, files

    def export(self, file, name, input_ref):
        """Saves a set of files to SHOCK for export"""
        export_package_dir = os.path.join(self.scratch, name+str(uuid.uuid4()))
        os.makedirs(export_package_dir)
        shutil.move(file, os.path.join(export_package_dir, os.path.basename(file)))

        # package it up and be done
        package_details = self.dfu.package_for_download({
            'file_path': export_package_dir,
            'ws_refs': [input_ref]
        })

        return {'shock_id': package_details['shock_id']}
