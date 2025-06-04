'use strict';

window.RealtimeLineChart = class RealtimeLineChart extends RealtimeChart {

    constructor(id, sensorTypes) {
        super(id, sensorTypes);
    }

    createYAxisLayout(device) {
        const uniqueChannels = Array.from(new Map(device.channels.map((channel, i) => {
            const unit = device.sensors[i].displayUnit || channel.unit;
            const name = [channel.channelName, device.sensors[i].displayName, unit].filter(x => x).join('-');
            return [name, { ...channel, ...device.sensors[i] }];
        })).values());
        uniqueChannels.forEach((channel, i) => {
            const unit = channel.displayUnit || channel.unit;
            const name = [channel.channelName, channel.displayName, unit].filter(x => x).join('-');
            const title = channel.displayName || channel.channelName
            if (i === 0) {
                this.layout['yaxis'] = {
                    axis: 'yaxis',
                    name,
                    autorange: true,
                    title: (unit ? `${title} [${unit}]` : title),
                };
            } else {
                const axis = `yaxis${i + 1}`;
                this.layout[axis] = {
                    axis,
                    name,
                    autorange: true,
                    title: (unit ? `${title} [${unit}]` : title),
                    overlaying: 'y',
                    side: (i < uniqueChannels.length / 2 ? 'left' : 'right'),
                };
                this.layout.margin.r = 60;
            }
        });
    }

    createInitChart(device, sensor, channel) {
        const name = this._getName(device, sensor);
        const unit = sensor.displayUnit || channel.unit;
        const plotData = {
            x: [],
            y: [],
            name,
            text: name,
            // mode: 'lines',
            xhoverformat: '%Y-%m-%d %H:%M:%S',
            hovertemplate: unit ? `%{y} [${unit}]` : '%{y}'
        };
        for (let i = 1; i < 100; i++) {
            if (this.layout[`yaxis${i + 1}`]) {
                const unit = sensor.displayUnit || channel.unit;
                const name = [channel.channelName, sensor.displayName, unit].filter(x => x).join('-');
                if (this.layout[`yaxis${i + 1}`].name === name) {
                    plotData.yaxis = `y${i + 1}`;
                }
            } else {
                break;
            }
        }
        return plotData;
    }

    addChartData(series, payload, sensor, index) {
        const date = new Date(payload.time);
        series.x.push(date);
        series.y.push(payload.values[index]);
        if (series.x.length > 60) {
            series.x.shift();
            series.y.shift();
        }
        return true;
    }
}
