function result = test_exp3v2_manifest_contract()
%TEST_EXP3V2_MANIFEST_CONTRACT Check every wrapper manifest field without sim.

scriptDir = fileparts([mfilename('fullpath') '.m']);
source = [fileread(fullfile(scriptDir, 'generate_exp3v2_heldout.m')) ...
    newline fileread(fullfile(scriptDir, 'generate_exp3v2_sentinel.m'))];
harnessManifest = jsondecode(fileread(fullfile(scriptDir, ...
    'EXP3_V2_HARNESS_FREEZE_MANIFEST.json')));
finalManifest = jsondecode(fileread(fullfile(scriptDir, ...
    'EXP3_V2_FREEZE_MANIFEST.json')));
tokens = regexp(source, ...
    '(?:freezeManifest|harnessManifest)\.([A-Za-z0-9_]+)', 'tokens');
required = unique(cellfun(@(x) x{1}, tokens, 'UniformOutput', false));
available = union(fieldnames(harnessManifest), fieldnames(finalManifest));
missing = setdiff(required, available);
assert(isempty(missing), 'EXP3V2:ManifestContract', ...
    'Manifest fields missing: %s', strjoin(missing, ', '));
result = true;
fprintf('PASS: V2 generator/manifest field contract complete; sim not called.\n');
end
