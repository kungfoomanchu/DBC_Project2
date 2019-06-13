var submit = d3.select("#filter-btn");
var draw = d3.select("#filter-btn-too");
var clear = d3.select("#filter-btn-three");
// var tbody = d3.select("tbody");
// var output = d3.select(".table table-striped");

var celestialData = [];
var resetArr = [];

submit.on("click", function () {
    d3.event.preventDefault();
    var inputElement = d3.select("#myList");
    var item = inputElement.property("value");
    console.log(item);

    var url = `http://127.0.0.1:5000/quantity_json/${item}`;

    function getQuantity() {
        d3.json(url).then(function (data) {
            console.log(data[0]);
            celestialData = [];
            var item_quantity_current = data[0].item_quantity_current;
            var item_quantity_max = data[0].item_quantity_max;
            celestialData = [1, item_quantity_current, item_quantity_max]
            console.log(celestialData)
            //   cb(item_quantities);
        });
    }
    getQuantity();
})

draw.on("click", function () {
    d3.event.preventDefault();
    var planets = new planetDisplay(celestialData);
    planets.initDisplay();
    // On click, transition to other scale
    // d3.select(document).on("click", planets.updateDisplay.bind(planets));
})

clear.on("click", function () {
    // d3.event.preventDefault();
    var planets = new planetDisplay(resetArr);
    planets.initDisplay();
    // On click, transition to other scale
    // d3.select(document).on("click", planets.updateDisplay.bind(planets));
})

const display = d3.select("#display");
// TODO: use scale instead of radius (more efficient transitions)
// also clean up this mess...
class planetDisplay {
    constructor(data) {
        this.data = data;
        this.xSum = 0;
        this.spacing = 2;
        this.currentScale = "linear";
        this.cScale = d3.scaleSequential(d3.interpolateViridis)
            .domain(d3.extent(data));
        this.rScale = d3.scaleLinear()
            .domain(d3.extent(data))
            .range([0.1, 1.5]);
    }

    toggleScale() {
        if (this.currentScale === "linear") {
            this.rScale = d3.scaleLog()
                .domain(d3.extent(this.data))
                .range([0.1, 1.5]);
            this.currentScale = "log";
        } else {
            this.rScale = d3.scaleLinear()
                .domain(d3.extent(this.data))
                .range([0.1, 1.5]);
            this.currentScale = "linear";
        }
    }

    // Calculates x-coordinate of a sphere given radius and index
    positioner(d, i) {
        var currentRadius = this.rScale(d);
        var previousRadius;
        if (i === 0) {
            previousRadius = 0;
        } else {
            previousRadius = this.rScale(this.data[i - 1]);
        }

        // (previousRadius + currentRadius) has spheres touching, (spacing) ensures separation
        this.xSum += previousRadius + currentRadius + this.spacing;
        var x = this.xSum;
        var y = 1.5;
        var z = -4;
        return x + " " + y + " " + z;
    }

    centerDisplay() {
        display.attr("position", () => {
            var x = -(this.xSum / 2);
            var y = 0;
            var z = -10;
            return x + " " + y + " " + z;
        });
    }

    initDisplay() {

        display.selectAll("a-sphere")
            .data(this.data)
            .enter()
            .append("a-sphere")
            .attr("position", this.positioner.bind(this))
            .attr("radius", (d) => this.rScale(d))
            .attr("color", (d) => this.cScale(d));

        this.centerDisplay();
    }

    updateDisplay() {
        this.xSum = 0;
        this.toggleScale();

        var self = this;
        display.selectAll("a-sphere")
            .data(this.data)
            .attr("position", this.positioner.bind(this));

        display.selectAll("a-sphere")
            .data(this.data)
            .transition()
            .duration(2000)
            .attrTween("radius", function (d, i) {
                var el = d3.select(this);
                var oldRadius = AFRAME.utils.coordinates.stringify(el.attr("radius"));
                return d3.interpolate(oldRadius, self.rScale(d));
            });

        this.centerDisplay();
    }
}

// var planets = new planetDisplay(celestialData);
// planets.initDisplay();

// // On click, transition to other scale
// d3.select(document).on("click", planets.updateDisplay.bind(planets));