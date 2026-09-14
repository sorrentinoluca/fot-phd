function generate_normal_dev_runs(planPath, outputDir)
% Delegate normal_dev execution to the qualified Phase 02 Normal generator.
phase02 = fullfile(fileparts(fileparts(fileparts(mfilename('fullpath')))), ...
    'fase02', 'simulator', 'matlab');
addpath(phase02, '-begin');
generate_normal_runs(planPath, outputDir);
end
