/*
Phylogenetic Tree and Multiple Sequence Alignment Services

This service provides a set of data types and methods for operating with multiple
sequence alignments (MSAs) and phylogenetic trees.

Authors
---------
Michael Sneddon, LBL (mwsneddon@lbl.gov)
Fangfang Xia, ANL (fangfang.xia@gmail.com)
Keith Keller, LBL (kkeller@lbl.gov)
Matt Henderson, LBL (mhenderson@lbl.gov)
Dylan Chivian, LBL (dcchivian@lbl.gov)
Roman Sutormin, LBL (rsutormin@lbl.gov)
*/
module KBaseTrees
{
    /* *********************************************************************************************** */
    /* ALIGNMENT AND TREE DATA TYPES */
    /* *********************************************************************************************** */

    /*
        Indicates true or false values, false = 0, true = 1
        @range [0,1]
    */
    typedef int boolean;

    /*
        Time in units of number of seconds since the epoch
    */
    typedef string timestamp;

    /*
        Integer number indicating a 1-based position in an amino acid / nucleotide sequence
        @range [1,
    */
    typedef int position;

    /*
        A KBase ID is a string starting with the characters "kb|".  KBase IDs are typed. The types are
        designated using a short string. For instance," g" denotes a genome, "tree" denotes a Tree, and
        "aln" denotes a sequence alignment. KBase IDs may be hierarchical.  For example, if a KBase genome
        identifier is "kb|g.1234", a protein encoding gene within that genome may be represented as
        "kb|g.1234.peg.771".
        @id kb
    */
    typedef string kbase_id;

    /*
        A string representation of a phylogenetic tree.  The format/syntax of the string is
        specified by using one of the available typedefs declaring a particular format, such as 'newick_tree',
        'phylo_xml_tree' or 'json_tree'.  When a format is not explictily specified, it is possible to return
        trees in different formats depending on addtional parameters. Regardless of format, all leaf nodes
        in trees built from MSAs are indexed to a specific MSA row.  You can use the appropriate functionality
        of the API to replace these IDs with other KBase Ids instead. Internal nodes may or may not be named.
        Nodes, depending on the format, may also be annotated with structured data such as bootstrap values and
        distances.
    */
    typedef string tree;

    /*
        Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format)
        and are returned to you in this format by default.
    */
    typedef tree newick_tree;

    /*
        Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format),
        but can optionally be converted to the more verbose phyloXML format, which is useful for compatibility or
        when additional information/annotations decorate the tree.
    */
    typedef tree phylo_xml_tree;

    /*
        Trees are represented in KBase by default in newick format (http://en.wikipedia.org/wiki/Newick_format),
        but can optionally be converted to JSON format where the structure of the tree matches the structure of
        the JSON object.  This is useful when interacting with the tree in JavaScript, for instance.
    */
    typedef tree json_tree;

    /*
        String representation of a sequence alignment, the format of which may be different depending on
        input options for retrieving the alignment.
    */
    typedef string alignment;

    /*
        @id ws
    */
    typedef string ws_obj_id;

    /* A workspace ID that references a Tree data object.
        @id ws KBaseTrees.Tree
    */
    typedef string ws_tree_id;

    /*
    	###  KBaseTrees.ConcatMSA KBaseTrees.MS
        @id ws KBaseTrees.MSA
    */
    typedef string ws_alignment_id;

    /* A workspace ID that references a Genome data object.
        @id ws KBaseGenomes.Genome
    */
    typedef string ws_genome_id;

    /* */
    typedef string node_id;


    typedef boolean is_leaf;


    typedef string label;

    /*
    An enumeration of reference types for a node.  Either the one letter abreviation or full
    name can be given.  For large trees, it is strongly advised you use the one letter abreviations.
    Supported types are:
        g | genome  => genome typed object or CDS data
        p | protein => protein sequence object or CDS data, often given as the MD5 of the sequence
        n | dna     => dna sequence object or CDS data, often given as the MD5 of the sequence
        f | feature => feature object or CDS data
    */
    typedef string ref_type;


    /* Data type for phylogenetic trees.

        @optional name description type tree_attributes
        @optional default_node_labels ws_refs kb_refs leaf_list
    */
    typedef structure {
        string name;
        string description;
        string type;

        newick_tree tree;

        mapping <string,string> tree_attributes;

        mapping <node_id,label> default_node_labels;
        mapping <node_id,mapping<ref_type,list<ws_obj_id>>> ws_refs;
        mapping <node_id,mapping<ref_type,list<kbase_id>>> kb_refs;

        list <node_id> leaf_list;
    } Tree;

    typedef string row_id;
    typedef string sequence;

    typedef int start_pos_in_parent;
    typedef int end_pos_in_parent;
    typedef int parent_len;
    typedef string parent_md5;

    typedef tuple <
        start_pos_in_parent,
        end_pos_in_parent,
        parent_len,
        parent_md5>
            trim_info;

    /* Type for multiple sequence alignment.
	sequence_type - 'protein' in case sequences are amino acids, 'dna' in case of
		nucleotides.
	int alignment_length - number of columns in alignment.
	mapping<row_id, sequence> alignment - mapping from sequence id to aligned sequence.
	list<row_id> row_order - list of sequence ids defining alignment order (optional).
	ws_alignment_id parent_msa_ref - reference to parental alignment object to which
		this object adds some new aligned sequences (it could be useful in case of
		profile alignments where you don't need to insert new gaps in original msa).
	@optional name description sequence_type
	@optional trim_info alignment_attributes row_order
	@optional default_row_labels ws_refs kb_refs
	@optional parent_msa_ref
    */
    typedef structure {
        string name;
        string description;
        string sequence_type;

        int alignment_length;
        mapping <row_id, sequence> alignment;

        mapping <row_id, trim_info> trim_info;

        mapping <string,string> alignment_attributes;
        list <row_id> row_order;

        mapping <node_id,label> default_row_labels;
        mapping <node_id,mapping<ref_type,list<ws_obj_id>>> ws_refs;
        mapping <node_id,mapping<ref_type,list<kbase_id>>> kb_refs;

        ws_alignment_id parent_msa_ref;
    } MSA;

    /*
        Type for MSA collection element. There could be mutual exclusively
        defined either ref or data field.
        @optional metadata
        @optional ref
        @optional data
    */
    typedef structure {
        mapping<string, string> metadata;
        ws_alignment_id ref;
        MSA data;
    } MSASetElement;

    /*
        Type for collection of MSA objects.
    */
    typedef structure {
        string description;
        list<MSASetElement> elements;
    } MSASet;
};