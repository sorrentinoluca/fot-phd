function generate_normal_runs_soglie(planPath, outputDir)
% Entry point in fase03; execution delegates to the qualified Phase 02 launcher.
phase02 = fullfile(fileparts(fileparts(fileparts(mfilename('fullpath')))), 'fase02', 'simulator', 'matlab');
addpath(phase02, '-begin');
generate_normal_runs(planPath, outputDir);
end
