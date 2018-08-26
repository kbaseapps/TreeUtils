package TreeUtils::TreeUtilsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

TreeUtils::TreeUtilsClient

=head1 DESCRIPTION





=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => TreeUtils::TreeUtilsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 get_trees

  $result = $obj->get_trees($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a TreeUtils.GetTreesParams
$result is a reference to a list where each element is a TreeUtils.TreeData
GetTreesParams is a reference to a hash where the following keys are defined:
	tree_refs has a value which is a reference to a list where each element is a string
	included_fields has a value which is a reference to a list where each element is a string
TreeData is a reference to a hash where the following keys are defined:
	data has a value which is a KBaseTrees.Tree
	info has a value which is a Workspace.object_info
Tree is a reference to a hash where the following keys are defined:
	name has a value which is a string
	description has a value which is a string
	type has a value which is a string
	tree has a value which is a KBaseTrees.newick_tree
	tree_attributes has a value which is a reference to a hash where the key is a string and the value is a string
	default_node_labels has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a KBaseTrees.label
	ws_refs has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a reference to a hash where the key is a KBaseTrees.ref_type and the value is a reference to a list where each element is a KBaseTrees.ws_obj_id
	kb_refs has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a reference to a hash where the key is a KBaseTrees.ref_type and the value is a reference to a list where each element is a KBaseTrees.kbase_id
	leaf_list has a value which is a reference to a list where each element is a KBaseTrees.node_id
newick_tree is a KBaseTrees.tree
tree is a string
node_id is a string
label is a string
ref_type is a string
ws_obj_id is a string
kbase_id is a string
object_info is a reference to a list containing 11 items:
	0: (objid) a Workspace.obj_id
	1: (name) a Workspace.obj_name
	2: (type) a Workspace.type_string
	3: (save_date) a Workspace.timestamp
	4: (version) an int
	5: (saved_by) a Workspace.username
	6: (wsid) a Workspace.ws_id
	7: (workspace) a Workspace.ws_name
	8: (chsum) a string
	9: (size) an int
	10: (meta) a Workspace.usermeta
obj_id is an int
obj_name is a string
type_string is a string
timestamp is a string
username is a string
ws_id is an int
ws_name is a string
usermeta is a reference to a hash where the key is a string and the value is a string

</pre>

=end html

=begin text

$params is a TreeUtils.GetTreesParams
$result is a reference to a list where each element is a TreeUtils.TreeData
GetTreesParams is a reference to a hash where the following keys are defined:
	tree_refs has a value which is a reference to a list where each element is a string
	included_fields has a value which is a reference to a list where each element is a string
TreeData is a reference to a hash where the following keys are defined:
	data has a value which is a KBaseTrees.Tree
	info has a value which is a Workspace.object_info
Tree is a reference to a hash where the following keys are defined:
	name has a value which is a string
	description has a value which is a string
	type has a value which is a string
	tree has a value which is a KBaseTrees.newick_tree
	tree_attributes has a value which is a reference to a hash where the key is a string and the value is a string
	default_node_labels has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a KBaseTrees.label
	ws_refs has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a reference to a hash where the key is a KBaseTrees.ref_type and the value is a reference to a list where each element is a KBaseTrees.ws_obj_id
	kb_refs has a value which is a reference to a hash where the key is a KBaseTrees.node_id and the value is a reference to a hash where the key is a KBaseTrees.ref_type and the value is a reference to a list where each element is a KBaseTrees.kbase_id
	leaf_list has a value which is a reference to a list where each element is a KBaseTrees.node_id
newick_tree is a KBaseTrees.tree
tree is a string
node_id is a string
label is a string
ref_type is a string
ws_obj_id is a string
kbase_id is a string
object_info is a reference to a list containing 11 items:
	0: (objid) a Workspace.obj_id
	1: (name) a Workspace.obj_name
	2: (type) a Workspace.type_string
	3: (save_date) a Workspace.timestamp
	4: (version) an int
	5: (saved_by) a Workspace.username
	6: (wsid) a Workspace.ws_id
	7: (workspace) a Workspace.ws_name
	8: (chsum) a string
	9: (size) an int
	10: (meta) a Workspace.usermeta
obj_id is an int
obj_name is a string
type_string is a string
timestamp is a string
username is a string
ws_id is an int
ws_name is a string
usermeta is a reference to a hash where the key is a string and the value is a string


=end text

=item Description



=back

=cut

 sub get_trees
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function get_trees (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to get_trees:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'get_trees');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "TreeUtils.get_trees",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'get_trees',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method get_trees",
					    status_line => $self->{client}->status_line,
					    method_name => 'get_trees',
				       );
    }
}
 


