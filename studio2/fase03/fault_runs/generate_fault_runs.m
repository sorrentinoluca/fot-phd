function generate_fault_runs(planPath, outputDir)
% Explicit approved plan, exclusively new campaign, immutable per-attempt manifests.
arguments
    planPath (1,1) string
    outputDir (1,1) string
end
here = string(fileparts(mfilename('fullpath')));
repo = string(fileparts(fileparts(fileparts(here))));
phase02 = fullfile(repo, 'studio2', 'fase02', 'simulator');
matlabDir = fullfile(phase02, 'matlab');
planPath = canonical(planPath);
outputDir = canonical(outputDir);
protocol = fullfile(here, 'fault_protocol.py');
runPython(protocol, "preflight " + shellq(planPath) + " " + shellq(outputDir));
% mkdir() in Java returns false if already present: exclusive campaign claim.
parent = fileparts(outputDir);
if ~isfolder(parent), mkdir(parent); end
claim = java.io.File(char(outputDir));
if ~claim.mkdir(), error('Refusing existing/racing campaign destination: %s', outputDir); end
cacheDir = fullfile(outputDir, 'cache');
mkdir(cacheDir);
Simulink.fileGenControl('set', 'CacheFolder', cacheDir, 'CodeGenFolder', cacheDir);
% uint64 identities are re-read as text; the MEX accepts exact doubles <= 2^53-1.
opts = detectImportOptions(planPath, 'TextType', 'string');
opts = setvartype(opts, {'run_index_uint64', 'stream_id', 'seed_descriptor'}, 'string');
plan = readtable(planPath, opts);
addpath(fullfile(here, 'runtime', 'build'), '-begin');
addpath(matlabDir, '-begin');
model = 'MultiLoop_mode1';
if bdIsLoaded(model), error('Model is already loaded; launch in a fresh MATLAB process.'); end
load_system(fullfile(matlabDir, [model '.mdl']));
cleanupModel = onCleanup(@() close_system(model, 0));
sfun = find_system(model, 'LookUnderMasks','all', 'FollowLinks','off', ...
    'BlockType','S-Function','FunctionName','temexd_philox');
if numel(sfun) ~= 1, error('Expected exactly one qualified S-function'); end
set_param(sfun{1}, 'FunctionName','temexd_fault_philox', 'Parameters','[] fot_stream_id 0');
set_param([model '/Constant'], 'Value','25');
delay = find_system(model, 'BlockType','VariableTransportDelay');
if numel(delay) ~= 1, error('Expected exactly one fault delay'); end
set_param(delay{1}, 'MaximumDelay','25');
set_param(model, 'Solver','ode45', 'StopFcn','');
mexPath = string(which('temexd_fault_philox'));
expectedMex = canonical(fullfile(here,'runtime','build', ['temexd_fault_philox.' mexext]));
if canonical(mexPath) ~= expectedMex, error('MEX path is not the controlled build'); end
modelPath = canonical(string(get_param(model, 'FileName')));
if modelPath ~= canonical(fullfile(matlabDir,[model '.mdl'])), error('Unexpected model path'); end
sourcePath = fullfile(here,'runtime','source','temexd_fault_philox.c');
baseSource = fullfile(phase02,'source','temexd_philox.c');
scriptPath = string(mfilename('fullpath')) + '.m';
specPath = fullfile(here,'SPECIFICA_RUN_FAULT.md');
[gitStatus, gitHead] = system('git -C ' + shellq(repo) + ' rev-parse HEAD');
if gitStatus ~= 0, error('Cannot record git commit'); end
hashes = struct('mex_sha256',sha256(mexPath), 'model_sha256',sha256(modelPath), ...
    'script_sha256',sha256(scriptPath), 'source_sha256',sha256(sourcePath), ...
    'base_source_sha256',sha256(baseSource), 'plan_sha256',sha256(planPath), ...
    'spec_sha256',sha256(specPath));
audit = jsondecode(fileread(fullfile(here,'SOURCE_AUDIT.json')));
depPaths = [string({audit.files.path}), ...
    "studio2/fase03/fault_runs/prepare_simulator.py", ...
    "studio2/fase03/fault_runs/fault_protocol.py", ...
    "studio2/fase03/fault_runs/build_generation_plan.py", ...
    "studio2/fase03/fault_runs/compile_fault_philox.m", ...
    "studio2/fase02/simulator/matlab/TElib.mdl", ...
    "studio2/fase02/simulator/matlab/tesys.mdl"];
dependencies = struct('path',{},'sha256',{});
for i=1:numel(depPaths)
    dependencies(i).path = char(depPaths(i));
    dependencies(i).sha256 = sha256(fullfile(repo,depPaths(i)));
end
modelOverrides = struct('sfunction_name','temexd_fault_philox','sfunction_parameters','[] fot_stream_id 0', ...
    'fault_delay_h',25,'maximum_delay_h',25,'solver','ode45','stop_fcn','', ...
    'ts_base_h',0.0005,'ts_save_h',1/60,'setpoints_changed',false);
% Record values exactly as used. No save_system: base model bytes remain untouched.
events = fullfile(outputDir,'events.jsonl');
event(events,'campaign_start','',struct('plan_sha256',hashes.plan_sha256,'expected_runs',height(plan)));
failed = false;
headers = [{'Time (h)'}, arrayfun(@(i)sprintf('XMEAS-%d',i),1:41,'UniformOutput',false), ...
    arrayfun(@(i)sprintf('XMV-%d',i),1:12,'UniformOutput',false)];
