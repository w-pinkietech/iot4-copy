'use strict';

window.RealtimeHeatmap = class RealtimeHeatmap {

    constructor(id, name) {
        this.id = id;
        this.initialized = false;
        this.data = {
            x: [],
            z: [],
            type: 'heatmap',
            // type: 'contour',
            colorscale: 'Portland',
            name: '',
            // xhoverformat: this.name + ' %Y-%m-%d %H:%M:%S',
            hovertemplate: `周波数：%{y}[Hz]<br>パワー：%{z}[G<sup>2</sup>/Hz]`,
            transpose: true,
            colorbar: {
                thickness: 10,
                orientation: 'h',
                y: -0.3,
                tickfont: {
                    size: 9
                }
            }
        };
        this.layout = {
            hovermode: 'x unified',
            showlegend: true,
            dragmode: false,
            margin: {
                t: 0,
                b: 10,
                l: 60,
                r: 20
            },
            legend: {
                orientation: 'h'
            },
            xaxis: {
                autorange: true,
                showgrid: false,
                zeroline: false,
                tickformat: '%H:%M:%S',
                hoverformat: '%H:%M:%S',
                tickangle: 0,
                tickfont: {
                    size: 9
                }
            },
            yaxis: {
                autorange: true,
                title: '周波数 [Hz]'
            }
        };
        this.config = {
            displayModeBar: false,
            showAxisDragHandles: false
        };
    }

    init(name) {
        if (this.initialized) {
            return;
        }

        this.data.xhoverformat = name + ' %Y-%m-%d %H:%M:%S';
        Plotly.newPlot(this.id, [this.data], this.layout, this.config);
        this.initialized = true;
    }

    add(payload) {
        if (!this.initialized) {
            return;
        }
        this.data.x.push(new Date(payload.time));
        this.data.z.push(payload.values);
        if (this.data.x.length > 60) {
            this.data.x.shift();
            this.data.z.shift();
        }
        Plotly.relayout(this.id, this.layout);
    }
};