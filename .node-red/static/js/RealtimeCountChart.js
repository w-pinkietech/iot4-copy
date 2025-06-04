'use strict';

window.RealtimeCountChart = class RealtimeCountChart extends RealtimeChart {

    constructor(id, sensorTypes) {
        super(id, sensorTypes);
        this.layout.yaxis = {
            autorange: true,
            tick0: 0,
            title: 'カウント'
        };
    }

    createInitChart(device, sensor, channel) {
        const name = this._getName(device, sensor);
        return {
            x: [],
            y: [],
            name,
            text: name,
            xhoverformat: '%Y-%m-%d %H:%M:%S',
            hovertemplate: '%{y}'
        };
    }

    addChartData(series, payload, sensor) {
        const lastCount = series.y[series.y.length - 1];
        if (lastCount !== sensor.count && payload.isSaveCount) {
            const date = new Date(payload.time);
            series.x.push(date);
            series.y.push(sensor.count);
            if (series.x.length > 60) {
                series.x.shift();
                series.y.shift();
            }
            return true;
        }
        return false;
    }
}
