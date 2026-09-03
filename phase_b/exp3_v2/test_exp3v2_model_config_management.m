function result = test_exp3v2_model_config_management()
%TEST_EXP3V2_MODEL_CONFIG_MANAGEMENT Test guarded changes without sim.

testExpectedValues();
testUnexpectedStopFcn();
testUnexpectedReturnWorkspaceOutputs();
testRestoreAfterException();
testPinnedModelByteIdentity();
result = true;
fprintf(['PASS: V2 StopFcn/ReturnWorkspaceOutputs/Dirty restoration and ' ...
    'model byte identity verified; sim not called.\n']);
end

function testExpectedValues()
name = new_test_model('expected');
cleanup = onCleanup(@() close_test_model(name));
set_param(name, 'StopFcn', 'TEplot', 'ReturnWorkspaceOutputs', 'off', ...
    'Dirty', 'off');
[guard, state] = configure_exp3v2_model(name); %#ok<ASGLU>
assert(strcmp(get_param(name, 'StopFcn'), '') && ...
    strcmp(get_param(name, 'ReturnWorkspaceOutputs'), 'on'), ...
    'EXP3V2:RegressionConfig', 'Temporary configuration failed.');
restore_exp3v2_model_config(state);
clear guard state;
assert(strcmp(get_param(name, 'StopFcn'), 'TEplot') && ...
    strcmp(get_param(name, 'ReturnWorkspaceOutputs'), 'off') && ...
    strcmp(get_param(name, 'Dirty'), 'off'), ...
    'EXP3V2:RegressionRestore', 'Configuration restoration failed.');
clear cleanup;
end

function testUnexpectedStopFcn()
name = new_test_model('stopfcn');
cleanup = onCleanup(@() close_test_model(name));
set_param(name, 'StopFcn', 'other', 'ReturnWorkspaceOutputs', 'off');
assert_identifier(@() configure_exp3v2_model(name), ...
    'EXP3V2:StopCallbackMismatch');
clear cleanup;
end

function testUnexpectedReturnWorkspaceOutputs()
name = new_test_model('returnoutputs');
cleanup = onCleanup(@() close_test_model(name));
set_param(name, 'StopFcn', 'TEplot', 'ReturnWorkspaceOutputs', 'on');
assert_identifier(@() configure_exp3v2_model(name), ...
    'EXP3V2:ReturnWorkspaceOutputsMismatch');
clear cleanup;
end

function testRestoreAfterException()
name = new_test_model('exception');
cleanup = onCleanup(@() close_test_model(name));
set_param(name, 'StopFcn', 'TEplot', 'ReturnWorkspaceOutputs', 'off', ...
    'Dirty', 'off');
induce_failure(name);
assert(strcmp(get_param(name, 'StopFcn'), 'TEplot') && ...
    strcmp(get_param(name, 'ReturnWorkspaceOutputs'), 'off') && ...
    strcmp(get_param(name, 'Dirty'), 'off'), ...
    'EXP3V2:RegressionExceptionRestore', ...
    'Cleanup did not restore configuration after exception.');
clear cleanup;
end

function induce_failure(name)
[guard, ~] = configure_exp3v2_model(name); %#ok<ASGLU>
errorObject = MException('EXP3V2:InjectedFailure', 'Injected test failure.');
try
    throw(errorObject);
catch exception
    assert(strcmp(exception.identifier, 'EXP3V2:InjectedFailure'), ...
        'EXP3V2:WrongInjectedFailure', 'Unexpected injected failure.');
end
end

function testPinnedModelByteIdentity()
scriptDir = fileparts([mfilename('fullpath') '.m']);
repoRoot = fileparts(fileparts(scriptDir));
simulatorDir = fullfile(repoRoot, 'tep_parent_a0413e16', 'simulator');
modelPath = fullfile(simulatorDir, 'MultiLoop_mode1.mdl');
before = sha256_file(modelPath);
originalPath = path;
originalDir = pwd;
cleanup = onCleanup(@() restore_environment(originalPath, originalDir));
addpath(scriptDir, '-begin');
addpath(simulatorDir, '-begin');
cd(simulatorDir);
close_test_model('MultiLoop_mode1');
load_system('MultiLoop_mode1');
[guard, state] = configure_exp3v2_model('MultiLoop_mode1'); %#ok<ASGLU>
restore_exp3v2_model_config(state);
clear guard state;
close_system('MultiLoop_mode1', 0);
assert(strcmp(before, sha256_file(modelPath)), ...
    'EXP3V2:PinnedModelChanged', 'Pinned model bytes changed.');
clear cleanup;
end

function name = new_test_model(suffix)
name = ['exp3v2_' suffix '_' char(java.util.UUID.randomUUID())];
name = strrep(name, '-', '_');
new_system(name);
end

function assert_identifier(operation, expected)
observed = '';
try
    operation();
catch exception
    observed = exception.identifier;
end
assert(strcmp(observed, expected), 'EXP3V2:RegressionIdentifier', ...
    'Expected %s, observed %s.', expected, observed);
end

function restore_environment(originalPath, originalDir)
close_test_model('MultiLoop_mode1');
path(originalPath);
cd(originalDir);
end

function close_test_model(name)
if bdIsLoaded(name)
    close_system(name, 0);
end
end

function digestHex = sha256_file(filePath)
fid = fopen(filePath, 'rb');
assert(fid ~= -1, 'EXP3V2:HashOpen', 'Cannot open %s.', filePath);
cleanup = onCleanup(@() fclose(fid));
bytes = fread(fid, Inf, 'uint8=>uint8');
digest = java.security.MessageDigest.getInstance('SHA-256');
digest.update(bytes);
raw = typecast(digest.digest(), 'uint8');
digestHex = lower(reshape(dec2hex(raw, 2).', 1, []));
end