=head2 save_trees

  $result = $obj->save_trees($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a TreeUtils.SaveTreesParams
$result is a reference to a list where each element is a Workspace.object_info
SaveTreesParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a Workspace.ws_id
	trees has a value which is a reference to a list where each element is a Workspace.ObjectSaveData
ws_id is an int
ObjectSaveData is a reference to a hash where the following keys are defined:
	type has a value which is a Workspace.type_string
	data has a value which is an UnspecifiedObject, which can hold any non-null object
	name has a value which is a Workspace.obj_name
	objid has a value which is a Workspace.obj_id
	meta has a value which is a Workspace.usermeta
	provenance has a value which is a reference to a list where each element is a Workspace.ProvenanceAction
	hidden has a value which is a Workspace.boolean
type_string is a string
obj_name is a string
obj_id is an int
usermeta is a reference to a hash where the key is a string and the value is a string
ProvenanceAction is a reference to a hash where the following keys are defined:
	time has a value which is a Workspace.timestamp
	epoch has a value which is a Workspace.epoch
	caller has a value which is a string
	service has a value which is a string
	service_ver has a value which is a string
	method has a value which is a string
	method_params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
	script has a value which is a string
	script_ver has a value which is a string
	script_command_line has a value which is a string
	input_ws_objects has a value which is a reference to a list where each element is a Workspace.obj_ref
	resolved_ws_objects has a value which is a reference to a list where each element is a Workspace.obj_ref
	intermediate_incoming has a value which is a reference to a list where each element is a string
	intermediate_outgoing has a value which is a reference to a list where each element is a string
	external_data has a value which is a reference to a list where each element is a Workspace.ExternalDataUnit
	subactions has a value which is a reference to a list where each element is a Workspace.SubAction
	custom has a value which is a reference to a hash where the key is a string and the value is a string
	description has a value which is a string
timestamp is a string
epoch is an int
obj_ref is a string
ExternalDataUnit is a reference to a hash where the following keys are defined:
	resource_name has a value which is a string
	resource_url has a value which is a string
	resource_version has a value which is a string
	resource_release_date has a value which is a Workspace.timestamp
	resource_release_epoch has a value which is a Workspace.epoch
	data_url has a value which is a string
	data_id has a value which is a string
	description has a value which is a string
SubAction is a reference to a hash where the following keys are defined:
	name has a value which is a string
	ver has a value which is a string
	code_url has a value which is a string
	commit has a value which is a string
	endpoint_url has a value which is a string
boolean is an int
object_info is a reference to a list containing 11 items:
	0: (objid) a Workspace.obj_id
	1: (name) a Workspace.obj_name
	2: (type) a Workspace.type_string
	3: (save_date) a Workspace.timestamp
	4: (version) an int
	5: (saved_by) a Workspace.username
	6: (wsid) a Workspace.ws_id
	7: (workspace) a Workspace.ws_name
	8: (chsum) a string
	9: (size) an int
	10: (meta) a Workspace.usermeta
username is a string
ws_name is a string

</pre>

=end html

=begin text

$params is a TreeUtils.SaveTreesParams
$result is a reference to a list where each element is a Workspace.object_info
SaveTreesParams is a reference to a hash where the following keys are defined:
	ws_id has a value which is a Workspace.ws_id
	trees has a value which is a reference to a list where each element is a Workspace.ObjectSaveData
ws_id is an int
ObjectSaveData is a reference to a hash where the following keys are defined:
	type has a value which is a Workspace.type_string
	data has a value which is an UnspecifiedObject, which can hold any non-null object
	name has a value which is a Workspace.obj_name
	objid has a value which is a Workspace.obj_id
	meta has a value which is a Workspace.usermeta
	provenance has a value which is a reference to a list where each element is a Workspace.ProvenanceAction
	hidden has a value which is a Workspace.boolean
type_string is a string
obj_name is a string
obj_id is an int
usermeta is a reference to a hash where the key is a string and the value is a string
ProvenanceAction is a reference to a hash where the following keys are defined:
	time has a value which is a Workspace.timestamp
	epoch has a value which is a Workspace.epoch
	caller has a value which is a string
	service has a value which is a string
	service_ver has a value which is a string
	method has a value which is a string
	method_params has a value which is a reference to a list where each element is an UnspecifiedObject, which can hold any non-null object
	script has a value which is a string
	script_ver has a value which is a string
	script_command_line has a value which is a string
	input_ws_objects has a value which is a reference to a list where each element is a Workspace.obj_ref
	resolved_ws_objects has a value which is a reference to a list where each element is a Workspace.obj_ref
	intermediate_incoming has a value which is a reference to a list where each element is a string
	intermediate_outgoing has a value which is a reference to a list where each element is a string
	external_data has a value which is a reference to a list where each element is a Workspace.ExternalDataUnit
	subactions has a value which is a reference to a list where each element is a Workspace.SubAction
	custom has a value which is a reference to a hash where the key is a string and the value is a string
	description has a value which is a string
timestamp is a string
epoch is an int
obj_ref is a string
ExternalDataUnit is a reference to a hash where the following keys are defined:
	resource_name has a value which is a string
	resource_url has a value which is a string
	resource_version has a value which is a string
	resource_release_date has a value which is a Workspace.timestamp
	resource_release_epoch has a value which is a Workspace.epoch
	data_url has a value which is a string
	data_id has a value which is a string
	description has a value which is a string
SubAction is a reference to a hash where the following keys are defined:
	name has a value which is a string
	ver has a value which is a string
	code_url has a value which is a string
	commit has a value which is a string
	endpoint_url has a value which is a string
boolean is an int
object_info is a reference to a list containing 11 items:
	0: (objid) a Workspace.obj_id
	1: (name) a Workspace.obj_name
	2: (type) a Workspace.type_string
	3: (save_date) a Workspace.timestamp
	4: (version) an int
	5: (saved_by) a Workspace.username
	6: (wsid) a Workspace.ws_id
	7: (workspace) a Workspace.ws_name
	8: (chsum) a string
	9: (size) an int
	10: (meta) a Workspace.usermeta
username is a string
ws_name is a string


=end text

=item Description



=back

=cut

 sub save_trees
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function save_trees (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to save_trees:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'save_trees');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "TreeUtils.save_trees",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'save_trees',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method save_trees",
					    status_line => $self->{client}->status_line,
					    method_name => 'save_trees',
				       );
    }
}
 


