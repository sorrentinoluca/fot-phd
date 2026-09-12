function generate_normal_runs(planPath, outputDir)
% Execute an explicit Normal-run plan and append a provenance manifest.

arguments
    planPath (1,1) string
    outputDir (1,1) string
end

thisDir = fileparts(mfilename('fullpath'));
phaseDir = fileparts(fileparts(thisDir));
repoRoot = fileparts(fileparts(phaseDir));
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
required = ["run_id", "set_name", "stream_id", "stop_time_h", "burn_in_h", "window_position"];
if ~all(ismember(required, string(plan.Properties.VariableNames)))
    error('Plan is missing required columns.');
end
if numel(unique(plan.stream_id)) ~= height(plan)
    if any(plan.set_name ~= "prefix_qual")
        error('Repeated stream_id is allowed only for prefix_qual.');
    end
    streams = unique(plan.stream_id);
    if numel(streams) ~= 10
        error('prefix_qual requires exactly ten distinct streams.');
    end
    for streamIndex = 1:numel(streams)
        positions = sort(plan.window_position(plan.stream_id == streams(streamIndex)));
        if ~isequal(positions(:), (0:10)')
            error('Each prefix_qual stream requires positions 0 through 10 exactly once.');
        end
    end
end

buildDir = fullfile(fileparts(thisDir), 'build');
Simulink.fileGenControl('set', 'CacheFolder', buildDir, 'CodeGenFolder', buildDir);
addpath(buildDir, '-begin');
addpath(thisDir, '-begin');
modelName = 'MultiLoop_mode1';
load_system(fullfile(thisDir, [modelName '.mdl']));
cleanupModel = onCleanup(@() close_system(modelName, 0));
set_param(modelName, 'Solver', 'ode45');
set_param(modelName, 'StopFcn', '');
modelPath = string(get_param(modelName, 'FileName'));
mexPath = string(which('temexd_philox'));
if strlength(mexPath) == 0
    error('temexd_philox MEX is not available on the controlled path.');
end
modelSha256 = string(sha256_file(modelPath));
mexSha256 = string(sha256_file(mexPath));
rngAlgorithm = "Philox4x32-10";
rngKeyHex = "0x464f545445503032";
outputIntervalH = 1/60;

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
    fot_stream_id = plan.stream_id(rowIndex);
    if fot_stream_id < 0 || fix(fot_stream_id) ~= fot_stream_id || fot_stream_id > 2^53 - 1
        error('Invalid exact stream_id for %s', runId);
    end
    assignin('base', 'Ts_base', Ts_base);
    assignin('base', 'fot_stream_id', fot_stream_id);
    assignin('base', 'dist', zeros(1, 28));
    evalin('base', 'clear fot_draw_counter_end');
    set_param(modelName, 'StopTime', sprintf('%.17g', plan.stop_time_h(rowIndex)));

    startedAt = datetime('now', 'TimeZone', 'UTC');
    sim(modelName);
    finishedAt = datetime('now', 'TimeZone', 'UTC');
    if ~evalin('base', 'exist(''fot_draw_counter_end'', ''var'')')
        error('The S-function did not export its final Philox draw counter.');
    end
    counterEnd = evalin('base', 'fot_draw_counter_end');
    dataToSave = [tout, simout, xmv];
    actualEndH = dataToSave(end, 1);
    if actualEndH < plan.stop_time_h(rowIndex) - 1e-9
        error('Normal run %s stopped at %.17g h before requested %.17g h.', ...
            runId, actualEndH, plan.stop_time_h(rowIndex));
    end
    temporaryPath = outputPath + ".tmp.xlsx";
    if isfile(temporaryPath)
        error('Refusing to overwrite temporary output: %s', temporaryPath);
    end
    writecell(headers, temporaryPath, 'Sheet', 1, 'Range', 'A1');
    writematrix(dataToSave, temporaryPath, 'Sheet', 1, 'Range', 'A2');
    movefile(temporaryPath, outputPath, 'f');

    digest = sha256_file(outputPath);
    status = "complete";
    counterStart = uint64(0);
    runtimeSeconds = seconds(finishedAt - startedAt);
    record = table(runId, plan.set_name(rowIndex), fot_stream_id, ...
        rngAlgorithm, rngKeyHex, counterStart, counterEnd, mexSha256, ...
        modelSha256, Ts_base, outputIntervalH, ...
        plan.stop_time_h(rowIndex), plan.burn_in_h(rowIndex), ...
        plan.window_position(rowIndex), actualEndH, status, ...
        startedAt, finishedAt, runtimeSeconds, ...
        string(outputPath), string(digest), size(dataToSave, 1), size(dataToSave, 2), ...
        'VariableNames', {'run_id','set_name','stream_id','rng_algorithm', ...
        'rng_key_hex','counter_start','counter_end','mex_sha256','model_sha256', ...
        'ts_base_h','output_interval_h','stop_time_h','burn_in_h','window_position', ...
        'actual_end_h','status','started_at_utc','finished_at_utc','runtime_seconds', ...
        'output_path','sha256','data_rows','columns'});
    records = [records; record]; %#ok<AGROW>
end

writetable(records, manifestPath);
fprintf('Generated %d runs; manifest: %s\n', height(records), manifestPath);
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
