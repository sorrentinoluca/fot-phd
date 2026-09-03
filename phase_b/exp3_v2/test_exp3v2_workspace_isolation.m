function result = test_exp3v2_workspace_isolation()
%TEST_EXP3V2_WORKSPACE_ISOLATION Verify scalar evalin text without simulation.

clear_injected_outputs();
cleanup = onCleanup(@() clear_injected_outputs());
stream = RandStream.getGlobalStream();
beforeState = stream.State;

[present, expression] = exp3v2_workspace_outputs_present();
assert((ischar(expression) && isrow(expression)) || ...
    (isstring(expression) && isscalar(expression)), ...
    'EXP3V2:WorkspaceExpressionRegression', ...
    'The expression passed to evalin is not a text scalar.');
assert(~present, 'EXP3V2:WorkspaceEmptyRegression', ...
    'An empty base workspace must pass the isolation check.');

assignin('base', 'tout', 1);
assert(exp3v2_workspace_outputs_present(), ...
    'EXP3V2:WorkspaceToutRegression', 'tout was not detected.');
evalin('base', 'clear tout');

assignin('base', 'simout', 1);
assert(exp3v2_workspace_outputs_present(), ...
    'EXP3V2:WorkspaceSimoutRegression', 'simout was not detected.');
evalin('base', 'clear simout');

assignin('base', 'xmv', 1);
assert(exp3v2_workspace_outputs_present(), ...
    'EXP3V2:WorkspaceXmvRegression', 'xmv was not detected.');
evalin('base', 'clear xmv');

assert(~exp3v2_workspace_outputs_present(), ...
    'EXP3V2:WorkspaceCleanupRegression', ...
    'Injected base-workspace variables were not removed.');
assert(isequal(beforeState, stream.State), ...
    'EXP3V2:WorkspaceRngRegression', ...
    'Workspace-isolation testing changed the MATLAB RNG state.');
testSource = fileread([mfilename('fullpath') '.m']);
assert(isempty(regexp(testSource, '\bsim\s*\(', 'once')), ...
    'EXP3V2:WorkspaceSimulationRegression', ...
    'Workspace-isolation regression must not call model simulation.');
clear cleanup;
result = true;
fprintf(['PASS: scalar evalin workspace isolation and cleanup verified; ' ...
    'RNG state unchanged; simulation not called.\n']);
end

function clear_injected_outputs()
evalin('base', 'clear tout simout xmv');
end
