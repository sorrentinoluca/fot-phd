function [cleanupGuard, state] = suppress_exp3_plot_stopfcn(modelName)
%SUPPRESS_EXP3_PLOT_STOPFCN Temporarily suppress the frozen plotting StopFcn.
%
% The loaded model must have exactly StopFcn = TEplot. The returned cleanup
% object restores both the callback and the model's original in-memory Dirty
% state if control leaves the caller unexpectedly. The returned state permits
% explicit restoration and verification immediately after sim.

assert(bdIsLoaded(modelName), 'EXP3:ModelNotLoaded', ...
    'Model must be loaded before managing its StopFcn.');
originalStopFcn = get_param(modelName, 'StopFcn');
originalDirty = get_param(modelName, 'Dirty');
assert(strcmp(originalStopFcn, 'TEplot'), 'EXP3:StopCallbackMismatch', ...
    'StopFcn must be exactly TEplot; refusing to suppress configuration drift.');

state = struct('model_name', modelName, ...
    'original_stopfcn', originalStopFcn, ...
    'original_dirty', originalDirty);
cleanupGuard = onCleanup(@() restore_exp3_plot_stopfcn(state));
set_param(modelName, 'StopFcn', '');
assert(strcmp(get_param(modelName, 'StopFcn'), ''), ...
    'EXP3:StopCallbackSuppressionFailed', ...
    'StopFcn was not neutralized for headless generation.');
end
