function restore_exp3_plot_stopfcn(state)
%RESTORE_EXP3_PLOT_STOPFCN Restore and verify callback and Dirty state.

modelName = state.model_name;
originalStopFcn = state.original_stopfcn;
originalDirty = state.original_dirty;
assert(bdIsLoaded(modelName), 'EXP3:StopCallbackRestoreModelClosed', ...
    'Cannot restore StopFcn because the model is no longer loaded.');
set_param(modelName, 'StopFcn', originalStopFcn);
assert(strcmp(get_param(modelName, 'StopFcn'), originalStopFcn), ...
    'EXP3:StopCallbackRestoreFailed', 'StopFcn was not restored exactly.');
if ~strcmp(get_param(modelName, 'Dirty'), originalDirty)
    set_param(modelName, 'Dirty', originalDirty);
end
assert(strcmp(get_param(modelName, 'Dirty'), originalDirty), ...
    'EXP3:ModelDirtyRestoreFailed', ...
    'Model Dirty state was not restored exactly.');
end
