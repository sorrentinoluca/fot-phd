function result = validate_exp3_rng_runtime(varargin)
%VALIDATE_EXP3_RNG_RUNTIME Reproduce the sentinel-only RNG plumbing probe.
%
% This is a technical validation utility, not an Experiment 3 generator. It
% uses two sentinel seeds outside the Experiment 3 allocation, keeps numeric
% outputs in memory, and performs no feature extraction or diagnosis.

parser = inputParser;
parser.addParameter('SimulatorDir', '', @(x) ischar(x) || isstring(x));
parser.parse(varargin{:});

scriptDir = fileparts([mfilename('fullpath') '.m']);
repoRoot = fileparts(fileparts(scriptDir));
simulatorDir = char(string(parser.Results.SimulatorDir));
if strlength(string(simulatorDir)) == 0
    simulatorDir = fullfile(repoRoot, 'tep_parent_a0413e16', 'simulator');
end

sameSeed = 987654321;
differentSeed = 123456789;
assert(all(~ismember([sameSeed differentSeed], 310001:310030)), ...
    'EXP3:RngProbeSeedCollision', ...
    'Sentinel seeds must remain outside the Experiment 3 allocation.');

runtime = capture_runtime();
first = run_sentinel(simulatorDir, sameSeed);
second = run_sentinel(simulatorDir, sameSeed);
different = run_sentinel(simulatorDir, differentSeed);

sameEqual = isequal(first.numeric_output, second.numeric_output);
sameMaxDifference = max(abs(first.numeric_output(:) - second.numeric_output(:)));
differentEqual = isequal(first.numeric_output, different.numeric_output);
differentMaxDifference = max(abs(first.numeric_output(:) - different.numeric_output(:)));

assert(sameEqual && sameMaxDifference == 0, ...
    'EXP3:SameSeedNotReproducible', ...
    'The same sentinel seed did not reproduce exactly.');
assert(~differentEqual && differentMaxDifference > 0, ...
    'EXP3:DifferentSeedNotSensitive', ...
    'Different sentinel seeds produced identical numeric output.');
assert(first.load_system_rng_unchanged && second.load_system_rng_unchanged && ...
    different.load_system_rng_unchanged, 'EXP3:LoadConsumesRandomness', ...
    'load_system or initialization changed the MATLAB RNG state.');
assert(first.sim_consumed_exactly_one_rand && ...
    second.sim_consumed_exactly_one_rand && ...
    different.sim_consumed_exactly_one_rand, 'EXP3:UnexpectedRandomConsumption', ...
    'sim did not consume exactly the S-function parameter rand().');

result = struct( ...
    'runtime', runtime, ...
    'same_seed', sameSeed, ...
    'same_seed_isequal', sameEqual, ...
    'same_seed_max_absolute_difference', sameMaxDifference, ...
    'same_seed_hash', first.output_sha256, ...
    'different_seed', differentSeed, ...
    'different_seed_isequal', differentEqual, ...
    'different_seed_max_absolute_difference', differentMaxDifference, ...
    'different_seed_hash', different.output_sha256, ...
    'preload_callback', first.preload_callback, ...
    'stop_callback', first.stop_callback, ...
    'sfunction_path', first.sfunction_path, ...
    'sfunction_parameters', first.sfunction_parameters, ...
    'load_system_rng_unchanged', true, ...
    'sim_consumed_exactly_one_rand', true);

end

function observed = run_sentinel(simulatorDir, seed)
modelName = 'MultiLoop_mode1';
originalPath = path;
originalDir = pwd;
cleanup = onCleanup(@() cleanup_environment(originalPath, originalDir, modelName));
addpath(simulatorDir, '-begin');
cd(simulatorDir);
rehash;
close_if_loaded(modelName);
close_if_loaded('TElib');
close_if_loaded('tesys');
evalin('base', 'clear tout simout xmv dist');

rng(seed, 'twister');
beforeLoad = rng;
load_system(modelName); % PreLoadFcn -> Mode_1_Init -> load Mode1xInitial.
afterLoad = rng;

