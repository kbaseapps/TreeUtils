# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os

from .core.Utils import Utils
from DataFileUtil.DataFileUtilClient import DataFileUtil
from Workspace.WorkspaceClient import Workspace
#END_HEADER


class TreeUtils:
    '''
    Module Name:
    TreeUtils

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "acb216cd302c161d5b4dfb272bd4bbae44cdac28"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.utils = Utils(config)
        self.scratch = config['scratch']
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.ws = Workspace(config['workspace-url'])
        logging.basicConfig(level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def get_trees(self, ctx, params):
        """
        :param params: instance of type "GetTreesParams" (tree_refs -
           (required) list of WS references included_fields - (optional)
           subset of tree fields to include) -> structure: parameter
           "tree_refs" of list of String, parameter "included_fields" of list
           of String
        :returns: instance of list of type "TreeData" -> structure: parameter
           "data" of type "Tree" (Data type for phylogenetic trees. @optional
           name description type tree_attributes @optional
           default_node_labels ws_refs kb_refs leaf_list) -> structure:
           parameter "name" of String, parameter "description" of String,
           parameter "type" of String, parameter "tree" of type "newick_tree"
           (Trees are represented in KBase by default in newick format
           (http://en.wikipedia.org/wiki/Newick_format) and are returned to
           you in this format by default.) -> type "tree" (A string
           representation of a phylogenetic tree.  The format/syntax of the
           string is specified by using one of the available typedefs
           declaring a particular format, such as 'newick_tree',
           'phylo_xml_tree' or 'json_tree'.  When a format is not explictily
           specified, it is possible to return trees in different formats
           depending on addtional parameters. Regardless of format, all leaf
           nodes in trees built from MSAs are indexed to a specific MSA row. 
           You can use the appropriate functionality of the API to replace
           these IDs with other KBase Ids instead. Internal nodes may or may
           not be named. Nodes, depending on the format, may also be
           annotated with structured data such as bootstrap values and
           distances.), parameter "tree_attributes" of mapping from String to
           String, parameter "default_node_labels" of mapping from type
           "node_id" to type "label", parameter "ws_refs" of mapping from
           type "node_id" to mapping from type "ref_type" (An enumeration of
           reference types for a node.  Either the one letter abreviation or
           full name can be given.  For large trees, it is strongly advised
           you use the one letter abreviations. Supported types are: g |
           genome  => genome typed object or CDS data p | protein => protein
           sequence object or CDS data, often given as the MD5 of the
           sequence n | dna     => dna sequence object or CDS data, often
           given as the MD5 of the sequence f | feature => feature object or
           CDS data) to list of type "ws_obj_id" (@id ws), parameter
           "kb_refs" of mapping from type "node_id" to mapping from type
           "ref_type" (An enumeration of reference types for a node.  Either
           the one letter abreviation or full name can be given.  For large
           trees, it is strongly advised you use the one letter abreviations.
           Supported types are: g | genome  => genome typed object or CDS
           data p | protein => protein sequence object or CDS data, often
           given as the MD5 of the sequence n | dna     => dna sequence
           object or CDS data, often given as the MD5 of the sequence f |
           feature => feature object or CDS data) to list of type "kbase_id"
           (A KBase ID is a string starting with the characters "kb|".  KBase
           IDs are typed. The types are designated using a short string. For
           instance," g" denotes a genome, "tree" denotes a Tree, and "aln"
           denotes a sequence alignment. KBase IDs may be hierarchical.  For
           example, if a KBase genome identifier is "kb|g.1234", a protein
           encoding gene within that genome may be represented as
           "kb|g.1234.peg.771". @id kb), parameter "leaf_list" of list of
           type "node_id", parameter "info" of type "object_info"
           (Information about an object, including user provided metadata.
           obj_id objid - the numerical id of the object. obj_name name - the
           name of the object. type_string type - the type of the object.
           timestamp save_date - the save date of the object. obj_ver ver -
           the version of the object. username saved_by - the user that saved
           or copied the object. ws_id wsid - the workspace containing the
           object. ws_name workspace - the workspace containing the object.
           string chsum - the md5 checksum of the object. int size - the size
           of the object in bytes. usermeta meta - arbitrary user-supplied
           metadata about the object.) -> tuple of size 11: parameter "objid"
           of type "obj_id" (The unique, permanent numerical ID of an
           object.), parameter "name" of type "obj_name" (A string used as a
           name for an object. Any string consisting of alphanumeric
           characters and the characters |._- that is not an integer is
           acceptable.), parameter "type" of type "type_string" (A type
           string. Specifies the type and its version in a single string in
           the format [module].[typename]-[major].[minor]: module - a string.
           The module name of the typespec containing the type. typename - a
           string. The name of the type as assigned by the typedef statement.
           major - an integer. The major version of the type. A change in the
           major version implies the type has changed in a non-backwards
           compatible way. minor - an integer. The minor version of the type.
           A change in the minor version implies that the type has changed in
           a way that is backwards compatible with previous type definitions.
           In many cases, the major and minor versions are optional, and if
           not provided the most recent version will be used. Example:
           MyModule.MyType-3.1), parameter "save_date" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time)), parameter "version" of Long,
           parameter "saved_by" of type "username" (Login name of a KBase
           user account.), parameter "wsid" of type "ws_id" (The unique,
           permanent numerical ID of a workspace.), parameter "workspace" of
           type "ws_name" (A string used as a name for a workspace. Any
           string consisting of alphanumeric characters and "_", ".", or "-"
           that is not an integer is acceptable. The name may optionally be
           prefixed with the workspace owner's user name and a colon, e.g.
           kbasetest:my_workspace.), parameter "chsum" of String, parameter
           "size" of Long, parameter "meta" of type "usermeta" (User provided
           metadata about an object. Arbitrary key-value pairs provided by
           the user.) -> mapping from String to String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN get_trees
        logging.info("Starting 'get_trees' with params:{}".format(params))
        self.utils.validate_params(params, ("tree_refs",), ("included_fields",))
        ws_objs = [{'ref': r, 'included': params.get('included_fields', None)}
                   for r in params['tree_refs']]
        result = self.ws.get_objects2({'objects': ws_objs})['data']
        #END get_trees

        # At some point might do deeper type checking...
        if not isinstance(result, list):
            raise ValueError('Method get_trees return value ' +
                             'result is not type list as required.')
        # return the results
        return [result]

    def save_trees(self, ctx, params):
        """
        :param params: instance of type "SaveTreesParams" -> structure:
           parameter "ws_id" of type "ws_id" (The unique, permanent numerical
           ID of a workspace.), parameter "trees" of list of type
           "ObjectSaveData" (An object and associated data required for
           saving. Required arguments: type_string type - the type of the
           object. Omit the version information to use the latest version.
           UnspecifiedObject data - the object data. Optional arguments: One
           of an object name or id. If no name or id is provided the name
           will be set to 'auto' with the object id appended as a string,
           possibly with -\d+ appended if that object id already exists as a
           name. obj_name name - the name of the object. obj_id objid - the
           id of the object to save over. usermeta meta - arbitrary
           user-supplied metadata for the object, not to exceed 16kb; if the
           object type specifies automatic metadata extraction with the 'meta
           ws' annotation, and your metadata name conflicts, then your
           metadata will be silently overwritten. list<ProvenanceAction>
           provenance - provenance data for the object. boolean hidden - true
           if this object should not be listed when listing workspace
           objects.) -> structure: parameter "type" of type "type_string" (A
           type string. Specifies the type and its version in a single string
           in the format [module].[typename]-[major].[minor]: module - a
           string. The module name of the typespec containing the type.
           typename - a string. The name of the type as assigned by the
           typedef statement. major - an integer. The major version of the
           type. A change in the major version implies the type has changed
           in a non-backwards compatible way. minor - an integer. The minor
           version of the type. A change in the minor version implies that
           the type has changed in a way that is backwards compatible with
           previous type definitions. In many cases, the major and minor
           versions are optional, and if not provided the most recent version
           will be used. Example: MyModule.MyType-3.1), parameter "data" of
           unspecified object, parameter "name" of type "obj_name" (A string
           used as a name for an object. Any string consisting of
           alphanumeric characters and the characters |._- that is not an
           integer is acceptable.), parameter "objid" of type "obj_id" (The
           unique, permanent numerical ID of an object.), parameter "meta" of
           type "usermeta" (User provided metadata about an object. Arbitrary
           key-value pairs provided by the user.) -> mapping from String to
           String, parameter "provenance" of list of type "ProvenanceAction"
           (A provenance action. A provenance action (PA) is an action taken
           while transforming one data object to another. There may be
           several PAs taken in series. A PA is typically running a script,
           running an api command, etc. All of the following fields are
           optional, but more information provided equates to better data
           provenance. resolved_ws_objects should never be set by the user;
           it is set by the workspace service when returning data. On input,
           only one of the time or epoch may be supplied. Both are supplied
           on output. The maximum size of the entire provenance object,
           including all actions, is 1MB. timestamp time - the time the
           action was started epoch epoch - the time the action was started.
           string caller - the name or id of the invoker of this provenance
           action. In most cases, this will be the same for all PAs. string
           service - the name of the service that performed this action.
           string service_ver - the version of the service that performed
           this action. string method - the method of the service that
           performed this action. list<UnspecifiedObject> method_params - the
           parameters of the method that performed this action. If an object
           in the parameters is a workspace object, also put the object
           reference in the input_ws_object list. string script - the name of
           the script that performed this action. string script_ver - the
           version of the script that performed this action. string
           script_command_line - the command line provided to the script that
           performed this action. If workspace objects were provided in the
           command line, also put the object reference in the input_ws_object
           list. list<obj_ref> input_ws_objects - the workspace objects that
           were used as input to this action; typically these will also be
           present as parts of the method_params or the script_command_line
           arguments. list<obj_ref> resolved_ws_objects - the workspace
           objects ids from input_ws_objects resolved to permanent workspace
           object references by the workspace service. list<string>
           intermediate_incoming - if the previous action produced output
           that 1) was not stored in a referrable way, and 2) is used as
           input for this action, provide it with an arbitrary and unique ID
           here, in the order of the input arguments to this action. These
           IDs can be used in the method_params argument. list<string>
           intermediate_outgoing - if this action produced output that 1) was
           not stored in a referrable way, and 2) is used as input for the
           next action, provide it with an arbitrary and unique ID here, in
           the order of the output values from this action. These IDs can be
           used in the intermediate_incoming argument in the next action.
           list<ExternalDataUnit> external_data - data external to the
           workspace that was either imported to the workspace or used to
           create a workspace object. list<SubAction> subactions - the
           subactions taken as a part of this action. mapping<string, string>
           custom - user definable custom provenance fields and their values.
           string description - a free text description of this action.) ->
           structure: parameter "time" of type "timestamp" (A time in the
           format YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "epoch" of type "epoch" (A Unix epoch (the time
           since 00:00:00 1/1/1970 UTC) in milliseconds.), parameter "caller"
           of String, parameter "service" of String, parameter "service_ver"
           of String, parameter "method" of String, parameter "method_params"
           of list of unspecified object, parameter "script" of String,
           parameter "script_ver" of String, parameter "script_command_line"
           of String, parameter "input_ws_objects" of list of type "obj_ref"
           (A string that uniquely identifies an object in the workspace
           service. There are two ways to uniquely identify an object in one
           string: "[ws_name or id]/[obj_name or id]/[obj_ver]" - for
           example, "MyFirstWorkspace/MyFirstObject/3" would identify the
           third version of an object called MyFirstObject in the workspace
           called MyFirstWorkspace. 42/Panic/1 would identify the first
           version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "resolved_ws_objects" of list of
           type "obj_ref" (A string that uniquely identifies an object in the
           workspace service. There are two ways to uniquely identify an
           object in one string: "[ws_name or id]/[obj_name or id]/[obj_ver]"
           - for example, "MyFirstWorkspace/MyFirstObject/3" would identify
           the third version of an object called MyFirstObject in the
           workspace called MyFirstWorkspace. 42/Panic/1 would identify the
           first version of the object name Panic in workspace with id 42.
           Towel/1/6 would identify the 6th version of the object with id 1
           in the Towel workspace. "kb|ws.[ws_id].obj.[obj_id].ver.[obj_ver]"
           - for example, "kb|ws.23.obj.567.ver.2" would identify the second
           version of an object with id 567 in a workspace with id 23. In all
           cases, if the version number is omitted, the latest version of the
           object is assumed.), parameter "intermediate_incoming" of list of
           String, parameter "intermediate_outgoing" of list of String,
           parameter "external_data" of list of type "ExternalDataUnit" (An
           external data unit. A piece of data from a source outside the
           Workspace. On input, only one of the resource_release_date or
           resource_release_epoch may be supplied. Both are supplied on
           output. string resource_name - the name of the resource, for
           example JGI. string resource_url - the url of the resource, for
           example http://genome.jgi.doe.gov string resource_version -
           version of the resource timestamp resource_release_date - the
           release date of the resource epoch resource_release_epoch - the
           release date of the resource string data_url - the url of the
           data, for example
           http://genome.jgi.doe.gov/pages/dynamicOrganismDownload.jsf?
           organism=BlaspURHD0036 string data_id - the id of the data, for
           example 7625.2.79179.AGTTCC.adnq.fastq.gz string description - a
           free text description of the data.) -> structure: parameter
           "resource_name" of String, parameter "resource_url" of String,
           parameter "resource_version" of String, parameter
           "resource_release_date" of type "timestamp" (A time in the format
           YYYY-MM-DDThh:mm:ssZ, where Z is either the character Z
           (representing the UTC timezone) or the difference in time to UTC
           in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500 (EST time)
           2013-04-03T08:56:32+0000 (UTC time) 2013-04-03T08:56:32Z (UTC
           time)), parameter "resource_release_epoch" of type "epoch" (A Unix
           epoch (the time since 00:00:00 1/1/1970 UTC) in milliseconds.),
           parameter "data_url" of String, parameter "data_id" of String,
           parameter "description" of String, parameter "subactions" of list
           of type "SubAction" (Information about a subaction that is invoked
           by a provenance action. A provenance action (PA) may invoke
           subactions (SA), e.g. calling a separate piece of code, a service,
           or a script. In most cases these calls are the same from PA to PA
           and so do not need to be listed in the provenance since providing
           information about the PA alone provides reproducibility. In some
           cases, however, SAs may change over time, such that invoking the
           same PA with the same parameters may produce different results.
           For example, if a PA calls a remote server, that server may be
           updated between a PA invoked on day T and another PA invoked on
           day T+1. The SubAction structure allows for specifying information
           about SAs that may dynamically change from PA invocation to PA
           invocation. string name - the name of the SA. string ver - the
           version of SA. string code_url - a url pointing to the SA's
           codebase. string commit - a version control commit ID for the SA.
           string endpoint_url - a url pointing to the access point for the
           SA - a server url, for instance.) -> structure: parameter "name"
           of String, parameter "ver" of String, parameter "code_url" of
           String, parameter "commit" of String, parameter "endpoint_url" of
           String, parameter "custom" of mapping from String to String,
           parameter "description" of String, parameter "hidden" of type
           "boolean" (A boolean. 0 = false, other = true.)
        :returns: instance of list of type "object_info" (Information about
           an object, including user provided metadata. obj_id objid - the
           numerical id of the object. obj_name name - the name of the
           object. type_string type - the type of the object. timestamp
           save_date - the save date of the object. obj_ver ver - the version
           of the object. username saved_by - the user that saved or copied
           the object. ws_id wsid - the workspace containing the object.
           ws_name workspace - the workspace containing the object. string
           chsum - the md5 checksum of the object. int size - the size of the
           object in bytes. usermeta meta - arbitrary user-supplied metadata
           about the object.) -> tuple of size 11: parameter "objid" of type
           "obj_id" (The unique, permanent numerical ID of an object.),
           parameter "name" of type "obj_name" (A string used as a name for
           an object. Any string consisting of alphanumeric characters and
           the characters |._- that is not an integer is acceptable.),
           parameter "type" of type "type_string" (A type string. Specifies
           the type and its version in a single string in the format
           [module].[typename]-[major].[minor]: module - a string. The module
           name of the typespec containing the type. typename - a string. The
           name of the type as assigned by the typedef statement. major - an
           integer. The major version of the type. A change in the major
           version implies the type has changed in a non-backwards compatible
           way. minor - an integer. The minor version of the type. A change
           in the minor version implies that the type has changed in a way
           that is backwards compatible with previous type definitions. In
           many cases, the major and minor versions are optional, and if not
           provided the most recent version will be used. Example:
           MyModule.MyType-3.1), parameter "save_date" of type "timestamp" (A
           time in the format YYYY-MM-DDThh:mm:ssZ, where Z is either the
           character Z (representing the UTC timezone) or the difference in
           time to UTC in the format +/-HHMM, eg: 2012-12-17T23:24:06-0500
           (EST time) 2013-04-03T08:56:32+0000 (UTC time)
           2013-04-03T08:56:32Z (UTC time)), parameter "version" of Long,
           parameter "saved_by" of type "username" (Login name of a KBase
           user account.), parameter "wsid" of type "ws_id" (The unique,
           permanent numerical ID of a workspace.), parameter "workspace" of
           type "ws_name" (A string used as a name for a workspace. Any
           string consisting of alphanumeric characters and "_", ".", or "-"
           that is not an integer is acceptable. The name may optionally be
           prefixed with the workspace owner's user name and a colon, e.g.
           kbasetest:my_workspace.), parameter "chsum" of String, parameter
           "size" of Long, parameter "meta" of type "usermeta" (User provided
           metadata about an object. Arbitrary key-value pairs provided by
           the user.) -> mapping from String to String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN save_trees
        logging.info("Starting 'save_trees'")
        self.utils.validate_params(params, ("ws_id", "trees"), ('type',))
        trees = []
        for i, t in enumerate(params['trees']):
            self.utils.validate_params(t, ("data",), ("name", "hidden", "meta", "type"))
            if 'type' in t and t['type'] != 'KBaseTrees.Tree':
                raise ValueError("This method only saves KBaseTrees.Tree objects")
            if "tree" not in t['data']:
                raise ValueError("Object {} missing 'tree' attribute containing newick tree"
                                 .format(i))
            if not Utils.validate_newick(t['data']['tree']):
                raise ValueError("Object {} has an invalid newick tree: {}"
                                 .format(i, t['data']['tree']))

            t['type'] = 'KBaseTrees.Tree'
            trees.append(t)

        result = self.dfu.save_objects({"id": params["ws_id"], "objects": trees})
        #END save_trees

        # At some point might do deeper type checking...
        if not isinstance(result, list):
            raise ValueError('Method save_trees return value ' +
                             'result is not type list as required.')
        # return the results
        return [result]

    def tree_to_newick_file(self, ctx, params):
        """
        :param params: instance of type "TreeToNewickFileParams" ->
           structure: parameter "input_ref" of type "Tree_id" (@id kb
           KBaseTrees.Tree), parameter "destination_dir" of String
        :returns: instance of type "TreeToNewickFileOutput" -> structure:
           parameter "file_path" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN tree_to_newick_file
        logging.info("Starting 'tree_to_newick' with params: {}".format(params))
        self.utils.validate_params(params, ("destination_dir", "input_ref"))
        _, result = self.utils.to_newick(params)
        #END tree_to_newick_file

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method tree_to_newick_file return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]

    def export_tree_newick(self, ctx, params):
        """
        :param params: instance of type "ExportTreeParams" -> structure:
           parameter "input_ref" of type "Tree_id" (@id kb KBaseTrees.Tree)
        :returns: instance of type "ExportTreeOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: result
        #BEGIN export_tree_newick
        logging.info("Starting 'export_tree_newick' with params:{}".format(params))
        self.utils.validate_params(params, ("input_ref",))
        params['destination_dir'] = self.scratch
        cs_id, files = self.utils.to_newick(params)
        result = self.utils.export(files['file_path'], cs_id, params['input_ref'])
        #END export_tree_newick

        # At some point might do deeper type checking...
        if not isinstance(result, dict):
            raise ValueError('Method export_tree_newick return value ' +
                             'result is not type dict as required.')
        # return the results
        return [result]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
