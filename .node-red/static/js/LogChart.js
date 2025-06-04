'use strict';

window.LogChart = class LogChart {

    constructor(id) {
        this.id = id;
        this.initialized = false;
    }

    init(payload, search) {
        if (this.initialized) {
            this.clear();
        }
        const layout = this.#createLayout(search);
        const datasets = [];
        for (const [name, data] of Object.entries(payload)) {
            const isTimeExist = data.values[0]?.time != null;
            const plotData = {
                x: data.values.map(x => new Date(x.time)),
                y: data.values.map(x => x.value),
                name,
                text: name,
                mode: 'lines',
                xhoverformat: (isTimeExist ? '%Y-%m-%d %H:%M:%S.%f' : '%Y-%m-%d %H:%M:%S'),
                hovertemplate: (data.unit ? `%{y} [${data.unit}]` : '%{y}')
            };
            const contacts = [257, 258, 294, 295, 296];
            if (contacts.includes(search.sensorType)) {
                plotData.line = {
                    shape: 'hv'
                };
                plotData.mode = 'lines+markers';
                plotData.marker = {
                    size: 2
                };
            }
            for (let i = 1; i < 100; i++) {
                if (layout[`yaxis${i + 1}`]) {
                    if (layout[`yaxis${i + 1}`].name === `${data.name}-${data.unit}`) {
                        plotData.yaxis = `y${i + 1}`;
                    }
                } else {
                    break;
                }
            }
            datasets.push(plotData);
        }
        Plotly.newPlot(this.id, datasets, layout);
        this.initialized = true;
    }

    clear() {
        Plotly.purge(this.id);
        this.initialized = false;
    }

    #createLayout(search) {
        const uniqueChannels = Array.from(new Map(search.channels.map((c) => [`${c.channelName}-${c.channelUnit}`, c])).values());
        const layout = {
            title: `${search.sensorTypeName}ログ`,
            hovermode: 'x unified',
            showlegend: true,
            margin: {
                t: 60,
                b: 0,
                l: 60,
                r: 30
            },
            legend: {
                orientation: 'h',
            },
            xaxis: {
                tickangle: 0,
            }
        };

        const contacts = [257, 258, 294, 295, 296];
        uniqueChannels.forEach((channel, i) => {
            if (i === 0) {
                if (contacts.includes(search.sensorType)) {
                    layout['yaxis'] = {
                        autorange: true,
                        tickmode: 'array',
                        tickvals: [0, 1],
                        ticktext: ['Low', 'High'],
                        range: [0, 1],
                        zeroline: false
                    };
                } else {
                    layout['yaxis'] = {
                        axis: 'yaxis',
                        name: `${channel.channelName}-${channel.unit}`,
                        autorange: true,
                        title: (channel.unit ? `${channel.channelName} [${channel.unit}]` : channel.channelName),
                    };
                }
            } else {
                const axis = `yaxis${i + 1}`;
                layout[axis] = {
                    axis,
                    name: `${channel.channelName}-${channel.unit}`,
                    autorange: true,
                    title: (channel.unit ? `${channel.channelName} [${channel.unit}]` : channel.channelName),
                    overlaying: 'y',
                    side: (i < uniqueChannels.length / 2 ? 'left' : 'right'),
                };
                layout.margin.r = 60;
            }
        });
        return layout;
    }
}
