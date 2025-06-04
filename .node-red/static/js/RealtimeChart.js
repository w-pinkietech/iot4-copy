'use strict';

window.RealtimeChart = class RealtimeChart {

    constructor(id, sensorTypes) {
        this.id = id;
        this.datasets = [];
        this.initialized = false;
        this.name = '';
        this.sensorTypes = Array.isArray(sensorTypes) ? sensorTypes : [sensorTypes];
        this.layout = {
            hovermode: 'x unified',
            showlegend: true,
            dragmode: false,
            margin: {
                t: 0,
                b: 0,
                l: 70,
                r: 20
            },
            legend: {
                orientation: 'h',
                font: {
                    size: 10
                }
            },
            xaxis: {
                autorange: true,
                showgrid: false,
                zeroline: false,
                tickformat: '%H:%M:%S',
                tickangle: 0,
                tickfont: {
                    size: 9
                }
            },
            yaxis: {
                autorange: true,
            }
        };
        this.config = {
            displayModeBar: false,
            showAxisDragHandles: false
        };
    }

    init(devices) {
        if (this.initialized) {
            return;
        }
        let initialized = false;

        for (const device of devices.filter(x => this.sensorTypes.includes(x.sensorType))) {
            if (!initialized) {
                this.createYAxisLayout(device);
            }
            device.sensors
                .forEach((sensor) => {
                    const channel = device.channels.find(c => c.channel === sensor.channel);
                    const chart = this.createInitChart(device, sensor, channel);
                    if (chart) {
                        this.datasets.push(chart);
                    }
                });
            initialized = true;
        }
        if (initialized) {
            Plotly.newPlot(this.id, this.datasets, this.layout, this.config);
            this.initialized = true;
        }
    }

    createYAxisLayout(device) {
    }

    createInitChart(device, sensor, channel) {
        return {};
    }

    add(payload) {
        if (!this.initialized) {
            return;
        }
        if (!this.sensorTypes.includes(payload.sensorType)) {
            return;
        }
        let relayout = false;
        payload.sensors
            .forEach((sensor, index) => {
                const name = this._getName(payload, sensor);
                const series = this.datasets.find(x => x.name === name);
                if (series) {
                    relayout = relayout | this.addChartData(series, payload, sensor, index);
                }
            });
        if (relayout) {
            Plotly.relayout(this.id, this.layout);
        }
    }

    addChartData(series, payload, sensor, index) {
        return false;
    }

    _getName(device, sensor) {
        return [device.deviceName, sensor.displayName, sensor.channel].filter(x => x).join('-');
    }
}