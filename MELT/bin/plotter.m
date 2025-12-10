% This script was generated with thye help of ChatGPT 5.1.

clear
clc
close all

uni = load("scan_entropy_weight_results_unimodal.mat");
bi  = load("scan_entropy_weight_results_bimodal.mat");

[TAU_uni, W_uni] = meshgrid(uni.tau_grid, uni.w_scan);
[TAU_bi,  W_bi ] = meshgrid(bi.tau_grid,  bi.w_scan);

% Common limits so there's no extra whitespace
tau_min = min([uni.tau_grid(:); bi.tau_grid(:)]);
tau_max = max([uni.tau_grid(:); bi.tau_grid(:)]);
w_min   = min([uni.w_scan(:);   bi.w_scan(:)]);
w_max   = max([uni.w_scan(:);   bi.w_scan(:)]);

% Log ticks (10^n style)
tau_exp   = floor(log10(tau_min)) : ceil(log10(tau_max));
w_exp     = floor(log10(w_min))   : ceil(log10(w_max));
tau_ticks = 10.^tau_exp;
w_ticks   = 10.^w_exp;

fs_axes   = 26;  % tick labels
fs_label  = 30;  % axis labels
fs_title  = 30;  % titles

% Shared color limits
all_vals = [uni.FC_map(:); bi.FC_map(:)];
clim = [min(all_vals) max(all_vals)];

% ===== Figure + layout =====
figure('Units','normalized','Position',[0.1 0.1 0.75 0.6]);
set(gcf,'Color','w');   % white background

t = tiledlayout(1,2,'TileSpacing','compact','Padding','compact');
colormap(parula(256));

%% Bimodal
ax2 = nexttile;
contourf(TAU_bi, W_bi, bi.FC_map.', 100, 'LineStyle', 'none');
set(ax2, 'XScale', 'log', 'YScale', 'log');
xlim(ax2, [tau_min 1.2E4]);
ylim(ax2, [w_min   w_max]);
xticks(ax2, tau_ticks);
yticks(ax2, w_ticks);
xlabel(ax2, 'Lifetime (ps)');
ylabel(ax2, '\alpha_{start}');
title(ax2, 'Bimodal');
axis(ax2, 'square');
ax2.FontSize = fs_axes;
ax2.XLabel.FontSize = fs_label;
ax2.YLabel.FontSize = fs_label;
ax2.Title.FontSize  = fs_title;
caxis(ax2, clim);
set(ax2, 'Color', 'w');   % white axes background (optional)
set(ax2, 'TickDir', 'out');
%set(ax2, 'TickLength', [0.02 0.02]);
set(ax2, 'XAxisLocation', 'bottom');
set(ax2, 'YAxisLocation', 'left');
set(ax2, 'Box', 'on');
set(ax2, 'LineWidth', 1.1);

%% Unimodal
ax1 = nexttile;
contourf(TAU_uni, W_uni, uni.FC_map.', 100, 'LineStyle', 'none');
set(ax1, 'XScale', 'log', 'YScale', 'log');
xlim(ax1, [tau_min 1.2E4]);
ylim(ax1, [w_min   w_max]);
xticks(ax1, tau_ticks);
yticks(ax1, w_ticks);
xlabel(ax1, 'Lifetime (ps)');
ylabel(ax1, '\alpha_{start}');
title(ax1, 'Unimodal');
axis(ax1, 'square');
ax1.FontSize = fs_axes;
ax1.XLabel.FontSize = fs_label;
ax1.YLabel.FontSize = fs_label;
ax1.Title.FontSize  = fs_title;
caxis(ax1, clim);
set(ax1, 'TickDir', 'out');
set(ax1, 'Box', 'on');
set(ax1, 'XAxisLocation', 'bottom');
set(ax1, 'YAxisLocation', 'left');
set(ax1, 'LineWidth', 1.1);

% Shared colorbar on the right of the figure
cb = colorbar(ax1);
cb.Location = 'eastoutside';   % <-- use Location, not Layout.Tile
cb.Label.String = 'Probability';
cb.FontSize = fs_axes;
