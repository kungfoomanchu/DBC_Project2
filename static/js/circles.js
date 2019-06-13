// Get Item Input
// var inputElement = d3.select("#myList");
// var inputValue = inputElement.property("value");
// item = inputValue;
item = "ps4"
console.log(item);

// item = "ps4"
// Feed Item Input into Flask and get JSON
var url =
    `http://127.0.0.1:5000/quantity_json/${item}`;

function getQuantity() {

    d3.json(url).then(function (data) {
        // To see what the data looks like, check the console
        console.log(data[0]);
        // Grab values from the data json object to build the plots
        var item_name = data[0].item_name;
        var item_date = data[0].item_date;
        var item_price = data[0].item_price;
        var bitcoin_shares = data[0].bitcoin_shares;
        var bitcoin_price_today = data[0].bitcoin_price_today;
        var btc_price_on_item_day = data[0].btc_price_on_item_day;
        var item_quantity_current = data[0].item_quantity_max;
        var item_quantity_max = data[0].item_quantity_current;
        var item_svg = data[0].item_svg;

        const item_quantities = [item_name, item_quantity_current, item_quantity_max, item_svg, item_date, item_price, bitcoin_shares, bitcoin_price_today, btc_price_on_item_day]
        console.log(item_quantities)

        return item_quantities;
    });
}

// Radius (km) of Mercury, Mars, Venus, Earth, Neptune, Uranus, Saturn, and Jupiter.
const celestialData = [2439.7,
    3396.2,
    6051.9,
    6378.1,
    24764,
    25559,
    60268,
    71492
];


////////////////////////////////////
// Attempt to make celestialData variable

getQuantity(function (data_of_item) {
    //getItems();
    console.log(data_of_item);


    const sizeData = [1,
        data_of_item[1],
        data_of_item[2]
    ];
    console.log(sizeData)
    return sizeData
});


// var item_sizes = getQuantity()
// console.log(item_sizes)

// const celestialData = [
//     1,
//     item_sizes[1],
//     item_sizes[2]
// ];
// console.log(celestialData)
//////////////////////////////////

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

var planets = new planetDisplay(celestialData);
// var planets = new planetDisplay(getQuantity(celestialData));
planets.initDisplay();

// On click, transition to other scale
d3.select(document).on("click", planets.updateDisplay.bind(planets));


