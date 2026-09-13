function mexPath = compile_fault_philox()
% Build the instrumented twin only below this phase's runtime directory.
here = fileparts(mfilename('fullpath'));
sourceDir = fullfile(here, 'runtime', 'source');
buildDir = fullfile(here, 'runtime', 'build');
if ~isfolder(buildDir), mkdir(buildDir); end
mexPath = fullfile(buildDir, ['temexd_fault_philox.' mexext]);
if isfile(mexPath)
    error('Refusing to overwrite existing MEX: %s', mexPath);
end
mex('-R2018a', '-outdir', buildDir, fullfile(sourceDir, 'temexd_fault_philox.c'), ['-I' sourceDir]);
fprintf('Compiled: %s\n', mexPath);
end
