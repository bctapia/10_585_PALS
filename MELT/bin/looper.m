% scan_entropy_weight.m
% Scan MELT over different starting entropy weights by running MELT
% in separate MATLAB processes so its 'clear all' can't touch this script.
% This script was generated with thye help of ChatGPT 5.1.

clear; clc; close all

% ---- choose your scan range ----
w_scan = 5e-6 : 1e-6 : 5e-4;   % tweak this as you like
Nw = numel(w_scan);

FC_map   = [];
tau_grid = [];

for iw = 1:Nw
    w = w_scan(iw);
    fprintf('=== Run %d / %d: entwghtstart = %g ===\n', iw, Nw, w);

    % --- Small job script that sets entwghtstart, runs MELT, saves tau/FC ---
    job_file = sprintf('melt_job_NAME_THIS_%d.m', iw); % NAME_THIS was either uni or bi
    out_file = sprintf('melt_output_NAME_THIS_%d.mat', iw); % NAME_THIS was either uni or bi

    fid = fopen(job_file, 'w');
    if fid < 0
        error('Could not create job file %s', job_file);
    end

    % Set entropy weight, then run usual MELT input + melt, then save tau/FC
    fprintf(fid, 'entwghtstart = %g;\n', w);
    fprintf(fid, 'm_input;\n');
    fprintf(fid, 'melt;\n');
    fprintf(fid, 'save(''%s'', ''tau'', ''FC'');\n', out_file);
    fclose(fid);

    % --- Figure out MATLAB executable and run the job in a *separate* process ---
    if ispc
        exe = fullfile(matlabroot, 'bin', 'matlab.exe');
    else
        exe = fullfile(matlabroot, 'bin', 'matlab');
    end

    cmd = sprintf('"%s" -batch "run(''%s'')"', exe, job_file);
    status = system(cmd);
    if status ~= 0
        error('Sub-MATLAB call failed for iw = %d (status %d).', iw, status);
    end

    % --- Load result from that run ---
    S = load(out_file);
    tau = S.tau(:);
    FC  = S.FC(:);

    if iw == 1
        tau_grid = tau;
        Ntau     = numel(tau_grid);
        FC_map   = zeros(Ntau, Nw);
    else
        % sanity check: tau grid must be identical across runs
        if numel(tau) ~= Ntau || any(abs(tau - tau_grid) > 1e-9)
            error('Tau grid changed between runs. Check MELT settings.');
        end
    end

    FC_map(:, iw) = FC;
end

% ---- Save everything ----
save('scan_entropy_weight_results_NAME_THIS.mat', 'tau_grid', 'w_scan', 'FC_map'); % NAME_THIS was either unimodal or bimodal