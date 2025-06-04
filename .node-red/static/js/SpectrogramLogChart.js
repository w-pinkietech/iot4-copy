'use strict';

window.SpectrogramLogChart = class SpectrogramLogChart {

    constructor(id) {
        this.id = id;
        this.initialized = false;
    }

    init(payload, search) {
        if (this.initialized) {
            this.clear();
        }

        const datasets = [];
        for (const [name, values] of Object.entries(payload)) {
            const times = Object.values(values).flatMap(x => [...Array(x.powers.length)].map(_ => new Date(x.time)));
            const powers = Object.values(values).flatMap(x => x.powers);
            const freqs = Object.values(values).flatMap(x => x.freqs);

            datasets.push({
                x: times,
                y: freqs,
                name: '',
                mode: 'markers',
                meta: name,
                hovertemplate: '%{meta}<br><i> 周波数</i>: %{y:d} [Hz]<br> Power: %{text:.2e} [G<sup>2</sup>/Hz]',
                text: powers,
                marker: {
                    colorscale: 'Portland',
                    color: powers,
                    cmin: 0,
                    cmax: search.cmax || 0.5,
                    // cmax: 1,
                    // cmin: log.log_scale ? (log.minv === 0 ? -5 : Math.log10(log.minv)) : log.minv,
                    // cmax: log.log_scale ? Math.log10(log.maxv) : log.maxv,
                    colorbar: {
                        tickmode: 'auto',
                        tickformat: '.1e',
                        showticklabels: true,
                    }
                }
            });
        }
        const layout = {
            title: '振動ログ',
            margin: {
                t: 60,
                // b: 0,
                l: 60,
                r: 30
            },
            xaxis: {
                title: '時間',
                // range: [Date.parse(log.from), Date.parse(log.to)]
            },
            yaxis: {
                title: '周波数 [Hz]',
                range: [0, 200]
            },
            showlegend: false,
            plot_bgcolor: '#0c3383'
        };
        Plotly.newPlot(this.id, datasets, layout);
        this.initialized = true;
    }

    clear() {
        Plotly.purge(this.id);
        this.initialized = false;
    }
}