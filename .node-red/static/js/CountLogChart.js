'use strict';

window.CountLogChart = class CountLogChart {

    constructor(id) {
        this.id = id;
        this.initialized = false;
    }

    init(payload, search) {
        if (this.initialized) {
            this.clear();
        }
        const sensorType = search.sensorType;
        const sensorTypeName = search.sensorTypeName;
        const unit = search.unit;
        const layout = this.#createLayout(sensorType, sensorTypeName, unit);
        const datasets = [];
        for (const [name, values] of Object.entries(payload)) {
            const isTimeExist = values[0]?.time != null;
            const data = {
                x: values.map(x => new Date(x.time)),
                y: values.map(x => x.value),
                name,
                text: name,
                mode: 'lines',
                xhoverformat: isTimeExist ? '%Y-%m-%d %H:%M:%S.%f' : '%Y-%m-%d %H:%M:%S',
                hovertemplate: '%{y}'
            };
            datasets.push(data);
        }
        Plotly.newPlot(this.id, datasets, layout);
        this.initialized = true;
    }

    clear() {
        Plotly.purge(this.id);
        this.initialized = false;
    }

    #createLayout(sensorType, sensorTypeName, unit) {
        return {
            title: `${sensorTypeName} カウントログ`,
            hovermode: 'x unified',
            showlegend: true,
            margin: {
                t: 60,
                b: 0,
                l: 60,
                r: 30
            },
            legend: {
                orientation: 'h'
            },
            xaxis: {
                tickangle: 0
            },
            yaxis: {
                autorange: true,
                title: `${sensorTypeName} カウント`
            }
        };
    }
}