function dependencies = assert_exp3v2_runtime_bundle(runtimeDir, manifest)
%ASSERT_EXP3V2_RUNTIME_BUNDLE Verify the exact materialized external bundle.

runtimeDir = char(java.io.File(char(string(runtimeDir))).getCanonicalPath());
assert(isfolder(runtimeDir) && ~is_symlink(runtimeDir), ...
    'EXP3V2:RuntimeBundleDirectory', ...
    'Materialized runtime directory is missing or is a symlink.');
assert(isfield(manifest, 'external_runtime_dependencies'), ...
    'EXP3V2:RuntimeDependencyManifest', ...
    'Harness manifest has no external runtime dependency inventory.');
dependencies = manifest.external_runtime_dependencies;
expectedPaths = sort({dependencies.path});
pinnedPaths = sort({'Mode1xInitial.mat', 'Mode_1_Init.m', ...
    'MultiLoop_mode1.mdl', 'TElib.mdl', 'TEplot.m', ...
    'temexd_mod.c', 'temexd_mod.mexmaca64', 'teprob_mod.h'});
assert(isequal(expectedPaths(:), pinnedPaths(:)), ...
    'EXP3V2:RuntimeDependencyAllowlist', ...
    'External runtime manifest has missing or extra required files.');
actualPaths = recursive_relative_files(runtimeDir);
assert(isequal(expectedPaths(:), actualPaths(:)), ...
    'EXP3V2:RuntimeBundleFileSet', ...
    'Materialized runtime bundle has missing or extra files.');

for index = 1:numel(dependencies)
    dependency = dependencies(index);
    dependencyPath = fullfile(runtimeDir, dependency.path);
    assert(isfile(dependencyPath) && ~is_symlink(dependencyPath), ...
        'EXP3V2:RuntimeDependencyMissing', ...
        'Missing regular runtime dependency: %s', dependency.path);
    info = dir(dependencyPath);
    assert(info.bytes == dependency.size_bytes, ...
        'EXP3V2:RuntimeDependencySize', ...
        'Runtime dependency size mismatch: %s', dependency.path);
    assert(strcmp(sha256_file(dependencyPath), dependency.sha256), ...
        'EXP3V2:RuntimeDependencyHash', ...
        'Runtime dependency hash mismatch: %s', dependency.path);
end
end

function paths = recursive_relative_files(root)
entries = dir(fullfile(root, '**', '*'));
paths = {};
for index = 1:numel(entries)
    if entries(index).isdir
        continue;
    end
    path = fullfile(entries(index).folder, entries(index).name);
    assert(~is_symlink(path), 'EXP3V2:RuntimeDependencySymlink', ...
        'Runtime bundle contains a symlink: %s', path);
    prefix = [root filesep];
    paths{end + 1} = strrep(path(numel(prefix) + 1:end), filesep, '/'); %#ok<AGROW>
end
paths = sort(paths);
end

function result = is_symlink(path)
emptyNames = javaArray('java.lang.String', 0);
javaPath = java.nio.file.Paths.get(char(string(path)), emptyNames);
result = java.nio.file.Files.isSymbolicLink(javaPath);
end

function digestHex = sha256_file(path)
fid = fopen(path, 'rb');
assert(fid ~= -1, 'EXP3V2:RuntimeHashOpen', ...
    'Cannot open runtime dependency: %s', path);
cleanup = onCleanup(@() fclose(fid));
bytes = fread(fid, Inf, 'uint8=>uint8');
digest = java.security.MessageDigest.getInstance('SHA-256');
digest.update(bytes);
raw = typecast(digest.digest(), 'uint8');
digestHex = lower(reshape(dec2hex(raw, 2).', 1, []));
end
