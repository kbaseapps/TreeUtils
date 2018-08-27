# -*- coding: utf-8 -*-
import json
import os
import time
import unittest
from configparser import ConfigParser

from TreeUtils.TreeUtilsImpl import TreeUtils
from TreeUtils.TreeUtilsServer import MethodContext
from TreeUtils.authclient import KBaseAuth as _KBaseAuth

from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace


class TreeUtilsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('TreeUtils'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'TreeUtils',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = TreeUtils(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        cls.dfu = DataFileUtil(cls.callback_url)
        suffix = int(time.time() * 1000)
        cls.wsName = "test_CompoundSetUtils_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.wsId = ret[0]
        cls.tree_obj = json.load(open('data/tree.json'))
        info = cls.dfu.save_objects({
            "id": cls.wsId,
            "objects": [{
                "type": "KBaseTrees.Tree",
                "data": cls.tree_obj,
                "name": "test_tree"
            }]
        })[0]
        cls.tree_ref = "%s/%s/%s" % (info[6], info[0], info[4])

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_missing_params(self):
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().get_trees(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().save_trees(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().tree_to_newick_file(self.getContext(), {})
        with self.assertRaisesRegexp(ValueError, "Required keys"):
            self.getImpl().export_tree_newick(self.getContext(), {})

    def test_get_trees(self):
        params = {'tree_refs': [self.tree_ref]}
        ret = self.getImpl().get_trees(self.getContext(), params)[0]
        self.assertEqual(set(ret[0]['data'].keys()), {'default_node_labels', 'kb_refs', 'tree',
                                                      'tree_attributes', 'type', 'leaf_list'})

        params = {'tree_refs': [self.tree_ref], 'included_fields': ['type', 'default_node_labels']}
        ret = self.getImpl().get_trees(self.getContext(), params)[0]
        self.assertEqual(set(ret[0]['data'].keys()), {'default_node_labels', 'type'})

    def test_save_trees(self):
        params = {'ws_id': self.wsId, 'trees': [{'name': 'test_save_trees',
                                                 'data': self.tree_obj}]}
        ret = self.getImpl().save_trees(self.getContext(), params)[0]
        self.assertEqual(len(ret[0]), 11)
        assert 'KBaseTrees.Tree' in ret[0][2]

        del params['trees'][0]['data']['tree']
        with self.assertRaisesRegexp(ValueError, "missing 'tree' attribute"):
            ret = self.getImpl().save_trees(self.getContext(), params)[0]

        params['trees'][0]['data']['tree'] = "foo"
        with self.assertRaisesRegexp(ValueError, "invalid newick tree"):
            ret = self.getImpl().save_trees(self.getContext(), params)[0]


    def test_make_newick(self):
        params = {'input_ref': self.tree_ref, 'destination_dir': self.scratch}
        ret = self.getImpl().tree_to_newick_file(self.getContext(), params)[0]
        assert ret and ('file_path' in ret)

    def test_export_newick(self):
        params = {'input_ref': self.tree_ref}
        ret = self.getImpl().export_tree_newick(self.getContext(), params)[0]
        assert ret and ('shock_id' in ret)