for k=1:height(plan)
    row = table2struct(plan(k,:));
    id = string(row.run_id);
    started = stamp();
    event(events,'run_start',id,struct('stream_id',row.stream_id,'idv',row.idv));
    assignin('base','Ts_base',0.0005);
    assignin('base','Ts_save',1/60);
    assignin('base','fot_stream_id',str2double(row.stream_id));
    dist = zeros(1,28); dist(row.idv) = 1;
    assignin('base','dist',dist);
    evalin('base','clear fot_draw_counter_end');
    set_param(model,'StopTime',sprintf('%.17g',row.stop_time_h));
    rawPath = fullfile(outputDir,id+'.csv');
    logPath = fullfile(outputDir,id+'.simulation.log');
    metaPath = fullfile(outputDir,id+'.attempt.json');
    sim_error = []; simResult = []; elapsed = tic;
    simtext = evalc('try; simResult = sim(model, ''ReturnWorkspaceOutputs'',''on''); catch sim_error; end');
    simulationSeconds = toc(elapsed);
    writeNewText(logPath,simtext);
    errtext = '';
    counterEnd = [];
    if ~isempty(sim_error)
        errtext = getReport(sim_error,'extended','hyperlinks','off');
    else
        try
            data = [simResult.get('tout'),simResult.get('simout'),simResult.get('xmv')];
            writeRaw(rawPath, headers, data);
        catch outputError
            errtext = getReport(outputError,'extended','hyperlinks','off');
        end
    end
    if evalin('base','exist(''fot_draw_counter_end'',''var'')')
        counterEnd = sprintf('%u',evalin('base','fot_draw_counter_end'));
    end
    if sha256(mexPath) ~= string(hashes.mex_sha256) || sha256(modelPath) ~= string(hashes.model_sha256) || ...
       sha256(scriptPath) ~= string(hashes.script_sha256) || sha256(planPath) ~= string(hashes.plan_sha256)
        errtext = 'Dependency changed during simulation';
    end
    meta = hashes;
    meta.plan_row = row;
    meta.platform = struct('computer',computer,'architecture',computer('arch'),'mexext',mexext);
    meta.matlab_version = version;
    meta.git_commit = strtrim(gitHead);
    meta.started_at_utc = started;
    meta.simulation_seconds = simulationSeconds;
    meta.counter_end = counterEnd;
    meta.dependency_hashes = dependencies;
    meta.model_overrides = modelOverrides;
    meta.technical_error = errtext;
    writeNewText(metaPath,jsonencode(meta));
    runPython(protocol, 'finalize ' + shellq(metaPath));
    record = jsondecode(fileread(fullfile(outputDir,id+'.manifest.json')));
    event(events,'run_end',id,struct('status',record.status,'runtime_seconds',record.runtime_seconds));
    if strcmp(record.status,'technical_failure'), failed=true; break; end
end
runPython(protocol, 'finish ' + shellq(planPath) + ' ' + shellq(outputDir));
event(events,'campaign_end','',struct('technical_failure',failed,'expected_runs',height(plan)));
runPython(protocol, 'audit ' + shellq(planPath) + ' ' + shellq(outputDir));
fprintf('[%s] FAULT_CAMPAIGN_COMPLETE manifests=%d destination=%s\n',stamp(),height(plan),outputDir);
end

function value = canonical(path)
value = string(java.io.File(char(path)).getCanonicalPath());
end
function s = shellq(s)
q=string(char(39)); d=string(char(34));
s=q+replace(string(s),q,q+d+q+d+q)+q;
end
function runPython(script,arguments)
[code,output]=system('python3 '+shellq(script)+' '+arguments);
fprintf('%s',output);
if code~=0, error('Fault protocol helper failed: %s', output); end
end
function s = stamp()
s=char(datetime('now','TimeZone','UTC','Format',"yyyy-MM-dd'T'HH:mm:ss.SSSXXX"));
end
function writeNewText(path,text)
f=java.io.File(char(path));
if ~f.createNewFile(), error('Refusing overwrite: %s',path); end
fid=fopen(path,'w');
if fid<0, error('Cannot open new file: %s',path); end
c=onCleanup(@()fclose(fid));
fprintf(fid,'%s',text);
end
function writeRaw(path,headers,data)
f=java.io.File(char(path));
if ~f.createNewFile(), error('Refusing overwrite: %s',path); end
fid=fopen(path,'w');
if fid<0, error('Cannot open new output'); end
c=onCleanup(@()fclose(fid));
fprintf(fid,'%s\n',strjoin(headers,','));
format = [repmat('%.17g,',1,size(data,2)-1) '%.17g\n'];
fprintf(fid,format,data');
end
function event(path,name,runId,details)
e=struct('timestamp_utc',stamp(),'event',name,'run_id',char(runId),'details',details);
fid=fopen(path,'a');
if fid<0, error('Cannot append event log'); end
c=onCleanup(@()fclose(fid));
fprintf(fid,'%s\n',jsonencode(e));
fprintf('[%s] %s %s\n',e.timestamp_utc,name,runId);
end
function result = sha256(path)
md=java.security.MessageDigest.getInstance('SHA-256');
s=java.io.FileInputStream(char(path));
d=java.security.DigestInputStream(s,md);
c=onCleanup(@()d.close());
buffer=zeros(1,1024*1024,'int8');
while d.read(buffer,0,numel(buffer))>=0
end
result=lower(reshape(dec2hex(typecast(md.digest(),'uint8'),2).',1,[]));
end
