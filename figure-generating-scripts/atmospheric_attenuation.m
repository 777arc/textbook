% requires comms system toolbox
clear all;
close all;

% NOTE I HAD AN EXTRA LOG HERE WHEN I FIRST MADE THE SCRIPT (NOW REMOVED) SO THE ANNOTATIONS WILL NEED UPDATING IF THIS IS RUN AGAIN
semilogx([1:400], gaspl(1e3, [1:400]*1e9, 20, 101300, 10));
xlabel('Frequency [GHz]');
ylabel('Attenuation [dB/km]');
grid;
xlim([1 400]);

annotation('textarrow',[0.535 0.535],[0.2 0.4],'String','H_{2}O')
annotation('textarrow',[0.655 0.655],[0.3 0.5],'String','O_{2}')
annotation('textarrow',[0.75 0.75],[0.35 0.5],'String','O_{2}')
annotation('textarrow',[0.805 0.805],[0.4 0.6],'String','H_{2}O')
annotation('textarrow',[0.88 0.88],[0.45 0.65],'String','H_{2}O')
% use the property inspector to increase text size and move stuff around
