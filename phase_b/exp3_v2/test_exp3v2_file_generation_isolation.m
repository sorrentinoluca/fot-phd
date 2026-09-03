function result = test_exp3v2_file_generation_isolation()
%TEST_EXP3V2_FILE_GENERATION_ISOLATION Test isolation and guaranteed restore.

scriptDir = fileparts([mfilename('fullpath') '.m']);
repoRoot = fileparts(fileparts(scriptDir));
sourceDir = fullfile(repoRoot, 'tep_parent_a0413e16', 'simulator');
beforeConfig = Simulink.fileGenControl('getConfig');
beforePath = path;
throwawayRoot = tempname;
mkdir(throwawayRoot);
directoryGuard = onCleanup(@() remove_directory(throwawayRoot));

[guard, state] = configure_exp3v2_file_generation( ...
    throwawayRoot, repoRoot, sourceDir); %#ok<ASGLU>
observed = Simulink.fileGenControl('getConfig');
assert(is_within(canonical_path(observed.CacheFolder), ...
    canonical_path(throwawayRoot)) && ...
    is_within(canonical_path(observed.CodeGenFolder), ...
    canonical_path(throwawayRoot)), ...
    'EXP3V2:FileGenRegressionIsolation', ...
    'File-generation directories are not inside the throwaway root.');
restore_exp3v2_file_generation(state);
clear guard state;
assert_configuration(beforeConfig, beforePath);

exercise_cleanup(throwawayRoot, repoRoot, sourceDir);
assert_configuration(beforeConfig, beforePath);
clear directoryGuard;
result = true;
fprintf(['PASS: Simulink cache/codegen isolation and guaranteed restore; ' ...
    'sim not called.\n']);
end

function exercise_cleanup(throwawayRoot, repoRoot, sourceDir)
try
    guard = configure_exp3v2_file_generation( ...
        throwawayRoot, repoRoot, sourceDir); %#ok<NASGU>
    error('EXP3V2:InjectedFileGenFailure', 'Injected failure.');
catch exception
    assert(strcmp(exception.identifier, 'EXP3V2:InjectedFileGenFailure'), ...
        'EXP3V2:FileGenWrongInjectedFailure', ...
        'Unexpected injected failure: %s', exception.identifier);
end
end

function assert_configuration(expected, expectedPath)
observed = Simulink.fileGenControl('getConfig');
assert(strcmp(char(string(observed.CacheFolder)), ...
    char(string(expected.CacheFolder))) && ...
    strcmp(char(string(observed.CodeGenFolder)), ...
    char(string(expected.CodeGenFolder))) && ...
    isequal(observed.CodeGenFolderStructure, ...
    expected.CodeGenFolderStructure) && strcmp(path, expectedPath), ...
    'EXP3V2:FileGenRegressionRestore', ...
    'File-generation configuration or MATLAB path was not restored.');
end

function remove_directory(pathValue)
if isfolder(pathValue)
    rmdir(pathValue, 's');
end
end

function value = canonical_path(pathValue)
value = char(java.io.File(char(string(pathValue))).getCanonicalPath());
end

function result = is_within(candidate, root)
result = strcmp(candidate, root) || startsWith(candidate, [root filesep]);
end
