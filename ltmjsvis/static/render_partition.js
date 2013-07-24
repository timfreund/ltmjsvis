var diameter = 900;
var format = d3.format(",d");

var svg = d3.select("#svgcontainer").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .append("g")
    .attr("transform", "translate(2, 2)");

var rendering_statistic = "STATISTIC_SERVER_SIDE_MAXIMUM_CONNECTIONS";

function render_partition(error, root){
    var pack = d3.layout.pack()
        .size([diameter - 4, diameter - 4])
        .value(function(d) { 
            if(d.stats == null){
                return 0;
            } else if(d.stats[rendering_statistic].low == 0){
                return 0.5;
            } else {
                return d.stats[rendering_statistic].low;
            }
        });

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
        .text(function(d) { if (d.name != null){
            return d.name + (d.children ? "" : ": " + format(d.size));
        } else if (d.address != null){
            return d.address;
        }});
    
    node.append("circle")
        .attr("r", function(d) { return d.r; })
        .attr("onmouseover", function(d) { 
            if (d.name != null){
                return "display_details('" + d.name + "');";
            } else if (d.address != null){
                return "display_details('" + d.address + "');";
            }});
}

function display_details(id){
    document.getElementById("nodename").innerText = id;
}

function populate_controls(error, root){
    var select = document.getElementById("target");

    for(var eidx = 0; eidx < root.environments.length; eidx++){
        var env = root.environments[eidx];
        var env_name = env.name;
        for(var pidx = 0; pidx < env.partitions.length; pidx++){
            var partition = env.partitions[pidx]
            console.log(env_name + "#" + partition);

            var option = document.createElement("option");
            option.value = env_name + "/" + partition;
            option.text = env_name + "/" + partition;
            select.appendChild(option);
        }
    }
}

function get_and_render_partition(){
    rendering_statistic = document.getElementById("statistic").value;
    var select = document.getElementById("target");
    var target = select.value;
    d3.json("./" + target + ".json", render_partition);
}

d3.select(self.frameElement).style("height", diameter + "px");
d3.json("/env.json", populate_controls);

