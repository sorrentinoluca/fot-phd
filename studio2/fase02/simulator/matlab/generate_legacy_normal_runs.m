function generate_legacy_normal_runs(planPath, outputDir)
% Generate explicit, seeded legacy Normal runs without modifying source files.

arguments
    planPath (1,1) string
    outputDir (1,1) string
end

thisDir = fileparts(mfilename('fullpath'));
phaseDir = fileparts(fileparts(thisDir));
repoRoot = fileparts(fileparts(phaseDir));
legacyDir = fullfile(repoRoot, 'tep_parent_a0413e16', 'simulator');
allowedRoot = fullfile(repoRoot, 'studio2');
outputDir = char(java.io.File(char(outputDir)).getCanonicalPath());
allowedRoot = char(java.io.File(allowedRoot).getCanonicalPath());
if ~(strcmp(outputDir, allowedRoot) || startsWith(outputDir, [allowedRoot filesep]))
    error('Output directory must remain under studio2/: %s', outputDir);
end
if ~isfile(planPath)
    error('Generation plan not found: %s', planPath);
end
if ~isfolder(outputDir)
    mkdir(outputDir);
end

plan = readtable(planPath, 'TextType', 'string');
required = ["run_id", "set_name", "stream_id", "legacy_seed", ...
    "stop_time_h", "burn_in_h", "window_position"];
if ~all(ismember(required, string(plan.Properties.VariableNames)))
    error('Plan is missing required columns.');
end
if any(plan.set_name ~= "legacy_generator_qual")
    error('This launcher accepts only legacy_generator_qual plans.');
end
if numel(unique(plan.legacy_seed)) ~= height(plan)
    error('Every row must have a distinct legacy seed.');
end
if any(plan.legacy_seed <= 0 | plan.legacy_seed >= 2147483647 | ...
        fix(plan.legacy_seed) ~= plan.legacy_seed)
    error('Legacy seeds must be exact integers in [1, 2147483646].');
end

buildDir = fullfile(phaseDir, 'simulator', 'build', 'legacy');
if ~isfolder(buildDir)
    mkdir(buildDir);
end
Simulink.fileGenControl('set', 'CacheFolder', buildDir, 'CodeGenFolder', buildDir);
addpath(legacyDir, '-begin');
modelName = 'MultiLoop_mode1';
load_system(fullfile(legacyDir, [modelName '.mdl']));
cleanupModel = onCleanup(@() close_system(modelName, 0));
set_param(modelName, 'Solver', 'ode45');
set_param(modelName, 'StopFcn', '');
set_param(modelName, 'StopTime', '70');

manifestPath = fullfile(outputDir, 'generation_manifest.csv');
if isfile(manifestPath)
    error('Refusing to append to an existing campaign manifest: %s', manifestPath);
end

headers = [{'Time (h)'}, ...
    arrayfun(@(i) sprintf('XMEAS-%d', i), 1:41, 'UniformOutput', false), ...
    arrayfun(@(i) sprintf('XMV-%d', i), 1:12, 'UniformOutput', false)];
records = table();

for rowIndex = 1:height(plan)
    runId = plan.run_id(rowIndex);
    if isempty(regexp(runId, '^[A-Za-z0-9_-]+$', 'once'))
        error('Unsafe run_id: %s', runId);
    end
    outputPath = fullfile(outputDir, runId + ".xlsx");
    if isfile(outputPath)
        error('Refusing to overwrite existing run: %s', outputPath);
    end

    Ts_base = 0.0005;
    legacySeed = plan.legacy_seed(rowIndex);
    assignin('base', 'Ts_base', Ts_base);
    assignin('base', 'dist', zeros(1, 28));
    set_param([modelName '/TE Plant/TE Code'], 'Parameters', ...
        sprintf('[] %.17g 0', legacySeed));
    set_param(modelName, 'StopTime', sprintf('%.17g', plan.stop_time_h(rowIndex)));

    startedAt = datetime('now', 'TimeZone', 'UTC');
    sim(modelName);
    finishedAt = datetime('now', 'TimeZone', 'UTC');
    dataToSave = [tout, simout, xmv];
    temporaryPath = outputPath + ".tmp.xlsx";
    if isfile(temporaryPath)
        error('Refusing to overwrite temporary output: %s', temporaryPath);
    end
    writecell(headers, temporaryPath, 'Sheet', 1, 'Range', 'A1');
    writematrix(dataToSave, temporaryPath, 'Sheet', 1, 'Range', 'A2');
    movefile(temporaryPath, outputPath, 'f');

    digest = sha256_file(outputPath);
    record = table(runId, plan.set_name(rowIndex), plan.stream_id(rowIndex), ...
        legacySeed, plan.stop_time_h(rowIndex), plan.burn_in_h(rowIndex), ...
        startedAt, finishedAt, string(outputPath), string(digest), ...
        size(dataToSave, 1), size(dataToSave, 2), ...
        'VariableNames', {'run_id','set_name','comparison_pair_id','legacy_seed', ...
        'stop_time_h','burn_in_h','started_at_utc','finished_at_utc', ...
        'output_path','sha256','data_rows','columns'});
    records = [records; record]; %#ok<AGROW>
end

writetable(records, manifestPath);
fprintf('Generated %d seeded legacy runs; manifest: %s\n', height(records), manifestPath);
end

function digest = sha256_file(path)
md = java.security.MessageDigest.getInstance('SHA-256');
stream = java.io.FileInputStream(char(path));
digestStream = java.security.DigestInputStream(stream, md);
cleanupStream = onCleanup(@() digestStream.close());
buffer = zeros(1, 1024 * 1024, 'int8');
while true
    count = digestStream.read(buffer, 0, numel(buffer));
    if count < 0
        break;
    end
end
digest = lower(reshape(dec2hex(typecast(md.digest(), 'uint8'), 2).', 1, []));
end
