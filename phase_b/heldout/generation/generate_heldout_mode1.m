%% Independent held-out Mode 1 run
% Pre-SP Tennessee Eastman workflow.
% Test: fault 1, new batch labelled 11.

simdir = '/Users/luker/fot-tep/tep_parent_a0413e16/simulator';
outdir = '/Users/luker/fot-tep/tep_heldout/mode1';

if ~isfolder(outdir)
    mkdir(outdir);
end

% Ensure the isolated pre-SP simulator has priority.
headDir = '/Users/luker/fot-tep/tennessee-eastman-dataset/simulator';

if contains(path,headDir)
    rmpath(headDir);
end

addpath(simdir,'-begin');
cd(simdir);
rehash;

% Close relevant models/libraries if already loaded.
names = {'MultiLoop_mode1','TElib','tesys'};

for k = 1:numel(names)
    if bdIsLoaded(names{k})
        close_system(names{k},0);
    end
end

% Loading the model executes its original PreLoadFcn -> Mode_1_Init.
modelName = 'MultiLoop_mode1';
load_system(modelName);

fprintf('MODEL = %s\n',get_param(modelName,'FileName'));
fprintf('StopTime = %s h\n',get_param(modelName,'StopTime'));

batchNum = 11;

% TEST ONLY: one fault.
for faultNum = 2:21

    dist = zeros(1,28);
    dist(faultNum) = 1;

    fprintf('\nFault %02d, batch %02d...\n',faultNum,batchNum);

    % Original simulation call.
    simOut = sim(modelName);

    % Match the 54-column format of the original dataset:
    % Time + 41 XMEAS + 12 XMV.
    dataToSave = [tout, simout, xmv];

    headers = [{'Time (h)'}, ...
        arrayfun(@(i) sprintf('XMEAS-%d',i),1:41,'UniformOutput',false), ...
        arrayfun(@(i) sprintf('XMV-%d',i),1:12,'UniformOutput',false)];

    filename = fullfile(outdir, ...
        sprintf('mode1_%d_%d.xlsx',faultNum,batchNum));

    writecell(headers,filename,'Sheet',1,'Range','A1');
    writematrix(dataToSave,filename,'Sheet',1,'Range','A2');

    fprintf('Saved: %s\n',filename);
    fprintf('Rows = %d\n',size(dataToSave,1));
    fprintf('Columns = %d\n',size(dataToSave,2));

    close all;
end

close_system(modelName,0);

fprintf('\nHELD-OUT TEST COMPLETE\n');