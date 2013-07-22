var diameter = 900;
var format = d3.format(",d");

var pack = d3.layout.pack()
    .size([diameter - 4, diameter - 4])
    .value(function(d) { 
        if(d.stats == null){
            return 0;
        } else if(d.stats.STATISTIC_SERVER_SIDE_MAXIMUM_CONNECTIONS.low == 0){
            return 0.5;
        } else {
            return d.stats.STATISTIC_SERVER_SIDE_MAXIMUM_CONNECTIONS.low;
        }
    });

var svg = d3.select("body").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .append("g")
    .attr("transform", "translate(2, 2)");

function render_partition(error, root){
    var node = svg.datum(root).selectAll(".node")
        .data(pack.nodes)
        .enter().append("g")
        .attr("class", function(d) { 
            return d.children ? "node" : "leaf node " + d.status; 
        })
        .attr("transform", function(d) { 
            return "translate(" + d.x + "," + d.y + ")"; 
        });
    
    node.append("title")
        .text(function(d) { return d.name + (d.children ? "" : ": " + format(d.size)); });
    
    node.append("circle")
        .attr("r", function(d) { return d.r; });
}

d3.json("./<one_of_your_environments>/<one_of_your_partitions>.json", render_partition);

d3.select(self.frameElement).style("height", diameter + "px");

