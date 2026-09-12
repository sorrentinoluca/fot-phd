function mexPath = compile_philox()
% Compile the Studio 2 S-function without writing outside studio2/.

thisDir = fileparts(mfilename('fullpath'));
sourceDir = fullfile(fileparts(thisDir), 'source');
buildDir = fullfile(fileparts(thisDir), 'build');
if ~isfolder(buildDir)
    mkdir(buildDir);
end

mexPath = fullfile(buildDir, ['temexd_philox.' mexext]);
if isfile(mexPath)
    error('Refusing to overwrite existing MEX: %s', mexPath);
end

mex('-R2018a', '-outdir', buildDir, ...
    fullfile(sourceDir, 'temexd_philox.c'), ...
    ['-I' sourceDir]);
fprintf('Compiled: %s\n', mexPath);
end