modeInit = fileread(fullfile(simulatorDir, 'Mode_1_Init.m'));
teplot = fileread(fullfile(simulatorDir, 'TEplot.m'));
randomCall = '(?<![A-Za-z0-9_])(rand|randn|rng)\s*\(';
assert(isempty(regexp(modeInit, randomCall, 'once')), ...
    'EXP3:ModeInitRandomCall', 'Mode_1_Init contains an RNG call.');
assert(isempty(regexp(teplot, randomCall, 'once')), ...
    'EXP3:StopCallbackRandomCall', 'TEplot contains an RNG call.');

dist = zeros(1, 28);
assignin('base', 'dist', dist);

teBlocks = find_system(modelName, 'LookUnderMasks', 'all', ...
    'FollowLinks', 'on', 'Name', 'TE Code');
assert(isscalar(teBlocks), 'EXP3:SFunctionBlockCount', ...
    'Expected exactly one TE Code block.');

% PROTOCOL-CRITICAL: no statement may be inserted between these two lines.
rng(seed, 'twister');
simResult = sim(modelName);

afterSim = rng;
availableOutputs = string(simResult.who);
if all(ismember(["tout" "simout" "xmv"], availableOutputs))
    tout = simResult.get('tout');
    simout = simResult.get('simout');
    xmv = simResult.get('xmv');
else
    assert(evalin('base', ...
        "exist('tout','var') && exist('simout','var') && exist('xmv','var')"), ...
        'EXP3:WorkspaceOutputsMissing', ...
        'Expected tout, simout, and xmv workspace outputs are missing.');
    tout = evalin('base', 'tout');
    simout = evalin('base', 'simout');
    xmv = evalin('base', 'xmv');
end
numericOutput = [double(tout), double(simout), double(xmv)];

rng(seed, 'twister');
rand();
afterOneExpectedDraw = rng;
rng(afterSim);

observed = struct( ...
    'numeric_output', numericOutput, ...
    'output_sha256', sha256_numeric(numericOutput), ...
    'load_system_rng_unchanged', isequal(beforeLoad, afterLoad), ...
    'sim_consumed_exactly_one_rand', isequal(afterSim, afterOneExpectedDraw), ...
    'preload_callback', get_param(modelName, 'PreLoadFcn'), ...
    'stop_callback', get_param(modelName, 'StopFcn'), ...
    'sfunction_path', teBlocks{1}, ...
    'sfunction_parameters', strtrim(get_param(teBlocks{1}, 'Parameters')));
end

function runtime = capture_runtime()
matlabProduct = ver('MATLAB'); %#ok<VERMATLAB>
simulinkProduct = ver('Simulink');
exactVersion = version;
buildToken = regexp(exactVersion, '\.(\d+) \(R\d{4}[ab]\)', 'tokens', 'once');
assert(~isempty(buildToken), 'EXP3:MatlabBuildUnavailable', ...
    'Could not parse MATLAB build from version string.');
runtime = struct( ...
    'matlab_version', exactVersion, ...
    'matlab_release', version('-release'), ...
    'matlab_build', buildToken{1}, ...
    'matlab_product_version', matlabProduct.Version, ...
    'matlab_product_release', matlabProduct.Release, ...
    'matlab_product_date', matlabProduct.Date, ...
    'simulink_version', simulinkProduct.Version, ...
    'simulink_release', simulinkProduct.Release, ...
    'simulink_product_date', simulinkProduct.Date, ...
    'architecture', computer, ...
    'matlabroot', matlabroot);
end

function digestHex = sha256_numeric(value)
bytes = typecast(value(:), 'uint8');
digest = java.security.MessageDigest.getInstance('SHA-256');
digest.update(bytes);
raw = typecast(digest.digest(), 'uint8');
digestHex = lower(reshape(dec2hex(raw, 2).', 1, []));
end

function close_if_loaded(modelName)
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end
end

function cleanup_environment(originalPath, originalDir, modelName)
close_if_loaded(modelName);
close_if_loaded('TElib');
close_if_loaded('tesys');
path(originalPath);
cd(originalDir);
end