=head2 tree_to_newick_file

  $result = $obj->tree_to_newick_file($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a TreeUtils.TreeToNewickFileParams
$result is a TreeUtils.TreeToNewickFileOutput
TreeToNewickFileParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a TreeUtils.Tree_id
	destination_dir has a value which is a string
Tree_id is a string
TreeToNewickFileOutput is a reference to a hash where the following keys are defined:
	file_path has a value which is a string

</pre>

=end html

=begin text

$params is a TreeUtils.TreeToNewickFileParams
$result is a TreeUtils.TreeToNewickFileOutput
TreeToNewickFileParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a TreeUtils.Tree_id
	destination_dir has a value which is a string
Tree_id is a string
TreeToNewickFileOutput is a reference to a hash where the following keys are defined:
	file_path has a value which is a string


=end text

=item Description



=back

=cut

 sub tree_to_newick_file
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function tree_to_newick_file (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to tree_to_newick_file:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'tree_to_newick_file');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "TreeUtils.tree_to_newick_file",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'tree_to_newick_file',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method tree_to_newick_file",
					    status_line => $self->{client}->status_line,
					    method_name => 'tree_to_newick_file',
				       );
    }
}
 


=head2 export_tree_newick

  $result = $obj->export_tree_newick($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a TreeUtils.ExportTreeParams
$result is a TreeUtils.ExportTreeOutput
ExportTreeParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a TreeUtils.Tree_id
Tree_id is a string
ExportTreeOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string

</pre>

=end html

=begin text

$params is a TreeUtils.ExportTreeParams
$result is a TreeUtils.ExportTreeOutput
ExportTreeParams is a reference to a hash where the following keys are defined:
	input_ref has a value which is a TreeUtils.Tree_id
Tree_id is a string
ExportTreeOutput is a reference to a hash where the following keys are defined:
	shock_id has a value which is a string


=end text

=item Description



=back

=cut

 sub export_tree_newick
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function export_tree_newick (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to export_tree_newick:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'export_tree_newick');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "TreeUtils.export_tree_newick",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'export_tree_newick',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method export_tree_newick",
					    status_line => $self->{client}->status_line,
					    method_name => 'export_tree_newick',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "TreeUtils.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "TreeUtils.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'export_tree_newick',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method export_tree_newick",
            status_line => $self->{client}->status_line,
            method_name => 'export_tree_newick',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for TreeUtils::TreeUtilsClient\n";
    }
    if ($sMajor == 0) {
        warn "TreeUtils::TreeUtilsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 Tree_id

=over 4



=item Description

@id kb KBaseTrees.Tree


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 GetTreesParams

=over 4



=item Description

tree_refs - (required) list of WS references
included_fields - (optional) subset of tree fields to include


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
tree_refs has a value which is a reference to a list where each element is a string
included_fields has a value which is a reference to a list where each element is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
tree_refs has a value which is a reference to a list where each element is a string
included_fields has a value which is a reference to a list where each element is a string


=end text

=back



=head2 TreeData

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
data has a value which is a KBaseTrees.Tree
info has a value which is a Workspace.object_info

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
data has a value which is a KBaseTrees.Tree
info has a value which is a Workspace.object_info


=end text

=back



=head2 SaveTreesParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
ws_id has a value which is a Workspace.ws_id
trees has a value which is a reference to a list where each element is a Workspace.ObjectSaveData

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
ws_id has a value which is a Workspace.ws_id
trees has a value which is a reference to a list where each element is a Workspace.ObjectSaveData


=end text

=back



=head2 TreeToNewickFileParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_ref has a value which is a TreeUtils.Tree_id
destination_dir has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_ref has a value which is a TreeUtils.Tree_id
destination_dir has a value which is a string


=end text

=back



=head2 TreeToNewickFileOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
file_path has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
file_path has a value which is a string


=end text

=back



=head2 ExportTreeParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
input_ref has a value which is a TreeUtils.Tree_id

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
input_ref has a value which is a TreeUtils.Tree_id


=end text

=back



=head2 ExportTreeOutput

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
shock_id has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
shock_id has a value which is a string


=end text

=back



=cut

package TreeUtils::TreeUtilsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
