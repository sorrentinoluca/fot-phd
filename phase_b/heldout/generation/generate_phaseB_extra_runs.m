%% Phase B extra held-out runs
% Targets:
%   Faults 1, 8, 10, 13 -> batches 12 and 13
%   Normal               -> batches 12 and 13
%
% Uses validated pre-SP workflow.
% No manual RNG seed.
% No custom setpoints.
% No model modifications.

simdir = '/Users/luker/fot-tep/tep_parent_a0413e16/simulator';
outdir = '/Users/luker/fot-tep/tep_heldout/mode1';
headDir = '/Users/luker/fot-tep/tennessee-eastman-dataset/simulator';

if ~isfolder(outdir)
    mkdir(outdir);
end

%% Ensure pre-SP simulator has priority

if contains(path,headDir)
    rmpath(headDir);
end

addpath(simdir,'-begin');
cd(simdir);
rehash;

names = {'MultiLoop_mode1','TElib','tesys'};

for k = 1:numel(names)
    if bdIsLoaded(names{k})
        close_system(names{k},0);
    end
end

modelName = 'MultiLoop_mode1';
load_system(modelName);

fprintf('MODEL    = %s\n',get_param(modelName,'FileName'));
fprintf('StopTime = %s h\n',get_param(modelName,'StopTime'));
fprintf('Solver   = %s\n\n',get_param(modelName,'Solver'));

%% Output schema

headers = [{'Time (h)'}, ...
    arrayfun(@(i) sprintf('XMEAS-%d',i),1:41,'UniformOutput',false), ...
    arrayfun(@(i) sprintf('XMV-%d',i),1:12,'UniformOutput',false)];

%% Fault runs

faults = [1 8 10 13];

for batchNum = [12 13]

    for faultNum = faults

        filename = fullfile(outdir, ...
            sprintf('mode1_%d_%d.xlsx',faultNum,batchNum));

        % Safety: do not overwrite an existing run.
        if isfile(filename)
            error('Refusing to overwrite existing file: %s',filename);
        end

        dist = zeros(1,28);
        dist(faultNum) = 1;

        fprintf('Fault %02d, batch %02d...\n',faultNum,batchNum);

        simOut = sim(modelName);

        dataToSave = [tout, simout, xmv];

        writecell(headers,filename,'Sheet',1,'Range','A1');
        writematrix(dataToSave,filename,'Sheet',1,'Range','A2');

        fprintf('Saved: %s\n',filename);
        fprintf('Rows = %d | Columns = %d\n\n', ...
            size(dataToSave,1),size(dataToSave,2));

        close all;
    end
end

%% Normal runs

for batchNum = [12 13]

    filename = fullfile(outdir, ...
        sprintf('mode1_normal_%d.xlsx',batchNum));

    % Safety: do not overwrite an existing run.
    if isfile(filename)
        error('Refusing to overwrite existing file: %s',filename);
    end

    % No active fault.
    dist = zeros(1,28);

    fprintf('NORMAL, batch %02d...\n',batchNum);

    simOut = sim(modelName);

    dataToSave = [tout, simout, xmv];

    writecell(headers,filename,'Sheet',1,'Range','A1');
    writematrix(dataToSave,filename,'Sheet',1,'Range','A2');

    fprintf('Saved: %s\n',filename);
    fprintf('Rows = %d | Columns = %d\n\n', ...
        size(dataToSave,1),size(dataToSave,2));

    close all;
end

close_system(modelName,0);

fprintf('PHASE B EXTRA RUN GENERATION COMPLETE\n');