'use strict';

window.RealtimeGpioChart = class RealtimeGpioChart extends RealtimeChart {

    constructor(id, sensorTypes) {
        super(id, sensorTypes);
        this.layout.margin = {
            t: 0,
            b: 10,
            l: 40,
            r: 20
        };
        this.layout.yaxis = {
            autorange: true,
            tickmode: 'array',
            tickvals: [0, 1],
            ticktext: ['Low', 'High'],
            range: [0, 1],
            zeroline: false
        };
    }

    createInitChart(device, sensor, channel) {
        const name = this._getName(device, sensor);
        const x = sensor.time ? [new Date(sensor.time)] : [];
        const y = sensor.time ? [sensor.value] : [];
        return {
            x,
            y,
            name,
            text: name,
            line: {
                shape: 'hv'
            },
            mode: 'lines+markers',
            marker: {
                size: 4,
            },
            xhoverformat: '%Y-%m-%d %H:%M:%S',
            hovertemplate: '%{y}'
        };
    }

    addChartData(series, payload, sensor, index) {
        if (series.y.length === 0 || series.y[series.y.length - 1] !== payload.values[index]) {
            const date = new Date(payload.time);
            series.x.push(date);
            series.y.push(payload.values[index]);
            if (series.x.length > 10) {
                series.x.shift();
                series.y.shift();
            }
        }
        return true;
    }
}
