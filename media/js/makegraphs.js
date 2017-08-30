/* global cubism: true, d3: true */

(function() {
    'use strict';
    window.makegraphs = function(el, graphite_name, size, step) {
        var context = cubism.context(); // a default context
        var graphite = context.graphite('');

        context.size(size).step(step);

        var counter_base = 'ccnmtl.app.counters.' + graphite_name;
        var timer_base = 'ccnmtl.app.timers.' + graphite_name;

        var metric_defs = [
            {
                metric: counter_base + '.response.200',
                alias: 'Requests'
            },
            {
                metric: timer_base + '.view.GET.mean',
                alias: 'request time (mean)'
            },
            {
                metric: timer_base + '.view.GET.lower',
                alias: 'request time (lower)'
            },
            {
                metric: timer_base + '.view.GET.upper',
                alias: 'request time (max)'
            },
            {
                metric: counter_base + '.response.500',
                alias: '500s'
            },
            {
                metric: counter_base + '.response.404',
                alias: '404s'
            }
        ];

        var gmetric = function(metric_def) {
            return graphite.metric(metric_def.metric).alias(metric_def.alias);
        };

        var metrics = metric_defs.map(gmetric);

        var oranges = ['#08519c', '#*82bd', '#6baed6',
            '#fee6ce', '#fdae6b', '#e6550d'];
        var greens = ['#edf8b8', '#b2e2e2', '#66c2a4',
            '#2ca25f', '#006d2c'];
        var blues = ['#eff3ff', '#c6dbef', '#9ecae1',
            '#6baed6', '#3182bd', '#08519c'];

        d3.select(el).call(function(div) {
            div.append('div')
                .attr('class', 'axis')
                .call(context.axis().orient('top'));

            div.append('div')
                .datum(metrics[0])
                .attr('class', 'horizon')
                .call(context.horizon().height(100).colors(greens));
            div.append('div')
                .datum(metrics[1])
                .attr('class', 'horizon')
                .call(context.horizon().height(120).colors(oranges));
            div.append('div')
                .datum(metrics[1].subtract(metrics[2]))
                .attr('class', 'horizon')
                .call(context.horizon().height(30).colors(blues));
            div.append('div')
                .datum(metrics[3].subtract(metrics[1]))
                .attr('class', 'horizon')
                .call(context.horizon().height(30).colors(greens));
            div.append('div')
                .datum(metrics[4])
                .attr('class', 'horizon')
                .call(context.horizon().height(60).colors(oranges));
            div.append('div')
                .datum(metrics[5])
                .attr('class', 'horizon')
                .call(context.horizon().height(60).colors(greens));
        });
    };

}());
