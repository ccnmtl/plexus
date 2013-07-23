// returns NaN if graphite data didn't contain a value
var parseFromGraphite = function(r) {
    r = r.replace(/\s+/g,'');
    var parts = r.split("|");
    var results = parts[1].split(",");
    var found = 0.0;
    for (var i=0; i < results.length; i++) {
        if (results[i].replace(/ /g,'') === "None") {
        } else {
            found = results[i];
        }
    }
    return parseFloat(found);
};

var makesmoketests = function(el, graphite_name) {
   var render_base = "/render";
   var run_base = "ccnmtl.app.smoketest." + graphite_name + ".run";
   var pass_base = "ccnmtl.app.smoketest." + graphite_name + ".passed";
   var combiner = {'run': undefined, 'passed': undefined};
   combiner.render = function() {
       if (combiner.run && combiner.passed) {
           var stclass = "badge-important";
           if (combiner.passed === combiner.run) {
							stclass = "badge-success";
           }
           combiner.div.html("<b class='badge " + stclass + "'>" + combiner.passed + "/" + combiner.run + "</b>");
       }
   };
   combiner.get_run = function() {
       d3.text(render_base + "?format=raw&from=-10minutes&target=" + run_base,
           function (r, e) {
               combiner.run = parseFromGraphite(r);
               combiner.render();
           });
   };

   combiner.get_passed = function() {
       d3.text(render_base + "?format=raw&from=-10minutes&target=" + pass_base,
           function (r, e) {
               combiner.passed = parseFromGraphite(r);
               combiner.render();
           });
   };

   d3.select(el).call(function (div) {
       combiner.div = div;
       combiner.get_run();
       combiner.get_passed();
    });
};
