function result = test_exp3_stopfcn_management()
%TEST_EXP3_STOPFCN_MANAGEMENT Validate callback management without calling sim.

scriptDir = fileparts([mfilename('fullpath') '.m']);
repoRoot = fileparts(fileparts(scriptDir));
helperPath = fullfile(scriptDir, 'suppress_exp3_plot_stopfcn.m');
assert(isfile(helperPath), 'EXP3:MissingStopFcnHelper', ...
    'StopFcn helper is missing.');

testExpectedCallback();
testUnexpectedCallback();
testEmptyCallback();
testRestoreAfterException();
testPinnedModelUnchanged(repoRoot, scriptDir);

result = true;
fprintf(['PASS: exact callback recognized, unexpected/empty callbacks rejected, ' ...
    'suppression/restoration verified, pinned model byte-identical; sim not called.\n']);
end

function testExpectedCallback()
modelName = unique_model_name('expected');
new_system(modelName);
cleanup = onCleanup(@() close_test_model(modelName));
set_param(modelName, 'StopFcn', 'TEplot');
set_param(modelName, 'Dirty', 'off');
originalDirty = get_param(modelName, 'Dirty');
[guard, state] = suppress_exp3_plot_stopfcn(modelName); %#ok<ASGLU>
assert(strcmp(get_param(modelName, 'StopFcn'), ''), ...
    'EXP3:RegressionSuppression', 'StopFcn was not suppressed.');
restore_exp3_plot_stopfcn(state);
clear guard state;
assert(strcmp(get_param(modelName, 'StopFcn'), 'TEplot'), ...
    'EXP3:RegressionRestore', 'StopFcn was not restored.');
assert(strcmp(get_param(modelName, 'Dirty'), originalDirty), ...
    'EXP3:RegressionDirtyRestore', 'Dirty state was not restored.');
clear cleanup;
end

function testUnexpectedCallback()
modelName = unique_model_name('unexpected');
new_system(modelName);
cleanup = onCleanup(@() close_test_model(modelName));
set_param(modelName, 'StopFcn', 'some_other_callback');
assert_identifier(@() suppress_exp3_plot_stopfcn(modelName), ...
    'EXP3:StopCallbackMismatch');
assert(strcmp(get_param(modelName, 'StopFcn'), 'some_other_callback'), ...
    'EXP3:RegressionUnexpectedChanged', ...
    'Unexpected callback was modified.');
clear cleanup;
end

function testEmptyCallback()
modelName = unique_model_name('empty');
new_system(modelName);
cleanup = onCleanup(@() close_test_model(modelName));
assert_identifier(@() suppress_exp3_plot_stopfcn(modelName), ...
    'EXP3:StopCallbackMismatch');
assert(strcmp(get_param(modelName, 'StopFcn'), ''), ...
    'EXP3:RegressionEmptyChanged', 'Empty callback was modified.');
clear cleanup;
end

function testRestoreAfterException()
modelName = unique_model_name('exception');
new_system(modelName);
cleanup = onCleanup(@() close_test_model(modelName));
set_param(modelName, 'StopFcn', 'TEplot');
set_param(modelName, 'Dirty', 'off');
induce_failure(modelName);
assert(strcmp(get_param(modelName, 'StopFcn'), 'TEplot'), ...
    'EXP3:RegressionExceptionRestore', ...
    'StopFcn was not restored after a controlled exception.');
assert(strcmp(get_param(modelName, 'Dirty'), 'off'), ...
    'EXP3:RegressionExceptionDirtyRestore', ...
    'Dirty state was not restored after a controlled exception.');
clear cleanup;
end

function induce_failure(modelName)
[guard, ~] = suppress_exp3_plot_stopfcn(modelName); %#ok<ASGLU>
assert(strcmp(get_param(modelName, 'StopFcn'), ''), ...
    'EXP3:RegressionSuppression', 'StopFcn was not suppressed.');
failure = MException('EXP3:ControlledRegressionFailure', ...
    'Controlled failure after StopFcn suppression.');
try
    throw(failure);
catch exception
    assert(strcmp(exception.identifier, failure.identifier), ...
        'EXP3:WrongControlledFailure', 'Unexpected controlled failure.');
end
end

function testPinnedModelUnchanged(repoRoot, scriptDir)
simulatorDir = fullfile(repoRoot, 'tep_parent_a0413e16', 'simulator');
modelName = 'MultiLoop_mode1';
modelPath = fullfile(simulatorDir, [modelName '.mdl']);
beforeHash = sha256_file(modelPath);
originalPath = path;
originalDir = pwd;
cleanup = onCleanup(@() restore_environment( ...
    originalPath, originalDir, modelName));
addpath(scriptDir, '-begin');
addpath(simulatorDir, '-begin');
cd(simulatorDir);
close_test_model(modelName);
load_system(modelName);
assert(strcmp(get_param(modelName, 'StopFcn'), 'TEplot'), ...
    'EXP3:PinnedModelStopFcnMismatch', ...
    'Pinned model StopFcn is not exactly TEplot.');
originalDirty = get_param(modelName, 'Dirty');
[guard, state] = suppress_exp3_plot_stopfcn(modelName); %#ok<ASGLU>
assert(strcmp(get_param(modelName, 'StopFcn'), ''), ...
    'EXP3:PinnedModelSuppression', 'Pinned model callback was not suppressed.');
restore_exp3_plot_stopfcn(state);
clear guard state;
assert(strcmp(get_param(modelName, 'StopFcn'), 'TEplot'), ...
    'EXP3:PinnedModelRestore', 'Pinned model callback was not restored.');
assert(strcmp(get_param(modelName, 'Dirty'), originalDirty), ...
    'EXP3:PinnedModelDirtyRestore', ...
    'Pinned model Dirty state was not restored.');
close_system(modelName, 0);
assert(strcmp(sha256_file(modelPath), beforeHash), ...
    'EXP3:PinnedModelHashChanged', ...
    'Pinned model file changed during callback-management test.');
clear cleanup;
end

function name = unique_model_name(suffix)
name = ['exp3_stopfcn_' suffix '_' char(java.util.UUID.randomUUID())];
name = strrep(name, '-', '_');
end

function assert_identifier(operation, expectedIdentifier)
observed = '';
try
    operation();
catch exception
    observed = exception.identifier;
end
assert(strcmp(observed, expectedIdentifier), 'EXP3:RegressionIdentifier', ...
    'Expected %s, observed %s.', expectedIdentifier, observed);
end

function restore_environment(originalPath, originalDir, modelName)
close_test_model(modelName);
path(originalPath);
cd(originalDir);
end

function close_test_model(modelName)
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end
end

function digestHex = sha256_file(filePath)
fid = fopen(filePath, 'rb');
assert(fid ~= -1, 'EXP3:HashInputOpen', 'Cannot open %s.', filePath);
cleanup = onCleanup(@() fclose(fid));
bytes = fread(fid, Inf, 'uint8=>uint8');
digest = java.security.MessageDigest.getInstance('SHA-256');
digest.update(bytes);
raw = typecast(digest.digest(), 'uint8');
digestHex = lower(reshape(dec2hex(raw, 2).', 1, []));
end
