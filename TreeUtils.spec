/*
A KBase module: TreeUtils
*/

#include <KBaseTrees.spec>
#include <workspace.spec>

module TreeUtils {
    /* @id kb KBaseTrees.Tree */
	typedef string Tree_id;

	typedef structure {
        list <string> tree_refs;
        list <string> included_fields;
    } GetTreesParams;

    typedef structure {
        KBaseTrees.Tree data;
        Workspace.object_info info;
    } TreeData;

	funcdef get_trees(GetTreesParams params)
	    returns (list<TreeData> returnVal) authentication required;

    typedef structure {
       Workspace.ws_id id;
       list<Workspace.ObjectSaveData> trees;
    } SaveTreesParams;

    typedef structure {
       Workspace.object_info info;
    } SaveTreeResult;

    funcdef save_trees(SaveTreesParams params)
               returns (list<SaveTreeResult> returnVal) authentication required;

    typedef structure {
        Tree_id input_ref;
        string destination_dir;
    } TreeToNewickFileParams;

    typedef structure {
        string file_path;
    } TreeToNewickFileOutput;

    funcdef tree_to_newick_file(TreeToNewickFileParams params)
        returns (TreeToNewickFileOutput result) authentication required;

    typedef structure {
       Tree_id input_ref;
    } ExportTreeParams;

    typedef structure {
       string shock_id;
    } ExportTreeOutput;

    funcdef export_tree_newick(ExportTreeParams params)
       returns (ExportTreeOutput result) authentication required;

};
